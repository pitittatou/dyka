from collections import deque
from sim.vibroUser import User, ComplexUser, RampFreqUser, StableFreqUser
import random

import env


env = env.Env()
for i in range(10):
    env.step(64)

us = User(80, 150, 2, 2)

for i in range(10):
    
    us.get_next_state_with_memory(us.get_next_freq(0))