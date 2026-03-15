import re
import main

mot = "[^/\s]*/" #tout sauf / et un espace 

det = "DET"

nc = "NC"
npp = "NPP"

#verbes
v = "V"
vinf = "VINF" # verbe à l'infinitif
vpr = "VPR" # participe présent 
vpp = "VPP" # participe passé 

adj = "ADJ" 

adv = "ADV" 
advwh = "ADVWH" # adverbe interrogatif, wh-questions 

p = "P" #préposition

cc = "CC" # conjonction de coordination
cs = "CS" # conjonction de subordination 

#pronoms
prorel = "PROREL" #pronom rélatif
pro = "PRO"
cls = "CLS" #pronom clitique sujet
clo = "CLO" #pronom clitique objet
clr = "CLR" # clitique réfléchi, ex. "SE maquiller" etc.

pref = "PREF" #préfixe

et = "ET" #mot étranger

ponct = "PONCT" 

pd = "P\+D"

expr = (mot + "(?:"+  det + "|" + nc + "|" + npp + "|" 
    + vinf + "|" + vpr + "|" + vpp + "|" + v + "|"
    + advwh + "|"  + adj + "|" + adv + "|" + et + "|"
    + cc + "|" + cs + "|" + cls + "|" + clo + "|" + clr + "|"
    + ponct + "|" + prorel + "|" + pro + "|" + pref + "|" + pd + "|" + p +")" )


if __name__ == "__main__" :
    main.main()