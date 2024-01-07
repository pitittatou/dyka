import threading
import MAB.NonStationaryMAB as NSMAB
from sim.constants import *
from sim.user import UserMAB
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import serial
import os
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


user = UserMAB(base_heart_rate=100, max_heart_rate=200, max_increase=10, max_decrease=10)
bandit = NSMAB.NArmedBandit(arms = NB_MOTIF, step_size = 0.2, eps = 0.1, UCB_c = 2, 
                            sample_avg_flag = False, init_estimates = 0.0, mu = 0, std_dev = 1, thomsonSample= False)

# Initialisation des listes pour stocker les valeurs
heart_rates = []
actions = []
motifs = []
freqVibro = []
targetFreq = []
actionsValue = [ [] for _ in range(NB_MOTIF)]
buttonPressed = False
buttonResult = 0
#os.remove('output.csv')

def update_info(freqVibroInstant, action, freq_cardiaque, freqVibroAll):
    print("freqVibroall : ", freqVibroAll)
    # Mettre à jour les étiquettes avec les nouvelles informations
    label_freq.config(text="Fréquence vibro : " + str(freqVibroInstant))
    label_action.config(text="Action choisi : " + str(action))
    label_freq_cardiaque.config(text="Fréquence cardiaque : " + str(freq_cardiaque))

    x = np.arange(len(freqVibroAll))
    ax.plot(x, freqVibroAll)
    fig.canvas.draw()
    

# Création de la fenêtre principale
root = tk.Tk()
root.title("Fréquences du module vibrant")

# Création du graphique Matplotlib
fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_xlabel('Temps')
ax.set_ylabel('Fréquence')
ax.set_title('Fréquence du module vibrant')

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Création des étiquettes pour afficher les informations
label_freq = tk.Label(root, text="Fréquence Vibro : ")
label_freq.pack()

label_action = tk.Label(root, text="Action choisie : ")
label_action.pack()

label_freq_cardiaque = tk.Label(root, text="Fréquence cardiaque : ")
label_freq_cardiaque.pack()

def buttonLikePressed():
    global buttonPressed
    global buttonResult
    buttonPressed = True
    buttonResult = 1

def buttonDislikePressed():
    global buttonPressed
    global buttonResult
    buttonPressed = True
    buttonResult = -1

buttonLike = tk.Button(root, text="J'aime", command= buttonLikePressed)
buttonLike.pack()

buttonDislike = tk.Button(root, text="J'aime pas", command=buttonDislikePressed)
buttonDislike.pack()

