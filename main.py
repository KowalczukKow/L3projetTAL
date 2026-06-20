import re
import os

from reconnaissance import expr

from corpusStats import CorpusStats

from stats import info_generale, ranks_and_freqs, stats_tags, plot_zipf

from collocations import cooccurrences, pmi, trier_pmi

from requetes import requete_mot, requete_tag

from regexSearch import requete_regex

from exprMixte import requete_mixte

from aide import afficher_aide


def main():
    automate = re.compile(expr)

    print("=== Chargement du corpus ===")

    chemin_corpus = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "corpus",
        "sequoia-9.2.fine.brown"
    )

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

        # Partie statistiques
        ranks_and_freqs(stats)
        cooccurrences(stats)
        pmi(stats)
        trier_pmi(stats)
        stats_tags(stats)

    except FileNotFoundError:
        print(f"Erreur : le fichier '{chemin_corpus}' est introuvable.")
        return

    except Exception as e:
        print("Une autre erreur est survenue :")
        print(e)
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

        print("\n7. Aide en ligne")

        print("\n0. Quitter")

        print("\n" + "=" * 55)
        choix = input("Votre choix : ").strip()
        
        if choix == '0':
            print("Au revoir !")
            break

        elif choix == '1':
            info_generale(stats, automate)

        elif choix == '2':
            plot_zipf(stats)

        elif choix == '3':
            requete_tag(stats)

        elif choix == '4':
            requete_mot(stats)

        elif choix == '5':
            requete_regex(stats)

        elif choix == '6':
            requete_mixte(stats)

        elif choix == '7':
            afficher_aide()

        else:
            print("Choix invalide, veuillez réessayer.")
    
if __name__ == "__main__":
    main()