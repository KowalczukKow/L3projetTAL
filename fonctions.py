
index = {} # nous permet de stocker des informations sur les mots 

def createur_index(valides) :

    for m in valides :
        mot, tag = m.split('/') #pour séparer le mot de sa classe grammaticale

        if(tag!='NPP') : mot = mot.lower() # S'il s'agit pas d'un nom propre, 
                                        # le mot sera en minuscules   

        if mot not in index:
            index[mot] = {
                'tags' : [],
                'nb' : 0
            }

        index[mot]['tags'].append(tag)
        index[mot]['nb'] +=1

    print(index)