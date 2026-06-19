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
        stats.read_corpus(automate, True)

    except Exception as e:
        print(f"Erreur : le fichier '{chemin_corpus}' est introuvable.")
        return

    while True:
        print("\n" + "=" * 55)
        print("MENU PRINCIPAL - CONCORDANCIER")
        print("-" * 55)

        print("\n1. Informations générales du corpus")
        print("   -> nombre de mots, phrases et formes")

        print("\n2. Graphe de Zipf")
        print("   -> visualisation des fréquences des mots")

        print("\n3. Afficher les statistiques d'un tag")
        print("   -> fréquence, rang et formes les plus fréquentes")

        print("\n4. Rechercher un mot")
        print("   -> fréquence, rang, collocations et KWIC optionnel")

        print("\n5. Rechercher par expression régulière (mot/tag)")
        print("   -> ex : '.*tion', 'N.*'")

        print("\n6. Rechercher une suite structurée (suite de mots/de tags/mixte)")
        print("   -> suite de mots, de tags ou mixte")
        print("   -> ex : 'DET NC', 'NPP V', 'le NC'")

        print("\n0. Quitter")

        print("\n" + "=" * 55)
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
            stats.requete_regex()
        elif choix == '6':
            requete_mixte(stats)
        else:
            print("Choix invalide, veuillez réessayer.")
    
if __name__ == "__main__":
    main()