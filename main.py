import re
from reconaissance import expr
from corpusStats import CorpusStats
from exprMixte import requete_mixte

def main():
    automate = re.compile(expr)

    print("=== Chargement du corpus ===")

    chemin_corpus = "corpus/sequoia-9.2.fine.brown"

    print(f"Le chemin du corpus actuel : {chemin_corpus}")
    choix_corpus = input("Voulez-vous changer le corpus (oui/non) : ").strip()

    if choix_corpus == 'oui' :

        chemin_corpus = input("Entrez le chemin du corpus : ").strip()

        while not chemin_corpus:
            print("Aucun chemin de corpus fourni.")
            chemin_corpus = input("Entrez le chemin du corpus : ").strip()

        print(f"\nCorpus sélectionné : {chemin_corpus}")
        
    print("Chargement du corpus...")

    try: 
        stats = CorpusStats(chemin_corpus)
        stats.read_corpus(automate)

    except Exception as e:
        print(f"Erreur : le fichier '{chemin_corpus}' est introuvable.")
        return

    while True:
        print("\n" + "="*40)
        print("MENU PRINCIPAL - CONCORDANCIER")
        print("1. Informations générales du corpus")
        print("2. Graphe de Zipf")
        print("3. Afficher les statistiques d'un tag (fréquence, rang, 10 formes les plus fréquentes)")
        print("4. Rechercher un mot (fréquence, rang, 5 collocations les plus fréquentes, KWIC optionnel)")
        print("5. Rechercher une suite de mots, une suite de tags ou une suite mixte")
        print("6. Rechercher une expression régulière (KWIC optionnel)")
        print("0. Quitter")

        choix = input("Votre choix : ").strip()
        
        if choix == '0':
            print("Au revoir !")
            break
        elif choix == '1':
            stats.info_generale(automate, True)
        elif choix == '2':
            stats.plot_zipf()
        elif choix == '3':
            stats.requete_tag()
        elif choix == '4':
            stats.requete_mot()
        elif choix == '5':
            requete_mixte(stats)
        elif choix == '6':
            stats.requete_regex()
        else:
            print("Choix invalide, veuillez réessayer.")
    
if __name__ == "__main__":
    main()