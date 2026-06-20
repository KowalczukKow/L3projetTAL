def kwic_words(corpus, word, size = 5, case_sensitive = False):

    if case_sensitive:
        query = word 
    else: 
        query = word
        if word in corpus.index:
            tags = corpus.index[word]['tags']
            if 'NPP' in tags:
                query = word  # garder la casse pour les noms propres
            else:
                query = word.lower()  # mettre en minuscules pour les autres mots

    if query not in corpus.index:
        print(f"Le mot '{word}' n'est pas trouvé dans le corpus.")
        return []
        
    infos = corpus.index[query]
    results = []

    for id_phrase, pos in zip(infos['n_phrase'], infos['pos_phrase']):
        sentence = corpus.sentences[id_phrase - 1]  # id_phrase commence à 1
        gauche_ind = max(0, pos - size - 1)  # pos commence à 1
        pos_enquete = pos - 1  # position du mot dans la phrase (0-indexé)
        droite_ind = min(len(sentence), pos + size)  # pos + size est exclusif
        results.append({
            'id_phrase' : id_phrase,
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