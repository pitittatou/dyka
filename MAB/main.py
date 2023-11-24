import MAB.NonStationaryMAB as NSMAB
from sim.constants import *
from sim.user import UserMAB
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

user = UserMAB(base_heart_rate=100, max_heart_rate=200, max_increase=10, max_decrease=10)
bandit = NSMAB.NArmedBandit(arms = NB_MOTIF, step_size = 0.1, eps = 0.1, UCB_c = 2, 
                            sample_avg_flag = False, init_estimates = 0.0, mu = 0, std_dev = 1)

# Initialisation des listes pour stocker les valeurs
heart_rates = []
actions = []
motifs = []
freqVibro = []
targetFreq = []
os.remove('output.csv')
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
    plt.show()

def play(bandit,user, num_time_steps):

    countActionOpt = 0

    for i in range(num_time_steps):

        action = bandit.act()   #On choisi une action

        hrPrev = user.get_state()   # On regarde la freq cardiaque actuelle
        user.get_next_state(action) # On fait l'action choisi
        reward = user.get_state() - hrPrev  # On regarde la variation
        if reward == 0 and user.get_state() == user.max_heart_rate :
            reward = 10
        elif reward == 0 and user.get_state() == user.min_heart_rate :
            reward = -10

        if action == user.motif :
            countActionOpt += 1

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

   

    return countActionOpt
   
nbIté = 500
countActionOpt = play(bandit,user,nbIté)
print("Nombre d'actions optimales : ", countActionOpt/nbIté)
df = pd.read_csv('output.csv', header=None)
#print(df)
drawGraph()

