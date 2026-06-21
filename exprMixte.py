import math
import re
from reconnaissance import tag_expr

class exprMixte:
    def __init__(self, corpus):
        self.corpus = corpus
        self.formes = {}
        self.sequence = ''
        self.demande = []
        self.coocc = []
        self.nb_occ = 0
        self.nb_motags = 0
        self.indices = []
        self.nb_total_corpus = 0
        self.mode = 0
        self.freq = 0
        

    def initialise_expr_mixte(self):
        regex = re.compile(tag_expr)
        self.sequence = input("\nEntrez la suite : ")
        pattern = self.sequence.strip().split()

        for motag in pattern :

            if regex.fullmatch(motag) :
                self.demande.append((motag, 1)) # 1 s'il s'agit d'un tag
            else :
                self.demande.append((motag.lower(), 0))

        self.nb_motags = len(self.demande)

        # éviter de produire un message d'erreur quand aucune saisie détectée
        if self.nb_motags == 0:
            print("Aucune suite saisie")
            return

        motag1, type = self.demande[0]

        for i in range(len(self.corpus.tokens) - self.nb_motags + 1) :
            valid = True
            if self.corpus.tokens[i][type] == motag1 :
                for j in range(1, self.nb_motags) : 
                    if self.corpus.tokens[i+j][self.demande[j][1]] != self.demande[j][0] :
                        valid = False
                        break
                if valid :
                    self.sauvegarde_forme(i)
                    self.indices.append(i)

        self.nb_occ = len(self.indices)
        
        if self.nb_occ == 0 :
            print("La suite n'est pas présente dans le corpus")
            return
        
        self.nb_total_corpus = self.corpus.nb_mots - self.nb_occ * (self.nb_motags-1)

        self.calc_freq()
        self.affiche_infos_deb()
        self.mode = self.demande_mode()
        self.cooccurences()
        self.affiche_infos_fin()
        


    def sauvegarde_forme(self, indice):
        form = ""
        indice_max = indice + self.nb_motags

        for i in range(indice, indice_max):
            form += self.corpus.tokens[i][2]
            if i < indice_max - 1 :
                form += " "

        if form.casefold() not in self.formes:
            self.formes[form.casefold()] = {
                'forme' : form,
                'nb' : 0
            } 

        self.formes[form.casefold()]['nb']+=1

    def calc_freq(self) :
        if self.nb_total_corpus > 0 :
            self.freq = round(self.nb_occ/self.nb_total_corpus * 100, 4)
        else : 
            self.freq = 0.0
        

    # mode = 0 pour les mots, mode = 1 pour les tags, mode = 2 pour mot/tag    
    def cooccurences(self) :
        self.coocc.append({}) # à gauche
        self.coocc.append({}) # à droite

        tokens = self.corpus.tokens

        max_id_tokens = len(tokens) - 1

        for id in self.indices : 
            if id != 0 :

                motag = tokens[id-1][self.mode]

                if motag not in self.coocc[0] :
                    self.coocc[0][motag] = {'nb': 0, 'pmi' : 0}

                self.coocc[0][motag]['nb'] += 1
            
            if id + self.nb_motags - 1 != max_id_tokens :

                motag = tokens[id + self.nb_motags][self.mode]

                if motag not in self.coocc[1] :
                    self.coocc[1][motag] = {'nb': 0, 'pmi' : 0}

                self.coocc[1][motag]['nb'] += 1
        
        if self.mode != 2 :
            self.calc_pmi()


    def calc_pmi(self) :
        index = self.corpus.index
        if self.mode == 1 :
            index = self.corpus.index_tags

        for i in range (2) :
            for motag in self.coocc[i] :
                nb_pair = self.coocc[i][motag]['nb']

                if motag not in index :
                    print(f"Le mot '{motag}' n'est pas trouvé dans le self.corpus.")
                    continue
                
                nb_occ_motag = index[motag]['nb_occ'] - self.nb_occ * self.verif_motag_pres(motag)

                if self.nb_occ == 0 or nb_occ_motag <= 0 :
                        continue
                
                pmi = math.log2(nb_pair * self.nb_total_corpus / (self.nb_occ * nb_occ_motag))
                self.coocc[i][motag]['pmi'] = pmi

        self.sort_pmi()


    def sort_pmi(self) :

        for i in range(2) :
            liste = []
            for motag in self.coocc[i]:
                nb, pmi = self.coocc[i][motag]['nb'], self.coocc[i][motag]['pmi']
                liste.append((motag, nb, pmi))

            # trier la liste par PMI décroissant
            liste.sort(key=lambda x: x[2], reverse=True)

            # stocker les cooccurrences triées dans l'index
            self.coocc[i] = {}

            for motag, nb, pmi in liste:
                self.coocc[i][motag] = {'nb': nb, 'pmi': pmi}
        


    def kwic(self, size=5) :
        results = [] 

        tokens = self.corpus.tokens

        for i in self.indices : 
            pos1 = i 
            pos2 = i + self.nb_motags - 1

            gauche_ind = max(0, pos1 - size)
            droite_ind = min(len(tokens) - 1, pos2 + size)

            results.append({
                'pos_debut' : pos1,
                'pos_fin' : pos2,
                'gauche' : [motag[self.mode] for motag in tokens[gauche_ind:pos1]],
                'expr' : [motag[0] for motag in self.demande],
                'droite' : [motag[self.mode] for motag in tokens[pos2+1:droite_ind+1]]
            })

        return results


    def verif_motag_pres(self, motag_a_verif) :
        compteur = 0
        for motag in self.demande:
            if motag[0] == motag_a_verif :
                compteur+=1
        return compteur




    ##############################
    ### AFFICHAGE ################
    ##############################

    def affiche_infos_deb(self) :
        print(f"\nSuite recherchée : ", self.sequence)
        print(f"Nombre d'occurrences : ", self.nb_occ)
        print(f"Fréquence : {self.freq} %")
        self.demande_formes()
        
    
    def affiche_infos_fin(self) :
        self.demande_coocc()
        size_kwic = self.demande_kwic()
        if size_kwic > 0 :
            results_kwic = self.kwic(size_kwic)
            self.affiche_kwic(results_kwic)


    def affiche_formes(self):
        print(f"\nLa suite [{self.sequence}] est présente sous formes suivantes : ")
        for form in self.formes.keys() :
            print(f"Forme : {self.formes[form]['forme']}, nombre d'occurrences : {self.formes[form]['nb']}")

    def affiche_coocc(self) :
        motag_str = 'mot' 
        show_pmi = True
        if self.mode == 1 :
            motag_str = 'tag'
        elif self.mode == 2 :
            motag_str = 'mot/tag'
            show_pmi = False

        if self.coocc[0]:
                print(f"\nPrincipales collocations à gauche ({motag_str} précédent : nb"
                      f"{', PMI' if show_pmi else ''}) :")
                for motag in list(self.coocc[0].keys())[:5]:
                    print(f"{motag} : {self.coocc[0][motag]['nb']}"
                          f"{f', {round(self.coocc[0][motag]['pmi'],5)}' if show_pmi else ''}")
        else:
            print("\nPas de collocations à gauche disponibles.")

        if self.coocc[1]:
            print(f"\nPrincipales collocations à droite ({motag_str} suivant : nb"
                  f"{', PMI' if show_pmi else ''}) :")
            for motag in list(self.coocc[1].keys())[:5]:
                print(f"{motag} : {self.coocc[1][motag]['nb']}"
                      f"{f', {round(self.coocc[1][motag]['pmi'],5)}' if show_pmi else ''}")
        
        else:
            print("\nPas de collocations à droite disponibles.")


    def affiche_kwic(self, results_kwic) :
        for res in results_kwic:
            gauche_str = ' '.join(res['gauche'])
            enquete_str = ' '.join(res['expr'])
            droite_str = ' '.join(res['droite'])
            # aligner à gauche et à droite avec une largeur fixe pour que les mots enquêtés soient alignés verticalement
            gauche_part = gauche_str.rjust(30) # 30 caractères pour la partie gauche
            droite_part = droite_str.ljust(30) # 30 caractères pour la partie droite
            print(gauche_part + "  [" + enquete_str + "]  " + droite_part)


    def demande_formes(self) :
        choix = input("\nVoulez-vous afficher les formes de votre suite ? (oui/non) : ").strip()
        if choix == 'oui' :
            self.affiche_formes()
    
    def demande_coocc(self):
        choix = input("\nVoulez-vous afficher les collocations principales de votre suite ? (oui/non) : ").strip()
        if choix == 'oui' :
            self.affiche_coocc()
    
    def demande_mode(self) :
            print("\nMode d'affichage du contexte et de relations :")
            print("1. Mots uniquement")
            print("2. Tags uniquement")
            print("3. Mot/tag")
            choix = input("Votre choix : ").strip()
            if not choix :
                return 0
            elif int(choix) not in [1, 2, 3] :
                return 0
            return int(choix) - 1


    def demande_kwic(self) :
        kwic_choix = input("\nVoulez-vous afficher le contexte (KWIC) ? (oui/non) : ").strip().lower()
        if kwic_choix == 'oui':
            size = int(input("Entrez le nombre de mots à gauche et à droite que vous souhaitez afficher, par défaut 5) : ") or 5)
            return size
        return -1



if __name__ == "__main__":
    import main
    main.main()