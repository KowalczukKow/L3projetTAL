import math
import re
from reconaissance import expr
import matplotlib.pyplot as plt

class Ngramme:
    def __init__(self, corpus_stats, sequence):
        self.corpus_stats = corpus_stats
        self.sequence = sequence
        self.liste_mots = self.sequence.strip().split() # la séquence sous la forme d'une liste
        self.nbMots = 0
        self.positions_n_grammes = {}
        self.nbOcc = 0
        # nb des mots dans le corpus si on considère le n gramme commme un seul mot
        self.nb_total_corpus = 0 
        self.freq = 0
        self.coocc = []
        self.initialise_ngramme()
    

    def initialise_ngramme(self) :
        self.nbMots = len(self.liste_mots)

        if self.nbMots == 0 :
            print("Requête vide")

        occurences = []
        mots_ids_phrases = []

        for mot in self.liste_mots :
            # on utilise set pour transformer la liste en ensemble
            mots_ids_phrases.append(set(self.corpus_stats.index[mot]['n_phrase']))

        phrases_communes = set.intersection(*mots_ids_phrases)

        positions_p = {}
        
        for id_phrase in phrases_communes :
            positions_p[id_phrase] = [[] for _ in range(self.nbMots)]

        for i, mot in enumerate(self.liste_mots) :
            
            for id_phrase, pos in zip(self.corpus_stats.index[mot]['n_phrase'], self.corpus_stats.index[mot]['pos_phrase']): 
                
                if id_phrase in phrases_communes :
                    positions_p[id_phrase][i].append(pos)

        self.sort_positions_n_grammes(positions_p, phrases_communes)
        self.calc_freq()
        self.cooccurrences_suite()
    
    
    def sort_positions_n_grammes(self, positions_p, phrases_communes) :
        # dictionnaire de structure [numero phrase] : [position mot 1, position mot 2...], 
        # (si 1+ occurences dans la phrase)[position mot 1, position mot 2...]
        for id in phrases_communes :
            n = len(positions_p[id])
            for pos_base in positions_p[id][0] :
                positions = []
                for i in range(n) :
                    if pos_base+i in positions_p[id][i] :
                        positions.append(pos_base+i)
                    else :
                        positions = []
                        break
                if positions :
                    self.nbOcc+=1
                    if id not in self.positions_n_grammes :
                        self.positions_n_grammes[id] = []

                    self.positions_n_grammes[id].append(positions)
    

    def calc_freq(self) :
        self.nb_total_corpus = self.corpus_stats.nb_mots - self.nbOcc * (self.nbMots - 1)
        self.freq = round(self.nbOcc / self.nb_total_corpus * 100, 4)
    

    def cooccurrences_suite(self) : 
        #mot1 = self.liste_mots[0] # le premier mot
        self.coocc.append({})

        #mot2 = self.liste_mots[-1] # le dernier mot
        self.coocc.append({})

        for id_phrase in self.positions_n_grammes.keys() :
            for i in range(len(self.positions_n_grammes[id_phrase])):
                pos1 = self.positions_n_grammes[id_phrase][i][0]
                
                # on vérifie s'il sagit pas du premier mot du corpus
                if not (id_phrase == 0 and pos1 == 1) : 
                    token = ""
                    if pos1 == 1 :
                        token = self.corpus_stats.sentences[id_phrase-2][-1]
                    else :
                        token = self.corpus_stats.sentences[id_phrase-1][pos1-2]

                    mot, tag = token.split('/', 1)

                    if mot not in self.coocc[0] :
                        self.coocc[0][mot] = {'nb': 0, 'pmi': 0.0}

                    self.coocc[0][mot]['nb'] += 1

                pos2 = self.positions_n_grammes[id_phrase][i][-1]
                posMax = len(self.corpus_stats.sentences[id_phrase-1])

                # on vérifie s'il sagit pas du dernier mot du corpus
                if not (pos2 == posMax and id_phrase == self.corpus_stats.nb_phrases) : 
                    token = ""
                    if pos2 == posMax :
                        token = self.corpus_stats.sentences[id_phrase][0]
                    else :
                        token = self.corpus_stats.sentences[id_phrase-1][pos2]

                    mot, tag = token.split('/', 1)

                    if mot not in self.coocc[1] :
                        self.coocc[1][mot] = {'nb': 0, 'pmi': 0.0}

                    self.coocc[1][mot]['nb'] += 1

        self.pmi_suite()

    # pour compter le nombre d'occurrences d'un mot dans le n-gramme pour
    # ensuite ajuster le calcul de pmi
    def verif_mot_pres(self, mot_a_verif) :
        compteur = 0
        for mot in self.liste_mots:
            if mot == mot_a_verif :
                compteur+=1
        return compteur

    
    def pmi_suite(self) :

        for mot in self.coocc[1] :

            nb_pair = self.coocc[1][mot]['nb']
            nb_occ_mot = self.corpus_stats.index[mot]['nb'] - self.nbOcc * self.verif_mot_pres(mot)
            pmi = math.log2(nb_pair * self.nb_total_corpus / (self.nbOcc * nb_occ_mot))

            self.coocc[1][mot]['pmi'] = pmi
        
        self.trier_pmi_suites()


    def trier_pmi_suites(self):
        # pour chaque mot, trier les cooccurrences par PMI décroissant
        liste = []

        for mot in self.coocc[1]:
            nb, pmi = self.coocc[1][mot]['nb'], self.coocc[1][mot]['pmi']
            liste.append((mot, nb, pmi))

        # trier la liste par PMI décroissant
        liste.sort(key=lambda x: x[2], reverse=True)

        # stocker les cooccurrences triées dans l'index
        self.coocc[1] = {}

        for mot, nb, pmi in liste:
            self.coocc[1][mot] = {'nb': nb, 'pmi': pmi}

    #     + kwi suites???

if __name__ == "__main__":
    import main
    main.main()