import re

index = {} # nous permet de stocker des informations sur les mots
nb_phrases = 0
nb_mots = 0
nb_formes = 0

def set_index(x) :
    global index
    index = x

def set_nb_phrases(x):
    global nb_phrases
    nb_phrases = x

def set_nb_mots(x):
    global nb_mots
    nb_mots = x

def affiche_index():
    for motIndex in index :
        print(motIndex,' : ', index[motIndex])

def createur_index(valides) :
    set_nb_mots(len(valides))
    n_phrase = 1
    print(nb_mots)
    for m in valides :
        mot, tag = m.split('/') #pour séparer le mot de sa classe grammaticale

        if(tag!='NPP') : mot = mot.lower() # S'il s'agit pas d'un nom propre, 
                                        # le mot sera en minuscules   
        if mot not in index:
            index[mot] = {
                'tags' : [],
                'nb' : 0,
                'n_phrase' : []
            }

        index[mot]['tags'].append(tag)
        index[mot]['nb'] +=1
        index[mot]['n_phrase'].append(n_phrase)

        if tag== 'PONCT' and mot in['.','!','?'] : 
            n_phrase+=1

    nb_phrases = n_phrase
    affiche_index()
    print("Nombre de phrases", nb_phrases)
    nb_formes = len(index)
    print("Nombre de formes (ponct inclus) : ", nb_formes)
    
def update_index() :
    index_trie = sorted(index.items(), key=lambda item: item[1]['nb'], reverse = True)
        # attention !!! index_triee est un liste est pas un dictionnaire

    new_index = {}

    rang_actuel = 0 # s'il y a quelques mots avec le même nb d'occurences
    nb_actuel = 0 #nombre d'occurences d'un mot
    #for i in index_trie : print(i)
    for i, (mot, infos) in enumerate(index_trie) :
        rang = i+1 
        nb_occ = infos['nb']
        freq = nb_occ/nb_mots * 100

        if(nb_actuel > nb_occ or nb_actuel == 0) :
            nb_actuel = nb_occ
            rang_actuel = rang

        new_index[mot] = {
            'tags' : infos['tags'],
            'nb' : nb_occ,
            'n_phrase' : infos['n_phrase'],
            'rang' : rang_actuel,
            'freq' : round(freq, 4)
        }
    
    set_index(new_index)