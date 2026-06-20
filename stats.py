import matplotlib.pyplot as plt

def info_generale(corpus, automate=None):
    if corpus.test == True and automate: 
        print("Nom du fichier : ", corpus.corpus)
        print("---TEST---")
        print("Nombre de mots recconus : ", corpus.nb_valides)

        if corpus.nb_valides != corpus.nb_mots :
            print("Nombre de mots non recconnus : ", corpus.nb_mots - corpus.nb_valides)

        print("Pourcentage de mots recconnus : ", corpus.nb_valides/corpus.nb_mots * 100, "%")
        print("\nMots non recconnus : ")

        for mot_inv in corpus.liste_invalides :
            print(mot_inv)
        print("----------")

    print(f"Nombre de mots: {corpus.nb_mots}")
    print(f"Nombre de lignes: {corpus.nb_lignes}")
    print(f"Nombre de formes: {corpus.nb_formes}")

    # Top 10 mots

    print("\nTop 10 des mots les plus fréquents :")

    liste_mots = []

    for mot, infos in corpus.index.items():
        liste_mots.append((mot, infos['nb_occ'], infos['freq'], infos['rang']))

    liste_mots.sort(key=lambda x: x[1], reverse=True)

    for mot, nb_occ, freq, rang in liste_mots[:10]:
        print(f"{rang}. {mot} : {nb_occ} occurrence(s), {freq}%")

    # Top 10 tags

    print("\nTop 10 des tags les plus fréquents :")

    liste_tags = []

    for tag, infos in corpus.index_tags.items():
        freq = round(infos['nb_occ'] / corpus.nb_mots * 100, 4)
        liste_tags.append((tag, infos['nb_occ'], freq))

    liste_tags.sort(key=lambda x: x[1], reverse=True)

    rang_tag = 1
    for tag, nb_occ, freq in liste_tags[:10]:
        print(f"{rang_tag}. {tag} : {nb_occ} occurrence(s), {freq}%")
        rang_tag+=1


def ranks_and_freqs(corpus):

    liste_mots = []

    for mot in corpus.index:    
        nb = corpus.index[mot]['nb_occ']
        liste_mots.append((mot, nb))

    liste_mots.sort(key=lambda x: x[1], reverse=True)

    rang = 0
    dernier_nb = None

    for i, (mot, nb) in enumerate(liste_mots, start=1):
        if nb != dernier_nb:
            rang = i
            dernier_nb = nb

        corpus.index[mot]['rang'] = rang
        corpus.index[mot]['freq'] = round(nb / corpus.nb_mots * 100, 4)


def stats_tags(corpus):
    corpus.index_tags = {}

    for mot, infos in corpus.index.items():
        for tag in infos['tags']:
            if tag not in corpus.index_tags:
                corpus.index_tags[tag] = {
                    'nb_occ': 0,
                    'formes': {}
                }
            corpus.index_tags[tag]['nb_occ'] += 1

            if mot not in corpus.index_tags[tag]['formes']:
                corpus.index_tags[tag]['formes'][mot] = 0

            corpus.index_tags[tag]['formes'][mot] += 1

    for tag, infos in corpus.index_tags.items():
        nb_occurrences = infos['nb_occ']

        liste_formes = list(infos['formes'].items())
        liste_formes.sort(key=lambda x: x[1], reverse=True)

        infos['nb_formes'] = len(liste_formes)
        infos['formes_triees'] = []

        rang = 0
        dernier_nb = None

        for i, (mot, nb) in enumerate(liste_formes, start=1):
            if nb != dernier_nb:
                rang = i
                dernier_nb = nb
            freq = round(nb / nb_occurrences * 100, 4)

            infos['formes_triees'].append({
                'mot': mot,
                'nb': nb,
                'freq': freq,
                'rang': rang
            })

def plot_zipf(corpus):

    rangs = []
    frequences = []

    for mot in corpus.index:
        rangs.append(corpus.index[mot]['rang'])
        frequences.append(corpus.index[mot]['freq'])

    plt.figure()
    plt.title("Loi de Zipf")
    plt.xlabel("log(rang)")
    plt.ylabel("log(fréquence)")
    plt.loglog(rangs, frequences, 'o', markersize=3)
    plt.show()



if __name__ == "__main__":
    import main
    main.main()
   
            