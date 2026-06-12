import re
from reconaissance import expr
from corpusStats import CorpusStats

def main():
    chemin_corpus = "corpus/small.brown"
    automate = re.compile(expr)

    print("Chargement du corpus...")
    stats = CorpusStats(chemin_corpus)

    stats.read_corpus(automate, True)

    while True:
        print("\n" + "="*40)
        print("MENU PRINCIPAL - CONCORDANCIER")
        print("1. Informations générales du corpus")
        print("2. Graphe de Zipf")
        print("3. Rechercher un mot (KWIC optionnel)")
        print("4. Rechercher une expression régulière (KWIC optionnel)")
        # print("5. n-gram")
        print("0. Quitter")
        choix = input("Votre choix : ").strip()
        
        if choix == '0':
            print("Au revoir !")
            break
        elif choix == '1':
            stats.info_generale()
        elif choix == '2':
            stats.plot_zipf()
        elif choix == '3':
            stats.requete_mot()
        elif choix == '4':
            stats.requete_regex()
        # elif choix == '5':

        else:
            print("Choix invalide, veuillez réessayer.")
    

if __name__ == "__main__":
    main()