#!/usr/bin/python
# coding: utf8

import argparse
import json
import os
import re
import sys
import csv


######
def readcalendarjson(cal="calendars.json"):
    dictcalendars={}
    with open(cal) as io_cal:
            for l in json.load(io_cal):
                chaineid=l["parcours"]+"*"+l["year"]+"*"+l["label"]
                l["code"]=str(l["code"])
                if chaineid in dictcalendars:
                    print("WARNING doublon %s"%(chaineid))
                else:
                    dictcalendars[chaineid]=l

    return dictcalendars


## le calendars.json dans un dictionnaire
dictcalendars=readcalendarjson()
listeparcours=[]
for c in dictcalendars:
    if dictcalendars[c]["parcours"] not in listeparcours:
        listeparcours.append(dictcalendars[c]["parcours"])

listcalsorted=list(dictcalendars)
#listcalsorted.sort()
##
##
def updatedicoviacsv(fichiermaj, dictio=dictcalendars, basedircsvfiles="csvcalendars/"):
    """
    Mise a jour du dictionnaire contenant le contenu de calendars.json via un csv.
    """
    fichiermaj=basedircsvfiles+fichiermaj
    codesmodifies={}

    with open(fichiermaj, newline='', encoding='utf-8') as csvmaj:
        csvreader = csv.reader(csvmaj, delimiter=',', quotechar='"')
        i=0
        for ligne in csvreader:
            if i==0:
                #MAJ des entetes
                j=0
                entetecsvmaj={}
                for col in ligne:
                    if col!="":
                        entetecsvmaj[col]=j
                    j+=1
            else:
                chaineid=ligne[entetecsvmaj["chaineid"]]
                if chaineid in dictio:
                    oldcode = dictio[chaineid]["code"]
                    newcode = ligne[entetecsvmaj["Numéro"]]
                    if oldcode != newcode:
                        # dans ade l'intitulé  du num  fiche est Numéro.
                        print("maj %s de %s vers %s"%(chaineid, oldcode, newcode))
                        codesmodifies[oldcode] = newcode
                        dictio[chaineid]["code"] = ligne[entetecsvmaj["Numéro"]]

                elif chaineid != "":
                    code=ligne[entetecsvmaj["Numéro"]]
                    label=ligne[entetecsvmaj["label"]]
                    parcours=ligne[entetecsvmaj["parcours"]]
                    year=ligne[entetecsvmaj["year"]]
                    title=ligne[entetecsvmaj["Nom"]]
                    dictio[chaineid]={"code":code, "title":title, "label":label, "parcours":parcours, "year":year}


            i+=1

    return codesmodifies
## fin

# export du json courant dans un csv
# with open('csvcalendars/output_calendarjson.csv', 'w', newline='', encoding='utf-8') as csvcalendarjson:
#     outputwriter = csv.writer(csvcalendarjson, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
#     L=[ "" for i in range(len(entetesoutput)+1)]
#     for x in entetesoutput:
#         L[entetesoutput[x]]=x

#     outputwriter.writerow(L)

#     for i  in listcalsorted:
#         L=[ "" for i in range(len(entetesoutput)+1)]
#         for x in dictcalendars[i]:
#             L[entetesoutput[x]]=dictcalendars[i][x]

#         outputwriter.writerow(L)
# fin d'export vers le csv




## MAJ via csv
#codesmodifies=updatedicoviacsv(fichiermaj="ufrmath.csv")
codesmodifiesmaths={'6700': '14383', '6699': '14381', '6649': '14396', '6650': '14397', '6651': '14400', '6611': '14420', '6612': '14419', '6609': '14418', '6610': '14415', '6608': '14426', '6607': '14425', '6606': '14423', '6605': '14422', '6736': '22129', '6737': '22130', '6656': '14453', '6655': '14450', '6654': '14449', '6598': '14463', '6599': '14464', '6600': '14466', '6603': '14470', '6601': '14471', '6604': '14472', '6602': '14475', '5517': '22145', '5511': '47465', '5482': '22133', '5512': '14492', '5515': '14493', '5516': '14496', '2359': '14499', '5510': '14504', '5509': '14505', '4601': '46992', '4637': '59387', '4636': '59105', '2457': '47495', '4652': '28325', '11271': '28473', '4670': '28347', '4654': '59404', '11687': '59188', '4598': '28457', '4578': '28376', '6029': '28433', '4653': '28329', '11270': '28494', '5310': '55515'}


#codesmodifies2=updatedicoviacsv(fichiermaj="ufrinfo.csv")
codesmodifiesinfo={'6197': '14516', '6696': '14517', '6292': '14518', '6697': '14519', '4546': '14520', '6295': '14521', '7811': '14525', '6296': '14524', '11489': '14523', '6699': '14522', '6700': '14527', '6274': '14546', '6275': '14552', '6299': '14554', '6300': '14557', '6530': '14559', '6665': '14576', '6666': '14575', '6736': '14574', '6737': '14573', '7465': '14543', '7466': '14577', '7467': '14579', '7708': '14580', '7468': '14581', '2189': '14584', '2201': '14585', '5482': '14586'}


#codesmodifies3=updatedicoviacsv(fichiermaj="eidd.csv")

#codesmodifies4=updatedicoviacsv(fichiermaj="halle.csv")

#codesmodifies5=updatedicoviacsv(fichiermaj="geo.csv")

#codesmodifies6=updatedicoviacsv(fichiermaj="socio.csv")

#codesmodifies7=updatedicoviacsv(fichiermaj="sdv.csv")

#codesmodifies8=updatedicoviacsv(fichiermaj="eco.csv")

#codesmodifies9=updatedicoviacsv(fichiermaj="hist.csv")
#codesmodifies9=updatedicoviacsv(fichiermaj="step.csv")
## save dictcalendars to csv
def builtcalendarsnew(dicodescal=dictcalendars, destfilename="calendars-new.json"):
    with open(destfilename,"w", encoding='utf8') as newcaljson:
        listcalsorted=list(dicodescal)
        # listcalsorted.sort() # ne plus trier ca change l'ordre des boutons
        newcaljson.write("[\n")
        for i in range(len(listcalsorted)):
            dico=(dicodescal[listcalsorted[i]])
            # ligne="   "+str(dico)
            # ligne=ligne.replace("'",'"')
            # ligne=ligne.replace("True","true")
            # ligne=ligne.replace("False","false")
            ligne="   "+json.dumps(dico,ensure_ascii=False)
            if i+1< len(listcalsorted):
                ligne=ligne+" ,\n"
            newcaljson.write(ligne)
        newcaljson.write("\n]\n")
##



##
builtcalendarsnew()

entetesoutput={ 'parcours':1, "year":2, "label":3, "code":4, "title":5, "annexe":6, "page":7}
dictcalendarsparparcours ={}
for c in listeparcours:
    dictcalendarsparparcours[c]={}
for c in dictcalendars:
    p=dictcalendars[c]["parcours"]
    if p in dictcalendarsparparcours:
        (dictcalendarsparparcours[p])[c]=(dictcalendars[c])
    else:
        (dictcalendarsparparcours[p])={}
        (dictcalendarsparparcours[p])[c]=(dictcalendars[c])

for p in dictcalendarsparparcours:
    builtcalendarsnew(dictcalendarsparparcours[p],destfilename='csvcalendars/calendars-%s.json'%(p))












############
## formations
formations = []



# tutu=str(formationsmath)
# for i in codesmodifies:
#     tutu=tutu.replace(i,codesmodifies[i])


formationsmath =[
    {'code': '14399', 'title': 'L1Math', 'fiches': '14396,14397,14400,61535'},
    {'code': '', 'title': 'L1MathMetis', 'fiches': '47483'},
    {'code': '14454', 'title': 'L2Math', 'fiches': '14449,14450,14453,61545'},
    {'code': '', 'title': 'L2MathMetis', 'fiches': '47489'},
    # L1/L2 MIASHS
    {'code': '14414,53767,53759,53779,53745', 'title': 'L1Miashs-ECO1', 'fiches': '14422'},
    {'code': '14414,53768,53760,53780,53746', 'title': 'L1Miashs-ECO24', 'fiches': '14423,14426'},
    {'code': '14414,53769,53761,53781,53747', 'title': 'L1Miashs-ECO3', 'fiches': '14425'},
    {'code': '14414', 'title': 'L1Miashs-Socio', 'fiches': '14420'},
    # {'code': '14414', 'title': 'L1Miashs-Ling', 'fiches': '14419'},
    {'code': '14414,54128,54125', 'title': 'L1Miashs-Ling', 'fiches': '14419'}, #+fusion du TD5+TD2 (54128,54125) init ling gen. prevu
    #{'code': '14414,35854,35867,35875,35907,35913,35925', 'title': 'L1Miashs-Hist', 'fiches': '14418'}, #+CM Hist.
    #TD S1 MIASHS HI01Y010-TD04	35858, HI01Y020-TD01	35866, HI01Y030-6 affiché TD08 53478
    {'code': '14414,35854,35867,35875,35907,35913,35925,35858,35866,53478,', 'title': 'L1Miashs-Hist', 'fiches': '14418'}, #+CM Hist.
    {'code': '14414,35687,35668,35693,35710', 'title': 'L1Miashs-GEO', 'fiches': '14415'},
    {'code': '14476,53837,53824,53818,53810', 'title': 'L2MiashsECO1', 'fiches': '14463'},
    {'code': '14476,53838,53825,53819,53811', 'title': 'L2MiashsECO23', 'fiches': '14464,14466'},
    {'code': '14476', 'title': 'L2Miashs-GSHL', 'fiches': '14475,14472'},
    #{'code': '14476,35737,35719,35715,35752,35742', 'title': 'L2Miashs-GEO', 'fiches': '14470'},#+ fiches des CM GAED
    {'code': '14476,35737,35719,35715,35752,35742', 'title': 'L2Miashs-GEO', 'fiches': '14470'},#+ fiches des CM GAED
    #TD3 esp.eco 35723 , TD3 Geomorpho 35717     (semestre 3)
    {'code': '14476,35737,35719,35715,35752,35742,35723,35717', 'title': 'L2Miashs-GEO', 'fiches': '14470'},#+ fiches des CM GAED + les deux TD3 de geo du S3
    # {'code': '14476,35954,35964,36007', 'title': 'L2Miashs-Hist', 'fiches': '14471'}, #+CM obligatoires Hist
    # 35936=HI03Y010 seule option comptatible L2MIASHS-Hist au S3 en 24-25.
    {'code': '14476,35954,35964,36007,35936,36000', 'title': 'L2Miashs-Hist', 'fiches': '14471'}, #Bug le CM de HI03Y030 est placé sur le calendrier de HI04Y090 donc on l'ajoute.(36000)
    {'code': '14380,14522', 'title': 'L1MathInfo-Gr1', 'fiches': '14381'},
    {'code': '14380,14527', 'title': 'L1MathInfo-Gr2', 'fiches': '14383'},
    {'code': '22128,14574', 'title': 'L2MathInfo', 'fiches': '22129'},
    {'code': '22128,14573', 'title': 'L2MathInfo', 'fiches': '22130'},
    {'code': '', 'title': 'L3MathInfo', 'fiches': '7670'},
    {'code': '14586', 'title': 'L3MathInfo', 'fiches': '22133'},
    {'code': '22145', 'title': 'L3MathIngeMath', 'fiches': ''},
    {'code': '14497', 'title': 'L3MathFonda', 'fiches': '14492,14493,14496,14499'},
    {'code': '14497,22145,14480,22140', 'title': 'L3Math classe entiere MFA+Inge+Ens+MI', 'fiches': 'AnglaisL3ufrmath'},  # pour l'anglais+filtre.
    {'code': '', 'title': 'L3MathMetis', 'fiches': '60915'},
    {'code': '', 'title': 'L3MathEns', 'fiches': '47465'},
    #{'code': '', 'title': 'AnglaisL3', 'fiches': '37844,37845,37846,37847'},
    #{'code': '5668,5669,5670,5671,5672,5673', 'title': 'AnglaisL3fusionnes', 'fiches': '5666'},
    #{'code': '', 'title': 'AnglaisL2', 'fiches': '11218,11226,11228,11229,11230,11231'},
    #{'code': '11218,11226,11228,11229,11230,11231', 'title': 'AnglaisL2fusionnes', 'fiches': '11217'},
    {'code': '14514', 'title': 'L3Miashs', 'fiches': '14504,14505'}, # informatique L3 MIASHS où? ,4549'},
    {'code': '', 'title': 'L3ProfEcoles', 'fiches': '46992'},
    {'code': '55502', 'title': 'M1-MATH-MFA', 'fiches': '55513,55514'},  # Fiche classe entiere + 2 groupes
    {'code': '', 'title': 'M1-MATH-ISIFAR', 'fiches': '28325'},
    {'code': '', 'title': 'M1-MATH-MEEF', 'fiches': '28473'},
    {'code': '14599', 'title': 'M1-MATH-MIC', 'fiches': '59387'},
    {'code': '14602', 'title': 'M1-MATH-MISD', 'fiches': '47495'},
    {'code': '', 'title': 'M2-Didactique', 'fiches': '28281,28315,28255,28301'},
    {'code': '', 'title': 'M2-MATH-LMFI', 'fiches': '28347'},
    {'code': '14617', 'title': 'M2-MATH-MIC', 'fiches': '59404'},
    {'code': '14629', 'title': 'M2-MATH-MISD', 'fiches': '59188'},
    {'code': '', 'title': 'M2-MATH-MO', 'fiches': '28457'},
    {'code': '', 'title': 'M2-MATH-MFA', 'fiches': '28376'},
    {'code': '', 'title': 'agreg ext math', 'fiches': '28433'},
    {'code': '', 'title': 'agreg int math', 'fiches': '55515'},
    {'code': '', 'title': 'M2-MATH-ISIFAR', 'fiches': '28329'},
    {'code': '', 'title': 'M2-MATH-MEEF', 'fiches': '28494'},
    {'code': '', 'title': 'M2-MATH-Enseignants', 'fiches': '61259'},
    {'code': '', 'title': 'DiversUFRmath', 'fiches': '58598,12499,39670'},
    #    à recreer     { "code": "", "title": "Colles L1/L2 Math", "fiches": "60239,60240"},
    { "code": "", "title": "Reservations Ponctuelles/Autres res.", "fiches": "3839"},
    {'code': '', 'title': 'Germain Salles TP UFRMath', 'fiches': '1200,1515,1279'},
    {'code': '', 'title': 'Germain Seminaires UFRMath', 'fiches': '1472,1437'}
]








formationsphys = [
    { "code": "", "title": "L1Physique", "fiches": "6361,6362,6363,6371,6639,39539,39540"},
    { "code": "", "title": "L1EPC", "fiches": "6534"},
    { "code": "", "title": "L1EPC", "fiches": "6535"},
    { "code": "", "title": "L1CUPGE", "fiches": "6532,6533"},
    { "code": "61536", "title": "L1DLPM", "fiches": "11220"}, # fusion avec fiche ds ufrmath
    { "code": "", "title": "L2Physique", "fiches": "6742,6743,6744"},
    { "code": "", "title": "L2EPC", "fiches": "6668"},
    { "code": "", "title": "L2DLPC", "fiches": "6147"},
    { "code": "61537", "title": "L2DLPM", "fiches": "3465"},
    { "code": "", "title": "L2CUPGE", "fiches": "6652,6653"},
    { "code": "", "title": "L2MEDPHY", "fiches": "11274"},
    { "code": "", "title": "L2PHYTECH", "fiches": "6675"},
    # { "code": "", "title": "L3DLPC", "fiches": "5710"},
    { "code": "", "title": "L3DLPC", "fiches": "6489,6491,6492"},
    { "code": "5311", "title": "L3Physique", "fiches": "7866,7867,7868,7869,7870,7871,7873,7874,5312,5313,5498,5499,5500"},
    { "code": "", "title": "L3EPC", "fiches": "11382"},
    {"code": "61463", "title": "L3DLPM", "fiches": "14337"},
    { "code": "", "title": "Condorcet Salles TP exp", "fiches": "1040,1251,1293,1016,1571,1541,1458,959,1636,1413,1354,1047,1294,1066,1565,1468,1343,1543,1028"},
    { "code": "", "title": "M1 phy", "fiches": "4864,6015,6016"}

]




formationschimie = [
    { "code": "", "title": "L1Chimie", "fiches": "5633,5634,5635,5636"},
    { "code": "", "title": "L1ChimieBio", "fiches": "5637"},
    { "code": "", "title": "L2Chimie", "fiches": "5638,5639,5640"},
    { "code": "", "title": "L2ChimieBio", "fiches": "5641"},
    { "code": "", "title": "L3ChimieBio", "fiches": "8160"},
    { "code": "", "title": "L3Chimie", "fiches": "5711,5712,5713,5715"},
    { "code": "42649,42657", "title": "M1 Chimie - PhyC1 et C2", "fiches": "5708,5709"},
    { "code": "42643,42673,42667,42670,42657,42664,42652,42681,42661,42649", "title": "M1 Chimie M1 MOLC1 et C2", "fiches": "6065,6200"},
    #42657 dans les 4 groupes M1 
    { "code": "", "title": "M1 Chimie RE-SGE", "fiches": "21593,6020,8390,8391,8392"},
    { "code": "", "title": "M1 Chimie RE", "fiches": "42638"}, # Saints Peres
    { "code": "42919,42835,42921,42845,42838,42843,42815", "title": "M2 Chimie Gr1&2 CHENS+SAFE", "fiches": "6213,6214"},
    { "code": "42915,42910,42913,42900,42905,42919,42835,42921,42845,42838,42843,42815", "title": "M2 Chimie Gr3 PCLife", "fiches": "6259"},
    { "code": "42870,42865,42923,42881,42875,42919,42835,42921,42845,42838,42843,42815", "title": "M2 Chimie Gr4 OBMC", "fiches": "6215"},
    { "code": "", "title": "M2 Chimie Gpes 5 et 6 vides?", "fiches": "6342,6500"}
]

formationsinfo = [
    {'code': '', 'title': 'L1Info', 'fiches': '14516,14517,14518,14519,14520,14521'},
    {'code': '', 'title': 'L1InfoBio', 'fiches': '14524,14525'},
    {'code': '11656', 'title': 'L1InfoJap', 'fiches': '14523'},
    {'code': '', 'title': 'L2Info', 'fiches': '14546,14552,14554,14557,14559'},
    {'code': '', 'title': 'L2InfoBio', 'fiches': '14576'},
    {'code': '11657', 'title': 'L2InfoJap', 'fiches': '14575'},
    {'code': '', 'title': 'L3 info', 'fiches': '14543,14577,14579,14580,14581'},
    {'code': '', 'title': 'L3 infoBio', 'fiches': '14584'},
    {'code': '', 'title': 'L3 infoJap', 'fiches': '14585'},
    {'code': '', 'title': 'M1Info', 'fiches': '14599,14588,58594,14590,14589,14595,14596,14602'},
    {'code': '', 'title': 'M2Info', 'fiches': '14617,14620,60821,14627,14623,14622,14626,14629'}
]
#old [
#     { "code": "", "title": "L1Info", "fiches": "6197,6696,6292,6697,4546,6295"},
#     { "code": "", "title": "L1InfoBio", "fiches": "6296,7811"},
#     { "code": "11656", "title": "L1InfoJap", "fiches": "11489,6297"},
#     { "code": "", "title": "L2Info", "fiches": "6274,6275,6299,6300,6530,22614"},
#     { "code": "", "title": "L2InfoBio", "fiches": "6665"},
#     { "code": "11657", "title": "L2InfoJap", "fiches": "6666"},
#     { "code": "", "title": "L3 info", "fiches": "7465,7466,7467,7708,7468"},
#     { "code": "", "title": "L3 infoBio", "fiches": "2189"},
#     { "code": "", "title": "L3 infoJap", "fiches": "2201"}
# ]
# tutu=str(formationsinfo)
# for j in codesmodifies2:
#         tutu=tutu.replace(j,codesmodifies2[j])
# print(tutu)



formationssdv = [
    { "code": "", "title": "L1SDV S1", "fiches": "43849,43912,43875,43821,43886"},
    { "code": "", "title": "L1SDV Modelisation Math", "fiches": "43879,43876,43881,43885,43880,43882,43877,43883,43884,43878,21987"},
    { "code": "", "title": "L2SDV S3", "fiches": "44157,44260,44071,44281,44098,44190,44241,44314,44289,44298,44311,44292,44295,44218,44229,44308"},
    { "code": "", "title": "L2SDV Maths pr Bio", "fiches": "44225,44226,44228,44227,44219,44220,44221,44222,44224,44223"}

]




formationslcao = [
    { "code": "", "title": "L1-LLCER-CHI", "fiches": "5598,5599,5600,5601,5602"},
    { "code": "", "title": "L1-LLCER-COR", "fiches": "5725,5726,5727,5728,5729,5730,6125,11337"},
    { "code": "", "title": "L1-LLCER-JAP", "fiches": "5718,11656,5719,5720,5721,5722,5724,6138"},
    { "code": "", "title": "L1-LLCER-VIET", "fiches": "6066,6067,6068,6069,6070,6071,7741"},
    { "code": "", "title": "L2-LLCER-CHI", "fiches": "5732,5733,5734,5735,5736"},
    { "code": "", "title": "L2-LLCER-COR", "fiches": "5737,5738,5739,5740,5741,5742"},
    { "code": "", "title": "L2-LLCER-JAP", "fiches": "5743,11657,5744,5745,5746,5747,5748"},
    { "code": "", "title": "L2-LLCER-VIET", "fiches": "6783,6784,6785,7860"},
    { "code": "", "title": "L3-LLCER-CHI", "fiches": "5749,3239,5750,5751,5752,5753"},
    { "code": "", "title": "L3-LLCER-COR", "fiches": "5754,26185,5755,5756,5757,5758,5759"},
    { "code": "", "title": "L3-LLCER-JAP", "fiches": "5760,5761,5762,5763,5764,5765,468"},
    { "code": "", "title": "L3-LLCER-VIET", "fiches": "6786,6787,6788,7863"},
    { "code": "", "title": "M1-LLCER-ens-COR", "fiches": "291"},
    { "code": "", "title": "M1-LLCER-etu-CHI", "fiches": "182"},
    { "code": "", "title": "M1-LLCER-etu-COR", "fiches": "10683"},
    { "code": "", "title": "M1-LLCER-etu-JAP", "fiches": "10705"},
    { "code": "", "title": "M1-LLCER-etu-VIET", "fiches": "183"},
    { "code": "", "title": "M1-LLCER-meef-CHI", "fiches": "244"},
    { "code": "", "title": "M2-LLCER-ens-COR", "fiches": "292"},
    { "code": "", "title": "M2-LLCER-etu-CHI", "fiches": "294"},
    { "code": "", "title": "M2-LLCER-etu-COR", "fiches": "379"},
    { "code": "", "title": "M2-LLCER-etu-JAP", "fiches": "296"},
    { "code": "", "title": "M2-LLCER-etu-VIET", "fiches": "233"},
    { "code": "", "title": "M2-LLCER-meef-CHI", "fiches": "391"}

]


formationseidd = [
    { "code": "", "title": "eidd 3A MN", "fiches": "14329"},
    { "code": "", "title": "eidd 2A BI", "fiches": "14317,14318"},
    { "code": "", "title": "eidd 3A BI", "fiches": "14320,14321"},
    { "code": "", "title": "eidd 2A GP", "fiches": "14322"},
    { "code": "", "title": "eidd 3A GP", "fiches": "14325"},
    { "code": "", "title": "eidd 2A MN", "fiches": "14327"},
    { "code": "", "title": "eidd 2A SIE", "fiches": "14331"},
    { "code": "", "title": "eidd 3A SIE", "fiches": "14333"},
    { "code": "", "title": "eidd 1A-S5", "fiches": "14225,14227,14226"},
    { "code": "", "title": "eidd 1A-S6", "fiches": "14309,14310,14313,14314,14311"}

]



formationshalle = [
    { "code": "", "title": "Halle Amphis", "fiches": "1276,1418,1274,1257,1182,1219,1298,1273,1416,1020,1013,1154,1271,1245"},
    { "code": "", "title": "Halle Salles 52", "fiches": "1469,1687,1498,1619,1686,1316,1084"},
    { "code": "", "title": "Halle Salles 60 et plus", "fiches": "1482,1615,1368,1489,1102,1551,1225,1520,1552,1510,1620,1300,1664"},
]


formationsgeo = [
    { "code": "", "title": "geo s1", "fiches": "35677,35672,35683,35666"},
    { "code": "", "title": "geo s2", "fiches": "35689,35695,35699,35705"},
    { "code": "", "title": "geo s3", "fiches": "35724,35718,35729,35713"},
    { "code": "", "title": "geo s4", "fiches": "35734,35767,35765,35749,35763,35754,35759,35739,35744"},
    { "code": "", "title": "geo miashs s1", "fiches": "53642,35670,35669,35667,35671,35684,35688,35685,35686"},
    { "code": "", "title": "geo miashs s2", "fiches": "53604,35690,35691,35694,35692,53610,35697,35696,35698,53609,53631,35707,35709,35706,35708"},
    { "code": "", "title": "geo miashs s3", "fiches": "53651,35720,35721,35723,35714,35716,35717,35719,35722,35715"},
    { "code": "", "title": "geo miashs s4", "fiches": "53659,53660,53661,35741,35743,35740,35737,35752,35750,35753,35751,35742"},
    { "code": "", "title": "geo s5", "fiches": "35798,35776,35796,35801,35778,35789,35771,35794,35774,35783"},
    { "code": "", "title": "geo s6", "fiches": "35826,35831,35838,35821,35812,35836,35814,35810,35834,35804,35806,35808,35816"}
]



formationssocio = [
    { "code": "", "title": "socio S1 a S6", "fiches": "14291,14292,14294,14295,14297,14298"},
    { "code": "", "title": "socio TD MIASHS S1", "fiches": "39276,39274,39275,61119,39269,39270,39268,39266,39271,61352,61353"},
    { "code": "", "title": "SO02Y020 TD", "fiches": "39297,39298,39296"},
    { "code": "", "title": "SO02Y030 TD", "fiches": "39304,39302,39303"},
    { "code": "", "title": "SO02Y040 TD", "fiches": "39308,39306,39307"},
    { "code": "", "title": "SO02Y010 TD", "fiches": "39293,39292,39294,39290"},
    { "code": "", "title": "socio TD MIASHS S3", "fiches": "39348,39350,39351,39329,39331,39333,39335,39334"},
    { "code": "", "title": "socio TD MIASHS S4", "fiches": "39367,39366,39356,39358"}
]  # S1 à S6

formationslinguistique = [
    { "code": "", "title": "Initiation a la linguistique generale tout", "fiches": "37266"},
    { "code": "", "title": "Initiation a la linguistique generale 1 à 5", "fiches": "54124,54125,54126,54127,54128"},
    { "code": "", "title": "Initiation a la linguistique generale CM+TD01 à TD05", "fiches": "37268,37269,37270,37267,37271,37272"},
    { "code": "", "title": "UElibres ling", "fiches": "37117"},
    { "code": "", "title": "L3 SCIENCES DU LANGAGE - FLE", "fiches": "5254"},
    { "code": "", "title": "L3 SCIENCES DU LANGAGE - STL", "fiches": "5272"},
    { "code": "", "title": "L3 SCIENCES DU LANGAGE - LI", "fiches": "5271"}
]


formationsSES = [
    { "code": "", "title": "SES eco S1", "fiches": "35506,35527,35534,35538"},
    { "code": "", "title": "SES eco S2", "fiches": "35562,35566,35518,35542,35553,35571"},
    { "code": "", "title": "SES eco S3", "fiches": "35591,35579,35585,35597,35595"},
    { "code": "", "title": "SES eco S4", "fiches": "35618,35608,35602,35620,35600"},
    { "code": "", "title": "SES eco S5", "fiches": "35629,35639,35634,35626,35632"},
    { "code": "", "title": "SES eco S6", "fiches": "35655,35651,35645,35659,35662"},
    { "code": "53869,53878,53856,53848,35638,35643,35652,35656", "title": "L3 SES MIASHS TD01 +CM", "fiches": "sesmiashs1"},
    { "code": "53869,53878,53856,53848,35635,35642,35653,35657", "title": "L3 SES MIASHS TD02 +CM", "fiches": "sesmiashs2"}

]


formationsHIST = [
    { "code": "", "title": "HIST S1", "fiches": "35868,35859,35850"},
    { "code": "", "title": "HIST S2", "fiches": "35890,35895,35898,35892,35903,35922,35912,35887,35900"},
    { "code": "", "title": "HIST S3", "fiches": "35951,35942,35966,35959,35933"},
    { "code": "", "title": "HIST S4", "fiches": "35971,35975,35973,35977,35999,35979,35988,36003,36009,35994,35969"},
    { "code": "", "title": "HIST S5", "fiches": "36017,36024,36036,36040,36033,36026,36045,36047,36031,36038,36043,36019,36022,36028,36069,36065,36067"},
    { "code": "", "title": "HIST S6", "fiches": "36054,36051,36057,36059,36062,36090,36071,36073,36088,36083,36086,36075,36097,36093,36107,36099,36101,36103,36080,36105,36095,36078"}
]


formationsSTEP = [
    { "code": "60839", "title": "IPGP/STEP L1", "fiches": "60767,60769,60768,60770,60771,60772,60838,60856"},
    { "code": "60847", "title": "IPGP/STEP L2", "fiches": "60840,60841,60842,60843,60844,60845,60846,60857"},
    { "code": "60854", "title": "IPGP/STEP L3", "fiches": "60848,60849,60850,60852,60853,37791,37793"}
]

#######################
Batiments = {}

with open("csvcalendars/sallesTD.csv", newline='', encoding='utf-8') as csvsallesTD:
        csvreader = csv.reader(csvsallesTD, delimiter=',', quotechar='"')
        for ligne in csvreader:
           bat,salle,code=ligne[0],ligne[1],ligne[2]
           salle=str(salle)
           if not bat in Batiments:
                   Batiments[bat]={}
           Batiments[bat][salle]=code

listesallesafilter = []

Buffon=Batiments['Buffon']
Condorcet=Batiments['Condorcet']
Germain=Batiments['Germain']
Gouges=Batiments['Gouges']
Halle=Batiments['Halle']
Lamarck=Batiments['Lamarck']
Lavoisier=Batiments['Lavoisier']
Moulins=Batiments['Moulins']

listesallesafilter += [Germain['10'],Germain['13'],Germain['14'],Germain['2017']]
listesallesafilter += [Gouges['358'],Gouges['166'],Gouges['137'],Gouges['147'],Gouges['164'],Gouges['165'],Gouges['166'],Gouges['358']]
listesallesafilter += [Lavoisier['227']]
listesallesafilter += [Halle['237C'],Halle['244E'],Halle['253E'],Halle['304B'],Halle['305B'],Halle['578F']]

liste  = ""
for i in range(len(listesallesafilter)):
    liste += listesallesafilter[i]
    if i < len(listesallesafilter)-1:
        liste +=  ","

formationssallesuelibreling = [
    { "code": liste, "title": "Salles pr resa sans groupe", "fiches":"sallesuelibreling"}
    ]

#############


formations = formationschimie
formations += formationseidd
formations += formationsinfo
formations += formationslcao
formations += formationsmath
formations += formationsphys
formations += formationshalle
formations += formationsgeo
formations += formationssocio
formations += formationslinguistique
formations += formationssdv
formations += formationsSES
formations += formationsHIST
formations += formationsSTEP
formations += formationssallesuelibreling


verifpasdoublons = []
for f in formations:
    l=f["fiches"].split(',')
    for i in l:
        if i in verifpasdoublons:
            print("PB ficher %s en Double"%(i))
        verifpasdoublons.append(i)



## save dictcalendars to csv
with open("formations-new.json","w") as newformationsjson:
    newformationsjson.write("[\n")
    for i in range(len(formations)-1):
         newformationsjson.write("    "+json.dumps(formations[i])+',\n')
    newformationsjson.write("    "+json.dumps(formations[i+1]))
    newformationsjson.write("\n]\n")
##





#toto={"S1":"", "S2":"", "S3":"", "S4":"", "S5":"", "S6":"", "miashs-s1":"", "miashs-s2":"", "miashs-s3":"", "miashs-s4":""}
toto={"s1":"", "s2":"", "s3":"", "s4":"", "s5":"", "s6":""}
for d in dictcalendars:
     tmpdict=dictcalendars[d]
     if tmpdict["parcours"]=="hist":
         toto[tmpdict["year"]]+=","+(tmpdict["code"])


for i in toto:
    print(i,toto[i])

toto={"l1":"", "l2":"", "l3":""}
for d in dictcalendars:
     tmpdict=dictcalendars[d]
     if tmpdict["parcours"]=="step":
         toto[tmpdict["year"]]+=","+(tmpdict["code"])


for i in toto:
    print(i,toto[i])


# toto={"s1":"", "s2":"", "s3":"", "s4":"", "s1-mod math":"", "s3-math pr bio":"" }
# for d in dictcalendars:
#     tmpdict=dictcalendars[d]
#     if tmpdict["parcours"]=="sdv":
#         toto[tmpdict["year"]]+=","+(tmpdict["code"])

# for i in toto:
#     print(i,toto[i])
##
# with open("toolsapogee/mkcodesapogee.py") as mkcodeapogee:
#     tutu=mkcodeapogee.read()

#     for i in codesmodifiesmaths:
#         tutu=tutu.replace(i,codesmodifiesmaths[i])
#     for i in codesmodifiesinfo:
#         tutu=tutu.replace(i,codesmodifiesinfo[i])
#     with open("toolsapogee/mkcodesapogee-new.py", "w") as mkcodeapogeenew:
#         mkcodeapogeenew.write(tutu)


# mkcodeapogeenew.close()
