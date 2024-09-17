#!/usr/bin/python
# coding: utf-8

import datetime
import json
import os.path
import re
import shutil
import time

import feedparser
import pytz
import requests

from calendriersfromtitres import (
    liens_rss,
    nextcloud_rss,
    titretocal1,
    titretocal1sdv,
    titretocal2,
    titretocal2sdv,
    titretocal3,
)
from codesapogee import apogee, filtreECUE

verbose = False


from get_ical import make_filter_ECUE, modif_salle, search_moves

regroupe = re.compile(
    "<p>(\d{2})/(\d{2})/(\d{4}) (\d{2}h\d{2}) - (\d{2}h\d{2})</p>.*<b>Ressources</b><br />(.*)<br />"
)

relocation = re.compile("^([a-zA-Z]* - \w+ -).*[0-9]+")
resummary = re.compile("SUMMARY:(.*)")
revevent = re.compile("BEGIN:VEVENT.*?END:VEVENT", re.DOTALL)
rebeginendparis = re.compile(
    "DTSTART;TZID=Europe/Paris:(\d{8}T\d{6}).*?DTEND;TZID=Europe/Paris:(\d{8}T\d{6})",
    re.DOTALL,
)
resalle = re.compile("LOCATION:([a-zA-Z]* - [0-9A-Z]+ -) ([0-9]+)")
redtstamp = re.compile("DTSTAMP:(\d{8}T\d{6})Z")
# les L1


def get_rss(nomrss, outdir="data", write=False, url=None, dryrun=False, rssdays=56):
    """
    BROKEN: Il faut que le flux rss soit allumé.
    Si quelqu'un va sous ADE avec firefox et fait une demande de flux RSS, alors meme en quittant firefox, le flux
    semble rester ouvert au moins 15min. (Sous chrome ou safari c'est beaucoup plus court)
    """
    from calendriersfromtitres import liens_rss, nextcloud_rss

    if url == None:
        url = liens_rss[nomrss]
    url = re.sub("&nbDays=\d+&", "&nbDays=%d&" % (rssdays), url)
    r = requests.get(url)
    if r.status_code == 200:
        t = datetime.datetime.now()
        rep = r.text.replace(
            "<channel><title>Planning</title><description>",
            "<channel><title>Planning %02d/%02d/%04d, %02dh%02d</title><description>"
            % (t.day, t.month, t.year, t.hour, t.minute),
        )
        if write:
            if dryrun:
                print(
                    "[DRYRUN] get_rss write in", "%s/%s" % (outdir, nomrss), rep[:200]
                )
            else:
                with open("%s/%s" % (outdir, nomrss), "w") as f:
                    f.write(rep)
    else:
        rep = None
    return rep


def checksalle(T):
    m = relocation.search(T)
    batiments = [
        "Halle",
        "Moulins",
        "Condorcet",
        "Moulins",
        "Gouges",
        "Germain",
        "Lamarck",
        "Lavoisier",
        "Buffon",
    ]
    salle = False
    if m != None:
        m1 = m.group(1).split(" - ")

        if m1[0] in batiments:
            salle = True
    return salle


def filtreoldcal(code, rssdate, olddata="data.1"):
    cal = ""
    calold = ""
    try:
        fold = open("%s/%s.ics" % (olddata, code), "r")
        calold = fold.read()
        fold.close()

    except:
        pass

    for mevent in revevent.finditer(calold):
        L = rebeginendparis.findall(mevent.group(0))
        if len(L) == 1:
            m = L[0]
            debut = datetime.datetime.strptime(m[0], "%Y%m%dT%H%M%S")
            # On ne met pas a jour au premier jour du flux car il manque les evenements
            # qui sont a cheval sur le bug horaire, meme si on ne voit pas de bug dans le
            # flux RSS, le fait d'avoir perdu un jour pose PB sur le premier jour du flux.
            if debut < datetime.datetime(
                rssdate.year, rssdate.month, rssdate.day, 23, 59, 0, 0
            ):
                cal += mevent.group(0) + "\n"

    return cal


def writecal(
    codeformation,
    calendriers,
    rssdate,
    outdir="data",
    moveto_olddir=False,
    olddata="data.1",
):
    """
    Ecrit un nouveau calendrier, et crée ses sous calendriers s'il en a.
    - Si moveto_olddir est true, il copie le calendrier dans data.1 avant dans mettre un nouveau.
    """
    if moveto_olddir:
        if os.path.exists("%s/%s.ics" % (outdir, codeformation)):
            shutil.copy2(
                "%s/%s.ics" % (outdir, codeformation),
                "%s/%s.ics" % (olddata, codeformation),
            )

    with open("%s/%s.ics" % (outdir, codeformation), "w+") as f:
        f.write("BEGIN:VCALENDAR\n")
        f.write("METHOD:REQUEST\n")
        f.write("PRODID:-//ADE/version 6.0\n")
        f.write("VERSION:2.0\n")
        f.write("CALSCALE:GREGORIAN\n")
        for listeev in calendriers[codeformation]:
            f.write("BEGIN:VEVENT\n")
            for i in listeev:
                f.write("%s\n" % (i))
            f.write("END:VEVENT\n")

        # on insere le vieux calendrier.
        f.write(filtreoldcal(codeformation, rssdate))
        f.write("END:VCALENDAR\n")
        f.seek(0)
        calendar = f.read()

    # Ajout de sous calendriers par ECUE dans certaines formations
    nomfiche = str(codeformation)
    if nomfiche in filtreECUE:
        subcalendars = make_filter_ECUE(nomfiche, calendar, filtreECUE[nomfiche])
        for sc in subcalendars:
            fnamesub = "%s/%s.ics" % (outdir, sc)
            tmp = subcalendars[sc]
            if moveto_olddir:
                shutil.copy2(fnamesub, "%s/%s.ics" % (olddata, sc))
            fsub = open(fnamesub, "w")
            fsub.write(tmp)
            fsub.close()


def makeical_via_rss(
    nomrss,
    titretocal,
    outdir="data",
    moveto_olddir=False,
    olddata="data.1",
    dryrun=False,
):
    """
    Ne telecharge rien.
    Cree les calendriers à partir des fichiers rss qui sont dans outdir (data)
    """

    url = str(outdir) + "/" + nomrss
    rssdate = datetime.datetime.fromtimestamp(os.path.getmtime(url))

    feed = feedparser.parse(url)
    if "title" in feed.feed:
        feedtitle = feed.feed["title"]
        # on essaie si la date a ete ajoutee dans le titre du flux
        try:
            rssdate = datetime.datetime.strptime(feedtitle, "Planning %d/%m/%Y, %Hh%M")
            print("found timestamp  %s in %s" % (rssdate, nomrss))
        except:
            pass

    paris_time = pytz.timezone("Europe/Paris")
    rssdate_utc = (paris_time.localize(rssdate)).astimezone(pytz.utc)

    calendriers = {}

    for c in titretocal:
        l = titretocal[c]
        for i in l:
            if not i in calendriers:
                calendriers[i] = []

    fichesviatitre = {}

    titresgroupes = set()
    titressalles = set()
    perdu = []

    min_debutdatetime = rssdate
    for c in feed.entries:
        tmp = c["summary_detail"]["value"]
        rep = regroupe.search(tmp)
        D, M, Y = rep.group(1), rep.group(2), rep.group(3)
        debut = (rep.group(4)).replace("h", "")
        fin = (rep.group(5)).replace("h", "")
        debut_datetime = datetime.datetime.strptime(Y + M + D + debut, "%Y%m%d%H%M")
        if debut_datetime < min_debutdatetime:
            min_debutdatetime = debut_datetime
        if min_debutdatetime.date() < rssdate.date():
            # si l'on trouve une date de debut du jour d'avant la date du fichier
            # c'est que le fichier rss a ete telecharge plus d'un jour apres la requette ADE.
            # et que la date n'a pas ete ajoutee dans le titre.
            rssdate = min_debutdatetime

        matiere = c["title"]
        matiereorig = matiere
        summary_detail = rep.group(6)
        gpesetsalle = re.split("<br ?/>", summary_detail)
        groupes_evenement = []
        desc = ""
        location = "LOCATION:"
        for g in gpesetsalle:
            if checksalle(g):
                titressalles.add(g)
                if location != "LOCATION:":
                    location = location + "," + g
                else:
                    location = location + g
            else:
                groupes_evenement.append(g)
                desc = desc + g + " "
                if g in titretocal:
                    code = str(titretocal[g][0])
                    if code in apogee:
                        if matiereorig in apogee[code]:
                            nouvcode = apogee[code][matiereorig]
                            if not nouvcode in matiere:
                                matiere += " (%s)" % (nouvcode)

        # on ajoute les CM? et TP via modifsalle
        location = resalle.sub(lambda m: modif_salle(m), location)

        # La date de creation de la reservation est dans le flux RSS.
        utcpublished = c["published_parsed"]
        publi = datetime.datetime(*utcpublished[:6])
        created = "CREATED:%04d%02d%02dT%02d%02d00Z" % (
            publi.year,
            publi.month,
            publi.day,
            publi.hour,
            publi.minute,
        )

        rssdatestr = "(via RSS le: %02d/%02d/%s %02d:%02d)" % (
            rssdate.day,
            rssdate.month,
            rssdate.year,
            rssdate.hour,
            rssdate.minute,
        )
        desc += rssdatestr
        # titresgroupes=titresgroupes.union(set(groupes_evenement))

        dtstamp = "%s%02d%02dT%02d%02d00Z" % (
            rssdate_utc.year,
            rssdate_utc.month,
            rssdate_utc.day,
            rssdate_utc.hour,
            rssdate_utc.minute,
        )
        event = ["DTSTAMP:%s" % (dtstamp)]
        event.append("DTSTART;TZID=Europe/Paris:%sT%s00" % (Y + M + D, debut))
        event.append("DTEND;TZID=Europe/Paris:%sT%s00" % (Y + M + D, fin))

        event.append("SUMMARY:%s" % (matiere))
        event.append("%s" % (location))
        event.append("DESCRIPTION:%s" % (desc))
        event.append("UID:%s" % (abs(hash(summary_detail + rssdatestr))))
        event.append(created)
        event.append("LAST-MODIFIED:%s" % (dtstamp))

        for g in groupes_evenement:
            if g in titretocal:
                l = titretocal[g]
                for c in l:
                    if debut_datetime > datetime.datetime(
                        rssdate.year, rssdate.month, rssdate.day, 23, 59, 0, 0
                    ):
                        # on n'ajoute pas les elements du permier jour du flux car il peut manquer ceux qui
                        # sont a cheval sur le bug horaire. On commence donc au lendemain.
                        if not event in calendriers[c]:
                            # pour eviter d'inclure 2 fois un meme evenement dans un calendrier
                            # vu que l'on fusionne parfois des fiches
                            (calendriers[c]).append(event)
            else:
                perdu.append(matiere)
                if verbose:
                    print(g)

    for code in calendriers:
        if dryrun:
            print(
                "[DRYRUN] not calling: writecal",
                code,
                list(calendriers)[:8],
                rssdate,
                outdir,
                moveto_olddir,
            )
        else:
            writecal(code, calendriers, rssdate, outdir, moveto_olddir=moveto_olddir)

    if moveto_olddir:
        if dryrun:
            print(
                "[dryrun] copy:",
                "%s/%s" % (outdir, nomrss),
                "%s/%s" % (olddata, nomrss),
            )
        else:
            if os.path.exists("%s/%s" % (outdir, nomrss)):
                shutil.copy2("%s/%s" % (outdir, nomrss), "%s/%s" % (olddata, nomrss))

    return rssdate


def get_nextcloudrss(nomrss, outdir="data", olddata="data.1", dryrun=False):
    """
    * Cette fonction n'interroge pas ADE.
    * data.1/ doit contenir la version actuellement utilisee du fichier rss que l'on veut
    telecharger
    comme on n'a pas acces a la date, on telecharge la nouvelle version, et si elle
    est identique a l'ancienne on copie l'ancienne pour garder l'ancienne date de mise
    a jour.
    """
    url = nextcloud_rss[nomrss]
    if not url.endswith("/download"):
        url = url + "/download"
    print("downloadind %s via nextcloud" % (nomrss))
    rss = (requests.get(url)).text
    # rss.headers['Date'] # heure de la requette http
    nomvieuxrss = "%s/%s" % (olddata, nomrss)
    nomnouveaurss = "%s/%s" % (outdir, nomrss)
    h = 0
    if os.path.isfile(nomvieuxrss):
        with open(nomvieuxrss, "r") as oldf:
            h = hash(oldf.read())

    t_prev = datetime.datetime.fromtimestamp(0)
    try:
        f_prev = feedparser.parse(nomnouveaurss)
        t_prev = datetime.datetime.strptime(
            f_prev.feed["title"], "Planning %d/%m/%Y, %Hh%M"
        )
    except:
        pass

    rep = datetime.datetime.fromtimestamp(0)
    f = feedparser.parse(rss)
    try:
        rep = datetime.datetime.strptime(f.feed["title"], "Planning %d/%m/%Y, %Hh%M")
    except:
        pass

    if rep < t_prev and t_prev.date() == datetime.datetime.now().date():
        # on ne fait rien si le fichier dans data est du jour et plus recent (ou que rep n'a pas de date)
        print("keeping %s" % nomrss)
        return t_prev
    else:
        # les deux ont une date fiable o
        if h == hash(rss):
            # une ancienne version identique existe donc on la copie pour preserver la date.
            if dryrun:
                print("[DRYRUN] get_nextcloudrss:" + "copying old %s" % (nomrss))
            else:
                shutil.copy2(nomvieuxrss, nomnouveaurss)
                print("copying old %s" % (nomrss))
        else:
            if dryrun:
                print("[DRYRUN] get_nextcloudrss:" + "writing new %s" % (nomrss))
            else:
                with open(nomnouveaurss, "w") as f:
                    f.write(rss)
                    print("writing new: %s" % (nomrss))
        return rep


def updateall_rss(
    outdir="data", moveto_olddir=False, olddata="data.1", dryrun=False, rssdays=56
):
    """
    Mise à jour des fichiers rss uniquement avec interogation minimale d'ADE:
      Pas de rotation des données vers data.1, il reste inchangé.
      Cette fonction peut être appellée plusieurs fois par jour.
      1) get_nextcloudrss: On compare la version du fichier nextcloud avec celle qui est deja dans data
         Si la version nextcloud est plus recente, elle prend la place de celle dans data
      2) Si la version du flux rss qui est dans data est du jour meme alors on n'interroge pas ADE.
         Sinon on interroge une fois ADE, si le flux RSS est allumé on fait la suite.
    """
    tryADErss = False
    for rss in nextcloud_rss:
        datarssfile = "%s/%s" % (outdir, rss)
        t = get_nextcloudrss(rss, outdir=outdir, olddata=olddata, dryrun=dryrun)
        if t.date() < datetime.datetime.now().date():
            # ni la version courante ni celle sur nextcloud ne sont du jour
            tryADErss = True

    if tryADErss == False:
        print("local RSS files d'aujourd'hui, on n'interroge pas ADE")

    for rss in liens_rss:
        if tryADErss:
            newrss = get_rss(rss, dryrun=dryrun, rssdays=rssdays)
            datarssfile = "%s/%s" % (outdir, rss)
            if newrss != None:
                print("success via ADE for %s" % rss)
                if dryrun:
                    print("[DRYRUN]", datarssfile, newrss[:110])
                else:
                    with open(datarssfile, "w") as f:
                        print("writing in %s" % (datarssfile), newrss[:110])
                        f.write(newrss)
            else:
                # La premiere tentative a echouee, le flux est ferme
                # on ne fait pas d'autres requettes.
                tryADErss = False
                print("Echec via flux rss ADE")


#################################################
def main(
    url_rssfiles=nextcloud_rss,
    external="calendars_external.json",
    outdir="data",
    moveto_olddir=False,
    olddata="data.1",
    dryrun=False,
    rssdays=56,
):
    """
    * outdir (data): peut etre vide, il recevra les calendriers et les fichiers rss pour archivage.
    * data.1 doit contenir une version courante des calendriers pour garder les evenements anterieurs au contenu rss.
    * data.1 contient aussi les fichiers rss utilises pour creer les calendriers.
    * moveto_olddir: si True, alors
       + on bouge les anciennes versions du fichier vers ce dir. (typiquement data.1)
    * On telecharge les fichiers rss depuis nextcloud, on compare aux version archivees pour preserver les dates
      s'ils n'ont pas changés, et on crée les calendriers en copiant les anciens evenements depuis data.1 et les
      nouveaux depuis les fichiers rss.
    """
    # on met a jour les calendriers qui etaient hors ADE (boutons remarques)
    from get_ical import get_external

    get_external(external, outdir, dry_run=dryrun)
    ## les fichiers telecharges depuis ADE
    ##

    updateall_rss(outdir=outdir, olddata=olddata, dryrun=dryrun, rssdays=rssdays)

    makeical_via_rss(
        "rss-l1sdv",
        titretocal1sdv,
        outdir=outdir,
        moveto_olddir=moveto_olddir,
        dryrun=dryrun,
    )
    makeical_via_rss(
        "rss-l1", titretocal1, outdir=outdir, moveto_olddir=moveto_olddir, dryrun=dryrun
    )
    makeical_via_rss(
        "rss-l2sdv",
        titretocal2sdv,
        outdir=outdir,
        moveto_olddir=moveto_olddir,
        dryrun=dryrun,
    )
    makeical_via_rss(
        "rss-l2", titretocal2, outdir=outdir, moveto_olddir=moveto_olddir, dryrun=dryrun
    )
    makeical_via_rss(
        "rss-l3", titretocal3, outdir=outdir, moveto_olddir=moveto_olddir, dryrun=dryrun
    )

    # creation des calendriers de differences:
    search_moves("calendars.json", outdir)


import argparse

parser = argparse.ArgumentParser(
    description="create icalendars from RSS ADE or nextcloud archive."
)
parser.add_argument(
    "--moveto_olddir",
    "-M",
    action="store_true",
    help="move current data to data.1 before writing a new calendar",
)
parser.add_argument(
    "--outdir", type=str, default="data", help="directory to save ics files"
)
parser.add_argument(
    "--external",
    type=str,
    default="calendars_external.json",
    help="json file listing external (non ADE) ressources",
)
parser.add_argument(
    "--dryrun", "-n", action="store_true", help="dry-run, do not write files"
)
parser.add_argument(
    "--rssdays",
    type=int,
    default=56,
    help="rssdays: number of days to ask ADE in rss request",
)


if __name__ == "__main__":
    args = parser.parse_args()
    print("archive des anciens data dans data.1? %s" % (args.moveto_olddir))
    main(
        moveto_olddir=args.moveto_olddir,
        dryrun=args.dryrun,
        outdir=args.outdir,
        external=args.external,
        rssdays=args.rssdays,
    )
