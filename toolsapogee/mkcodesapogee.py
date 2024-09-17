# script utilisé pour créer les fichier codesapogee.py depuis les csv
# pour creer les csv on peut utiliser le script bash: mkcsvfrompdf.txt
# et créer les pdf en imprimant les activites selectionnees dans ADE

import csv

print("##################################################################")
print("## NE pas Editer manuellement")
print("# Ce fichier est cree automatiquement par toolapogee/mkcodeapogee.py")
print("##################################################################\n")

miashsgenerique = {}
with open("miashsgenerique.csv", "r") as fichier:
    f = csv.reader(fichier, delimiter=",", quotechar='"')
    for ligne in f:
        miashsgenerique[ligne[0]] = ligne[1]

miashsling = {}

with open("miashsling.csv", "r") as fichier:
    f = csv.reader(fichier, delimiter=",", quotechar='"')
    for ligne in f:
        miashsling[ligne[0]] = ligne[1]

uelibreling = {}

with open("linguistique-uelibre.csv", "r") as fichier:
    f = csv.reader(fichier, delimiter=",", quotechar='"')
    for ligne in f:
        uelibreling[ligne[0]] = ligne[1]



l1l2math = {}
with open("l1l2math.csv", "r") as fichier:
    f = csv.reader(fichier, delimiter=",", quotechar='"')
    for ligne in f:
        l1l2math[ligne[0]] = ligne[1]

# on a separe les l2 des l3 car il y a des modules avec le meme titre. (probas?)
l3math = {}
with open("l3math.csv", "r") as fichier:
    f = csv.reader(fichier, delimiter=",", quotechar='"')
    for ligne in f:
        l3math[ligne[0]] = ligne[1]

# on a separe les l2 des l3 car il y a des modules avec le meme titre. (probas?)
# et les l1 des l2 pour l'anglais
l1mathinfo = {}
with open("l1mathinfo.csv", "r") as fichier:
    f = csv.reader(fichier, delimiter=",", quotechar='"')
    for ligne in f:
        l1mathinfo[ligne[0]] = ligne[1]

l2mathinfo = {}
with open("l2mathinfo.csv", "r") as fichier:
    f = csv.reader(fichier, delimiter=",", quotechar='"')
    for ligne in f:
        l1mathinfo[ligne[0]] = ligne[1]

l3mathinfo = {}
with open("l3mathinfo.csv", "r") as fichier:
    f = csv.reader(fichier, delimiter=",", quotechar='"')
    for ligne in f:
        l3mathinfo[ligne[0]] = ligne[1]

info = {}
with open("info.csv", "r") as fichier:
    f = csv.reader(fichier, delimiter=",", quotechar='"')
    for ligne in f:
        info[ligne[0]] = ligne[1]

phy = {}
with open("phy.csv", "r") as fichier:
    f = csv.reader(fichier, delimiter=",", quotechar='"')
    for ligne in f:
        phy[ligne[0]] = ligne[1]


socio = {}
with open("socio.csv", "r") as fichier:
    f = csv.reader(fichier, delimiter=",", quotechar='"')
    for ligne in f:
        socio[ligne[0]] = ligne[1]


print(
    """apogee: dict[str, dict[str, str]] = {}
# un dictionnaire code ECUE/regexpr
filtreECUE: dict[str, dict[str, str]] = {}
# miashsgenerique
"""
)
fichesmiashsgenerique = [14422, 14423, 14425, 14426, 14418, 14415, 14420]
fichesmiashsgenerique += [14463, 14464, 14466, 14471, 14475, 14470]
fichesmiashsgenerique += [14504, 14505]
fichesmiashsgenerique += [12446, 12447, 4557]  # L3SES + UE libre ling

# fichesl1geoafiltrer = [11236]
# filtrel1geo = {"l1miashsgeoCM": ".*GA11Y0[14]0.*|.*GA12Y0[124]0.*"}
# for i in fichesl1geoafiltrer:
#     print("filtreECUE['%d'] = %s\n" % (i, filtrel1geo))

# fichesl2geoafiltrer = [11238]
# filtrel2geo = {"l2miashsgeoCM": ".*GA13Y0[12]0.*|.*GA14Y0[124]0.*"}
# for i in fichesl2geoafiltrer:
#     print("filtreECUE['%d'] = %s\n" % (i, filtrel2geo))

fichesl1socio = [14291, 14292]  # L1socio
fichesl2socio = [14294, 14295]  # L2socio
fichesl3socio = [14297, 14298]  # L3 socio
fichesSO0= { "SO01Y020":[39276,39274,39275,61119], "SO01Y010":[39269,39270,39268,39266,39271,61352,61353],\
              "SO02Y020": [39297,39298,39296],"SO02Y030":[39304,39302,39303],"SO02Y040":[39308,39306,39307],\
              "SO02Y010":[39293,39292,39294,39290],\
              "SO03Y070":[39348,39350,39351],"SO03Y010":[39329,39331],"SO03Y020":[39333,39335,39334],\
              "SO04Y010":[39356,39358],"SO04Y040":[39367,39366]}

fichessocio = fichesl1socio + fichesl2socio + fichesl3socio
for i in fichesSO0:
    fichessocio+=fichesSO0[i]


for i in fichesmiashsgenerique:
    print("apogee['%d'] = %s\n" % (i, miashsgenerique))

for i in fichessocio:
    print("apogee['%d'] = %s\n" % (i, socio))

filtrel1socio = {
    "SO01Y010": ".*SO01Y010.*",
    "SO01Y020": ".*SO01Y020.*",
    "SO02Y010": ".*SO02Y010.*",
    "SO02Y020": ".*SO02Y020.*",
    "SO02Y030": ".*SO02Y030.*",
    "SO02Y040": ".*SO02Y040.*",
    "miashsSocioS1": "^(?:(?!SO01Y050).)+.$",
}
filtrel2socio = {
    "SO03Y010": ".*SO03Y010.*",
    "SO03Y020": ".*SO03Y020.*",
    "SO03Y070": ".*SO03Y070.*",
    "SO04Y010": ".*SO04Y010.*",
    "SO04Y040": ".*SO04Y040.*",
}
filtrel3sociofichel3 = {
    "SO5Y010": ".*SO05Y010.*",
    "SO05Y020": ".*SO05Y020.*",
    "SO05ou6Y030": ".*SO0[56]Y030.*",
    "SO06Y040": ".*SO06Y040.*",
    "SO05ou6Y050": ".*SO0[56]Y050.*",
    "SO05ou6Y060": ".*SO0[56]Y060.*",
    "SO06Y070": ".*SO06Y070.*",
}
filtrel3sociofichesgroupes = {
    "SO06Y010": ".*SO06Y010.*",
    "SO06Y020": ".*SO06Y020.*",
    "questionnaires": ".*SO05Y070.*|.*SO06Y080.*",
    "SO05Y080": ".*SO05Y080.*",
    "SO05ou6Y090": ".*SO0[56]Y090.*",
}
for i in fichesl1socio:
    print("filtreECUE['%d'] = %s\n" % (i, filtrel1socio))
for i in fichesl2socio:
    print("filtreECUE['%d'] = %s\n" % (i, filtrel2socio))
for i in fichesl3socio:
    print("filtreECUE['%d'] = %s\n" % (i, filtrel3sociofichesgroupes))
for i in fichesl3socio[:1]:
    print("(filtreECUE['%d']).update(%s)\n" % (i, filtrel3sociofichel3))
# menage pour les fiches de TD de socio qui on des choses en trop mal rattachées:
for i in fichesSO0:
    for j in fichesSO0[i]:
        print("filtreECUE['%d'] = %s\n" % (j, '{"%s":".*%s.*"}'%(i,i)))



fichesmiashsling = [14419, 14472, 4557]
fichesL3SDL = [5254,5271,5272]
fichesmiashsling += fichesL3SDL

print("\n#miashs ling")
for i in fichesmiashsling:
    print("apogee['%d'] = %s\n" % (i, miashsling))

for i in fichesL3SDL:
    print("apogee['%d'] = %s\n" % (i, miashsling))

l3SDL_filtreECUE = {
    "l3sdl_l2miashs": ".*SL1[56]Y010.*",
    "l3sdl_l3miashs": ".*SL15Y0[23]0.*|.*SL25Y0[12]0.*|.*SL16Y020.*|.*SL26Y0[124]0.*",
}
for i in fichesL3SDL:
    print("filtreECUE['%d'] = %s\n" % (i, l3SDL_filtreECUE))


# Fiches autres reservations a filtrer.
fichesmath_autrereservations = [3839]
mathautresresa_filtre = {"tutorat": ".*Tutorat.*", "erasmus": ".*Erasmus.*"}
print("\n#math autres reservations")
for i in fichesmath_autrereservations:
    print("filtreECUE['%d'] = %s\n" % (i, mathautresresa_filtre))


fichesl1l2math = [14396, 14397, 14400, 6658, 14449, 14450, 14453, 7295]
print("\n#l1l2math")
for i in fichesl1l2math:
    print("apogee['%d'] = %s\n" % (i, l1l2math))

fichesl3math = [14492, 14493, 14496, 14499]
print("\n#l3math")
for i in fichesl3math:
    print("apogee['%d'] = %s\n" % (i, l3math))
# L3 math filtre ECUE du S5.
# dictionnaire code ECUE : expression reguliere de recherche
# ne pas utiliser de + ni & ni /
l3math_filtreECUE1234 = {"MT15Y020-MT15Y030": ".*MT15Y020.*|.*MT15Y030.*"}
for i in fichesl3math[:4]:
    print("filtreECUE['%d'] = %s\n" % (i, l3math_filtreECUE1234))
# semestre 5
l3math_filtreECUE123 = {
    "MT15Y010": ".*MT15Y010.*",
    "MT15E070": ".*MT15E070.*",
}
l3math_filtreECUE12 = {
    "MT15Y080": ".*MT15Y080.*",
    "MT15E050": ".*MT15E050.*",
}
# l3math_filtreECUE3={'MT15E060' : '.*MT15E060.*'} # action de groupes passe avec gpe 1 en 2022-23.
# semestre 6
# nb stat n'a que 2 gpes mais placés ds 1 et 3 en 20-21 mais en 2 en 21-22.
l3math_filtreECUE123.update(
    {"MT16E010": ".*MT16E010.*", "MT16Y100": ".*MT16Y100.*", "MT16E060": ".*MT16E060.*"}
)
l3math_filtreECUE12.update({
    "MT16Y030": ".*MT16Y030.*",
    "MT16Y050": ".*MT16Y050.*",
    "MT16Y020": ".*MT16Y020.*",
})

l3math_filtreECUE1 = {
    "MT15E060": ".*MT15E060.*",
    "MT16Y040": ".*MT16Y040.*",
    "MT16Y060": ".*MT16Y060.*",
    "MT16Y130": ".*MT16Y130.*",
}

for i in fichesl3math[:3]:
    print("(filtreECUE['%d']).update( %s)\n" % (i, l3math_filtreECUE123))
for i in fichesl3math[:2]:
    print("(filtreECUE['%d']).update( %s)\n" % (i, l3math_filtreECUE12))
# action de gpes est en 22 dans le gpe1 alors qu'il etait avant ds le gpe 3
# i = fichesl3math[2]
# print("(filtreECUE['%d']).update( %s)\n"%(i, l3math_filtreECUE3))
i = fichesl3math[0]
print("(filtreECUE['%d']).update( %s)\n" % (i, l3math_filtreECUE1))


fichesmathinfo = [14381, 14383]
print("\n#l1mathinfo")
for i in fichesmathinfo:
    print("apogee['%d'] = %s\n" % (i, l1mathinfo))

fichesmathinfo = [22129, 22130, 12166, 12167]
print("\n#l2mathinfo")
for i in fichesmathinfo:
    print("apogee['%d'] = %s\n" % (i, l1mathinfo))

fichesmathinfo = [7670, 2426, 22133, 2203]
print("\n#l3mathinfo")
for i in fichesmathinfo:
    print("apogee['%d'] = %s\n" % (i, l3mathinfo))


fichesinfo = [
    14516,
    14517,
    14518,
    14519,
    14521,
    14524,
    14546,
    14552,
    14554,
    14557,
    14559,
    11688,
    12164,
    12165,
]
print("\n#info")
for i in fichesinfo:
    print("apogee['%d'] = %s\n" % (i, info))


fichesphy = [6361, 6362, 6363, 6371, 6639, 8068, 8069, 6742, 6743, 6744, 6675, 5885]
fichesphy += [6532, 6533, 6652, 6653, 5885]
print("\n#physique")
for i in fichesphy:
    print("apogee['%d'] = %s\n" % (i, phy))


# fichesanglaisufrmathl2 = [11217, 11218, 11226, 11228, 11229, 11230, 11231]
# fichesanglaisufrmathl3 = [5666, 5668, 5669, 5670, 5671, 5672, 5673]
# fichesanglaisufrmath = fichesanglaisufrmathl2 + fichesanglaisufrmathl3

# filtreAnglaisSemestriel = {
#     "sem2": ".*DTSTART;TZID=Europe/Paris:[0-9]{4}0[123456][0-9]{2}T.*",
#     "sem1": ".*DTSTART;TZID=Europe/Paris:[0-9]{4}09[0-9]{2}T.*|.*DTSTART;TZID=Europe/Paris:[0-9]{4}1[012]{1}[0-9]{2}T.*",
# }
# print("\n#Anglais UFR math a decouper en semestres")
# for i in fichesanglaisufrmath:
#     print("filtreECUE['%d'] = %s\n" % (i, filtreAnglaisSemestriel))
filtreAnglaisTD = {
    "1": ".*Anglais.*TD01",
    "2": ".*Anglais.*TD02",
    "3": ".*Anglais.*TD03",
    "4": ".*Anglais.*TD04",
    "5": ".*Anglais.*TD05",
    "6": ".*Anglais.*TD06"
 }

fichesanglaisufrmathl3 = ["AnglaisL3ufrmath"] # franck saisit maintenant sur L3 promo entiere.
for i in fichesanglaisufrmathl3:
     print("filtreECUE['%s'] = %s\n" % (i, filtreAnglaisTD))


fichessallesuelibreling = ["sallesuelibreling"] # pour les salles reservees sans groupe d'etudiant.
print("\n#LAC")
for i in fichessallesuelibreling:
    print("apogee['%s'] = %s\n" % (i, uelibreling))

filtreUElibreLing = {
    "LL012Y" : ".*LL0[12]Y.*"
}
for i in fichessallesuelibreling:
     print("filtreECUE['%s'] = %s\n" % (i, filtreUElibreLing))
