from parser import parser_token

class CorpusStats:
    def __init__(self, corpus_path):
        self.corpus = corpus_path
        self.test = False
        self.nb_valides = 0
        self.liste_invalides = []
        self.index = {}
        self.index_tags = {} # pour les statistiques sur les tags
        self.coocc_gauche = {} #collocations à gauche
        self.coocc_droite = {} #collocations à droite
        self.tokens = []
        self.nb_mots = 0
        self.nb_phrases = 0
        self.nb_formes = 0
        self.sentences = [] # pour le KWIC
        self.id_debut_sentences = []


    def read_corpus(self, automate=None, test=False):

        self.test = test

        with open(self.corpus, 'r', encoding='utf-8') as f:
            id_phrase = 1 # numéroter les phrases à partir de 1
            for line in f:
                line = line.strip()
                if not line:
                    continue

                if self.nb_phrases != 0 :
                    self.id_debut_sentences.append(len(self.sentences[-1]) + self.id_debut_sentences[-1])
                else :
                    self.id_debut_sentences.append(0)

                words = line.split()   # les mots sont sous la forme "mot/tag"
                self.sentences.append(words)   # stocke la phrase originale pour le KWIC
                self.nb_phrases += 1

                # parcourir tous les mots de la phrase
                for pos, token in enumerate(words, start=1):   # pos à partir de 1
                    self.tokens.append(parser_token(token))
                    self.nb_mots += 1

                    if automate :
                        if automate.fullmatch(token) :
                            self.nb_valides += 1
                        elif test == True:
                            self.liste_invalides.append(token)

                    # séparer le mot et son tag
                    mot, tag, token_new = parser_token(token)
                    # rendre le mot en minuscules s'il n'est pas un nom propre
                    if tag != 'NPP':
                        mot = mot.lower()

                    # si le mot n'est pas encore dans l'index, l'ajouter
                    if mot not in self.index:
                        self.index[mot] = {
                            'nb_occ': 0, # le nombre d'occurrences
                            'tags': [],         # les tags associés
                            'n_phrase': [],     # les numéros de phrase où il apparaît
                            'pos_phrase': []    # les positions dans la phrase où il apparaît
                        }
                    # renouveler les informations pour ce mot
                    self.index[mot]['nb_occ'] += 1
                    self.index[mot]['tags'].append(tag)
                    self.index[mot]['n_phrase'].append(id_phrase)
                    self.index[mot]['pos_phrase'].append(pos)

                id_phrase += 1

        self.nb_formes = len(self.index)

if __name__ == "__main__":
    import main
    main.main()

    
    
