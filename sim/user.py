import collections
import random

from sim.constants import *


class User:
    def __init__(self, base_heart_rate, max_heart_rate, max_increase, max_decrease):
        self.heart_rate = base_heart_rate
        # The heart rate increase when conditions are ideal
        self.min_heart_rate = base_heart_rate
        # The highest possible heart rate reduction, must be positive
        self.max_increase = max_increase
        self.max_decrease = max_decrease
        self.max_heart_rate = max_heart_rate
        self.freq = 0
        #  2 times the number of steps we want to remember (for action and frequency) + 2 for the new frequency/action
        self.memory = collections.deque(maxlen=STEP_MEMORY_SIZE*2+2)
        for _ in range(0, STEP_MEMORY_SIZE*2):
            self.memory.append(None)
        # There is None first action
        self.memory.extend((self.heart_rate, None))

    def get_next_state(self, freq):
        pass

    def get_state(self):
        return self.heart_rate

    def get_state_with_memory(self):
        return list(self.memory)[:-1]

    def get_next_state_with_memory(self, freq):
        self.get_next_state(freq)
        return list(self.memory)[:-1]

    @staticmethod
    def new_random_user():
        pass


class StableFreqUser(User):
    """A user that prefers a stable frequency"""

    def __init__(self, base_heart_rate, max_heart_rate, max_increase, max_decrease, target_freq, freq_tolerance):
        super().__init__(base_heart_rate, max_heart_rate, max_increase, max_decrease)
        self.target_freq = target_freq
        self.freq_tolerance = freq_tolerance

    def get_next_state(self, freq):
        freq_err = abs(freq - self.target_freq)
        self.heart_rate += max(-self.max_decrease, self.max_increase *
                               (1 - freq_err / self.freq_tolerance))
        self.heart_rate = min(
            max(self.min_heart_rate, self.heart_rate), self.max_heart_rate)
        self.freq = freq
        self.memory.extend((self.heart_rate, self.freq))
        return self.heart_rate

    @staticmethod
    def new_random_user():
        base_heart_rate = random.randint(MIN_BASE_HR, MAX_BASE_HR)
        max_increase = MIN_MAX_INCREASE + \
            random.random() * (MAX_MAX_INCREASE - MIN_MAX_INCREASE)
        max_decrease = MIN_MAX_DECREASE + \
            random.random() * (MAX_MAX_DECREASE - MIN_MAX_DECREASE)
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

    def get_next_state(self, freq):
        target_freq = self.freq + self.freq_slope
        freq_err = abs(freq - target_freq)
        self.heart_rate += max(-self.max_decrease, self.max_increase *
                               (1 - freq_err / self.freq_tolerance))
        self.heart_rate = min(
            max(self.min_heart_rate, self.heart_rate), self.max_heart_rate)
        self.freq = freq
        self.memory.extend((self.heart_rate, self.freq))

        return self.heart_rate

    @staticmethod
    def new_random_user():
        base_heart_rate = random.randint(MIN_BASE_HR, MAX_BASE_HR)
        max_increase = MIN_MAX_INCREASE + \
            random.random() * (MAX_MAX_INCREASE - MIN_MAX_INCREASE)
        max_decrease = MIN_MAX_DECREASE + \
            random.random() * (MAX_MAX_DECREASE - MIN_MAX_DECREASE)
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

    def get_next_state(self, freq):
        self.heart_rate = self.user.get_next_state(freq)
        self.freq = freq
        self.memory = self.user.memory

        self.step_counter += 1
        if self.step_counter == self.profile_change_interval:
            self.change_profile
            self.step_counter = 0

        return self.heart_rate

    @staticmethod
    def new_random_user():
        base_heart_rate = random.randint(MIN_BASE_HR, MAX_BASE_HR)
        max_heart_rate = random.randint(MIN_MAX_HR, MAX_MAX_HR)
        return ComplexUser(base_heart_rate, max_heart_rate, None, None, PROFILE_CHANGE_INTERVAL)


class UserMAB:
    def __init__(self, base_heart_rate, max_heart_rate, max_increase, max_decrease):
        self.heart_rate = base_heart_rate
        # The heart rate increase when conditions are ideal
        self.min_heart_rate = base_heart_rate
        # The highest possible heart rate reduction, must be positive
        self.max_increase = max_increase
        self.max_decrease = max_decrease
        self.max_heart_rate = max_heart_rate

        self.freq = 0
        self.targetFreq = 50
        self.freq_tolerance = 5
        self.variation_freq_preference = 100

        # Les motifs sont 0 (ne rien faire), 1 (augmenter la fréquence), 2 (diminuer la fréquence)
        self.motif = 0
        # Compteur qui permet de keep track du nombre d'action prise (permet de pas melanger bandit et user)
        self.nbActionTaken = 0

    def get_next_stateBis(self, motif, inputUser):

        self.nbActionTaken += 1

        if inputUser == 1:  # Si on a aimé on envoit un 1, sinon c est 0

            if self.heart_rate != self.max_heart_rate:

                # Calculer le facteur de réduction en fonction de la proximité de la fréquence cardiaque actuelle par rapport à la fréquence cardiaque maximale
                reduction_factor = 1
                # reduction_factor = 1 - (self.heart_rate / self.max_heart_rate)
                # reduction_factor = 1 - abs((self.targetFreq - self.freq) / self.max_heart_rate)

                # Appliquer le facteur de réduction au gain de fréquence cardiaque
                self.heart_rate = min(self.heart_rate + reduction_factor *
                                      max(-self.max_decrease, self.max_increase), self.max_heart_rate)
            else:
                self.heart_rate = self.max_heart_rate
        else:

            if self.heart_rate != self.min_heart_rate:

                self.heart_rate = max(
                    self.heart_rate - max(-self.max_decrease, self.max_increase), self.min_heart_rate)
            else:
                self.heart_rate = self.min_heart_rate

        self.modifFreq(motif)

        if self.nbActionTaken % (self.variation_freq_preference) == 0:
            print("action taken : ", self.nbActionTaken)
            print("ancienne freq : ", self.targetFreq)
            self.targetFreq = random.randint(MIN_FREQ, MAX_FREQ)
            print("New target freq : ", self.targetFreq)

    def get_next_state(self, motif):

        self.nbActionTaken += 1

        if self.motif == motif:

            if self.heart_rate != self.max_heart_rate:

                # Calculer le facteur de réduction en fonction de la proximité de la fréquence cardiaque actuelle par rapport à la fréquence cardiaque maximale
                reduction_factor = 1
                # reduction_factor = 1 - (self.heart_rate / self.max_heart_rate)
                # reduction_factor = 1 - abs((self.targetFreq - self.freq) / self.max_heart_rate)

                # Appliquer le facteur de réduction au gain de fréquence cardiaque
                self.heart_rate = min(self.heart_rate + reduction_factor *
                                      max(-self.max_decrease, self.max_increase), self.max_heart_rate)
            else:
                self.heart_rate = self.max_heart_rate
        else:
            if self.heart_rate != self.min_heart_rate:

                self.heart_rate = max(
                    self.heart_rate - max(-self.max_decrease, self.max_increase), self.min_heart_rate)
            else:
                self.heart_rate = self.min_heart_rate

        self.modifFreq(motif)  # On actualise la freq de vibration du vibro

        if self.nbActionTaken % (self.variation_freq_preference) == 0:
            print("action taken : ", self.nbActionTaken)
            print("ancienne freq : ", self.targetFreq)
            self.targetFreq = random.randint(MIN_FREQ, MAX_FREQ)
            print("New target freq : ", self.targetFreq)

        self.new_motif()  # On change le motif selon la freq de l'user

        return self.heart_rate

    def get_state(self):
        return self.heart_rate

    def get_state_with_memory(self):
        return list(self.memory)[:-1]

    def get_next_state_with_memory(self, freq):
        self.get_next_state(freq)
        return list(self.memory)[:-1]

    def modifFreq(self, motif):

        # Incrément de la fréquence de vibration a faire varier

        if motif == 0:
            self.freq = self.freq - 10
        elif motif == 1:
            self.freq = self.freq - 5
        elif motif == 2:
            self.freq = self.freq
        elif motif == 3:
            self.freq = self.freq + 5
        elif motif == 4:
            self.freq = self.freq + 10

        if self.freq < 0:
            self.freq = 0
        if self.freq > MAX_FREQ:
            self.freq = MAX_FREQ,

    def new_motif(self):

        # on actualise le motif en fonction de la freq de l'user
        # print(" sefl.freq : ", self.freq , " Type : ", self.freq)
        if type(self.freq) == tuple:
            self.freq = int(self.freq[0])
            # print(" J'etais un tuple")
        # On est dans l'intervalle de tolerance
        if abs(self.freq - self.targetFreq) <= self.freq_tolerance:
            self.motif = 2

        # On est en dessous de l'intervalle de tolerance
        elif self.targetFreq - self.freq + self.freq_tolerance < 0:
            # On est TRES en dessous de l'intervalle de tolerance
            if self.targetFreq - self.freq + self.freq_tolerance < -20:
                self.motif = 0
            else:
                self.motif = 1

        # On est au dessus de l'intervalle de tolerance
        elif self.targetFreq - self.freq - self.freq_tolerance > 0:
            # On est TRES au dessus de l'intervalle de tolerance
            if self.targetFreq - self.freq - self.freq_tolerance > 20:
                self.motif = 4
            else:
                self.motif = 3

    @staticmethod
    def new_random_user():
        pass
