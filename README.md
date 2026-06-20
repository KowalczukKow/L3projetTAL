# IV. Manuel utilisateur

## 4.1 Démarrage du programme

Ce programme a été développé en Python 3. La seule bibliothèque externe à installer est `matplotlib`, utilisée pour afficher le graphe de Zipf.

```bash
pip install matplotlib
```

Pour le lancer, il vous suffit d’exécuter le fichier principal à l’aide de la commande suivante:

```bash
python main.py
```

Au démarrage, le programme affiche le chemin du corpus utilisé par défaut:

```text
corpus/sequoia-9.2.fine.brown
```

L’utilisateur peut choisir de conserver ce corpus ou d’en indiquer un autre. Si l’utilisateur souhaite changer de corpus, le programme lui demande de saisir le nouveau chemin d’accès. Si aucun chemin n’est fourni, une nouvelle saisie est demandée. En cas de chemin invalide ou de fichier inexistant, un message d’erreur est affiché..

Une fois le corpus chargé correctement, le programme parcourt l’ensemble des lignes et construit un index lexical. Pour chaque mot, cet index stocke les informations suivantes:

- le nombre d'occurrences;
- les étiquettes morphosyntaxiques associées;
- les numéros de lignes dans lesquelles le mot apparaît;
- la position du mot dans chaque ligne

A partir de cet index, le programme calcule ensuite plusieurs statistiques:

- les fréquences et les rangs correspondants;
- les cooccurrences à gauche et à droite;
- les scores PMI des collocations;
- les contextes KWIC
- les statistiques par étiquette grammaticale

## 4.2 Format attendu

Le corpus doit être au format mot/étiquette. Par exemple :

```text
Pourquoi/ADVWH ce/DET thème/NC ?/PONCT (df. small.brown)
```

Les tokens doivent être séparés par des espaces. Chaque ligne du corpus représente dans ce programme une unité textuelle indépendante à traiter. Elle peut être une phrase complète, un titre, un sous-titre ou un fragment de phrase selon la segmentation du corpus d’origine.

Le programme réalise la séparation de chaque forme de son étiquette grammaticale à l’aide d’une fonction de parsing des tokens. Il est ainsi relativement adaptable à d’autres formats du corpus, à condition de modifier cette fonction de parsing si nécessaire.

## 4.3 Menu principal

Après le chargement du corpus, le menu principal apparaît:

```text
=======================================================
MENU PRINCIPAL - CONCORDANCIER
-------------------------------------------------------

1. Informations générales du corpus
   -> nombre de mots, unités textuelles et formes

2. Graphe de Zipf
   -> visualisation des fréquences des mots

3. Afficher les statistiques d'un tag
   -> fréquence, rang et formes les plus fréquentes

4. Rechercher un mot
   -> fréquence, rang, collocations et KWIC optionnel

5. Rechercher par expression régulière (mot/tag)
   -> ex : '.*tion', 'N.*'

6. Rechercher une suite structurée (suite de mots/de tags/mixte)
   -> suite de mots, de tags ou mixte
   -> ex : 'DET NC', 'NPP V', 'le NC'

0. Quitter
=======================================================
```

L’utilisateur sélectionne une option en saisissant le numéro correspondant. Après chaque recherche, le programme revient automatiquement au menu principal, jusqu’à ce que l’utilisateur choisisse l’option 0 pour quitter le programme.

### Option 1 : Informations générales du corpus

Cette fonctionnalité fournit des informations quantitative générales sur le corpus:

- le nombre total de mots;
- le nombre total de lignes;
- le nombre de formes distinctes

### Option 2 : Graphe de Zipf

Cette option génère automatiquement le graphe de Zipf du corpus.

Elle permet de vérifier visuellement si la distribution des fréquences des mots en fonction de leur rang suit approximativement la loi  de Zipf, généralement observée dans les langues naturelles.

### Option 3 : Statistiques d’un tag

L’option 3 permet d’afficher les statistiques associées à une étiquette grammaticale spécifique, par exemple NC, V, ADJ, ADV, NPP ou PONCT.

Les informations affichées sont les suivantes :

- Nombre d’occurrences : nombre total de mots portant ce tag dans le corpus ;
- Nombre de formes distinctes : nombre de mots différents associés à ce tag ;
- Fréquence dans le corpus : proportion de ce tag par rapport à l’ensemble des mots du corpus ;
- Formes les 10 plus fréquentes : liste des dix mots les plus fréquents possédant ce tag, avec leur nombre d’occurrences, leur fréquence interne au tag et leur rang.

Si le tag saisi n’existe pas dans le corpus, le programme affiche un message d’erreur :

```text
Le tag '...' n'est pas trouvé dans le corpus.
```

Cette option offre ainsi une vue d’ensemble des formes lexicales associées à une catégorie grammaticale donnée.

### Option 4 : Recherche d’un mot

Cette option permet de rechercher un mot dans le corpus. Après la saisie du mot, le programme affiche :

- son nombre d’occurrences ;
- son rang selon sa fréquence ;
- sa fréquence dans le corpus ;
- ses principales collocations à gauche et à droite.

Les collocations sont triées selon leur score PMI. Le programme affiche les cinq meilleures collocations à gauche et les cinq meilleures collocations à droite.

Après la recherche du mot, l’utilisateur peut choisir d’afficher les contextes KWIC du mot cible. Il peut également définir le nombre de mots à afficher à gauche et à droite du mot recherché. Par défaut, cinq mots se présentent de chaque côté..

Exemple (pour le mot “un” dans le corpus small.brown):

```text
été/VPP lancés/VPP par/P  [un/DET]  F-16/NC israélien/ADJ et/CC   
       Reuters/NPP a/V mis/VPP  [un/DET]  terme/NC à/P sa/DET           
     travail/NC ,/PONCT dans/P  [un/DET]  lieu/NC peu/ADV éclairé/VPP   
     des/P+D piastres/NC est/V  [un/DET]  scandale/NC financier/ADJ et/CC
les/DET inculpations/NC ,/PONCT  [un/DET]  trafic/NC florissant/ADJ par/P
      ne/ADV suscita/V qu'/ADV  [un/DET]  intérêt/NC limité/ADJ chez/P
```

Après chaque recherche, le programme demande automatiquement si l’utilisateur souhaite rechercher un autre mot.

### Option 5 : Recherche par expression régulière

Cette option sert à effectuer une recherche à l’aide d’une expression régulière, par exemple [A-Z][a-z]+ pour les mots commençant par une majuscule.

L’utilisateur doit ensuite choisir la cible de la recherche :

- mot pour la recherche sur la forme du mot (après normalisation si non NPP) ;
- tag pour la recherche sur l’étiquette grammaticale comme DET, NPP.

L’utilisateur peut également indiquer s’il souhaite respecter la case (non par défaut).

Si l’affichage KWIC est choisi, l’utilisateur peut définir la taille du contexte. Le résultat montre alors chaque occurrence avec son entourage. Si l’affichage KWIC n’est pas choisi, le programme liste les vingt premières occurrences avec le numéro de ligne, la position, et la forme mot/tag.

### Option 6 : Recherche d’une suite structurée

Cette option permet de rechercher une suite structurée dans le corpus. La suite peut être composée uniquement de mots, uniquement de tags, ou d’un mélange de mots et de tags. Cette fonctionnalité est réalisée par le fichier exprMixte.py.

Par exemple, l’utilisateur peut saisir DET NC ADJ pour rechercher une suite composée d’un déterminant suivi d’un nom commun et un adjectif; Il peut aussi saisir l’ effet indésirable pour rechercher cette suite de mots spécifique; Il est également possible de mélanger le mot et le tag comme DET NC indésirable pour chercher la suite où un syntagme nominal précède l’adjectif indésirable.

Grâce au fichier reconnaissance.py, le programme distingue automatiquement les tags et les mots. Si un élément dans la saisie de l’utilisateur correspond à un tag connu, il est traité comme une étiquette grammaticale. Sinon, il est traité comme une forme lexicale.

Le programme indique alors :

- la suite recherchée ;
- le nombre d’occurrences de la suite recherchée ;
- sa fréquence dans le corpus.

De plus, le programme peut afficher les différentes formes concrètes de la suite recherchée et le nombre d’occurrences de chaque forme, et puis l’utilisateur peut choisir le mode d’affichage des collocations et du contexte KWIC :

- Mots uniquement ;
- Tags uniquement ;
- Mot/tag.

L’utilisateur peut ensuite choisir d’afficher les cinq principales collocations à gauche et à droite de la suite recherchée. Lorsque l’affichage se fait en mode mots ou en mode tags, les collocations sont accompagnées d’un score PMI, ainsi qu’en mode mot/tag, le programme affiche seulement le nombre d’occurrences, sans PMI.

Enfin, l’utilisateur peut choisir d’afficher le contexte KWIC de la suite recherchée. Par défaut, le contexte KWIC affiche cinq mots à gauche et cinq mots à droite. L’utilisateur peut toutefois modifier cette taille de contexte.

### Option 0 : Quitter

En choisissant cette option, l’utilisateur termine le programme.