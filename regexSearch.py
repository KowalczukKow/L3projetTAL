import re
from kwic import afficher_kwic
from parser import parser_token

def requete_regex(corpus):
        
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

        results = kwic_regex(corpus, pattern, type = type, size = size, case_sensitive = case_sensitive)
        if results:
            afficher_kwic(results, size = size)
        else:
            print("Aucune occurrence trouvée.")

    else:
        case_choix = input("Respecter la casse ? (oui/non, défaut non) : ").strip().lower()
        case_sensitive = (case_choix == 'oui')

        regex = re.compile(pattern)
        results = []

        for id_ligne, ligne in enumerate(corpus.sentences, start=1):
            for pos, token in enumerate(ligne, start=1):
                mot, tag, token_new = parser_token(token)
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
                        'ligne_id': id_ligne,
                        'pos': pos
                    })
        if results:
            print(f"\n{len(results)} occurrence(s) trouvée(s) :")
            for res in results[:20]:
                print(f"Ligne {res['ligne_id']}, position {res['pos']} : {res['mot']}/{res['tag']}")
            if len(results) > 20:
                print(f"... et {len(results)-20} autres.")
        else:
            print("Aucune occurrence trouvée.")



def kwic_regex(corpus, pattern, type = 'mot', size = 5, case_sensitive = False):

    regex = re.compile(pattern)
    results = []

    for id_ligne, ligne in enumerate(corpus.sentences, start=1):
        for pos, token in enumerate(ligne, start=1):
            mot, tag, token_new = parser_token(token)
            if type == 'tag':
                cible = tag
            else:
                if tag != 'NPP' and not case_sensitive:
                    cible = mot.lower()
                else:
                    cible = mot

            if regex.search(cible):
                  
                gauche_ind = max(0, pos - 1 - size) 
                droite_ind = min(len(ligne), pos + size) 
                results.append({
                    'id_ligne': id_ligne,
                    'pos': pos,
                    'gauche': ligne[gauche_ind:pos-1],
                    'mot_enquete': token,
                    'droite': ligne[pos:droite_ind]
                })

    return results



if __name__ == "__main__":
    import main
    main.main()