import MAB.NonStationaryMAB as NSMAB
from demo import Demo
from sim.constants import *
from sim.user import UserMAB

ARDUINO_CONNECTED = False
IT_PER_CLICK = 20


def main():
    user = UserMAB(base_heart_rate=70, max_heart_rate=150, max_increase=0.15, max_decrease=0.15)
    bandit = NSMAB.NArmedBandit(arms=NB_MOTIF, step_size=0.2, eps=0.1, UCB_c=2, sample_avg_flag=False, init_estimates=0.0, mu=0, std_dev=1, thomsonSample=False)

    demo = Demo(user, bandit, IT_PER_CLICK, ARDUINO_CONNECTED)
    demo.run()


if __name__ == '__main__':
    main()
