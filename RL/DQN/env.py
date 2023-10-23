"""

Dans ce fichier, on va devoir implementer l'environnement,c'est a dire :

    - La description de d'un état
    - Les actions possibles
    - La fonction de transition .step(action) qui va donner l'etat suivant en fonction de l'action pris par l'agent
    - La fonction de recompense .reward() qui va donner la recompense en fonction de l'etat actuel
    - La fonction de reset .reset() qui va remettre l'etat a 0
    

PB :  la fonction .step() de env doit pouvoir donner l'etat suivant en fonction de l'action choisie
        OR on ne connait pas l'etat suivant selon une action qui est autre que "VIBRER PLUS FORT" 
        donc on ne peut pas faire de fonction de transition

        Fondamentalement ce que je comprend pas c'est imaginons qu'on a deux personne qui sont totalement opposé. Un adore 
        quand ca vibre et l'autre deteste. On va dire a l'algo que dans un premier temps dans l'etat 120 bpm avec action augmenter vibration on a une recompense 
        positive et dans un second temps pour le même etat on a une recompense negative.
        L'algo va donc devoir utiliser enorement de data de "gens" different pour au final deduire que si une plus grande moyenne de gens prefere un certain 
        comportement alors c'est ce comportement qui va l'emporter?
        SINON on se focalise que sur 1 personne et on fait en sorte que l'algo apprenne a connaitre cette personne et a savoir ce qu'elle aime ou pas.
        Comme ca ca assure une certaine coherence puisque supposement on garde toujours les meme gouts. (plus ou moins)

"""
from sim.vibroUser import User, ComplexUser, RampFreqUser, StableFreqUser
import random

class Env:
    def __init__(self):
        self.user = StableFreqUser(70, 150, 2, 2, 40, 0)
        self.initState = self.user.get_state()
        self.state = self.initState
        self.done = False
        

    def step(self,action):
        #Ici l'acttion est une frequence 
        next_state = self.user.get_next_state(action)
        reward = self.reward(self.state, next_state)
        self.state = next_state
        self.is_done()
        return next_state, reward, self.done, None
    
    def reward(self, state, next_state):
        # Calculate the reward based on the current state and the next state
        # For example, you can use the difference between the current and next state as the reward
        print("State : ",state," Next state : ",next_state, " Reward : ",(next_state - state))
        reward = (next_state - state) # Division arbitraire pour pas que la recompense soit trop elevée
        return reward

    def reset(self):
        #self.user = ComplexUser.new_random_user()
        self.user = StableFreqUser(70, 150, 2, 2, 10, 3)
        return self.state

    def get_state(self):
        return self.state
    
    def is_done(self):

        return self.done
       
           
    
    
