import re
from reconaissance import expr
from corpusStats import CorpusStats

def main():

    automate = re.compile(expr)

    stats = CorpusStats("corpus/sequoia-9.2.fine.brown")
    stats.read_corpus(automate, True)

    while True:
        print("\n" + "="*40)
        print("MENU PRINCIPAL - CONCORDANCIER")
        print("1. Rechercher un mot (Statistiques + KWIC optionnel)")
        print("2. Rechercher une suite de mots")
        print("3. Rechercher une expression régulière")
        print("0. Quitter")
        choix = input("Votre choix : ").strip()
        
        if choix == '0':
            print("Au revoir !")
            break
        elif choix == '1':
            stats.requete_mot()
        elif choix == '2':
            stats.requete_n_gramme()
        elif choix == '3':
            stats.requete_regex()
        else:
            print("Choix invalide, veuillez réessayer.")
    

if __name__ == "__main__":
    main()