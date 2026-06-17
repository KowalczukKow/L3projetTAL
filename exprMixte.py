import re
from reconaissance import tag_expr

def requete_mixte(corpus) :

    regex = re.compile(tag_expr)
    sequence = input("Entrez la suite : ")
    pattern = sequence.strip().split()

    demande = []

    for motag in pattern :

        if regex.fullmatch(motag) :
            demande.append((motag, 1)) # 1 s'il s'agit d'un tag
        else :
            demande.append((motag.lower(), 0))

    nb_mots = len(demande)

    indices = []
    #ph_pos = [] # numéros des phrases et positions dans les phrases

    motag1, type = demande[0]

    for i in range(len(corpus.tokens) - nb_mots + 1) :
        valid = True
        if corpus.tokens[i][type] == motag1 :
            for j in range(1, nb_mots) : 
                if corpus.tokens[i+j][demande[j][1]] != demande[j][0] :
                    valid = False
                    break
            if valid :
                indices.append(i)
                #ph_pos.append(phrase_et_position(corpus, i))

    nb_occ = len(indices)
    
    freq = calc_freq(corpus, nb_occ, nb_mots)
    affiche_infos(sequence, nb_occ, freq, cooccurences(corpus.tokens, indices, nb_mots, 1))


def phrase_et_position(corpus, indice) :
    for i, id_deb in enumerate(corpus.id_debut_sentences) :
        if indice < id_deb :
            return i - 1, indice - corpus.id_debut_sentences[i-1]
        
def calc_freq(corpus, nb_occ, nb_mots) :
    nb_total_corpus = corpus.nb_mots - nb_occ * (nb_mots-1)

    if nb_total_corpus > 0 :
        return round(nb_occ/nb_total_corpus * 100, 4)
    
    return 0.0
        
#def calc_pmi(corpus, mode ) 

# mode = 0 pour les mots, mode = 1 pour les tags      
def cooccurences(tokens, indices, nb_mots, mode=0) :
    coocc = []
    coocc.append({}) # à gauche
    coocc.append({}) # à droite

    max_id_tokens = len(tokens) - 1

    for id in indices : 
        if id != 0 :
            motag = tokens[id-1][mode]

            if motag not in coocc[0] :
                coocc[0][motag] = {'nb': 0}

            coocc[0][motag]['nb'] += 1
        
        if id + nb_mots - 1 != max_id_tokens :
            motag = tokens[id+nb_mots][mode]

            if motag not in coocc[1] :
                coocc[1][motag] = {'nb': 0}

            coocc[1][motag]['nb'] += 1
    
    return coocc


def affiche_infos(sequence, nbOcc, frequence, coocc) :
    print(f"\nSuite recherchée : ", sequence)
    print(f"Nombre d'occurrences : ", nbOcc)
    print(f"Fréquence : {frequence} %")
    print(coocc)

if __name__ == "__main__":
    import main
    main.main()