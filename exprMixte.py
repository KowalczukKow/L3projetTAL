import math
import re
from reconaissance import tag_expr
from ngrammes import Ngramme
import matplotlib.pyplot as plt

def requete_mixte(corpus) :

    regex = re.compile(tag_expr)
    pattern = input("Votre choix : ").strip().split()

    demande = []
    suite_cherchee = ''

    #mot = '\S+'

    for motag in pattern :

        #if suite_cherchee != '' :
        #    suite_cherchee += ' '

        if regex.fullmatch(motag) :
            demande.append((motag, 1)) # 1 s'il s'agit d'un tag
            #suite_cherchee += mot + '/' + motag
        else :
            demande.append((motag.lower(), 0))
            #suite_cherchee += motag.lower() + '/' + mot

    #regex_cherchee = re.compile(suite_cherchee, re.IGNORECASE)
    len_suite = len(demande)

    indices = []

    motag1, type = demande[0]

    for i in range(len(corpus.tokens) - len_suite + 1) :
        valid = True
        if corpus.tokens[i][type] == motag1 :
            print(corpus.tokens[i][type])
            for j in range(1, len_suite) : 
                # case à corriger
                if corpus.tokens[i+j][demande[j][1]] != demande[j][0] :
                    #print(corpus.tokens[i+j][demande[j][1]])
                    #print(demande[j][0])
                    valid = False
                    break
                else :
                    print(corpus.tokens[i+j][demande[j][1]])
            if valid :
                indices.append(i)
                print("valid\n")

    print("\n",len(indices))

def phrase_et_position(corpus, indice) :
    for i, id_deb in enumerate(corpus.id_debut_sentences) :
        if indice < id_deb :
            return i - 1, indice - corpus.id_debut_sentences[i-1]

if __name__ == "__main__":
    import main
    main.main()