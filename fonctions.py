import re
import matplotlib.pyplot as plt
import numpy as np

index = {} # nous permet de stocker des informations sur les mots
coocc = {}
nb_phrases = 0
nb_mots = 0
nb_formes = 0
valides = []

def set_index(x) :
    global index
    index = x

def set_nb_phrases(x):
    global nb_phrases
    nb_phrases = x

def set_nb_mots(x):
    global nb_mots
    nb_mots = x

def set_valides(liste) :
    global valides 
    valides = liste

def affiche_index():
    for motIndex in index :
        print(motIndex,' : ', index[motIndex])

def createur_index(valid) :
    set_valides(valid)
    set_nb_mots(len(valid))
    n_phrase = 1
    pos_phrase = 1 # position dans la phrase, on inclut les ponct 
    print(nb_mots)
    for m in valides :
        mot, tag = m.split('/') #pour séparer le mot de sa classe grammaticale

        if(tag!='NPP') : mot = mot.lower() # S'il s'agit pas d'un nom propre, 
                                        # le mot sera en minuscules   
        if mot not in index:
            index[mot] = {
                'tags' : [],
                'nb' : 0,
                'n_phrase' : [],
                'pos_phrase' : []
            }

        index[mot]['tags'].append(tag)
        index[mot]['nb'] +=1
        index[mot]['n_phrase'].append(n_phrase)
        index[mot]['pos_phrase'].append(pos_phrase)

        pos_phrase +=1

        if tag== 'PONCT' and mot in['.','!','?'] : 
            n_phrase+=1
            pos_phrase = 1

    nb_phrases = n_phrase
    #affiche_index()
    print("Nombre de phrases", nb_phrases)
    nb_formes = len(index)
    print("Nombre de formes (ponct inclus) : ", nb_formes)
    
def update_index() :
    index_trie = sorted(index.items(), key=lambda item: item[1]['nb'], reverse = True)
        # attention !!! index_triee est un liste est pas un dictionnaire

    new_index = {}

    rang_actuel = 0 # s'il y a quelques mots avec le même nb d'occurences
    nb_actuel = 0 #nombre d'occurences d'un mot

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
            'pos_phrase' : infos['pos_phrase'],
            'rang' : rang_actuel,
            'freq' : round(freq, 4)
        }
    
    set_index(new_index)
    cooccurence()

def loi_zipf_graphe() :

    frequences = []
    rangs = []

    for mot in index :
        frequences.append(index[mot]['freq'])
        rangs.append(index[mot]['rang'])

    plt.figure()
    plt.title("Loi de Zipf")
    plt.xlabel("log(rang)")
    plt.ylabel("log(freq)")
    plt.loglog(rangs, frequences) # à l'échelle logarithmique
    plt.show()

def cooccurence() :
    for pos in range(nb_mots-1) :
        mot1, tag1 = valides[pos].split('/') #pour séparer le mot de sa classe grammaticale
        mot2, tag2 = valides[pos+1].split('/')

        if(tag1!='NPP') : mot1 = mot1.lower() # S'il s'agit pas d'un nom propre, 
                                        # le mot sera en minuscules 
        if(tag2!='NPP') : mot2 = mot2.lower() 
        
        if mot1 not in coocc :
            coocc[mot1] = {}
        if mot2 not in coocc[mot1] :
            coocc[mot1][mot2] = 1 # nb d'occurences de mot1 mot2 
        else :
            coocc[mot1][mot2]+=1

        affiche_coocc()

def affiche_coocc() :
    for mot1 in coocc :
        for mot2 in coocc[mot1] :
            print(mot1 + ", " + mot2 + ":",coocc[mot1][mot2])