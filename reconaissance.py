import re

mot = "[^/\s]*/" #tout sauf / et un espace 

det = "DET"

nc = "NC"
npp = "NPP"

#verbes
vinf = "VINF" # verbe à l'infinitif
vpr = "VPR" # participe présent 
vpp = "VPP" # participe passé 
v = "V"

adj = "ADJ" 

advwh = "ADVWH" # adverbe interrogatif, wh-questions 
adv = "ADV" 

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

p = "P" #préposition

expr = (mot + "(?:"+  det + "|" + nc + "|" + npp + "|" 
    + vinf + "|" + vpr + "|" + vpp + "|" + v + "|"
    + advwh + "|"  + adj + "|" + adv + "|" + et + "|"
    + cc + "|" + cs + "|" + cls + "|" + clo + "|" + clr + "|"
    + ponct + "|" + prorel + "|" + pro + "|" + pref + "|" + pd + "|" + p +")" )


if __name__ == "__main__" :
    import main
    main.main()