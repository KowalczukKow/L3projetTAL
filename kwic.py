def kwic_words(corpus, word, size = 5, case_sensitive = False):
    # je corrige ici car quand case_sensitive False, l'utilisateur tape "The" mais on cherche query = The donc on n'arrive pas à trouver les vrais "the"

    if case_sensitive:
        query = word 
    else: 
        query = word.lower()

        # Si la forme miniscule n'est pas dans l'index, c'est possible d'être NPP et on doit conserver la casse
        if query not in corpus.index and word in corpus.index:
            query = word

    if query not in corpus.index:
        print(f"Le mot '{word}' n'est pas trouvé dans le corpus.")
        return []
        
    infos = corpus.index[query]
    results = []

    for id_ligne, pos in zip(infos['n_ligne'], infos['pos_ligne']):
        sentence = corpus.sentences[id_ligne - 1]  # id_ligne commence à 1
        gauche_ind = max(0, pos - size - 1)  # pos commence à 1
        pos_enquete = pos - 1  # position du mot dans la ligne (0-indexé)
        droite_ind = min(len(sentence), pos + size)  # pos + size est exclusif
        results.append({
            'id_ligne' : id_ligne,
            'pos' : pos,
            'gauche' : sentence[gauche_ind:pos_enquete],
            'mot_enquete' : sentence[pos_enquete],
            'droite' : sentence[pos_enquete + 1:droite_ind]
        })
    return results

def afficher_kwic(kwic_results, size = 5, show_tag=True):
    for res in kwic_results:
        gauche_str = ' '.join(res['gauche'])
        enquete_str = res['mot_enquete']
        droite_str = ' '.join(res['droite'])
        # aligner à gauche et à droite avec une largeur fixe pour que les mots enquêtés soient alignés verticalement
        gauche_part = gauche_str.rjust(30) # 30 caractères pour la partie gauche
        droite_part = droite_str.ljust(30) # 30 caractères pour la partie droite
        print(gauche_part + "  [" + enquete_str + "]  " + droite_part)



if __name__ == "__main__":
    import main
    main.main()