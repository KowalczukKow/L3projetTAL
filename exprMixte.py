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

    len_suite = len(demande)

    indices = []
    ph_pos = [] # numéros des phrases et positions dans les phrases

    motag1, type = demande[0]

    for i in range(len(corpus.tokens) - len_suite + 1) :
        valid = True
        if corpus.tokens[i][type] == motag1 :
            for j in range(1, len_suite) : 
                if corpus.tokens[i+j][demande[j][1]] != demande[j][0] :
                    valid = False
                    break
            if valid :
                indices.append(i)
                ph_pos.append(phrase_et_position(corpus, i))

    affiche_infos(sequence, len(indices), cooccurences(corpus.tokens, indices, len_suite, 1))


def phrase_et_position(corpus, indice) :
    for i, id_deb in enumerate(corpus.id_debut_sentences) :
        if indice < id_deb :
            return i - 1, indice - corpus.id_debut_sentences[i-1]
        

# mode = 0 pour les mots, mode = 1 pour les tags      
def cooccurences(tokens, indices, len_suite, mode=0) :
    coocc = []
    coocc.append({}) # à gauche
    coocc.append({}) # à droite

    max_id_tokens = len(tokens) - 1

    for id in indices : 
        if id != 0 :
            mot = tokens[id-1][mode]

            if mot not in coocc[0] :
                coocc[0][mot] = {'nb': 0}

            coocc[0][mot]['nb'] += 1
        
        if id + len_suite - 1 != max_id_tokens :
            mot = tokens[id+len_suite][mode]

            if mot not in coocc[1] :
                coocc[1][mot] = {'nb': 0}

            coocc[1][mot]['nb'] += 1
    
    return coocc


def affiche_infos(sequence, nbOcc, coocc) :
    print(f"\nSuite recherchée : ", sequence)
    print(f"Nombre d'occurrences : ", nbOcc)
    print(coocc)

if __name__ == "__main__":
    import main
    main.main()