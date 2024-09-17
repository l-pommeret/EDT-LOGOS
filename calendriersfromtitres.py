titretocal1={}
titretocal2={}
titretocal3={}
titretocal1sdv={}
titretocal2sdv={}

import json


## les liens pour requette rss
liens_rss={}
#yearId=4 # 2021-2022
yearId=10 # 2022-2023
#
telechargement={}
telechargement['rss-l1'] = ""
telechargement['rss-l2'] = ""
telechargement['rss-l3'] = ""
telechargement['rss-l1sdv'] = ""
telechargement['rss-l2sdv'] = ""

with open("formations.json") as cfile:
    for c in json.load(cfile):
        # Les L1
        if c["title"].startswith("L1") or c["title"]=="DiversUFRmath":
            if c["title"].startswith("L1SDV"):
                # L1 SDV
                if telechargement['rss-l1sdv'] != "":
                    telechargement['rss-l1sdv'] += ","

                virg=""
                if str(c["code"])!="" and c["fiches"]!="":
                    virg=","
                telechargement['rss-l1sdv'] += str(c["code"]) + virg + c["fiches"]
            else:
                # L1 sauf SDV
                if telechargement['rss-l1'] != "":
                    telechargement['rss-l1'] += ","
                virg=""
                if str(c["code"])!="" and c["fiches"]!="":
                    virg=","
                telechargement['rss-l1'] += str(c["code"]) + virg + c["fiches"]
        # Les L2
        if c["title"].startswith("L2"):
            if c["title"].startswith("L2SDV"):
                # L1 sauf SDV
                if telechargement['rss-l2sdv'] != "":
                    telechargement['rss-l2sdv'] += ","

                virg=""
                if str(c["code"])!="" and c["fiches"]!="":
                    virg=","
                telechargement['rss-l2sdv'] += str(c["code"]) + virg + c["fiches"]
            else:
                # L2 sauf SDV
                if telechargement['rss-l2'] != "":
                    telechargement['rss-l2'] += ","

                virg=""
                if str(c["code"])!="" and c["fiches"]!="":
                    virg=","
                telechargement['rss-l2'] += str(c["code"]) + virg + c["fiches"]

        # Les L3
        if c["title"].startswith("L3"):
                # L3
                if telechargement['rss-l3'] != "":
                    telechargement['rss-l3'] += ","

                virg=""
                if str(c["code"])!="" and c["fiches"]!="":
                    virg=","
                telechargement['rss-l3'] += str(c["code"]) + virg + c["fiches"]




#liens_rss['rss-l1'] = 'https://adeprod.app.univ-paris-diderot.fr/ade/gwtclient/rss?projectId=%s&resources=6552,6551,7437,6594,1607,6769,6347,6345,6346,6343,6539,8226,6543,6555,311,5274,5259,12499,5057&nbDays=56&since=0'%(yearId)
#liens_rss['rss-l2'] = 'https://adeprod.app.univ-paris-diderot.fr/ade/gwtclient/rss?projectId=%s&resources=5275,5277,4888,6540,6544,6545,6549,6546,6541,6593,6548,6542,6554,6550,6547,6553&nbDays=56&since=0'%(yearId)
#liens_rss['rss-l3'] = 'https://adeprod.app.univ-paris-diderot.fr/ade/gwtclient/rss?projectId=%s&resources=5517,4814,4604,4819,4549,2418,7426,7488,5254,5272,5271,4656,5301,4557&nbDays=56&since=0'%(yearId)
#liens_rss['rss-l1sdv']="https://adeprod.app.univ-paris-diderot.fr/ade/gwtclient/rss?projectId=%s&resources=4772&nbDays=56&since=0"%(yearId)
#liens_rss['rss-l2sdv']="https://adeprod.app.univ-paris-diderot.fr/ade/gwtclient/rss?projectId=%s&resources=3744&nbDays=56&since=0"%(yearId)
#
# Creation des liens via formations.json qui etait utilise pour les telechargements ds get_ical.py
#
liens_rss['rss-l1'] = 'https://adeprod.app.univ-paris-diderot.fr/ade/gwtclient/rss?projectId=%s&resources=%s&nbDays=56&since=0'%(yearId, telechargement['rss-l1'])
liens_rss['rss-l2'] = 'https://adeprod.app.univ-paris-diderot.fr/ade/gwtclient/rss?projectId=%s&resources=%s&nbDays=56&since=0'%(yearId, telechargement['rss-l2'])
liens_rss['rss-l3'] = 'https://adeprod.app.univ-paris-diderot.fr/ade/gwtclient/rss?projectId=%s&resources=%s&nbDays=56&since=0'%(yearId, telechargement['rss-l3'])
liens_rss['rss-l1sdv'] = 'https://adeprod.app.univ-paris-diderot.fr/ade/gwtclient/rss?projectId=%s&resources=%s&nbDays=56&since=0'%(yearId, telechargement['rss-l1sdv'])
liens_rss['rss-l2sdv'] = 'https://adeprod.app.univ-paris-diderot.fr/ade/gwtclient/rss?projectId=%s&resources=%s&nbDays=56&since=0'%(yearId, telechargement['rss-l2sdv'])

# archives nextcloud des fichiers telecharges:
nextcloud_rss = {}
nextcloud_rss["rss-l1"] = "https://cloud.math.univ-paris-diderot.fr/s/xESMEgxXrka6Piq"
nextcloud_rss["rss-l2"] = "https://cloud.math.univ-paris-diderot.fr/s/JXLBmRfRmT3E5iZ"
nextcloud_rss["rss-l3"] = "https://cloud.math.univ-paris-diderot.fr/s/A4bKcZdWW6C3dQF"
nextcloud_rss["rss-l1sdv"] = "https://cloud.math.univ-paris-diderot.fr/s/aFmoeTKdL8X3sw5"
nextcloud_rss["rss-l2sdv"] = "https://cloud.math.univ-paris-diderot.fr/s/fGNAdn9HTWdAtp9"



#########################################################################
##
#titretocal1['L1 INFORMATIQUE - INFORMATIQUE GENERALE -GM'] = [6197,6696,6292,6697,6295,6767]
titretocal1['L1 INFORMATIQUE - INFORMATIQUE GENERALE - GM'] = [6197,6696,6292,6697,6295,6767]
titretocal1['L1 INFO 1'] = [6197]
titretocal1['L1 INFO 2'] = [6696]
titretocal1['L1 INFO 3'] = [6292]
titretocal1['L1 INFO 4'] = [6697]
titretocal1['L1 INFO 5'] = [6295]
titretocal1['L1 INFO 6'] = [6767]
titretocal1['L1 INFORMATIQUE - INFORMATIQUE/BIOLOGIE (DL) - GM']=[6296,7811]
titretocal1['L1 INFO BIO A'] = [7811]
titretocal1['L1 INFO BIO B'] = [6296]
titretocal1['L1 INFORMATIQUE - INFORMATIQUE/JAPONAIS (DL) - GM']=[6297,7814]
titretocal1['L1 INFO JAP A'] = [6297]
titretocal1['L1 INFO JAP B'] = [7814]

titretocal1[ 'L1 MATHEMATIQUES - MATHS FONDAMENTALES ET APPLIQUEES - GM'] = [6649,6650,6651,6658,7295]
titretocal1['L1 MFA Gr 1'] = [6649]
titretocal1['L1 MFA Gr 2'] = [6650]
titretocal1['L1 MFA Gr 3'] = [6651]
titretocal1['L1 MFA Gr 4'] = [6658]
titretocal1['L1 MATH METIS'] = [7295]
titretocal1['Travail en groupes Licence']=[1607]
titretocal1['TUTORAT MATHS']=[12499]


titretocal1['L1 MATHEMATIQUES - MATHEMATIQUES/INFORMATIQUE (DL) - GM'] = [6699,6700]
titretocal1['L1 Math-info Gr 1'] = [6699]
titretocal1['L1 Math-info Gr 2'] = [6700]
#titretocal1['MATH-INFO 1'] = [6699]
#titretocal1['MATH-INFO 2'] = [6700]
titretocal1['L1 MI1'] = [6699]   # 7296
titretocal1['L1 MI2'] = [6700] # 7301


titretocal1['L1 MIASHS - Campus GM'] = [6605,6606,6607,6608,6609,6610,6611,6612]
titretocal1['L1 MIASHS ECO Gr 1'] = [6605]
titretocal1['L1 MIASHS ECO Gr 2'] = [6606]
titretocal1['L1 MIASHS ECO Gr 3'] = [6607]
titretocal1['L1 MIASHS ECO Gr 4'] = [6608]
titretocal1['L1 MIASHS HISTOIRE']=[6609]
titretocal1['L1 MIASHS GEOGRAPHIE'] = [6610]
titretocal1['L1 MIASHS SOCIOLOGIE'] = [6611]
titretocal1['L1 MIASHS LINGUISTIQUE'] = [6612]


titretocal1['L1 SOCIOLOGIE - GM']=[5867,5868,5869,5870,5871,5872,5873]
titretocal1['groupe 1']=[5867]
titretocal1['groupe 2']=[5868]
titretocal1['groupe 3']=[5869]
titretocal1['groupe 4']=[5870]
titretocal1['groupe 5']=[5871]
titretocal1['groupe 6']=[5872]
titretocal1['groupe 7']=[5873]
# L1 options de linguistiques SDL avec les L3 pour ne pas poser de conflit avec SDV.


titretocal1['L1 PHYSIQUE - GM']=[6361,6362,6363,6371,6639,8068,8069]
titretocal1['PHY 1'] = [6361]
titretocal1['PHY 2'] = [6362]
titretocal1['PHY 3'] = [6363]
titretocal1['PHY 4'] = [6371]
titretocal1['PHY 5'] = [6639]
titretocal1['REB1'] = [8068]
titretocal1['REB2'] = [8069]
titretocal1['L1 PHYSIQUE - DOUBLE LICENCE PHYSIQUE-CHIMIE - GM'] = [6534]
titretocal1['DLPC'] = [6534]
titretocal1['L1 PHYSIQUE - CYCLE UNIV PREPA GRANDES ECOLES (CUPGE) - GM']=[6532,6533]
titretocal1['CUPGE 1'] = [6532]
titretocal1['CUPGE 2'] = [6533]
titretocal1['L1 PHYSIQUE - ENSEIGNEMENT PHYSIQUE-CHIMIE - GM'] = [6535]
titretocal1['EPC'] = [6535]

titretocal1['L1 CHIMIE']=[5633,5634,5635,5636]
titretocal1['CHIM 1']=[5633]
titretocal1['CHIM 2']=[5634]
titretocal1['CHIM 3']=[5635]
titretocal1['CHIM 4']=[5636]
titretocal1['L1 STEP']=[6770,6771]
titretocal1['STEP 1']=[6770]
titretocal1['STEP 2']=[6771]
titretocal1['L1 CHIMIE - CHIMIE/BIOLOGIE - GM']=[5637]
titretocal1['1 CHIM BIO 1']=[5637]

# L1 Geographie (GAED)
titretocal1['intro. à la géographie']=[5211,5209,5210,5208,5212]  # fiche 5140
titretocal1['Grp 1 (11Y010)']=[5211]
titretocal1['Grp 2 (11Y010)']=[5209]
titretocal1['Grp 3 (11Y010)']=[5210]
titretocal1['Grp 4 (11Y010)']=[5208]
titretocal1['Grp Eco/Géo (11Y010)']=[5212]

titretocal1['Geo. urbaine/rurale']=[5196,5180,5182,5177]  # fiche 5141
titretocal1['Grp 1 (11Y020)']=[5196]
titretocal1['Grp 2 (11Y020)']=[5180]
titretocal1['Grp 3 (11Y020)']=[5182]
titretocal1['Grp 4 (11Y020)']=[5177]

titretocal1['Géo. des Suds']=[5184,5188,5190,5191]  # ficher 5142
titretocal1['Grp 1 (11Y030)']=[5184]
titretocal1['Grp 2 (11Y030)']=[5188]
titretocal1['Grp 3 (11Y030)']=[5190]
titretocal1['Grp 4 (11Y030)']=[5191]

titretocal1['Images et cartes']=[5203,5204,5205,5206]   # fiche 5143
titretocal1['Grp 1 (11Y040)']=[5203]
titretocal1['Grp 2 (11Y040)']=[5204]
titretocal1['Grp 3 (11Y040)']=[5205]
titretocal1['Grp 4 (11Y040)']=[5206]

titretocal1['Climatologie']=[7530,7531,7532,7533,7508] # fiche 5147
titretocal1['Grp 1 (12Y010)']=[7530]
titretocal1['Grp 2 (12Y010)']=[7531]
titretocal1['Grp 3 (12Y010)']=[7532]
titretocal1['Grp 4 (12Y010)']=[7533]
titretocal1['Grp Eco/Géo (12Y010)']=[7508]

titretocal1['Diagnostic territorial']=[8195,7534,7544,7545,7546] # fiche 5146
titretocal1['Grp (ECO/GEO)']=[8195]
titretocal1['Grp 1 (12Y020)']=[7534]
titretocal1['Grp 2 (12Y020)']=[7544]
titretocal1['Grp 3 (12Y020)']=[7545]
titretocal1['Grp 4 (12Y020)']=[7546]

titretocal1['Stats et Cartographie']=[7538,7539,7540,7541,7542] # fiche
titretocal1['Grp 1 (12Y040)']=[7538]
titretocal1['Grp 2 (12Y040)']=[7539]
titretocal1['Grp 3 (12Y040)']=[7540]
titretocal1['Grp 4 (12Y040)']=[7541]
titretocal1['Grp Eco/Géo (12Y040)']=[7542]


#sdv est incompatible avec MIASHS car les CM d'eco ont aussi des "Groupes 1" attaches
titretocal1sdv['L1 SCIENCES DE LA VIE - GM']=[5454,5455,6094,6099,6096,6097,6098,6095,6100,6101,6102,2630] # 4772
titretocal1sdv['Cours']=[5454,5455] # 4772
titretocal1sdv['Cours Section 1'] = [5454]
titretocal1sdv['Cours Section 2'] = [5455]
titretocal1sdv['Groupe 1'] = [6094]
titretocal1sdv['Groupe 2'] = [6099]
titretocal1sdv['Groupe 3'] = [6096]
titretocal1sdv['Groupe 4'] = [6097]
titretocal1sdv['Groupe 5'] = [6098]
titretocal1sdv['Groupe 6'] = [6095]
titretocal1sdv['Groupe 7'] = [6100]
titretocal1sdv['Groupe 8'] = [6101]
titretocal1sdv['Groupe 9'] = [6102]
titretocal1sdv['Groupe 10'] = [2630]





#################################################################################################################
#titretocal1['L1 SOCIOLOGIE - GM']=[]
titretocal2['L2 INFORMATIQUE - INFORMATIQUE GENERALE - GM'] = [6274,6275,6299,6300,6350]
titretocal2['L2 INFO 1'] =[6274]
titretocal2['L2 INFO 2'] =[6275]
titretocal2['L2 INFO 3'] =[6299]
titretocal2['L2 INFO 4'] =[6300]
titretocal2['L2 INFO 5'] =[6350]
titretocal2['L2 INFORMATIQUE - INFORMATIQUE/BIOLOGIE (DL) - GM']=[6665,7815]
titretocal2['L2 INFO-BIO A']=[6665]
titretocal2['L2 INFO-BIO B']=[7815]
titretocal2['L2 INFORMATIQUE - INFORMATIQUE/BIOLOGIE (DL) - GM']=[6666,7816]
titretocal2['L2 INFO-JAP A'] = [6666]
titretocal2['L2 INFO-JAP B'] = [7816]




titretocal2['L2 MATHEMATIQUES - MATHEMATIQUES/INFORMATIQUE (DL) - GM'] = [6736,6737]
titretocal2['L2 INFORMATIQUE - INFORMATIQUE/MATHEMATIQUES (DL) - GM'] = [6736,6737]
titretocal2['L2 Math-info Gr 1'] = [6736]
#titretocal2['MATH-INFO 1'] = [6736]
titretocal2['L2 MI1'] = [6736] #7313
titretocal2['L2 Math-info Gr 2'] = [6737]
#titretocal2['MATH-INFO 2'] = [6737]
titretocal2['L2 MI2'] = [6737] # 7314

titretocal2['L2 MIASHS - Campus GM']=[6598,6599,6600,6601,6602,6603,6604]
titretocal2['L2 MIASHS ECO Gr 1'] = [6598]
titretocal2['L2 MIASHS ECO Gr 2'] = [6599]
titretocal2['L2 MIASHS ECO Gr 3'] = [6600]
titretocal2['L2 MIASHS HISTOIRE']=[6601]
titretocal2['L2 MIASHS SOCIOLOGIE'] = [6602]
titretocal2['L2 MIASHS GEOGRAPHIE'] = [6603]
titretocal2['L2 MIASHS LINGUISTIQUE'] = [6604]
titretocal2['L2 SOCIOLOGIE - GM']=[5880,5881,5882,5883,6946]
titretocal2['groupe 1']=[5880]
titretocal2['groupe 2']=[5881]
titretocal2['groupe 3']=[5882]
titretocal2['groupe 4']=[5883]
titretocal2['groupe 5']=[6946]



titretocal2['L2 MATHEMATIQUES - MATHS FONDAMENTALES ET  APPLIQUEES - GM'] = [6654,6655,6656]
titretocal2['L2 MFA Gr 1']=[6654]
titretocal2['L2 MFA Gr 2']=[6655]
titretocal2['L2 MFA Gr 3']=[6656]



titretocal2['L2 PHYSIQUE - GM']=[6742,6743,6744]
titretocal2['PHY 1'] = [6742]
titretocal2['PHY 2'] = [6743]
titretocal2['PHY 3'] = [6744]
titretocal2['L2 PHYSIQUE - DOUBLE LICENCE PHYSIQUE-CHIMIE - GM'] = [6147]
titretocal2['DLPC'] = [6147]
titretocal2['L2 PHYSIQUE - CYCLE UNIV PREPA GRANDES ECOLES (CUPGE) - GM']=[6652,6653]
titretocal2['CUPGE 1'] = [6652]
titretocal2['CUPGE 2'] = [6653]
titretocal2['L2 PHYSIQUE - ENSEIGNEMENT PHYSIQUE-CHIMIE - GM'] = [6668]
titretocal2['EPC'] = [6668]
titretocal2['L2 MEDPHY']=[5885]
titretocal2['PHYTECH']=[6675]


titretocal2['L2 CHIMIE']=[5638,5639,5640]
titretocal2['CHIM 1']=[5638]
titretocal2['CHIM 2']=[5639]
titretocal2['CHIM 3']=[5640]

titretocal2['L2 CHIMIE - CHIMIE/BIOLOGIE - GM']=[5641]
titretocal2['2 CHIM BIO 1']=[5641]


# L2 Geographie (GAED)
titretocal2['Espace économique']=[5234,5235,5236,5237]  # fiche 5152
titretocal2['Grp 1 (13Y020)']=[5234]
titretocal2['Grp 2 (13Y020)']=[5235]
titretocal2['Grp 3 (13Y020)']=[5236]
titretocal2['Grp L1 Eco/Géo (13Y020)']=[5237]

titretocal2['Géomorphologie']=[5231,5232,5233]  # fiche 5153
titretocal2['Grp 1 (13Y010)']=[5231]
titretocal2['Grp 2 (13Y010)']=[5232]
titretocal2['Grp 3 (13Y010)']=[5233]

titretocal2['Aménagement en France']=[5238,5239,5240] # fiche 5151  (pas miashs)
titretocal2['Grp 1 (13Y030)']=[5238]
titretocal2['Grp 2 (13Y030)']=[5239]
titretocal2['Grp 3 (13Y030)']=[5240]
titretocal2['Stat. et cartographie']=[5241,5242,5243,5244] # fiche 5150  (pas miashs)
titretocal2['Grp 1 (13Y040)']=[5241]
titretocal2['Grp 2 (13Y040)']=[5242]
titretocal2['Grp 3 (13Y040)']=[5243]
titretocal2['Grp 4 (13Y040)']=[5244]


titretocal2['Télédétection/SIG']=[7565,7579,7580,7581] # ficher 5159
titretocal2['Grp 1 (14Y040)']=[7565]
titretocal2['Grp 2 (14Y040)']=[7579]
titretocal2['Grp 3 (14Y040)']=[7580]
titretocal2['Grp 4 (14Y040)']=[7581]

titretocal2['Biogéographie/Pédologie']=[7547,7573,7574] # fiche 5162
titretocal2['Grp 1 (14Y010)']=[7547]
titretocal2['Grp 2 (14Y010)']=[7573]
titretocal2['Grp 3 (14Y010)']=[7574]

titretocal2['Mobilité, migration']=[7558,7575,7576] #fiche 5161
titretocal2['Grp 1 (14Y020)']=[7558]
titretocal2['Grp 2 (14Y020)']=[7575]
titretocal2['Grp 3 (14Y020)']=[7576]


# SDV est incompatible avec MIASHS. Ex un CM d ECO contient des entrees pour les groupes de eco cote LSH qui
# peuvent s'appeler Groupe 1
titretocal2sdv['L2 SCIENCES DE LA VIE - GM']=[5457,5456,3554,6108,6109,6110,6111,6113,6114,6115,6116,6117,3925,3556] # 3744
titretocal2sdv['Cours'] = [5456,5457]
titretocal2sdv['Cours L2BB'] = [5457]
titretocal2sdv['Cours L2BB + L2VT'] = [5456]
titretocal2sdv['Groupe 1'] = [6108]
titretocal2sdv['Groupe 2'] = [6109]
titretocal2sdv['Groupe 3'] = [6110]
titretocal2sdv['Groupe 4'] = [6111]
titretocal2sdv['Groupe 5'] = [6113]
titretocal2sdv['Groupe 6'] = [6114]
titretocal2sdv['Groupe 7'] = [6115]
titretocal2sdv['Groupe 8'] = [6116]
titretocal2sdv['Groupe 9'] = [6117]
titretocal2sdv['Agro'] = [3554]
titretocal2sdv['Groupe DL2'] = [3925]










################################################################"
titretocal3['L3 INGE-MATH']=[5517]
titretocal3["L3 MATHEMATIQUES - MATHEMATIQUES POUR L'ENSEIGNEMENT - GM"]=[5511]
titretocal3["L3 Enseignement"]=[5511]


titretocal3['L3 MATHEMATIQUES - MATHS FONDAMENTALES ET  APPLIQUEES - GM'] = [5512,5515,5516,2359]
titretocal3['L3 Fonda et Appliquées G1'] = [5512]
#titretocal3['L3 Fonda et Appliquées G2'] = [5515]
titretocal3['L3 Fonda et Appliquées G2'] = [5515]
titretocal3['L3 Fonda et Appliquées G3'] = [5516]
titretocal3['L3 Fonda et Appliquées G4'] = [2359]

#titretocal3['L3 INFORMATIQUE - INFORMATIQUE/MATHEMATIQUES (DL) - GM']=[]

titretocal3['L3 INFORMATIQUE - INFORMATIQUE/MATHEMATIQUES (DL) - GM'] = [5482,2203]
titretocal3['L3 Maths Info'] = [7670,2426]
titretocal3['L3 MI1'] = [5482]
titretocal3['L3 MI2'] = [2203]
titretocal3['L3 MI Groupe 1'] = [7670]
titretocal3['L3 MI Groupe 2'] = [2426]

titretocal3['L3 MIASHS - MATHEMATIQUES, INFORMATIQUE ET ECONOMIE - GM']= [5510,5509]
titretocal3['L3 MIASH G1'] = [5510]
titretocal3['L3 MIASH G2'] = [5509]
titretocal3['L3 ECONOMIE - SCIENCES ECONOMIQUES ET SOCIALES - GM'] = [5423,12446,12447]   # fiche 5301
titretocal3['L3 CM ECO DL MIASHS'] = [5423,12446,12447]   # fiche 2414
titretocal3['L3 CM ECO MIASHS'] = [5423,12446,12447]   # fiche 3196
titretocal3['L3 MIASHS ÉCO GR 3'] = [5423]
titretocal3['L3 SES + DL + MIASHS'] = [5423,12446,12447]   #6922
titretocal3['L3 SES EG + Miashs'] = [5423,12446,12447]   #5418
titretocal3['L3 MIASHS ÉCO GR 4'] = [12446]
titretocal3['L3 MIASHS ÉCO GR 3 + GR 4'] = [5423,12446] # 7372
titretocal3['Banque, finance CM'] = [5423,12446,12447] # 7356
titretocal3['Banque, finance'] = [5423,12446,12447] # 7330
titretocal3['Banque, finance MIASH TD 1'] = [12446] # 7360
titretocal3['Banque, finance MIASH TD 2'] = [12447] # 7361
titretocal3['La concurrence imparfaite et stratégie des acteurs'] = [12446,12447] #
titretocal3['La concurrence imparfaite et stratégie des acteurs CM'] = [12446,12447] #
titretocal3['La concurrence imparfaite et stratégie des acteurs MIASH TD 1'] = [12446] # 7353
titretocal3['a concurrence imparfaite et stratégie des acteurs MIASH TD 2'] = [12446] # 7354. il manque bien le L


titretocal3['L3 MIASHS - MATHEMATIQUES,INFORMATIQUE ET LINGUISTIQUE - GM'] = [4549]
titretocal3['L3 SCIENCES DU LANGAGE - LINGUISTIQUE ET INFORMATIQUE -GM'] = [5909,5910]
titretocal3['L3 SCIENCES DU LANGAGE - LINGUISTIQUE ET INFORMATIQUE -GM'] = [5909,5910]    # 2022-2023
titretocal3['L3 SCIENCES DU LANGAGE - LINGUISTIQUE ET INFORMATIQUE - GM'] = [5909,5910]   # 2022-2023
titretocal3['L3 SCIENCES DU LANGAGE - LINGUIST. THEORIQUE EXPERIM. -GM'] = [5909,5910]
titretocal3['L3 SCIENCES DU LANGAGE - LINGUIST. THEORIQUE EXPERIM. - GM'] = [5909,5910]   # 2022-2023
titretocal3['L3 SCIENCES DU LANGAGE - FRANÇAIS LANGUE ETRANGÈRE -GM'] = [5909,5910]
titretocal3['CM L3 LI'] = [5909,5910] # 5908
titretocal3['EXAMEN L3LI'] = [5909,5910] # 7649
titretocal3['GR. 1'] = [5909] # et 5902 5905
titretocal3['GR. 1 BIS'] = [5909] # et 5902 5905
titretocal3['GR. 2'] = [5910]
titretocal3['GR. 2 BIS'] = [5910]

titretocal3['L1 LETTRES/SCIENCES DU LANGAGE - GM']=[4557]
# on regroupe toutes les options de linguistiques dans le meme calendrier
# INCOMPATIBLE avec SDV ET les amphis d'ECO donc on les mets avec les L3
titretocal3['Groupe 1'] = [4557]
titretocal3['Groupe 2'] = [4557]
titretocal3['Groupe 1 A'] = [4557]
titretocal3['Groupe 1 B'] = [4557]



titretocal3['L3 SOCIOLOGIE - GM']=[6929,6927,6928,4373]
titretocal3['L3 SOCIOLOGIE']=[6929,6927,6928,4373]
titretocal3['L3 SOCIOLOGIE - GRP 1']=[6929]
titretocal3['L3 SOCIOLOGIE - GRP 2']=[6927]
titretocal3['L3 SOCIOLOGIE - GRP 3']=[6928]
titretocal3['L3 SOCIOLOGIE - GRP 4']=[4373]
