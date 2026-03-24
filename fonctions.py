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


# mais en vrai, c'est quoi le but de zipf ?
    def loi_zipf_graphe() :

        frequences = []
        rangs = []

        for mot in self.index :
            frequences.append(self.index[mot]['freq'])
            rangs.append(self.index[mot]['rang'])

        plt.figure()
        plt.title("Loi de Zipf")
        plt.xlabel("log(rang)")
        plt.ylabel("log(freq)")
        plt.loglog(rangs, frequences) # à l'échelle logarithmique
        plt.show()


    # crée un dictionnaire des mots avec les mots qui les suivent et
    # le nombre d'occurences de la paire dans l'ordre donné
    def cooccurence() :
        for pos in range(self.nb_mots-1) :
            token1 = self.tokens[pos]
            token2 = self.tokens[pos+1]

            mot1, tag1 = token1.split('/') #pour séparer le mot de sa classe grammaticale
            mot2, tag2 = token2.split('/')

            if(tag1!='NPP') : mot1 = mot1.lower() # S'il s'agit pas d'un nom propre, 
                                            # le mot sera en minuscules 
            if(tag2!='NPP') : mot2 = mot2.lower() 
            
            if mot1 not in self.coocc :
                self.coocc[mot1] = {}
            if mot2 not in self.coocc[mot1] :
                self.coocc[mot1][mot2] = {
                    'nb' : 0, # nb d'occurences de mot1 mot2 
                    'pmi' : 0 # pontwise mutual information
                }
            
            self.coocc[mot1][mot2]['nb']+=1 


    # je fais la partie pmi par des fonctions séparées pour que ce soit plus clair, mais on peut aussi faire tout dans la même fonction
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
            # mais je pense la complexité ici n'est pas assez bonne que sort() ou sorted()
            liste.sort(key=lambda x: x[2], reverse=True)

            # stocker les cooccurrences triées dans l'index
            self.index[mot1]['coocc'] = {}

            for mot2, nb, pmi in liste:
                self.index[mot1]['coocc'][mot2] = {'nb': nb, 'pmi': pmi}        


    def affiche_coocc() :
        for mot1 in coocc :
            for mot2 in coocc[mot1] :
                print(mot1 + ", " + mot2 + ":",coocc[mot1][mot2]['nb'], coocc[mot1][mot2]['pmi'])


    def calcul_pmi() :
        for mot1 in coocc :
            for mot2 in coocc[mot1] :
                nb_paire = coocc[mot1][mot2]['nb']
                nb_1 = index[mot1]['nb']
                nb_2 = index[mot2]['nb']
                #print(nb_paire, nb_1, nb_2, nb_formes)
                coocc[mot1][mot2]['pmi'] = math.log2(nb_paire * nb_formes/(nb_1 * nb_2))


    
    def sort_pmi_mot() :

        new_coocc = {}

        for mot1 in coocc :
            coocc_trie = sorted(coocc[mot1].items(), key=lambda item: item[1]['pmi'], reverse = True)
            
            new_coocc[mot1] = {}

            for mot2, infos in coocc_trie :
                # on pourrait ignorer des mots s'il y a peu d'occ de la paire
                new_coocc[mot1][mot2] = {
                    'nb' : infos['nb'],
                    'pmi' : infos['pmi']
                }
            
            index[mot1]['coocc'] = new_coocc[mot1]

        set_coocc(new_coocc)



    if __name__ == "__main__" :
        main.main()
