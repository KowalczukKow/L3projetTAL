import math
import matplotlib.pyplot as plt

class CorpusStats:
    def __init__(self):
        self.index = {}
        self.coocc = {} #collocations prinicipales
        self.tokens = []
        self.nb_mots = 0
        self.nb_phrases = 0
        self.nb_formes = 0
        self.sentences = [] # pour le KWIC

    def read_corpus(self, corpus):

        with open(corpus, 'r', encoding='utf-8') as f:
            id_phrase = 1 # numéroter les phrases à partir de 1
            for line in f:
                line = line.strip()
                if not line:
                    continue
                words = line.split()   # les mots sont sous la forme "mot/tag"
                self.sentences.append(words)   # stocke la phrase originale pour le KWIC
                self.nb_phrases += 1

                # parcourir tous les mots de la phrase
                for pos, token in enumerate(words, start=1):   # pos à partir de 1
                    self.tokens.append(token)
                    self.nb_mots += 1

                    # séparer le mot et son tag
                    mot, tag = token.split('/')
                    # rendre le mot en minuscules s'il n'est pas un nom propre
                    if tag != 'NPP':
                        mot = mot.lower()

                    # si le mot n'est pas encore dans l'index, l'ajouter
                    if mot not in self.index:
                        self.index[mot] = {
                            'nb': 0,            # le nombre d'occurrences
                            'tags': [],         # les tags associés
                            'n_phrase': [],     # les numéros de phrase où il apparaît
                            'pos_phrase': []    # les positions dans la phrase où il apparaît
                        }
                    # renouveler les informations pour ce mot
                    self.index[mot]['nb'] += 1
                    self.index[mot]['tags'].append(tag)
                    self.index[mot]['n_phrase'].append(id_phrase)
                    self.index[mot]['pos_phrase'].append(pos)

                id_phrase += 1

        self.nb_formes = len(self.index)
        print(f"Nombre de mots: {self.nb_mots}")
        print(f"Nombre de phrases: {self.nb_phrases}")
        print(f"Nombre de formes: {self.nb_formes}")

        # Partie statistiques
        self.ranks_and_freqs()
        self.cooccurrences()
        self.pmi()
        self.trier_pmi()

    def ranks_and_freqs(self):

        liste_mots = []

        for mot in self.index:
            
            nb = self.index[mot]['nb']
            liste_mots.append((mot, nb))

            for i in range(len(liste_mots)):
                for j in range(i+1, len(liste_mots)):
                    if liste_mots[i][1] < liste_mots[j][1]:
                        liste_mots[i], liste_mots[j] = liste_mots[j], liste_mots[i]

            rang = 0
            dernier_nb = None

            for i, (mot, nb) in enumerate(liste_mots, start=1):
                if nb != dernier_nb:
                    rang = i
                    dernier_nb = nb

                self.index[mot]['rang'] = rang
                self.index[mot]['freq'] = round(nb / self.nb_mots * 100, 4)

    def cooccurrences(self):
        # calculer les cooccurrences pour chaque paire de mots adjacents dans le corpus

        for i in range(self.nb_mots - 1):
        
            token1 = self.tokens[i]
            token2 = self.tokens[i+1]

            mot1, tag1 = token1.split('/')
            mot2, tag2 = token2.split('/')

            if tag1 != 'NPP':
                mot1 = mot1.lower()
            if tag2 != 'NPP':
                mot2 = mot2.lower()

            if mot1 not in self.coocc:
                self.coocc[mot1] = {}
            if mot2 not in self.coocc[mot1]:
                self.coocc[mot1][mot2] = {'nb': 0, 'pmi': 0.0}

            self.coocc[mot1][mot2]['nb'] += 1

    def pmi(self):
        # calculer le PMI pour chaque paire de mots dans les cooccurrences

        for mot1 in self.coocc:
        
            for mot2 in self.coocc[mot1]:
            
                nb_pair = self.coocc[mot1][mot2]['nb']
                nb_1 = self.index[mot1]['nb']
                nb_2 = self.index[mot2]['nb']

                # PMI = log2( C(w1,w2) * N / (C(w1)*C(w2)) )
                pmi = math.log2(nb_pair * self.nb_mots / (nb_1 * nb_2))

                self.coocc[mot1][mot2] = (nb_pair, pmi)

    def trier_pmi(self):
        # pour chaque mot, trier les cooccurrences par PMI décroissant et stocker dans l'index

        for mot1, dico in self.coocc.items():
            if mot1 not in self.index:
                continue
            
            liste = []

            for mot2 in self.coocc[mot1]:
                nb, pmi = self.coocc[mot1][mot2]
                liste.append((mot2, nb, pmi))

            # trier la liste par PMI décroissant
            for i in range(len(liste)):
                for j in range(i+1, len(liste)):
                    if liste[i][2] < liste[j][2]:
                        liste[i], liste[j] = liste[j], liste[i]

            # stocker les cooccurrences triées dans l'index
            self.index[mot1]['coocc'] = {}

            for mot2, nb, pmi in liste:
                self.index[mot1]['coocc'][mot2] = {'nb': nb, 'pmi': pmi}


    def plot_zipf(self):
        """画出 Zipf 图（频率-等级双对数图）"""
        rangs = []
        frequences = []

        for mot in self.index:
            rangs.append(self.index[mot]['rang'])
            frequences.append(self.index[mot]['freq'])

        plt.figure()
        plt.title("Loi de Zipf")
        plt.xlabel("log(rang)")
        plt.ylabel("log(fréquence)")
        plt.loglog(rangs, frequences, 'o', markersize=2)
        plt.show()

if __name__ == "__main__":
    stats = CorpusStats()
    stats.read_corpus("/Users/ajd.ifbeau/Desktop/L3projetTAL/L3projetTAL/corpus/small.brown")
    stats.plot_zipf()