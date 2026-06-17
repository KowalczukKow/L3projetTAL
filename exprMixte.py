import math
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
    
    mode = demande_mode()

    nb_total_corpus = corpus.nb_mots - nb_occ * (nb_mots-1)
    freq = calc_freq(nb_total_corpus, nb_occ)
    coocc = cooccurences(corpus, indices, nb_mots, nb_occ, demande, nb_total_corpus, mode)
    affiche_infos(sequence, nb_occ, freq, coocc)


def phrase_et_position(corpus, indice) :
    for i, id_deb in enumerate(corpus.id_debut_sentences) :
        if indice < id_deb :
            return i - 1, indice - corpus.id_debut_sentences[i-1]


def calc_freq(nb_total_corpus, nb_occ) :

    if nb_total_corpus > 0 :
        return round(nb_occ/nb_total_corpus * 100, 4)
    
    return 0.0
    

# mode = 0 pour les mots, mode = 1 pour les tags      
def cooccurences(corpus, indices, nb_mots, nb_occ, liste_motags, nb_total_corpus, mode=0) :
    coocc = []
    coocc.append({}) # à gauche
    coocc.append({}) # à droite

    tokens = corpus.tokens

    max_id_tokens = len(tokens) - 1

    for id in indices : 
        if id != 0 :
            motag = tokens[id-1][mode]

            if motag not in coocc[0] :
                coocc[0][motag] = {'nb': 0, 'pmi' : 0}

            coocc[0][motag]['nb'] += 1
        
        if id + nb_mots - 1 != max_id_tokens :
            motag = tokens[id+nb_mots][mode]

            if motag not in coocc[1] :
                coocc[1][motag] = {'nb': 0, 'pmi' : 0}

            coocc[1][motag]['nb'] += 1
    
    coocc = calc_pmi(corpus, nb_occ, liste_motags, nb_total_corpus, coocc, mode)
    return coocc


def calc_pmi(corpus, nb_occ, liste_motags, nb_total_corpus, coocc, mode) :
    index = corpus.index
    if mode == 1 :
        index = corpus.index_tags

    for i in range (2) :
        for motag in coocc[i] :
            nb_pair = coocc[i][motag]['nb']

            if motag not in index :
                print(f"Le mot '{motag}' n'est pas trouvé dans le corpus.")
                continue
            
            nb_occ_motag = index[motag]['nb_occ'] - nb_occ * verif_motag_pres(liste_motags, motag)

            if nb_occ == 0 or nb_occ_motag <= 0 :
                    continue
            
            pmi = math.log2(nb_pair * nb_total_corpus / (nb_occ * nb_occ_motag))
            coocc[i][motag]['pmi'] = pmi

    return sort_pmi(coocc)


def sort_pmi(coocc) :
    liste = []

    for i in range(2) :
        for motag in coocc[i]:
            nb, pmi = coocc[i][motag]['nb'], coocc[i][motag]['pmi']
            liste.append((motag, nb, pmi))

        # trier la liste par PMI décroissant
        liste.sort(key=lambda x: x[2], reverse=True)

        # stocker les cooccurrences triées dans l'index
        coocc[i] = {}

        for motag, nb, pmi in liste:
            coocc[i][motag] = {'nb': nb, 'pmi': pmi}
    
    return coocc


def verif_motag_pres(liste_motags, motag_a_verif) :
    compteur = 0
    for motag in liste_motags:
        if motag == motag_a_verif :
            compteur+=1
    return compteur


def affiche_infos(sequence, nbOcc, frequence, coocc) :
    print(f"\nSuite recherchée : ", sequence)
    print(f"Nombre d'occurrences : ", nbOcc)
    print(f"Fréquence : {frequence} %")
    print(coocc)

def demande_mode() :
        print("Mode d'affichage du contexte et de relations :")
        print("1. Mots uniquement")
        print("2. Tags uniquement")
        return int(input("Votre choix : ").strip()) - 1

if __name__ == "__main__":
    import main
    main.main()