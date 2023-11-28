from sim.constants import *
import numpy as np
from random import *

freq = 90
targetFreq = 100
freq_tolerance = 5



if abs(freq - targetFreq) <= freq_tolerance:
    motif = 2
elif targetFreq - freq + freq_tolerance < 0:  
    if targetFreq - freq + freq_tolerance < -20:
        motif = 0
    else:
        motif = 1
elif targetFreq - freq - freq_tolerance > 0:
    if targetFreq - freq - freq_tolerance > 20:
        motif = 4
    else:
        motif = 3

print(motif)

actionsValue = [ [] for _ in range(NB_MOTIF)]
successes = np.array([ 0 for _ in range(NB_MOTIF)])
failures = np.array([ 0 for _ in range(NB_MOTIF)])

print(actionsValue)
print(successes)
print(failures)

beta_samples = np.random.beta(successes + 1, failures + 1)

print(beta_samples)

action = np.argmax(beta_samples)

print(action)