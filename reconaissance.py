import re

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
#faut traiter P+D ex. au

expr = (mot + "(?:"+  det + "|" + nc + "|" + npp + "|" 
    + vinf + "|" + vpr + "|" + vpp + "|" + v + "|"
    + advwh + "|"  + adj + "|" + adv + "|" + et + "|"
    + cc + "|" + cs + "|" + cls + "|" + clo + "|" + clr + "|"
    + ponct + "|" + prorel + "|" + pro + "|" + pref + "|" + pd + "|" + p +")" )

automate = re.compile(expr)

# verifie si les mots étaient reconnus
with open("corpus/small.brown", "r", encoding="utf-8") as f:
    contenu = f.read()
    valides = automate.findall(contenu)
    motsTotal = contenu.split()
    print("Mots reconnus: "+ str(len(valides)))
    print("Mots en total: "+str(len(motsTotal)))
    pourcentage = len(valides)/len(motsTotal) * 100
    print("Pourcentage des mots bien annotés: " + str(pourcentage) + "%")

exclus = re.sub(expr, "", contenu) # ce qui nest pas inclu dans expr
print(exclus)
#print(valides[:100])