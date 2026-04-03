import math
import re
from reconaissance import expr
import matplotlib.pyplot as plt

class CorpusStats:
    def __init__(self, corpus_path):
        self.corpus = corpus_path
        self.index = {}
        self.coocc = {} #collocations prinicipales
        self.tokens = []
        self.nb_mots = 0
        self.nb_phrases = 0
        self.nb_formes = 0
        self.sentences = [] # pour le KWIC

    def read_corpus(self, automate=None, test=False):
        nb_valides = 0

        with open(self.corpus, 'r', encoding='utf-8') as f:
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

                    if automate and automate.fullmatch(token) :
                        nb_valides += 1

                    # séparer le mot et son tag
                    mot, tag = token.rsplit('/',1)
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
        if test == True and automate: 
            print("Nom du fichier : ", self.corpus)
            print("---TEST---")
            print("Nombre de mots recconus :", nb_valides)
            print("Pourcentage de mots reconnus : ", nb_valides/self.nb_mots * 100, "%")
            print("----------")

        print(f"Nombre de mots: {self.nb_mots}")
        print(f"Nombre de phrases: {self.nb_phrases}")
        print(f"Nombre de formes: {self.nb_formes}")

        # Partie statistiques
        self.ranks_and_freqs()
        self.cooccurrences()
        self.pmi()
        self.trier_pmi()
        self.requete_mot()

    def ranks_and_freqs(self):

        liste_mots = []

        for mot in self.index:
            
            nb = self.index[mot]['nb']
            liste_mots.append((mot, nb))

        liste_mots.sort(key=lambda x: x[1], reverse=True)

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
        for sentence in self.sentences:
            for i in range(len(sentence) - 1):
                token1 = sentence[i]
                token2 = sentence[i+1]

                mot1, tag1 = token1.rsplit('/', 1)
                mot2, tag2 = token2.rsplit('/', 1)

                # je lai mis en commentaire parce que peut-être cest utile de savoir si le
                # mot est à la fin / début de la phrase
                # if tag1 == 'PONCT' or tag2 == 'PONCT':
                #     continue

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

                self.coocc[mot1][mot2]['pmi'] = pmi

    def trier_pmi(self):
        # pour chaque mot, trier les cooccurrences par PMI décroissant et stocker dans l'index

        for mot1, dico in self.coocc.items():
            if mot1 not in self.index:
                continue
            
            liste = []

            for mot2 in self.coocc[mot1]:
                nb, pmi = self.coocc[mot1][mot2]['nb'], self.coocc[mot1][mot2]['pmi']
                liste.append((mot2, nb, pmi))

            # trier la liste par PMI décroissant
            liste.sort(key=lambda x: x[2], reverse=True)

            # stocker les cooccurrences triées dans l'index
            self.index[mot1]['coocc'] = {}

            for mot2, nb, pmi in liste:
                self.index[mot1]['coocc'][mot2] = {'nb': nb, 'pmi': pmi}


    def plot_zipf(self):

        rangs = []
        frequences = []

        for mot in self.index:
            rangs.append(self.index[mot]['rang'])
            frequences.append(self.index[mot]['freq'])

        plt.figure()
        plt.title("Loi de Zipf")
        plt.xlabel("log(rang)")
        plt.ylabel("log(fréquence)")
        plt.loglog(rangs, frequences, 'o', markersize=3)
        plt.show()

    def requete_mot(self):
        while True:
            mot = input("Entrez un mot (ou 'exit' pour quitter) : ")

            if mot.lower() == 'exit':
                break

            if mot in self.index:
                cible = mot
            else:
                mot_minus = mot.lower()
                if mot_minus in self.index:
                    cible = mot_minus
                else:
                    print(f"Le mot '{mot}' n'est pas trouvé dans le corpus.")
                    rep = input("Voulez-vous essayer un autre mot (oui/non) : ")
                    if rep.lower() != 'oui':
                        print("Fin de la requête.")
                        break
                    continue

            infos = self.index[cible]

            print(f"Mot: {cible}")
            print(f"Nombre d'occurrences: {infos['nb']}")
            print(f"Rang: {infos['rang']}")
            print(f"Fréquence: {infos['freq']}%")

            if 'coocc' in infos and infos['coocc']:
                print("Principales collocations (mot suivant : nb, PMI) :")
                N = 5  # afficher les 5 meilleures collocations
                for mot2, co in list(infos['coocc'].items())[:N]:
                    print(f"{mot2} : {co['nb']}, {round(co['pmi'], 5)}")
            else:
                print("Pas de collocations disponibles.")

            reponse = input("\nVoulez-vous analyser un autre mot ? (oui/non) : ").strip().lower()
            if reponse != 'oui':
                print("Fin de la consultation.")
                break

if __name__ == "__main__":
    import main
    main.main()
    # stats = CorpusStats()
    # stats.read_corpus("/Users/ajd.ifbeau/Desktop/L3projetTAL/L3projetTAL/corpus/small.brown")
    # stats.plot_zipf()
    # stats.requete_mot()