import tkinter as tk
from tkinter import ttk
import re

from corpusStats import CorpusStats
from reconaissance import expr


automate = re.compile(expr)

stats = CorpusStats("corpus/small.brown")
stats.read_corpus(automate)


fenetre = tk.Tk()
fenetre.title("L3 PROJET TAL")
fenetre.geometry("1000x1000")
fenetre.configure(bg="#0f1115")


tk.Label(
    fenetre,
    text="Concordancier",
    font=("Arial", 18, "bold"),
    fg="white",
    bg="#0f1115"
).pack(pady=10)



# STATS

frame_stats = tk.Frame(fenetre, bg="#1a1d24")
frame_stats.pack(fill="x", padx=20, pady=10)

tk.Label(
    frame_stats,
    text=f"Corpus : {stats.corpus}            | Mots : {stats.nb_mots}            | Phrases : {stats.nb_phrases}",
    fg="white",
    bg="#1a1d24",
    font=("Arial", 14, "bold")
).pack(pady=20)



# ZONE INPUT + BOUTONS 

frame_top = tk.Frame(fenetre, bg="#0f1115")
frame_top.pack(pady=10)


tk.Label(frame_top, text="Mot :", fg="white", bg="#0f1115").grid(row=0, column=0)

champ_mot = tk.Entry(frame_top, width=25)
champ_mot.grid(row=0, column=1, padx=5)

tk.Label(frame_top, text="KWIC: nombre de mots (gauche , droite)", fg="white", bg="#0f1115").grid(row=0, column=2)

champ_kwic = tk.Entry(frame_top, width=5)
champ_kwic.insert(0, "5")
champ_kwic.grid(row=0, column=3, padx=5)





def rechercher():
    resultat.delete("1.0", tk.END)

    mot = champ_mot.get().strip()

    if mot not in stats.index:
        resultat.insert(tk.END, "Mot non trouvé")
        return

    infos = stats.index[mot]

    resultat.insert(tk.END, f"Mot : {mot}\n")
    resultat.insert(tk.END, f"Occurrences : {infos['nb']}\n\n")
    resultat.insert(tk.END, f" Rang : {infos['rang']}\n")
    resultat.insert(tk.END, f" Fréquence : {infos['freq']}%\n\n")

    resultat.insert(tk.END, " Collocations :\n")

    if "coocc" in infos:
        for mot2, co in list(infos["coocc"].items())[:6]:
            resultat.insert(tk.END,
                f"   • {mot2} ({co['nb']}, PMI={round(co['pmi'],2)})\n"
            )

    try:
        size = int(champ_kwic.get())
    except ValueError:
        size = 5

    resultat.insert(tk.END, "\n KWIC\n" + "-"*60 + "\n")

    kwic = stats.kwic_words(mot, size=size)

    for ligne in kwic[:25]:
        gauche = " ".join(ligne["gauche"])
        centre = ligne["mot_enquete"]
        droite = " ".join(ligne["droite"])

        resultat.insert(tk.END, f"{gauche} [ {centre} ] {droite}\n")


btn_recherche = ttk.Button(frame_top, text="🔍 Rechercher", command=rechercher)
btn_recherche.grid(row=0, column=4, padx=10)

btn_zipf = ttk.Button(frame_top, text="📉 Zipf", command=stats.plot_zipf)
btn_zipf.grid(row=0, column=5, padx=10)



# RESULTATS 

frame_result = tk.Frame(fenetre)
frame_result.pack(fill="both", expand=True, padx=20, pady=10)

resultat = tk.Text(frame_result, bg="#161a22", fg="white")
resultat.pack(side="left", fill="both", expand=True)

scroll = tk.Scrollbar(frame_result, command=resultat.yview)
scroll.pack(side="right", fill="y")

resultat.config(yscrollcommand=scroll.set)


fenetre.mainloop()