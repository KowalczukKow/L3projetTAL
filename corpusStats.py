import math
import re
from reconaissance import expr
from ngrammes import Ngramme
import matplotlib.pyplot as plt

class CorpusStats:
    def __init__(self, corpus_path):
        self.corpus = corpus_path
        self.index = {}
        self.coocc_gauche = {} #collocations à gauche
        self.coocc_droite = {} #collocations à droite
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

                    if automate :
                        if automate.fullmatch(token) :
                            nb_valides += 1
                        elif test == True:
                            print(token)

                    # séparer le mot et son tag
                    mot, tag = self.parser_token(token)
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

        # Partie statistiques
        self.ranks_and_freqs()
        self.cooccurrences()
        self.pmi()
        self.trier_pmi()

    def info_generale(self, automate=None, test=False):
        if test == True and automate: 
            print("Nom du fichier : ", self.corpus)
            print("---TEST---")
            print("Nombre de mots recconus :", nb_valides)
            print("Pourcentage de mots reconnus : ", nb_valides/self.nb_mots * 100, "%")
            print("----------")

        print(f"Nombre de mots: {self.nb_mots}")
        print(f"Nombre de phrases: {self.nb_phrases}")
        print(f"Nombre de formes: {self.nb_formes}")


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

                mot1, tag1 = self.parser_token(token1)
                mot2, tag2 = self.parser_token(token2)

                # je lai mis en commentaire parce que peut-être cest utile de savoir si le
                # mot est à la fin / début de la phrase
                # if tag1 == 'PONCT' or tag2 == 'PONCT':
                #     continue

                if tag1 != 'NPP':
                    mot1 = mot1.lower()
                if tag2 != 'NPP':
                    mot2 = mot2.lower()

                if mot1 not in self.coocc_droite:
                    self.coocc_droite[mot1] = {}
                if mot2 not in self.coocc_droite[mot1]:
                    self.coocc_droite[mot1][mot2] = {'nb': 0, 'pmi': 0.0}

                self.coocc_droite[mot1][mot2]['nb'] += 1

                if mot2 not in self.coocc_gauche:
                        self.coocc_gauche[mot2] = {}
                    if mot1 not in self.coocc_gauche[mot2]:
                        self.coocc_gauche[mot2][mot1] = {'nb': 0, 'pmi': 0.0}

                    self.coocc_gauche[mot2][mot1]['nb'] += 1


    def pmi(self):
        # calculer le PMI pour chaque paire de mots dans les cooccurrences

        for mot1 in self.coocc_droite:
        
            for mot2 in self.coocc_droite[mot1]:
            
                nb_pair = self.coocc_droite[mot1][mot2]['nb']
                nb_1 = self.index[mot1]['nb']
                nb_2 = self.index[mot2]['nb']

                pmi = math.log2(nb_pair * self.nb_mots / (nb_1 * nb_2))

                self.coocc_droite[mot1][mot2]['pmi'] = pmi

        for mot2 in self.coocc_gauche:
            for mot1 in self.coocc_gauche[mot2]:
                nb_pair = self.coocc_gauche[mot2][mot1]['nb']
                nb_1 = self.index[mot1]['nb']
                nb_2 = self.index[mot2]['nb']

                # PMI = log2( C(w1,w2) * N / (C(w1)*C(w2)) )
                pmi = math.log2(nb_pair * self.nb_mots /(nb_1 * nb_2))

                self.coocc_gauche[mot2][mot1]['pmi'] = pmi
    


    def trier_pmi(self):
        # pour chaque mot, trier les cooccurrences par PMI décroissant et stocker dans l'index

        for mot1, dico in self.coocc_droite.items():
            if mot1 not in self.index:
                continue
            
            liste_droite = []

            for mot2 in self.coocc_droite[mot1]:
                nb, pmi = self.coocc_droite[mot1][mot2]['nb'], self.coocc_droite[mot1][mot2]['pmi']
                liste_droite.append((mot2, nb, pmi))

            # trier la liste par PMI décroissant
            liste_droite.sort(key=lambda x: x[2], reverse=True)

            # stocker les cooccurrences triées dans l'index
            self.index[mot1]['coocc_droite'] = {}

            for mot2, nb, pmi in liste_droite:
                self.index[mot1]['coocc_droite'][mot2] = {'nb': nb, 'pmi': pmi}
        

        for mot2, dico in self.coocc_gauche.items():

            liste_gauche = []

            for mot1 in dico:
                nb = dico[mot1]['nb']
                pmi = dico[mot1]['pmi']
                liste_gauche.append((mot1, nb, pmi))

            liste_gauche.sort(key=lambda x: x[2], reverse=True)

            if mot2 not in self.index:
                continue

            self.index[mot2]['coocc_gauche'] = {}

            for mot1, nb, pmi in liste_gauche:
                self.index[mot2]['coocc_gauche'][mot1] = {'nb': nb, 'pmi': pmi}


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
            mot = input("Entrez un mot (ou appuyer sur ENTREE pour quitter) : ")

            if not mot :
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

            if 'coocc_gauche' in infos and infos['coocc_gauche']:
                print("\nPrincipales collocations à gauche (mot précédent : nb, PMI) :")

                for mot2, co in list(infos['coocc_gauche'].items())[:5]:
                    print(f"{mot2} : {co['nb']}, {round(co['pmi'], 5)}")

            if 'coocc_droite' in infos and infos['coocc_droite']:
                print("Principales collocations à droite (mot suivant : nb, PMI) :")
                # afficher les 5 meilleures collocations
                for mot2, co in list(infos['coocc_droite'].items())[:5]:
                    print(f"{mot2} : {co['nb']}, {round(co['pmi'], 5)}")
            else:
                print("Pas de collocations disponibles.")


            kwic_choix = input("\nVoulez-vous afficher le contexte (KWIC) ? (oui/non) : ").strip().lower()

            if kwic_choix == 'oui':
                size = int(input("Entrez le nombre de mots à gauche et à droite que vous souhaitez afficher, par défaut 5) : ") or 5)

                kwic_results = self.kwic_words(cible, size = size, case_sensitive=False)

                if kwic_results:
                    self.afficher_kwic(kwic_results, size = size)
                else:
                    print("Aucun contexte trouvé.")

            reponse = input("\nVoulez-vous analyser un autre mot ? (oui/non) : ").strip().lower()
            if reponse != 'oui':
                print("Fin de la consultation.")
                break

    # KWIC

    def kwic_words(self, word, size = 5, case_sensitive = False):

        if case_sensitive:
            query = word 
        else: 
            query = word
            if word in self.index:
                tags = self.index[word]['tags']
                if 'NPP' in tags:
                    query = word  # garder la casse pour les noms propres
                else:
                    query = word.lower()  # mettre en minuscules pour les autres mots

        if query not in self.index:
            print(f"Le mot '{word}' n'est pas trouvé dans le corpus.")
            return []
        
        infos = self.index[query]
        results = []

        for id_phrase, pos in zip(infos['n_phrase'], infos['pos_phrase']):
            sentence = self.sentences[id_phrase - 1]  # id_phrase commence à 1
            gauche_ind = max(0, pos - size - 1)  # pos commence à 1
            pos_enquete = pos - 1  # position du mot dans la phrase (0-indexé)
            droite_ind = min(len(sentence), pos + size)  # pos + size est exclusif
            results.append({
                'id_phrase' : id_phrase,
                'pos' : pos,
                'gauche' : sentence[gauche_ind:pos_enquete],
                'mot_enquete' : sentence[pos_enquete],
                'droite' : sentence[pos_enquete + 1:droite_ind]
            })
        return results

    def afficher_kwic(self, kwic_results, size = 5, show_tag=True):
        for res in kwic_results:
            gauche_str = ' '.join(res['gauche'])
            enquete_str = res['mot_enquete']
            droite_str = ' '.join(res['droite'])
            # aligner à gauche et à droite avec une largeur fixe pour que les mots enquêtés soient alignés verticalement
            gauche_part = gauche_str.rjust(30) # 30 caractères pour la partie gauche
            droite_part = droite_str.ljust(30) # 30 caractères pour la partie droite
            print(gauche_part + "  [" + enquete_str + "]  " + droite_part)


    def requete_regex(self):
        import re
        pattern = input("Entrez l'expression régulière : ").strip()

        if not pattern:
            print("Expression invalide, retour au menu.")
            return

        type = input("Recherche sur le mot ou sur son étiquette grammaticale ? (mot/tag, defaut mot) ").strip().lower()
        while type not in ('mot', 'tag'):
            type = input("Veuillez répondre 'mot' ou 'tag' : ").strip().lower()

        kwic_choix = input("Afficher le contexte (KWIC) ? (oui/non, défaut non) : ").strip().lower()
        kwic = (kwic_choix == 'oui')

        if kwic:
            size = int(input("Entrez le nombre de mots à gauche et à droite que vous souhaitez afficher, par défaut 5) : ") or 5)
            case_choix = input("Respecter la casse ? (oui/non, défaut non) : ").strip().lower()
            case_sensitive = (case_choix == 'oui')

            results = self.kwic_regex(pattern, type = type, size = size, case_sensitive = case_sensitive)
            if results:
                self.afficher_kwic(results, size = size)
            else:
                print("Aucune occurrence trouvée.")

        else:
            case_choix = input("Respecter la casse ? (oui/non, défaut non) : ").strip().lower()
            case_sensitive = (case_choix == 'oui')

            regex = re.compile(pattern)
            results = []

            for id_phrase, phrase in enumerate(self.sentences, start=1):
                for pos, token in enumerate(phrase, start=1):
                    mot, tag = self.parser_token(token)
                    if type == 'tag':
                        cible = tag
                    else:
                        if tag != 'NPP' and not case_sensitive:
                            cible = mot.lower()
                        else:
                            cible = mot

                    if regex.search(cible):
                        results.append({
                            'mot': mot,
                            'tag': tag,
                            'phrase_id': id_phrase,
                            'pos': pos
                        })
            if results:
                print(f"\n{len(results)} occurrence(s) trouvée(s) :")
                for res in results[:20]:
                    print(f"Phrase {res['phrase_id']}, position {res['pos']} : {res['mot']}/{res['tag']}")
                if len(results) > 20:
                    print(f"... et {len(results)-20} autres.")
            else:
                print("Aucune occurrence trouvée.")



    def kwic_regex(self, pattern, type = 'mot', size = 5, case_sensitive = False):

        regex = re.compile(pattern)
        results = []

        for id_phrase, phrase in enumerate(self.sentences, start=1):
            for pos, token in enumerate(phrase, start=1):
                mot, tag = self.parser_token(token)
                if type == 'tag':
                    cible = tag
                else:
                    if tag != 'NPP' and not case_sensitive:
                        cible = mot.lower()
                    else:
                        cible = mot

                if regex.search(cible):
                  
                    gauche_ind = max(0, pos - 1 - size) 
                    droite_ind = min(len(phrase), pos + size) 
                    results.append({
                        'id_phrase': id_phrase,
                        'pos': pos,
                        'gauche': phrase[gauche_ind:pos-1],
                        'mot_enquete': token,
                        'droite': phrase[pos:droite_ind]
                    })

        return results
    
    # N-GRAMMES
    def requete_n_gramme(self) :
        sequence = input("Entrez la suite de mots : ")
        
        ngramme = Ngramme(self, sequence)
        if ngramme.nbOcc == 0:
            print(f"La suite '{sequence}' n'est pas trouvée dans le corpus.")
            return

        print(f"Suite recherchée: ", sequence)
        print(f"Nombre d'occurrences: ", ngramme.nbOcc)
        print(f"Fréquence: ", ngramme.freq, "%")
        print("Principales collocations (mot suivant : nb, PMI) :")

    
        # On peut choisir d'afficher aussi les collocations à gauche.
        if ngramme.coocc[0]:
            print("Principales collocations à gauche (mot précédent : nb) :")
            for mot in list(ngramme.coocc[0].keys())[:5]:
                print(mot, ":", ngramme.coocc[0][mot]['nb'])
        else:
            print("\nPas de collocations à gauche disponibles.")

        for mot in ngramme.coocc[1].keys():
            print(mot, " : ", ngramme.coocc[1][mot]['nb'], ", ", round(ngramme.coocc[1][mot]['pmi'],5))
        
        else:
            print("\nPas de collocations à droite disponibles.")

        kwic_choix = input("\nVoulez-vous afficher le contexte (KWIC) ? (oui/non) : ").strip().lower()

        if kwic_choix == 'oui':
            size = int(input("Entrez le nombre de mots à gauche et à droite que vous souhaitez afficher, par défaut 3) : ") or 3)

            kwic_results = ngramme.kwic_suites(size)

            if kwic_results:
                ngramme.afficher_kwic_suite(kwic_results)
            else:
                print("Aucun contexte trouvé.")

    """
    Pour rendre votre concordancier relativement indépendant du format du corpus, il faut découpler 
    la logique de parsing des tokens (la façon dont on extrait le mot et son tag) du reste du code. 
    Actuellement, votre corpus utilise le format mot/tag (par exemple chat/N). Mais si vous changez 
    de format (mot_tag, mot:tag, ou même du texte sans tag), vous ne voulez pas réécrire toutes vos
    fonctions.
    """

    def parser_token(self, token):
        # Cette fonction prend un token brut et retourne le mot et son tag
        # Par défaut, elle suppose le format mot/tag
        if '/' in token:
            mot, tag = token.rsplit('/', 1)
        else:
            mot, tag = token, None  # si pas de tag, on retourne None
        return mot, tag


if __name__ == "__main__":
    import main
    main.main()

    
    
