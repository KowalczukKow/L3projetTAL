"""
Pour rendre votre concordancier relativement indépendant du format du corpus, il faut découpler 
la logique de parsing des tokens (la façon dont on extrait le mot et son tag) du reste du code. 
Actuellement, votre corpus utilise le format mot/tag (par exemple chat/N). Mais si vous changez 
de format (mot_tag, mot:tag, ou même du texte sans tag), vous ne voulez pas réécrire toutes vos
fonctions.
"""

def parser_token(token):
    # Cette fonction prend un token brut et retourne le mot et son tag
    # Par défaut, elle suppose le format mot/tag
    if '/' in token:
        mot, tag = token.rsplit('/', 1)
        mot = mot.lower()
    else:
        mot, tag = token, None  # si pas de tag, on retourne None
    return mot, tag, token
