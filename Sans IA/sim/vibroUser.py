import random
import collections
from sim.constants import *


class User:
    def __init__(self, base_heart_rate, max_heart_rate, max_increase, max_decrease):
        self.heart_rate = base_heart_rate
        self.min_heart_rate = base_heart_rate  # The heart rate increase when conditions are ideal
        self.max_increase = max_increase  # The highest possible heart rate reduction, must be positive
        self.max_decrease = max_decrease
        self.max_heart_rate = max_heart_rate
        self.freq = 0

        self.heart_rate_list = collections.deque([self.heart_rate]*5, maxlen = 5)  # The last 5 heart rates (initialiser a la fréquence de base de l'utilisateur)
        self.actions_taken_list = collections.deque([0]*5, maxlen = 5)  # The last 5 actions taken (initialiser a 0)
       # print(self.heart_rate, self.heart_rate_list, self.actions_taken_list)
        self.memory = collections.deque(maxlen=STEP_MEMORY_SIZE*2+2)  # 2 times the number of steps we want to remember (for action and frequency) + 2 for the new frequency/action
        for _ in range(0, STEP_MEMORY_SIZE*2):
            self.memory.append(None)
        self.memory.extend((self.heart_rate, None))  # There is None first action

    def get_next_state(self, freq):
        pass

    def get_state(self):
        state = list(self.heart_rate_list)+list(self.actions_taken_list)
       # print("State : ",state)
        return state

    def get_state_with_memory(self):
        return list(self.memory)[:-1]

    def get_next_state_with_memory(self, freq):
        self.get_next_state(freq)
        return list(self.memory)[:-1]
    
    def get_next_freq(self, action):
        """
        Recap des actions : 
        0 : NE RIEN FAIRE
        1 : VIBRER MOINS FORT
        2 : VIBRER PLUS FORT
        3 : VIBRER PLUS PLUS FORT
        4 : VIBRER MOINS MOINS FORT
        """

        #Pour l'instant on utilise des valeur de pas aléatoire mais c'ets a modifié

        #print("Freq entrée : ",self.freq, " Action : ",action)
        if action == 0:
            result = self.freq
        elif action == 1:
            result = self.freq - 2
        elif action == 2:
            result = self.freq + 2
        elif action == 3:
            result = self.freq + 10
        elif action == 4:
            result = self.freq - 10
        else:
            result = self.freq
        
        if result <0 :
            result = 0
        if result > MAX_FREQ:
            result = MAX_FREQ
        return result
       
        
        

    @staticmethod
    def new_random_user():
        pass


class StableFreqUser(User):
    """A user that prefers a stable frequency"""

    def __init__(self, base_heart_rate, max_heart_rate, max_increase, max_decrease, target_freq, freq_tolerance):
        super().__init__(base_heart_rate, max_heart_rate, max_increase, max_decrease)
        self.target_freq = target_freq
        self.freq_tolerance = freq_tolerance

    def get_next_state(self, action):
        freq = self.get_next_freq(action)
        #print("Freq en sortie :",self.freq)
        freq_err = abs(freq - self.target_freq)
        self.heart_rate += max(-self.max_decrease, self.max_increase * (1 - freq_err / self.freq_tolerance))
        self.heart_rate = min(max(self.min_heart_rate, self.heart_rate), self.max_heart_rate)
   

        self.freq = freq
        self.memory.extend((self.heart_rate, self.freq))

        self.heart_rate_list.append(self.heart_rate)
        self.actions_taken_list.append(action)
        next_state = self.get_state()
        return next_state

    @staticmethod
    def new_random_user():
        base_heart_rate = random.randint(MIN_BASE_HR, MAX_BASE_HR)
        max_increase = MIN_MAX_INCREASE + random.random() * (MAX_MAX_INCREASE - MIN_MAX_INCREASE)
        max_decrease = MIN_MAX_DECREASE + random.random() * (MAX_MAX_DECREASE - MIN_MAX_DECREASE)
        max_heart_rate = random.randint(MIN_MAX_HR, MAX_MAX_HR)
        target_freq = random.randint(MIN_FREQ, MAX_FREQ)
        freq_tolerance = random.randint(MIN_FREQ_TOLERANCE, MAX_FREQ_TOLERANCE)

        return StableFreqUser(base_heart_rate, max_heart_rate, max_increase, max_decrease, target_freq, freq_tolerance)


class RampFreqUser(User):
    """A user that prefers a rising or decreasing frequency"""

    def __init__(self, base_heart_rate, max_heart_rate, max_increase, max_decrease, freq_slope, freq_tolerance):
        super().__init__(base_heart_rate, max_heart_rate, max_increase, max_decrease)
        self.freq_slope = freq_slope
        self.freq_tolerance = freq_tolerance

    def get_next_state(self, action):
        freq = self.get_next_freq(action)
        #print("Freq en sortie :",self.freq)
        target_freq = self.freq + self.freq_slope
        freq_err = abs(freq - target_freq)
        self.heart_rate += max(-self.max_decrease, self.max_increase * (1 - freq_err / self.freq_tolerance))
        self.heart_rate = min(max(self.min_heart_rate, self.heart_rate), self.max_heart_rate)
        self.freq = freq
        self.memory.extend((self.heart_rate, self.freq))

        self.heart_rate_list.append(self.heart_rate)
        self.actions_taken_list.append(action)
        next_state = self.get_state()

        return next_state

    @staticmethod
    def new_random_user():
        base_heart_rate = random.randint(MIN_BASE_HR, MAX_BASE_HR)
        max_increase = MIN_MAX_INCREASE + random.random() * (MAX_MAX_INCREASE - MIN_MAX_INCREASE)
        max_decrease = MIN_MAX_DECREASE + random.random() * (MAX_MAX_DECREASE - MIN_MAX_DECREASE)
        max_heart_rate = random.randint(MIN_MAX_HR, MAX_MAX_HR)
        slope = random.randint(MIN_FREQ_SLOPE, MAX_FREQ_SLOPE)
        slope = -slope if random.random() < 0.5 else slope
        freq_tolerance = random.randint(MIN_FREQ_TOLERANCE, MAX_FREQ_TOLERANCE)

        return RampFreqUser(base_heart_rate, max_heart_rate, max_increase, max_decrease, slope, freq_tolerance)


class ComplexUser(User):
    """A user whose preferences change over time, every profile_change_interval steps"""

    def __init__(self, base_heart_rate, max_heart_rate, max_increase, max_decrease, profile_change_interval):
        super().__init__(base_heart_rate, max_heart_rate, max_increase, max_decrease)
        self.profile_change_interval = profile_change_interval
        self.step_counter = 0
        self.user = None
        self.change_profile()

    def change_profile(self):
        if random.random() < 0.5:
            self.user = StableFreqUser.new_random_user()
        else:
            self.user = RampFreqUser.new_random_user()
        self.user.freq = self.freq
        self.user.heart_rate = self.heart_rate
        self.user.max_heart_rate = self.max_heart_rate
        self.user.min_heart_rate = self.min_heart_rate

    def get_next_state(self, action):
        freq = self.get_next_freq(action)
        next_state = self.user.get_next_state(freq)
        self.freq = freq
        self.memory = self.user.memory

        self.step_counter += 1
        if self.step_counter == self.profile_change_interval:
            self.change_profile
            self.step_counter = 0

        return next_state

    @staticmethod
    def new_random_user():
        base_heart_rate = random.randint(MIN_BASE_HR, MAX_BASE_HR)
        max_heart_rate = random.randint(MIN_MAX_HR, MAX_MAX_HR)
        return ComplexUser(base_heart_rate, max_heart_rate, None, None, PROFILE_CHANGE_INTERVAL)
