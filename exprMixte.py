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

    nb_motags = len(demande)

    indices = []
    #ph_pos = [] # numéros des phrases et positions dans les phrases

    motag1, type = demande[0]

    for i in range(len(corpus.tokens) - nb_motags + 1) :
        valid = True
        if corpus.tokens[i][type] == motag1 :
            for j in range(1, nb_motags) : 
                if corpus.tokens[i+j][demande[j][1]] != demande[j][0] :
                    valid = False
                    break
            if valid :
                indices.append(i)
                #ph_pos.append(phrase_et_position(corpus, i))

    nb_occ = len(indices)
    
    mode = demande_mode()

    nb_total_corpus = corpus.nb_mots - nb_occ * (nb_motags-1)

    infos = infos_expr_mixtes(corpus, sequence, demande, nb_occ, nb_motags, indices, nb_total_corpus, mode)

    freq = calc_freq(nb_total_corpus, nb_occ)
    coocc = cooccurences(infos)
    affiche_infos(infos, freq, coocc)


def infos_expr_mixtes(corpus, sequence, demande, nb_occ, nb_motags, indices, nb_total_corpus, mode) :
    infos = {
        'corpus' : corpus,
        'sequence' : sequence,
        'demande' : demande,
        'nb_occ' : nb_occ,
        'nb_motags' : nb_motags,
        'indices' : indices,
        'nb_tot_corp' : nb_total_corpus,
        'mode' : mode
    }
    return infos


def phrase_et_position(corpus, indice) :
    for i, id_deb in enumerate(corpus.id_debut_sentences) :
        if indice < id_deb :
            return i - 1, indice - corpus.id_debut_sentences[i-1]


def calc_freq(nb_total_corpus, nb_occ) :

    if nb_total_corpus > 0 :
        return round(nb_occ/nb_total_corpus * 100, 4)
    
    return 0.0
    

# mode = 0 pour les mots, mode = 1 pour les tags      
def cooccurences(infos) :
    coocc = []
    coocc.append({}) # à gauche
    coocc.append({}) # à droite

    tokens = infos['corpus'].tokens

    max_id_tokens = len(tokens) - 1

    for id in infos['indices'] : 
        if id != 0 :

            motag = tokens[id-1][infos['mode']]

            if motag not in coocc[0] :
                coocc[0][motag] = {'nb': 0, 'pmi' : 0}

            coocc[0][motag]['nb'] += 1
        
        if id + infos['nb_motags'] - 1 != max_id_tokens :

            motag = tokens[id+infos['nb_motags']][infos['mode']]

            if motag not in coocc[1] :
                coocc[1][motag] = {'nb': 0, 'pmi' : 0}

            coocc[1][motag]['nb'] += 1
    
    coocc = calc_pmi(infos['corpus'], infos['nb_occ'], infos['demande'], infos['nb_tot_corp'], infos['mode'], coocc)
    return coocc


def calc_pmi(corpus, nb_occ, liste_motags, nb_total_corpus, mode, coocc) :
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

    for i in range(2) :
        liste = []
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


def kwic(corpus, demande, indices, nb_motags, mode, size=5) :
    results = [] 

    tokens = corpus.tokens

    for i in indices : 
        pos1 = i 
        pos2 = i + nb_motags - 1

        gauche_ind = max(0, pos1 - size)
        droite_ind = min(len(tokens) - 1, pos2 + size)

        results.append({
            'pos_debut' : pos1,
            'pos_fin' : pos2,
            'gauche' : [motag[mode] for motag in tokens[gauche_ind:pos1]],
            'expr' : [motag[0] for motag in demande],
            'droite' : [motag[mode] for motag in tokens[pos2+1:droite_ind+1]]
        })

    return results


def verif_motag_pres(demande, motag_a_verif) :
    compteur = 0
    for motag in demande:
        if motag[0] == motag_a_verif :
            compteur+=1
    return compteur


def affiche_infos(infos, freq, coocc) :
    print(f"\nSuite recherchée : ", infos['sequence'])
    print(f"Nombre d'occurrences : ", infos['nb_occ'])
    print(f"Fréquence : {freq} %")
    affiche_coocc(coocc, infos['mode'])
    size_kwic = demande_kwic()
    if size_kwic > 0 :
        results_kwic = kwic(infos['corpus'], infos['demande'], infos['indices'], infos['nb_motags'], infos['mode'], size_kwic)
        affiche_kwic(results_kwic)



def affiche_coocc(coocc, mode) :
    motag_str = 'tag' if mode == 1 else 'mot'

    if coocc[0]:
            print(f"\nPrincipales collocations à gauche ({motag_str} précédent : nb, PMI) :")
            for motag in list(coocc[0].keys())[:5]:
                print(motag, ":", coocc[0][motag]['nb'], ", ", round(coocc[0][motag]['pmi'],5))
    else:
        print("\nPas de collocations à gauche disponibles.")

    if coocc[1]:
        print(f"\nPrincipales collocations à droite ({motag_str} suivant : nb, PMI) :")
        for motag in list(coocc[1].keys())[:5]:
            print(motag, " : ", coocc[1][motag]['nb'], ", ", round(coocc[1][motag]['pmi'],5))
    
    else:
        print("\nPas de collocations à droite disponibles.")


def affiche_kwic(results_kwic) :
    for res in results_kwic:
        gauche_str = ' '.join(res['gauche'])
        enquete_str = ' '.join(res['expr'])
        droite_str = ' '.join(res['droite'])
        # aligner à gauche et à droite avec une largeur fixe pour que les mots enquêtés soient alignés verticalement
        gauche_part = gauche_str.rjust(30) # 30 caractères pour la partie gauche
        droite_part = droite_str.ljust(30) # 30 caractères pour la partie droite
        print(gauche_part + "  [" + enquete_str + "]  " + droite_part)


def demande_mode() :
        print("Mode d'affichage du contexte et de relations :")
        print("1. Mots uniquement")
        print("2. Tags uniquement")
        choix = input("Votre choix : ").strip()
        if not choix :
            return 0
        elif int(choix) not in [1, 2] :
            return 0
        return int(choix) - 1


def demande_kwic() :
    kwic_choix = input("\nVoulez-vous afficher le contexte (KWIC) ? (oui/non) : ").strip().lower()
    if kwic_choix == 'oui':
        size = int(input("Entrez le nombre de mots à gauche et à droite que vous souhaitez afficher, par défaut 5) : ") or 5)
        return size
    return -1

if __name__ == "__main__":
    import main
    main.main()