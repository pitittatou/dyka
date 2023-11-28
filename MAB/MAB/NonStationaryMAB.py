import numpy as np
import csv
from scipy.stats import beta
import matplotlib.pyplot as plt
from sim.constants import *

class NArmedBandit:

    #10-armed bandit testbed with sample averages 
    def __init__(self,arms=NB_MOTIF,step_size = 0.1,eps = 0,UCB_c = None, sample_avg_flag = False,init_estimates = 0.0,mu = 0, std_dev = 1, thomsonSample = False):

        self.arms = arms  #number of arms
        self.step_size = step_size  #constant step size
        self.eps = eps  #probability of exploration
        self.init_estimates = init_estimates    #initial estimates for each action
        self.mu = mu    #true mean for each action
        self.std_dev = std_dev  #standard deviation for each action
        self.actions = np.zeros(arms)  #true values of rewards for each action
        self.successes = np.array([ 0 for _ in range(NB_MOTIF)]) #Keep tracks of all the successes for each action
        self.failures = np.array([ 0 for _ in range(NB_MOTIF)]) # Keep tracks of all the failures for each action
        self.true_reward = 0.0  #average reward with non-stationary
        self.UCB_c = UCB_c  #exploration parameter for UCB
        self.sample_avg_flag = sample_avg_flag  #if true, use sample averages to update estimates instead of constant step size
        self.thomsonSample = thomsonSample
        self.re_init()


    def re_init(self):

        #true values of rewards for each action
        self.actions = np.random.normal(self.mu,self.std_dev,self.arms) 
      

        # estimation for each action
        self.Q_t = np.zeros(self.arms) + self.init_estimates
        

        # num of chosen times for each action
        self.N_t = np.zeros(self.arms)

        #best action chosen
        self.optim_action = np.argmax(self.actions)

        self.time_step = 0


    def act(self):
        
        # Version UCB
        if self.thomsonSample == False :
            #1e-5 is added so as to avoid division by zero
            ucb_estimates = self.Q_t + self.UCB_c * np.sqrt(np.log(self.time_step + 1) / (self.N_t + 1e-5))
            A_t = np.max(ucb_estimates)
            action = np.random.choice(np.where(ucb_estimates == A_t)[0])
            return action
        
        else : 
            # Version Thomson Sampling
            beta_samples = np.random.beta(self.successes + 1, self.failures + 1)
            action = np.argmax(beta_samples)

            if self.time_step % 10000 ==0 and self.time_step != 0:
                # Créer un tableau de valeurs x pour lesquelles nous calculerons la PDF
                x = np.linspace(0, 1, 1000)

                # Tracer la PDF pour chaque distribution bêta
                for i in range(NB_MOTIF):
                    y = beta.pdf(x, self.successes[i] + 1, self.failures[i] + 1)
                    plt.plot(x, y, label=f'Action {i+1}')

                plt.title('Beta Distributions')
                plt.xlabel('Value')
                plt.ylabel('Density')
                plt.legend()

                plt.show()
            return action



    def step(self,action, reward):

        # generating the reward under N(real reward, 1)
        #reward = np.random.randn() + self.actions[action]
        reward = reward
        self.time_step += 1
        self.N_t[action] += 1

        if reward < 0 :
            self.failures[action] += 1
        else :
            self.successes[action] += 1


        # estimation with sample averages
        if self.sample_avg_flag == True:
            self.Q_t[action] += (reward - self.Q_t[action]) / self.N_t[action]
        else:
            # non-staationary with constant step size 
            self.Q_t[action] += self.step_size * (reward - self.Q_t[action])

        with open('output.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            # Écriture des valeurs de Q_t dans le fichier
            writer.writerow(self.Q_t)

"""

def play(bandit,tasks,num_time_steps):
        rewards = np.zeros((tasks, num_time_steps))
        print("rewards : ",rewards)
        optim_action_counts = np.zeros(rewards.shape)
        for task in range(tasks):
            bandit.re_init()
            for t in range(num_time_steps):
                action = bandit.act()
                reward = bandit.step(action)
                rewards[task, t] = reward
                if action == bandit.optim_action:
                    optim_action_counts[task, t] = 1
        avg_optim_action_counts = optim_action_counts.mean(axis=0)
        avg_rewards = rewards.mean(axis=0)
        return avg_optim_action_counts, avg_rewards

"""


   