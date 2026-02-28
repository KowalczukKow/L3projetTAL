import re
from reconaissance import expr
import fonctions

def main():
    print("hello")

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

    fonctions.createur_index(valides)

if __name__ == "__main__":
    main()