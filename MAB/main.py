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
    print("Button like pressed")

def buttonDislikePressed():
    global buttonPressed
    global buttonResult
    buttonPressed = True
    buttonResult = -1
    print("Button dislike pressed")

buttonLike = tk.Button(root, text="J'aime", command= buttonLikePressed)
buttonLike.pack()

buttonDislike = tk.Button(root, text="J'aime pas", command=buttonDislikePressed)
buttonDislike.pack()



# Lancement de la boucle principale de la fenêtre

def arduinoReady():
    port = 'COM8'
    baudrate = 9600

    # Initialise la connexion série
    arduino = serial.Serial(port, baudrate, timeout=1)
    
    # Attendez que la connexion soit établie
    time.sleep(2)

    return arduino


def drawGraph():
         
    plt.figure(1)
    plt.plot(heart_rates)
    plt.title('Evolution de la fréquence cardiaque')
    plt.xlabel('Temps')
    plt.ylabel('Fréquence cardiaque')
    

    # Tracer les actions prises
    plt.figure(2)
    plt.plot(actions)
    plt.title('Actions prises')
    plt.xlabel('Temps')
    plt.ylabel('Action')
    plt.legend(['Action'])

    # Tracer le motif de l'utilisateur
    plt.plot(motifs, '--')
    plt.title('Motif de l\'utilisateur')
    plt.xlabel('Temps')
    plt.ylabel('Motif')
    plt.legend(['Motif'])
 

    # Tracer les actions prises
    plt.figure(3)
    plt.plot(freqVibro)
    plt.title('Fréquence de vibration du vibro')
    plt.xlabel('Temps')
    plt.ylabel('Freq')
    plt.legend(['Freq Vibro'])

    # Tracer le motif de l'utilisateur
    plt.plot(targetFreq, '--')
    plt.title('Fréquence cible du vibro')
    plt.xlabel('Temps')
    plt.ylabel('Freq')
    plt.legend()

    plt.figure()

    # Supposons que actionValue soit un tableau 2D
    for i in range(5):
        plt.plot(actionsValue[i])

        plt.title('Action Values')
        plt.xlabel('Temps')
        plt.ylabel('Valeur')
        plt.legend(['Courbe 1', 'Courbe 2', 'Courbe 3', 'Courbe 4', 'Courbe 5'])
    plt.show()

def play(bandit,user, num_time_steps):
   

    countActionOpt = 0
    
    for i in range(num_time_steps):

        action = bandit.act()   #On choisi une action

        hrPrev = user.get_state()   # On regarde la freq cardiaque actuelle
        print("HR prev : ", hrPrev)
        action_value = 'uwu'
        if action == 0 : 
            action_value = -10
        if action == 1 :
            action_value = -5
        if action == 2 :
            action_value = 0
        if action == 3 :
            action_value = 5
        if action == 4 :
            action_value = 10

        print(action_value)
        update_info(str(user.freq), str(action_value), str(user.get_state()), freqVibro) # On met a jour les infos sur la fenetre
        print("Avant button")
        #user.get_next_state(action) # On fait l'action choisi
        global buttonPressed
        #while buttonPressed == False :
            #pass
        print(buttonResult)
        while buttonPressed == False : 
            root.update()
        user.get_next_stateBis(action, buttonResult)
        buttonPressed = False
        print(" HR actuelle : ", user.get_state())
        reward = user.get_state() - hrPrev  # On regarde la variation
        if reward == 0 and user.get_state() == user.max_heart_rate :
            #print("On est a HR max mais pas d'évolution donc reward +10")
            reward = 10
        elif reward == 0 and user.get_state() == user.min_heart_rate :
            #print("On est a HR min mais pas d'évolution donc reward -10")
            reward = -10

        if action == user.motif :
            countActionOpt += 1

        #print("Time : ", i, " Action : ", action, " VibroFreq : ", user.freq," Target freq : ", user.targetFreq , " User motif : ", user.motif, " Reward : ", reward, " Heart rate : ", user.get_state())
        with open('output.txt', 'a') as f:
            f.write("Time : " + str(i) + " Action : " + str(action) + " VibroFreq : " + str(user.freq) + " Target freq : " + str(user.targetFreq) + " User motif : " + str(user.motif) + " Reward : " + str(reward) + " Heart rate : " + str(user.get_state()) + "\n")
        """
        if i % (num_time_steps//5) == 0 :
             user.new_motif() #On change le motif
        """   
      

        bandit.step(action, reward)

         # Stockage des valeurs
        heart_rates.append(user.get_state())
        actions.append(action)
        motifs.append(user.motif)  # Assurez-vous que l'utilisateur a un attribut de motif
        freqVibro.append(user.freq)
        targetFreq.append(user.targetFreq)

        for i in range(NB_MOTIF):
            actionsValue[i].append(bandit.Q_t[i])


        if i % 30000 == 0 :
            bandit.re_init()

        #arduino.write(f'{user.freq}\n'.encode())
        #time.sleep(0.5)
   

    return countActionOpt

sum = 0 
"""
for i in range(100):
    nbIté = 1000
    countActionOpt = play(bandit,user,nbIté)
    print("Nombre d'actions optimales : ", countActionOpt/nbIté)
    sum += countActionOpt/nbIté

print("Moyenne : ", sum/100)
    

"""

#arduino = arduinoReady()
nbIté = 300

with open('output.txt', 'w'):
    pass
play(bandit,user,nbIté)



"""
countActionOpt = play(bandit,user,nbIté)
print("Nombre d'actions optimales : ", countActionOpt/nbIté)
df = pd.read_csv('output.csv', header=None)
#print(df)

print(bandit.successes)
print(bandit.failures)
print(bandit.successes.sum() + bandit.failures.sum())
"""
drawGraph()


