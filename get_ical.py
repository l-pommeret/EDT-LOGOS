#!/usr/bin/python
# coding: utf8

import argparse
import concurrent.futures
import datetime
import enum
import inspect
import json
import os
import random
import re
import sys
import time
from textwrap import dedent

import requests
import unidecode

from codesapogee import apogee, filtreECUE
from salles import amphis, salles_TP


# Logging
class LogLevel(enum.Enum):
    """
    An enumeration of log levels.
    """

    INFO = 0
    """Informative message."""
    SUCCESS = 1
    """Success message."""
    WARNING = 2
    """Warning message."""
    ERROR = 3
    """Error message."""

    def color(self):
        """
        Returns the ANSI color code for the log level.
        See https://en.wikipedia.org/wiki/ANSI_escape_code for the colors.

        Returns:
            str: The ANSI color code.
        """
        match self:
            case LogLevel.INFO:
                return "\033[34m"
            case LogLevel.SUCCESS:
                return "\033[32m"
            case LogLevel.WARNING:
                return "\033[33m"
            case LogLevel.ERROR:
                return "\033[31m"
            case _:
                return ""

    def label(self):
        """
        Returns the label for the log level.

        Returns:
            str: The label.
        """
        match self:
            case LogLevel.INFO:
                return "info"
            case LogLevel.SUCCESS:
                return "success"
            case LogLevel.WARNING:
                return "warning"
            case LogLevel.ERROR:
                return "error"
            case _:
                return "unknown"


log_level = LogLevel.SUCCESS
"""The log level. Defaults to LogLevel.SUCCESS. Only messages with a level greater or equal to this level will be logged."""


def log(msg: str, level: LogLevel = LogLevel.INFO):
    """
    Logs a message with a specified log level.

    Args:
        msg (str): The message to log.
        level (LogLevel, optional): The log level. Defaults to LogLevel.INFO.
    """

    if level.value < log_level.value:
        return

    timestamp = datetime.datetime.now(datetime.UTC).isoformat(timespec="seconds")

    frame = inspect.currentframe()

    # Get the line number of the caller
    line_no = 0
    # Some day, Python will have a null coalescing operator or optional chaining...
    # And I'll be able to simply write inspect.currentframe()?.f_back?.f_lineno ?? 0
    if frame is not None:
        if frame.f_back is not None:
            line_no = frame.f_back.f_lineno

    print(
        f"{timestamp} {sys.argv[0]}:{line_no}: {level.color()}[{level.label()}] {msg}\033[0m"
    )


# Common regexps
# Compiled once for all
re_begin_end = re.compile(
    "DTSTART:(\\d{8}T\\d{6}Z).*?DTEND:(\\d{8}T\\d{6}Z)", re.DOTALL
)
re_salle = re.compile("LOCATION:([a-zA-Z]* - [0-9A-Z]+ -) ([0-9]+)")
re_summary = re.compile("SUMMARY:(.*)")
re_shift = re.compile("(DTSTART:20\\d{2}082[23]T)(\\d{2})(\\d{4})Z")
# si l'on veut recuperer tout le vevent
re_vevent = re.compile("BEGIN:VEVENT.*?END:VEVENT", re.DOTALL)
# Fonction de recherche pour les fichiers modifies avec l'heure de Paris:
re_begin_end_paris = re.compile(
    "DTSTART;TZID=Europe/Paris:(\\d{8}T\\d{6}).*?DTEND;TZID=Europe/Paris:(\\d{8}T\\d{6})",
    re.DOTALL,
)
re_variable = re.compile(
    "(DTSTAMP:.*\n)|(LAST-MODIFIED:.*\n)|(CREATED:.*\n)|(SEQUENCE:.*\n)|(ORIGSTART:.*\n)|(ORIGEND:.*\n)|(UID:.*\n{0,1}[ a-z0-9]*\n)|(LAST-MODIFIED:.*\n)|\\s\\s.*|(DESCRIPTION:.*)"
)
re_export = re.compile("\\(.*?\\)|\n", re.DOTALL)


class ProgArgs(argparse.Namespace):
    """
    A class representing the program arguments.
    """

    dryrun: bool
    """Whether to perform a dry run."""
    verbose: bool
    """Whether to enable verbose logging."""
    start: str
    """The start date of the time range in YYYY-MM-DD format."""
    end: str
    """The end date of the time range in YYYY-MM-DD format."""
    year: int
    """The year from ADE."""
    fiche_etalon: str
    """The fiche etalon."""
    formations: str
    """The path to the formations file, describing calendars view."""
    calendars: str
    """The path to the calendars file, describing calendar views."""
    outdir: str
    """The output directory."""
    oldoutdir: str
    """The old output directory."""
    external: str
    """The external calendar file."""
    fatal: bool
    """Whether to exit on error."""
    presets: str
    """Automatic choice for start, end, outdir."""


class Backoff:
    """
    A class implementing a backoff strategy.
    """

    base_delay: float
    """The base delay for the backoff strategy."""

    max_delay: float
    """The maximum delay for the backoff strategy."""

    max_retries: int
    """The maximum number of retries."""

    attempts: int
    """The number of attempts."""

    def __init__(self, base_delay: float, max_delay: float, max_retries: int):
        """
        Initializes a Backoff instance.

        Args:
            base (int, optional): The base of the exponential backoff. Defaults to 2.
            max (int, optional): The maximum backoff time. Defaults to 30.
        """
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.max_retries = max_retries
        self.attempts = 0

    def next(self) -> float | None:
        """
        Returns the current backoff time, or None if the max number of retries has been reached.
        """
        if self.attempts >= self.max_retries:
            return None
        ret = random.uniform(0, min(self.max_delay, self.base_delay * 2**self.attempts))
        self.attempts += 1
        return ret

    def reset(self):
        """
        Resets the backoff time.
        """
        self.attempts = 0


def fetch_ical(
    code: str,
    start: str = "2024-08-23",
    end: str = "2025-07-17",
    year: int = 5,  # base 2024-25
    fiche_etalon: str = "58598,",
) -> str:
    """
    Retrieves the iCal calendar for a given course code and time range.

    Args:
        code (str): The course code.
        start (str, optional): The start date of the time range in YYYY-MM-DD format. Defaults to "2023-08-23".
        end (str, optional): The end date of the time range in YYYY-MM-DD format. Defaults to "2024-07-17".
        year (int, optional): The projectId from ADE. Defaults to 2.
        fiche_etalon (str, optional): The fiche etalon. Defaults to "".

    Returns:
        str: The iCal calendar as a string.
    """
    # url = 'https://adeprod.app.univ-paris-diderot.fr:443/jsp/custom/modules/plannings/anonymous_cal.jsp'
    # adeconsult 2023-05-30
    url = "https://adeconsult.app.u-paris.fr/jsp/custom/modules/plannings/anonymous_cal.jsp"
    params = {
        "calType": "ical",
        "firstDate": start,
        "lastDate": end,
        "resources": fiche_etalon + code,
        "projectId": year,
    }

    response = requests.get(url, params=params, timeout=5)
    return response.text


def modif_dates(match: re.Match[str], shift: int) -> str:
    """
    Fonction auxiliaire qui corrige la chaîne de deux lignes consécutives DTSTART DTEND
    ADE introduit un décalage qui depend de l'heure d'été/hiver.
    Il y a en plus un problème de 24h lorsque les heures voulues sont vers l'apres midi.
    - En 2021-2022 jusqu'au 15/10/21 le shift est de -10 et l'heure frontière du jour perdu est à 12h.
      !le 16/10/21 le shift d'été est passé brutalement à -9 et l'heure frontière à 13h!
    - En 2020-2021 le shift est de -11 en ete et l'heure frontière du jour perdu est à 11h.
    - En 2019-2020 le shift est de -12 en ete et l'heure frontière du jour perdu est à 10h.
      De plus les cours qui terminaient à 20h en 19-20 ne semble pas transmis par ADE...

    * REMARQUE dans tous ces cas on peut maintenant deviner la formule:

            heurefrontiere - shiftete = 22h

    * En hiver il faut encore retrancher 1 au shift.

    * ADE613: Attention ce comportement a maintenant l'air de ne dépendre que de l'heure du debut de l'évènement.

    match est la valeur trouvée par:

        re.compile('DTSTART:(\\d{8}T\\d{6}Z).*?DTEND:(\\d{8}T\\d{6}Z)',re.DOTALL)
    """
    start = datetime.datetime.strptime(match.group(1), "%Y%m%dT%H%M%SZ")
    end = datetime.datetime.strptime(match.group(2), "%Y%m%dT%H%M%SZ")
    orig = (
        "ORIGSTART:%d%02d%02dT%02d%02d%02dZ\r\nORIGEND:%d%02d%02dT%02d%02d%02dZ\r\n"
        % (
            start.year,
            start.month,
            start.day,
            start.hour,
            start.minute,
            start.second,
            end.year,
            end.month,
            end.day,
            end.hour,
            end.minute,
            end.second,
        )
    )

    # PB le shift change avec l'heure d'hiver/ete:
    date1 = datetime.datetime(start.year, 10, 31)
    date2 = datetime.datetime(start.year, 3, 31)
    last_sunday_oct = date1 - datetime.timedelta(days=(date1.weekday() + 1) % 7)
    last_sunday_march = date2 - datetime.timedelta(days=(date2.weekday() + 1) % 7)
    # shift a ajouter aux heures recues en ete
    # shiftete_manuel = -10 # vaut -10 au semestre 1 2021-2022, avant 21/10/2021.
    # shiftete_manuel = -9 # vaut -9 au 22/10/2021. (base 2021-22)

    # shiftete_manuel = -8 # vaut -8 au 3/6/2022 sur la base 2022-23
    # shift_summer_manual = 5  # valeur au 2023-05-30 sur la base 4  ADECONSULT
    # shift_summer_manual = 7  # chgt valeur au 2023-10-20 sur la base 4  ADECONSULT
    # shift_summer_manual = 8  # chgt valeur au 2023-11-14 sur la base 4  ADECONSULT
    # shift_summer_manual = -15  # chgt valeur au 2023-11-24 sur la base 4  ADECONSULT
    # shift_summer_manual = -14  # ENCORE un chgt valeur au 2023-12-04 sur la base 4  ADECONSULT
    # shift_summer_manual = -15  # ENCORE un chgt valeur au 2023-12-06 sur la base 2  ADECONSULT
    shift_summer_manual = (
        2  # ENCORE un chgt valeur au 2024-02-05 sur la base 2  ADECONSULT
    )

    # frontiere ou le bug de jour apparait
    # Remarque dans tous les exmples on a heurefrontiere = shiftete + 22
    # heurefrontiere_manuel = 12 # vaut 12h au semestre 1 2021-2022, avant 21/10/2021

    # inutilisé ?
    _frontier_hour_manual = 13  # vaut 13, au 22/10/2021

    #
    # on utilise le shift etalon.
    shift_summer = shift
    frontier_hour = shift_summer + 22
    if shift != shift_summer_manual:
        log(
            f"Décalage {shift} != {shift_summer_manual}. La valeur du shift n'est pas celle connue pour l'année la plus récente.",
            LogLevel.WARNING,
        )
        # print("[WARNING] on utilise l'heurefrontiere 22+shiftete; à VERIFIER!")

    if start.month > 7:
        # l'annee vaut pour aout-decembre. (Semestre 1)

        # if debut.year == 2021:
        # annee 2021-2022
        # on a un etalon pour 2021-2022 on evite la config manuelle
        # heurefrontiere = 12
        # shiftete = -10

        if start.year == 2020:
            # annee 2020-2021
            frontier_hour = 11
            shift_summer = -11
        if start.year == 2019:
            # annee 2019-2020
            frontier_hour = 10
            shift_summer = -12

        if start >= last_sunday_oct:
            # print("hiver")
            shift = shift_summer - 1
        else:
            # print("ete")
            shift = shift_summer
    if start.month < 8:
        # l'annee vaut pour janvier-juillet (Semestre2)
        # if debut.year == 2022:
        # annee 2021-2022
        # on a un etalon pour 2021-2022 on evite la config manuelle
        # heurefrontiere = 13
        # shiftete = -9

        if start.year == 2021:
            # annee 2020-2021
            frontier_hour = 11
            shift_summer = -11
        if start.year == 2020:
            # annee 2019-2020
            frontier_hour = 10
            shift_summer = -12

        # Ces 4 reservations sont les jeudis de 10h45-12h45
        # 2021-04-01|21:45:00|2021-03-31|23:45:00|ALGORITHMIQUE|432C
        # 2021-02-11|22:45:00|2021-02-11|00:45:00|ALGORITHMIQUE|432C
        # 2021-02-18|22:45:00|2021-02-18|00:45:00|ALGORITHMIQUE|432C
        # 2021-03-04|22:45:00|2021-03-04|00:45:00|ALGORITHMIQUE|432C
        if start < last_sunday_march:
            # print("hiver")
            shift = shift_summer - 1
        else:
            # print("ete")
            shift = shift_summer

    # parfois il manque un jour a la date de fin, Exemple:
    # ORIGSTART:20210915T201500Z
    # ORIGEND:20210914T221500Z
    #
    # il existe des créneaux dont le debut et la fin sont la veille!
    #
    # Ex 6736.ics (avec shift = -10)
    # debut et fin peuvent etre le jour d'avant
    # ORIGSTART:20210912T221500Z
    # ORIGEND:20210912T234500Z
    #
    # Ex 6658.ics
    # ORIGSTART:20210823T180000Z
    # ORIGEND:20210823T184500Z
    # SUMMARY:étalon pour Calendar
    # pour IP1 le lundi 13/9 a 13h45 (paris)
    # ORIGSTART:20210912T234500Z
    # ORIGEND:20210913T014500Z
    #
    #
    # En fait il semble que si l'heure voulue etait apres:
    # 12h au semestre1 2021-2022 (13h à partir du 16/10/21), et 11h en 2020-2021,
    # ADE a perdu un jour
    # en voulant faire une certaine modif de decalage.
    #
    fix_for_ade_version_after_613 = False
    if start.hour >= frontier_hour - shift or start.hour <= 21 - shift - 24:
        # si l'heure voulue >= heurefrontiere et <= 20h
        # dans ce cas il faut augmenter d'un jour avant d'appliquer le shift
        # TODO: on peut maintenant reserver jusque 21h!
        start = start + datetime.timedelta(hours=24)
        fix_for_ade_version_after_613 = True

    if (
        end.hour >= frontier_hour - shift or end.hour <= 21 - shift - 24
    ) and fix_for_ade_version_after_613:
        # si l'heure voulue >= heurefrontiere et <= 20h
        # dans ce cas il faut augmenter d'un jour
        end = end + datetime.timedelta(hours=24)

    # On a ajusté les decalages de jours, on peut appliquer le shift a tous.
    start = start + datetime.timedelta(hours=shift)
    end = end + datetime.timedelta(hours=shift)

    return (
        orig
        + "DTSTART;TZID=Europe/Paris:%d%02d%02dT%02d%02d%02d\r\nDTEND;TZID=Europe/Paris:%d%02d%02dT%02d%02d%02d"
        % (
            start.year,
            start.month,
            start.day,
            start.hour,
            start.minute,
            start.second,
            end.year,
            end.month,
            end.day,
            end.hour,
            end.minute,
            end.second,
        )
    )


def modif_salle(match_salle: re.Match[str]):
    """
    En entrée un match de:
        re.compile('LOCATION:([a-zA-Z]* - \\w+ -) ([0-9]+)')
    Ex: Halle - 331C -
    en sortie: "TP" si c'est une salle de TP connue. sinon une chaine vide.
    """

    salle: str = match_salle.group(1)
    effectif: str = match_salle.group(2)
    if salle in salles_TP:
        salle = salle + "TP-"
    # elif salle in amphis:
    # On desactive le tag des granges salles car maintenant le titre
    # fait souvent apparaitre CM ou TD.
    #    salle = salle + "CM?-"
    #
    salle = f"LOCATION:{salle} ({effectif}p)"
    return salle


def modif_vevent(match_event: re.Match[str], shift: int, ical_name: str):
    """
    En entrée, event est un match d'un VEVENT,
    en sortie le VEVENT modifé:
    - correction des heures en appelant modifdate
    - détection des salles de TP et ajout du tag
    """
    event = match_event.group(0)
    # il vaut mieux celle ci au cas ou les nouvelles lignes ne soient pas \r\n selon l'OS.
    # pour rebeginend on suppose qu'ils sont ordonnes DTSTART avant DTEND
    # fonction de recherche pour les fichiers emis par ADE.
    # on corrige les heures
    event = re_begin_end.sub(lambda m: modif_dates(m, shift), event)
    #
    event = re_salle.sub(lambda m: modif_salle(m), event)

    match = re_summary.search(event)

    code = ical_name

    if match != None:
        summary = match.group(1)
        if summary.endswith("\r"):
            summary = summary.replace("\r", "")
            chariot = "\r"
        else:
            chariot = ""

        if code in apogee:
            summary2 = summary.replace("\\", "")
            if re.match(
                ".* CMT[DP][0-9]{2}$|.* T[DP]7?[0-9]{2}$|.* CM[0-9]{2}$", summary2
            ):
                # summary = summary[:-2]
                summary2 = summary2[:-2]
            if re.match(".* CMT[DP][0-9]$|.* T[DP][0-9]$|.* CM[0-9]$", summary2):
                # summary = summary[:-1]
                summary2 = summary2[:-1]
            summary2 = re.sub(" CMT[DP]$| T[DP]$| CM$", "", summary2)

            dict_without_accents: dict[str, str] = {}
            for dict_with_accents in apogee[code]:
                dict_without_accents[unidecode.unidecode(dict_with_accents)] = (
                    dict_with_accents
                )
            if summary2 in apogee[code]:
                event = re_summary.sub(
                    lambda m: "SUMMARY:%s (%s)%s"
                    % (summary, apogee[code][summary2], chariot),
                    event,
                )
            elif summary2 in dict_without_accents:
                summary2 = dict_without_accents[summary2]
                event = re_summary.sub(
                    lambda _m: f"SUMMARY:{summary} ({apogee[code][summary2]}){chariot}",
                    event,
                )
    return event


def fix_timezone(ical: str, ical_name: str = "", enable_FATAL: bool = True):
    """
    La fonction transforme un calendrier en utilisant des fonctions auxilaires pour:
        - réparer les données de début et fin.
          DTSTART:20210915T183000Z
          DTEND:20210915T203000Z
        - Vérifier que le calendrier n'a pas de créneaux incohérents.
        - Détecter les salles de TP et amphis car ces données ne sont pas présentes dans le calendrier émis par ADE.
    """
    index = 2

    m = re_shift.search(ical)
    shift_UTC = 0
    if not m:
        shift = 2 - shift_UTC
        log(
            f"{ical_name}: no reference for etalon 0823T, set shift to {shift}",
            LogLevel.WARNING,
        )
        # NB le shift passe de -10 a -9 le 22/10/2021
        # NB le shift sur la base 2022-23 semble etre à -8 ke 3/6/2022.
    else:
        shift = -shift_UTC + 8 - int(m.group(index))  # le vrai shift sans le modulo.
        # if (shift != -decalageUTC -10):
        #    print("[WARNING] %s: %s -> shift = %d  != %d)"%(icalname, m.group(0),shift,-decalageUTC-10))

    # ical = rebeginend.sub(lambda m: modifdate(m,shift), ical)
    ical = re_vevent.sub(lambda m: modif_vevent(m, shift, ical_name), ical)

    # Quelques verifs
    list_event = re_vevent.finditer(ical)
    tmp_count = 0
    for m_event in list_event:
        L = re_begin_end_paris.findall(m_event.group(0))
        if len(L) == 1:
            m = L[0]
            start = datetime.datetime.strptime(m[0], "%Y%m%dT%H%M%S")
            end = datetime.datetime.strptime(m[1], "%Y%m%dT%H%M%S")
            tmp_count += 1
            if end - start < datetime.timedelta(hours=0):
                # probleme il reste un créneau negatif.
                log(
                    f"{ical_name}: créneau mal corrige {m}",
                    LogLevel.ERROR,
                )
                if enable_FATAL:
                    return None
            if end - start > datetime.timedelta(hours=8):
                # tres rare mais ca existe, Ex en L1 info/biole 19/10/21
                log(
                    f"{ical_name}: créneau de plus de 8h {str(m)}",
                    LogLevel.WARNING,
                )
            if end - start > datetime.timedelta(hours=13):
                # il y a maintenant des reservations de 8h-20h45 ...
                log(
                    f"{ical_name}: créneau de plus de 13h {m}",
                    LogLevel.ERROR,
                )
                if enable_FATAL:
                    return None
            if start.weekday() == 6 or end.weekday() == 6:
                log(
                    f"{ical_name}: créneau sur un dimanche {str(m)}",
                    LogLevel.ERROR,
                )
                if enable_FATAL:
                    return None

        else:
            log(
                f"{ical_name}: vevent contient {len(L)} start/end: {m_event.group(0)}.",
                LogLevel.ERROR,
            )
            return None

    log(f"({ical_name}): {tmp_count} fiches trouvées et vérifiées.", LogLevel.SUCCESS)

    return ical


def search_moves(
    cal: str = "calendars.json",
    out_dir: str = "data",
    old_out_dir: str = "data.28",
    label_obsolete: str = "obsolète",
):
    """
    Cherche les différences dans les deux versions de tous les calendriers de chaque formation pour:

    - Créer pour chaque formation un calendrier 1234.ics où 1234 est le code de la formation.
      (ie en general (*) le code à gauche dans formations.json)
    - ce 1234.ics contient les anciens événements qui ont été modifiés ou supprimés.
    - si l'on déclare 1234.ics comme un groupe de la formation avec le label 'obsolète' , on pourra voir ces modifications.

    (*) En fait certain groupes ont une formation mère mais sont présents et affichés dans une autre.
    (ex en l3 mathinfo 2 codes formations meres: 2418 et 7426). On utilise donc le fichier
    calendars.json où l'on crée des listes de tous les labels attachés à la formation.
    """

    # on recupere les noms des boutons via le code, on utilise donc calendars.json
    noms: dict[str, str] = {}
    list_formations: dict[str, list[str]] = {}
    # la liste des formations qui ont un bouton obsolete.
    obsolete_found: list[str] = []
    # deux ensembles pour s'assurer qu'un code de groupe n'a pas ete saisi dans un code pour bouton obsolete
    obsolete_set = set[str]()
    group_set = set[str]()
    with open(cal) as io_cal:
        for l in json.load(io_cal):
            # un dictionnaire pour trouver le label d'une formation
            if str(l["code"]) not in noms:
                # il y a des entrees qui ont plusieurs noms de bouton
                # Ex: Socio en miash et MIASHS-S2 en formation socio
                # donc on prend plutot la premiere entree.
                noms[str(l["code"])] = l["label"]
            # Une formation = année + parcours. Ex: l1 math
            if not l["parcours"] + l["year"] in list_formations:
                list_formations[l["parcours"] + l["year"]] = []
            if l["label"] == label_obsolete:
                # On place le code de la formation en premier
                list_formations[l["parcours"] + l["year"]] = [
                    str(l["code"])
                ] + list_formations[l["parcours"] + l["year"]]
                # OK on note qu'il y a bien un bouton obsolete pour cette formation
                obsolete_found.append(l["parcours"] + l["year"])
                obsolete_set.update({l["code"]})
            else:
                # ensuite on place les codes des groupes
                (list_formations[l["parcours"] + l["year"]]).append(str(l["code"]))
                group_set.update({l["code"]})

        if not obsolete_set.isdisjoint(group_set):
            log(
                f"[ERROR] un code de fiche est présent dans un code pour archive obsolète: {obsolete_set.intersection(group_set)}",
                LogLevel.ERROR,
            )
            exit(1)

        for c in list_formations:
            # Une sécurité s'il n'y a pas de bouton obsolète pour cette formation
            # pour ne pas écraser son calendrier
            if c in obsolete_found:
                # on étudie une formation
                _changes = ""
                fiches = list_formations[c][1:]
                code_formation = list_formations[c][0]
                old_events: dict[int, str] = {}
                num_orig = 0
                for code in fiches:
                    try:
                        with open("%s/%s.ics" % (out_dir, code), "r") as io_new:
                            cal_new = io_new.read()
                        with open("%s/%s.ics" % (old_out_dir, code), "r") as io_old:
                            cal_old = io_old.read()

                        for m_event in re_vevent.finditer(cal_old):
                            event = m_event.group(0)
                            reliable = re_export.sub("", re_variable.sub("", event))
                            # on ajoute le groupe dans le hash au cas ou une fiche commune soit modifiee
                            # fiable=fiable.replace('\n','')
                            reliable = reliable.replace("\\,", "")
                            reliable = reliable.replace(",", "")
                            reliable = reliable.replace(
                                "SUMMARY:", "SUMMARY:[%s]" % (noms[code])
                            )
                            old_events[hash(reliable)] = event.replace(
                                "SUMMARY:", "SUMMARY:[%s]" % (noms[code])
                            )
                        # on regarde le total des événements d'une page.
                        num_orig += len(old_events)
                        for m_event in re_vevent.finditer(cal_new):
                            event = m_event.group(0)
                            reliable = re_export.sub("", re_variable.sub("", event))
                            # fiable=fiable.replace('\n','')
                            reliable = reliable.replace("\\,", "")
                            reliable = reliable.replace(",", "")
                            # on ajoute le groupe dans le hash au cas ou une fiche commune soit modifiee
                            reliable = reliable.replace(
                                "SUMMARY:", "SUMMARY:[%s]" % (noms[code])
                            )
                            old_events.pop(hash(reliable), None)
                    except:
                        log(
                            f"Échec dans le diff de ({code}) {c}. (manque archive?) => on crée un cal. vide",
                            LogLevel.WARNING,
                        )

                # On ajoute un calendrier pour toutes les fiches.
                with open(f"{out_dir}/{code_formation}.ics", "w") as f:
                    f.write(
                        dedent(
                            """\
                            BEGIN:VCALENDAR
                            METHOD:REQUEST
                            PRODID:-//ADE/version 6.0
                            VERSION:2.0
                            CALSCALE:GREGORIAN
                            """
                            # the last newline is important!
                        )
                    )
                    if len(old_events) < 50 or len(old_events) * 4 < num_orig:
                        for key in old_events:
                            f.write(re_variable.sub("", old_events[key]) + "\n")
                    else:
                        log(
                            dedent(
                                f"""\
                                ({c}) plus de 50 changements et plus de 1/4 de modifications; on ne les enregistre pas.
                                Si les données de référence (data.28) sont fiables il faut vérifier data.
                                (et voir s'il n'y a pas un problème de shift/calibrage ADE?)\
                                """
                            ),
                            LogLevel.WARNING,
                        )

                    f.write("END:VCALENDAR\n")


def tests():
    """
    Une fonction de test pour traiter un exemple avec shift de -11h si l'on n'arrive pas
    a obtenir de tels exemples.
    """
    cal = "test_6651L1MATH3delta_moins11.ics"
    with open(cal) as f:
        ical = f.read()
        ical = fix_timezone(ical)
        if ical is None:
            log(f"{cal}: impossible de réparer la timezone", LogLevel.ERROR)
            return

    log("Test L1 MATH3 semaine du 11/10/21")
    with open("data/6651.ics", "w") as dest:
        dest = open("data/6651.ics", "w")
        dest.write(ical)

    cal = "test_5510L3MIASHS1delta_moins11.ics"
    with open(cal) as f2:
        ical = f2.read()
        ical = fix_timezone(ical)
        if ical is None:
            log(f"{cal}: impossible de réparer la timezone", LogLevel.ERROR)
            return

    log("Test L3 MIASHS GR1 semaine du 15/11/21")
    with open("data/5510.ics", "w") as dest2:
        dest2.write(ical)


def list_calendars(fname: str):
    """
    Le fichier formation contient le code d'une formation annuelle et de ses sous fiches ADE.
    On ajoute au calendrier de la sous fiche celui de la formation parente car certains evenements
    peuvent y etre saisis.

    ADE6.13: il ne faut plus fusionner les fiches parents car leur calendrier contient maintenenant
    toutes ses fiches enfants. Il faut donc les retirer dans formations.json
    """
    rep: list[str] = []
    with open(fname) as cfile:
        for c in json.load(cfile):
            fiches = (c["fiches"]).split(",")
            for j in fiches:
                if j != "":
                    rep.append(str(c["code"]) + "," + j)
                else:
                    rep.append(str(c["code"]))

        return rep


def get_single_calendar(
    code: str,
    out_dir: str,
    start: str,
    end: str,
    year: int,
    fiche_etalon: str,
    dry_run: bool,
    fatal: bool,
):
    """
    Fetches an iCalendar file and saves it to a specified directory.

    Args:
        code (str): The formation code.
        out_dir (str): The directory where the iCalendar files will be saved.
        start (str, optional): The start date of the academic year. Defaults to "2023-08-23".
        end (str, optional): The end date of the academic year. Defaults to "2024-07-17".
        year (int, optional): The academic year. Defaults to 4.
        fiche_etalon (str, optional): The reference formation code. Defaults to "".
        dry_run (bool, optional): If True, the function will only print the first 300 characters of each iCalendar file. Defaults to False.
        fatal (bool, optional): If True, the function will raise an error if it encounters an invalid timezone. Defaults to True.
    """

    # on prend le nom de la derniere fiche
    nomfiche = code.split(",")[-1]
    # on autorise le dernier element a etre une chaine pour creer un calendrier par fusion de nom
    # qui n'est pas un numero de fiche a telecharger.
    if not nomfiche.isnumeric():
        # le dernier argument n'est pas numerique on le retire il ne faut pas tenter de le telecharger.
        code = code.removesuffix("," + nomfiche)
    fname = f"{out_dir}/{nomfiche}.ics"
    log(f"Fetching {code} -> {fname}.")

    backoff = Backoff(0.1, 1, 5)
    calendar = None
    while calendar is None:
        delay = backoff.next()
        if delay is None:
            log(f"{code} -> trop de tentatives", LogLevel.ERROR)
            return

        try:
            calendar = fetch_ical(code, start, end, year, fiche_etalon)
            # check we actually got a calendar
            if not calendar.startswith("BEGIN:VCALENDAR"):
                calendar25 = calendar[:25]
                calendar = None  # sinon le while ne fait pas d'autres tours.
                raise Exception(f"{code} -> pas de ressource {calendar25}")
        except Exception as e:
            log(f"{code} -> {e}", LogLevel.ERROR)
            time.sleep(delay)
            continue

    calendar = fix_timezone(calendar, nomfiche, fatal)

    if calendar is None:
        log(
            f"{calendar}:{nomfiche} -> impossible de réparer le fuseau horaire",
            LogLevel.ERROR,
        )
        return

    # Ajout de sous calendriers par ECUE dans certaines formations
    if nomfiche in filtreECUE:
        subcalendars = make_filter_ECUE(nomfiche, calendar, filtreECUE[nomfiche])
        for sc in subcalendars:
            fnamesub = "%s/%s.ics" % (out_dir, sc)
            tmp = subcalendars[sc]
            with open(fnamesub, "w") as f:
                f.write(tmp)

    if dry_run:
        log(calendar[:300])
    else:
        with open(fname, "w") as f:
            f.write(calendar)


def get_all_calendars(
    executor: concurrent.futures.ThreadPoolExecutor,
    formations: str,
    out_dir: str,
    start: str,
    end: str,
    year: int,
    fiche_etalon: str,
    dry_run: bool,
    fatal: bool,
):
    """
    Fetches iCalendar files for a list of formations and saves them to a specified directory.

    Args:
        executor (concurrent.futures.ThreadPoolExecutor): The executor to use for concurrent fetching.
        formations (str): A comma-separated string of formation codes.
        out_dir (str): The directory where the iCalendar files will be saved.
        start (str, optional): The start date of the academic year. Defaults to "2023-08-23".
        end (str, optional): The end date of the academic year. Defaults to "2024-07-17".
        year (int, optional): The academic year. Defaults to 4.
        fiche_etalon (str, optional): The reference formation code. Defaults to "".
        dry_run (bool, optional): If True, the function will only print the first 300 characters of each iCalendar file. Defaults to False.
        fatal (bool, optional): If True, the function will raise an error if it encounters an invalid timezone. Defaults to True.
    """
    for code in list_calendars(formations):
        executor.submit(
            get_single_calendar,
            code,
            out_dir,
            start,
            end,
            year,
            fiche_etalon,
            dry_run,
            fatal,
        )


def make_filter_ECUE(code: str, ical: str, filtre: dict[str, str]):
    """
    Une fonction pour filtrer et creer des sous calendriers à partir d'un calendrier.

    Args:
        code: le code du calendrier d'origine, ie num fiche ADE
        calendrier: le calendrier apres corrections
        filtre: un dictionnaire de filtres: code ECUE/ expression reg
    """
    subcals: dict[str, str] = {}
    start_cal = dedent(
        """\
        BEGIN:VCALENDAR
        METHOD:REQUEST
        PRODID:-//ADE/version 6.0
        VERSION:2.0
        CALSCALE:GREGORIAN\
        """
    )
    end_cal = "\nEND:VCALENDAR"
    for ecue in filtre:
        tmp = str(code) + "." + ecue
        subcals[tmp] = start_cal
    search_UE = [re.compile(filtre[ecue], re.DOTALL) for ecue in filtre]
    L_event = re_vevent.finditer(ical)

    for m_event in L_event:
        event = m_event.group(0)
        event = event.replace("\r", "")
        for i in range(len(filtre)):
            s = search_UE[i]
            ecue = list(filtre)[i]
            if s.match(event) != None:
                subcals[str(code) + "." + ecue] += "\n" + event

    for sc in subcals:
        subcals[sc] += end_cal

    return subcals


def get_external(
    executor: concurrent.futures.ThreadPoolExecutor,
    fcalen: str,
    out_dir: str,
    dry_run: bool = False,
):
    """
    Download external (non ADE) resources.

    Args:
        fcalen (str): json file listing external (non ADE) ressources. Its content must be a list of : { 'id' : xxx, 'url' : www, ... }
        out_dir (str): directory to save ics files
        dry_run (bool, optional): If True, the function will only print the first 200 characters of each iCalendar file. Defaults to False.
    """

    log("Fetching external calendars")

    def curl(url: str):
        r = requests.get(url)
        return r.text

    def get_one_external(c: dict[str, str]):
        fname = f"{out_dir}/{c['id']}.ics"
        log(f"Fetching {c['id']} -> {fname}.")
        cal = curl(c["url"])
        if dry_run:
            log(cal[:200])
        else:
            with open(fname, "w") as f:
                f.write(cal)
        log(f"Done {c['id']} -> {fname}", LogLevel.SUCCESS)

    with open(fcalen) as calenfile:
        for c in json.load(calenfile):
            executor.submit(get_one_external, c)


# paramètres ADE ufr maths
presets = {
    "2024-25": dict(
        start="2024-08-23", end="2025-07-17", year=5, fiche_etalon="58598,"
    ),
    "2023-24": dict(start="2023-08-23", end="2024-07-17", year=2, fiche_etalon="1607,"),
    # "2022-23": dict(start="2022-08-23", end="2023-07-17", year=0, fiche_etalon="1607,"),
    #'2021-22': dict(start="2021-08-23", end="2022-07-17", year=4, fiche_etalon="2769,"),
    #'2020-21': dict(start="2020-08-31", end="2021-07-14", year=15),
    #'2019-20': dict(start="2019-08-31", end="2020-07-14", year=6),
}

parser = argparse.ArgumentParser(description="fetch icalendars from ADE.")

parser.add_argument(
    "--dryrun", "-n", action="store_true", help="dry-run, do not write files"
)
parser.add_argument(
    "--verbose", "-v", action="store_true", help="verbose, show progress"
)
parser.add_argument(
    "--start", type=str, default="2024-08-23", help="first day, format yyyy-mm-dd"
)
parser.add_argument(
    "--end", type=str, default="2025-07-17", help="last day, format yyyy-mm-dd"
)
parser.add_argument("--year", type=int, default=5, help="ADE year")  #
parser.add_argument(
    "--fiche_etalon",
    type=str,
    default="58598,",
    help="fiches à ajouter à chaque récupération",
)
parser.add_argument(
    "--formations",
    type=str,
    default="formations.json",
    help="json file describing calendar views",
)
parser.add_argument(
    "--calendars",
    type=str,
    default="calendars.json",
    help="json file describing calendar views",
)
parser.add_argument(
    "--outdir", type=str, default="data", help="directory to save ics files"
)
parser.add_argument(
    "--oldoutdir",
    type=str,
    default="data.28",
    help="directory to save old ics files for diff button",
)
parser.add_argument(
    "--external",
    type=str,
    default="calendars_external.json",
    help="json file listing external (non ADE) ressources",
)

parser.add_argument(
    "--fatal",
    type=bool,
    default=True,
    help="enable None output instead of broken calendars",
)
parser.add_argument(
    "--presets",
    choices=presets.keys(),
    help="automatic choice of --start, --end, --outdir options",
)

if __name__ == "__main__":
    args_nsp = ProgArgs()
    args = parser.parse_args(namespace=args_nsp)

    if args.verbose:
        log_level = LogLevel.INFO

    if args.presets:
        args.outdir = "data/%s" % args.presets
        args.oldoutdir = "data.28/%s" % args.presets
        args.__dict__.update(presets[args.presets])

    if not os.path.isdir(args.outdir):
        log(f"Creating directory: {args.outdir}")
        os.mkdir(args.outdir)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        if args.formations:
            get_all_calendars(
                executor,
                args.formations,
                args.outdir,
                args.start,
                args.end,
                args.year,
                args.fiche_etalon,
                dry_run=args.dryrun,
                fatal=args.fatal,
            )

        if args.external:
            get_external(
                executor,
                args.external,
                args.outdir,
                dry_run=args.dryrun,
            )

    if args.calendars:
        search_moves(
            args.calendars,
            args.outdir,
            args.oldoutdir,
        )
