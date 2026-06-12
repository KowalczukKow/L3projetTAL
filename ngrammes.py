import math
import re
from reconaissance import expr
import matplotlib.pyplot as plt

class Ngramme:
    def __init__(self, corpus_stats, sequence):
        self.corpus_stats = corpus_stats
        self.sequence = sequence
        self.nbMots = 0
        self.positions_n_grammes = {}
        self.nbOcc = 0
        self.initialise_ngramme()
    

    def initialise_ngramme(self) :
        suite_cherchee = self.sequence.strip().split()
        self.nbMots = len(suite_cherchee)

        if self.nbMots == 0 :
            print("Requête vide")

        occurences = []
        mots_ids_phrases = []

        for mot in suite_cherchee :
            # on utilise set pour transformer la liste en ensemble
            mots_ids_phrases.append(set(self.corpus_stats.index[mot]['n_phrase']))

        phrases_communes = set.intersection(*mots_ids_phrases)

        positions_p = {}
        
        for id_phrase in phrases_communes :
            positions_p[id_phrase] = [[] for _ in range(self.nbMots)]

        for i, mot in enumerate(suite_cherchee) :
            
            for id_phrase, pos in zip(self.corpus_stats.index[mot]['n_phrase'], self.corpus_stats.index[mot]['pos_phrase']): 
                
                if id_phrase in phrases_communes :
                    positions_p[id_phrase][i].append(pos)

        self.sort_positions_n_grammes(positions_p, phrases_communes)
    
    
    def sort_positions_n_grammes(self, positions_p, phrases_communes) :
        # dictionnaire de structure [numero phrase] : [position mot 1, position mot 2...]
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
    
    
    # def pmi_suite(self, positions_n_grammes) :
    #     + kwi suites???

if __name__ == "__main__":
    import main
    main.main()