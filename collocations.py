import math
from parser import parser_token

def cooccurrences(corpus):
        # calculer les cooccurrences pour chaque paire de mots adjacents dans le corpus
        for sentence in corpus.sentences:
            for i in range(len(sentence) - 1):
                token1 = sentence[i]
                token2 = sentence[i+1]

                mot1, tag1, token_new1 = parser_token(token1)
                mot2, tag2, token_new2 = parser_token(token2)

                # je lai mis en commentaire parce que peut-être cest utile de savoir si le
                # mot est à la fin / début de la ligne
                # if tag1 == 'PONCT' or tag2 == 'PONCT':
                #     continue

                if tag1 != 'NPP':
                    mot1 = mot1.lower()
                if tag2 != 'NPP':
                    mot2 = mot2.lower()

                if mot1 not in corpus.coocc_droite:
                    corpus.coocc_droite[mot1] = {}
                if mot2 not in corpus.coocc_droite[mot1]:
                    corpus.coocc_droite[mot1][mot2] = {'nb': 0, 'pmi': 0.0}

                corpus.coocc_droite[mot1][mot2]['nb'] += 1

                if mot2 not in corpus.coocc_gauche:
                        corpus.coocc_gauche[mot2] = {}
                if mot1 not in corpus.coocc_gauche[mot2]:
                        corpus.coocc_gauche[mot2][mot1] = {'nb': 0, 'pmi': 0.0}

                corpus.coocc_gauche[mot2][mot1]['nb'] += 1

def pmi(corpus):
        # calculer le PMI pour chaque paire de mots dans les cooccurrences

        for mot1 in corpus.coocc_droite:
        
            for mot2 in corpus.coocc_droite[mot1]:
            
                nb_pair = corpus.coocc_droite[mot1][mot2]['nb']
                nb_1 = corpus.index[mot1]['nb_occ']
                nb_2 = corpus.index[mot2]['nb_occ']

                pmi = math.log2(nb_pair * corpus.nb_mots / (nb_1 * nb_2))

                corpus.coocc_droite[mot1][mot2]['pmi'] = pmi

        for mot2 in corpus.coocc_gauche:
            for mot1 in corpus.coocc_gauche[mot2]:
                nb_pair = corpus.coocc_gauche[mot2][mot1]['nb']
                nb_1 = corpus.index[mot1]['nb_occ']
                nb_2 = corpus.index[mot2]['nb_occ']

                # PMI = log2( C(w1,w2) * N / (C(w1)*C(w2)) )
                pmi = math.log2(nb_pair * corpus.nb_mots /(nb_1 * nb_2))

                corpus.coocc_gauche[mot2][mot1]['pmi'] = pmi
    


def trier_pmi(corpus):
     # pour chaque mot, trier les cooccurrences par PMI décroissant et stocker dans l'index

    for mot1, dico in corpus.coocc_droite.items():
        if mot1 not in corpus.index:
            continue
            
        liste_droite = []

        for mot2 in corpus.coocc_droite[mot1]:
            nb, pmi = corpus.coocc_droite[mot1][mot2]['nb'], corpus.coocc_droite[mot1][mot2]['pmi']
            liste_droite.append((mot2, nb, pmi))

        # trier la liste par PMI décroissant
        liste_droite.sort(key=lambda x: x[2], reverse=True)

        # stocker les cooccurrences triées dans l'index
        corpus.index[mot1]['coocc_droite'] = {}

        for mot2, nb, pmi in liste_droite:
            corpus.index[mot1]['coocc_droite'][mot2] = {'nb': nb, 'pmi': pmi}
        

    for mot2, dico in corpus.coocc_gauche.items():

        liste_gauche = []

        for mot1 in dico:
            nb = dico[mot1]['nb']
            pmi = dico[mot1]['pmi']
            liste_gauche.append((mot1, nb, pmi))

        liste_gauche.sort(key=lambda x: x[2], reverse=True)

        if mot2 not in corpus.index:
            continue

        corpus.index[mot2]['coocc_gauche'] = {}

        for mot1, nb, pmi in liste_gauche:
            corpus.index[mot2]['coocc_gauche'][mot1] = {'nb': nb, 'pmi': pmi}

