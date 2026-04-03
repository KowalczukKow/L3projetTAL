import re

mot = r"\S+/" #tout sauf espace 

detwh = "DETWH" # déterminant interrogatif
det = "DET"

nc = "NC"
npp = "NPP"

#verbes
vimp = "VIMP" # impératif
vinf = "VINF" # verbe à l'infinitif
vpr = "VPR" # participe présent 
vpp = "VPP" # participe passé 
vs = "VS" # subjonctif
v = "V"

adjwh = "ADJWH" # adjectif interrogatif
adj = "ADJ" 

advwh = "ADVWH" # adverbe interrogatif, wh-questions 
adv = "ADV" 

cc = "CC" # conjonction de coordination
cs = "CS" # conjonction de subordination 

#pronoms
prorel = "PROREL" #pronom rélatif
prowh = "PROWH" # pronom intérrogatif
pro = "PRO"
cls = "CLS" #pronom clitique sujet
clo = "CLO" #pronom clitique objet
clr = "CLR" # clitique réfléchi, ex. "SE maquiller" etc.

pref = "PREF" #préfixe

et = "ET" #mot étranger

ponct = "PONCT" 

pd = r"P\+D"

ppro = r"P\+PRO" # préposition + pronom rélatif
p = "P" #préposition

i = "I" #interjection

expr = (mot + "(?:" +  detwh + "|" +  det + "|" + nc + "|" + npp + "|" 
    + vimp + "|" + vinf + "|" + vpr + "|" + vpp + "|" + v + "|" + vs + "|"
    + advwh + "|"  + adjwh + "|" + adj + "|" + adv + "|" + et + "|"
    + cc + "|" + cs + "|" + cls + "|" + clo + "|" + clr + "|"
    + ponct + "|" + prorel + "|" + prowh + "|" + pro + "|" + pref + "|" + pd + "|"
    + ppro + "|" + p + "|" + i + ")" )


if __name__ == "__main__" :
    import main
    main.main()