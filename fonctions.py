import re

index = {} # nous permet de stocker des informations sur les mots 

def affiche_index():
    for motIndex in index :
        print(motIndex,' : ', index[motIndex])

def createur_index(valides) :
    n_phrase = 1
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
    print("Nombre de formes (ponct inclus) : ", len(index))
    
