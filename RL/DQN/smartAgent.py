"""
Ce fichier sert de preuve final. Un vibro qui saura se comporter de maniere autonome

"""
from dqnAgent import *
from env import *

#load the weights from file
agent = Agent(state_size=10,action_size=5,seed=0)
agent.qnetwork_local.load_state_dict(torch.load('checkpoint.pt'))
env = Env()

actions = [
    "0 : NE RIEN FAIRE",
    "1 : VIBRER MOINS FORT",
    "2 : VIBRER PLUS FORT",
    "3 : VIBRER PLUS PLUS FORT",
    "4 : VIBRER MOINS MOINS FORT"
]
for i in range(1):
    state = env.reset()
    for j in range(200):
        action = agent.act(state)
        print("Action choisie : ",actions[action])
        state,reward,done,_ = env.step(action)
        print("Fréquence : ",env.user.freq, " Heart rate : ",env.user.heart_rate)
        if done:
            break

env.close()