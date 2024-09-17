"""
Fichier contenant les salles de TP et les amphis.
"""

salles_TP: list[str] = []
"""
La liste des salles de TP, sous la forme \"Batiment - Salle -\".
"""

amphis: list[str] = []
"""
La liste des amphis, sous la forme \"Batiment - Salle -\".
"""

#############
# Salles TP #
#############
tpHalle = ["331C", "446C", "452C", "557C", "443C", "449C", "532C", "548C"]
tpHalle += ["432C", "434C", "436C", "442C", "531C", "537C", "538C", "554C", "551C"]
salles_TP += ["Halle - %s -" % i for i in tpHalle]

tpMoulins = ["688C", "785C", "789C", "791C", "797C"]
salles_TP += ["Moulins - %s -" % i for i in tpMoulins]

tpGermain = ["2001", "2003", "2004", "2005", "2006", "2027", "2028", "2031", "2032"]
salles_TP += ["Germain - %s -" % i for i in tpGermain]

tpCondorcet = [
    "073A",
    "075A",
    "077A",
    "156A",
    "172A",
    "173A",
    "174A",
    "176A",
    "192A",
]
tpCondorcet += [
    "193A",
    "202A",
    "213A",
    "241A",
    "250A",
    "276A",
    "285A",
    "292A",
    "293A",
]
tpCondorcet += ["322A", "313A", "338A"]
salles_TP += ["Condorcet - %s -" % i for i in tpCondorcet]

tpLavoisier = ["210", "240"]
salles_TP += ["Lavoisier - %s -" % i for i in tpLavoisier]

tpLamarck = [
    "122B",
    "132B",
    "142B",
    "149B",
    "154B",
    "201B",
    "213B",
    "222B",
    "232B",
    "249B",
    "254B",
]
tpLamarck += ["179B", "181B", "189B", "281B", "289B", "521A", "525A"]
salles_TP += ["Lamarck - %s -" % i for i in tpLamarck]

# NB: Manque les TP de Gouges.

##########
# Amphis #
##########
amphisHalle = [
    "11E",
    "7C",
    "10E",
    "12E",
    "3B",
    "4C",
    "5C",
    "6C",
    "9E",
    "13E",
    "1A",
    "2A",
    "8C",
]  # amphis
amphisHalle += ["234C", "247E", "580F"]  # gdes salles 84 places
amphisHalle += [
    "027C",
    "064E",
    "226C",
    "227C",
    "264E",
    "265E",
    "418C",
    "419C",
    "470E",
    "471E",
]  # gd salles 70 places
amphis += ["Halle - %s -" % i for i in amphisHalle]

amphisGouges = ["Gouges - 1 -", "Gouges - 2 -"]
amphis += amphisGouges
