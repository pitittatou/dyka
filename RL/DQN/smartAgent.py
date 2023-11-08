"""
Ce fichier sert de preuve final. Un vibro qui saura se comporter de maniere autonome

"""
from matplotlib import pyplot as plt
from dqnAgent import *
from env import *
from sim.constants import *

#load the weights from file
agent = Agent(state_size=10,action_size=5,seed=0)
agent.qnetwork_local.load_state_dict(torch.load('checkpoint.pt'))
env = Env(68)

pointFreq = []
pointAction = []
pointHR = []

actions = [
    "0 : NE RIEN FAIRE",
    "1 : VIBRER MOINS FORT",
    "2 : VIBRER PLUS FORT",
    "3 : VIBRER PLUS PLUS FORT",
    "4 : VIBRER MOINS MOINS FORT"
]
for i in range(1):
    state = env.reset()
    print("La target choisi est ", env.targetfreq)
    for j in range(50):
        action = agent.act(state)
        
        print("Action choisie : ",actions[action])
        state,reward,done,_ = env.step(action)
        print("Fréquence : ",env.user.freq, " Heart rate : ",env.user.heart_rate, " Reward : ",reward)
        pointFreq.append(env.user.freq)
        pointAction.append(action)
        pointHR.append(env.user.heart_rate) 

        if done:
            break

print("Fin du programme")

temps = list(range(50))

# Supposons que pointFreq est votre liste de fréquences
# pointFreq = [...]

plt.figure(figsize=(10, 10))

plt.subplot(3, 1, 1)
plt.plot(temps, pointFreq)
plt.xlabel('Temps')
plt.ylabel('Fréquence')
plt.title('Fréquence en fonction du temps')

plt.subplot(3, 1, 2)
plt.plot(temps, pointAction)
plt.xlabel('Temps')
plt.ylabel('Action')
plt.title('Action en fonction du temps')

plt.subplot(3, 1, 3)
plt.plot(temps, pointHR)
plt.xlabel('Temps')
plt.ylabel('Heart Rate')
plt.title('Heart Rate en fonction du temps')

plt.tight_layout()
plt.show()