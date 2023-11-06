from collections import deque
from sim.vibroUser import User, ComplexUser, RampFreqUser, StableFreqUser
import random

import env


env = env.Env()
for i in range(10):
    env.step(64)
