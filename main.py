import re
from reconaissance import expr
from corpusStats import CorpusStats

def main():
    chemin_corpus = "corpus/sequoia-9.2.fine.brown"
    automate = re.compile(expr)

    print("Chargement du corpus...")
    stats = CorpusStats(chemin_corpus)

    stats.read_corpus(automate, True)

    while True:
        print("\n" + "="*40)
        print("MENU PRINCIPAL - CONCORDANCIER")
        print("1. Informations générales du corpus")
        print("2. Graphe de Zipf")
        print("3. Afficher les statistiques d'un tag (fréquence, rang, 10 formes les plus fréquentes)")
        print("4. Rechercher un mot (fréquence, rang, 5 collocations les plus fréquentes, KWIC optionnel)")
        print("5. Rechercher une suite de mots ou une suite des tags")
        print("6. Rechercher une expression régulière (KWIC optionnel)")
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
            stats.requete_tag()
        elif choix == '4':
            stats.requete_mot()
        elif choix == '5':
            print("Entrez :")
            print("1. Pour une suite des mots")
            print("2. pour une suite des tags")
            choix2 = input("Votre choix : ").strip()
            if choix2 == '1' :
                stats.requete_n_gramme()
            elif choix2 == '2':
                stats.requete_mixte()
        elif choix == '6':
            stats.requete_regex()
        else:
            print("Choix invalide, veuillez réessayer.")
    
if __name__ == "__main__":
    main()