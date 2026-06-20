from kwic import kwic_words, afficher_kwic

def requete_mot(corpus):
    while True:
        mot = input("Entrez un mot (ou appuyer sur ENTREE pour quitter) : ")

        if not mot :
            break

        if mot in corpus.index:
            cible = mot
        else:
            mot_minus = mot.lower()
            if mot_minus in corpus.index:
                cible = mot_minus
            else:
                print(f"Le mot '{mot}' n'est pas trouvé dans le corpus.")
                rep = input("Voulez-vous essayer un autre mot (oui/non) : ")
                if rep.lower() != 'oui':
                    print("Fin de la requête.")
                    break
                continue

        infos = corpus.index[cible]

        print(f"Mot: {cible}")
        print(f"Nombre d'occurrences: {infos['nb_occ']}")
        print(f"Rang: {infos['rang']}")
        print(f"Fréquence: {infos['freq']}%")
            
        existe_collocation = False

        if 'coocc_gauche' in infos and infos['coocc_gauche']:
            existe_collocation = True
            print("\nPrincipales collocations à gauche (mot précédent : nb, PMI) :")

            for mot2, co in list(infos['coocc_gauche'].items())[:5]:
                print(f"{mot2} : {co['nb']}, {round(co['pmi'], 5)}")

        if 'coocc_droite' in infos and infos['coocc_droite']:
            existe_collocation = True
            print("\nPrincipales collocations à droite (mot suivant : nb, PMI) :")
            # afficher les 5 meilleures collocations
            for mot2, co in list(infos['coocc_droite'].items())[:5]:
                print(f"{mot2} : {co['nb']}, {round(co['pmi'], 5)}")

        if not existe_collocation:
            print("Pas de collocations disponibles.")


        kwic_choix = input("\nVoulez-vous afficher le contexte (KWIC) ? (oui/non) : ").strip().lower()

        if kwic_choix == 'oui':
            size = int(input("Entrez le nombre de mots à gauche et à droite que vous souhaitez afficher, par défaut 5) : ") or 5)

            kwic_results = kwic_words(corpus, cible, size = size, case_sensitive=False)

            if kwic_results:
                afficher_kwic(kwic_results, size = size)
            else:
                print("Aucun contexte trouvé.")

        reponse = input("\nVoulez-vous analyser un autre mot ? (oui/non) : ").strip().lower()
        if reponse != 'oui':
            print("Fin de la consultation.")
            break

def requete_tag(corpus):
    tag = input("Entrez un tag (ex: NC, NPP, V, ADJ, ADV, PONCT) : ").strip()

    if tag not in corpus.index_tags:
        print(f"Le tag '{tag}' n'est pas trouvé dans le corpus.")
        return
        
    infos = corpus.index_tags[tag]

    print(f"\nTag: {tag}")
    print(f"Nombre d'occurrences: {infos['nb_occ']}")
    print(f"Nombre de formes distinctes: {infos['nb_formes']}")
    print(f"Fréquence dans le corpus : {round(infos['nb_occ'] / corpus.nb_mots * 100, 4)}%")
        
    print(f"\nFormes les 10 plus fréquentes pour ce tag (mot : nb, freq, rang) :")
    for forme in infos['formes_triees'][:10]:
        print(f"{forme['mot']} : {forme['nb']}, {forme['freq']}%, rang {forme['rang']}")



if __name__ == "__main__":
    import main
    main.main()