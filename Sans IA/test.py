from sim.vibroUser import User, ComplexUser, RampFreqUser, StableFreqUser
from sim.constants import *

testeur = StableFreqUser(80, 150, 2, 2, 50, 3)

actions = [
    "0 : NE RIEN FAIRE",
    "1 : VIBRER MOINS FORT -2",
    "2 : VIBRER PLUS FORT +2",
    "3 : VIBRER PLUS PLUS FORT +10",
    "4 : VIBRER MOINS MOINS FORT -10"
]



def rampUpFreq():
    """
    Cette fonction permet de tester le comportement de l'utilisateur en fonction de la frequence
    On part d'une frequence de 1 et on augmente petit a petit la frequence jusqu'a 100
    Fonction initiale
    """
    testeur.user = 0
    freqPossible = []
    print(testeur.freq)
    for i in range(50):
        hr = testeur.heart_rate
        testeur.get_next_state(2)
        print("Freq : ",testeur.freq, " Heart rate : ",testeur.heart_rate)
        if testeur.heart_rate > hr:
            freqPossible.append(testeur.freq)

    print("Freq possible : ",freqPossible) 

    #Avec notre modèle simpliste, quand on a atteint la target freq on va plus pouvoir augmenter  
    return freqPossible[-1]   