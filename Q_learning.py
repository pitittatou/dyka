import random
import matplotlib.pyplot as plt

# Définition de l'environnement
num_actions = 2  
num_users = 2   

# Initialisation du Q-table (état-action)
q_table = {}
for user_id in range(num_users):
    q_table[user_id] = {}
    for bpm in range(60, 161, 10):
        q_table[user_id][bpm] = [0] * num_actions

alpha = 0.1  
gamma = 0.9  
epsilon = 0.2  

# Fonction pour choisir une action en utilisant epsilon-greedy
def choose_action(user_id, current_bpm):
    if random.uniform(0, 1) < epsilon:
        return random.randint(0, num_actions - 1)  # Exploration
    else:
        return q_table[user_id][current_bpm].index(max(q_table[user_id][current_bpm]))  # Exploitation

# Fonction pour obtenir le prochain état en fonction de l'action choisie
def get_next_state(user_id, current_bpm, action, current_intensity):
    next_bpm = max(min(current_bpm + random.choice([-5, 5]), 160), 60)
    next_intensity = max(min(current_intensity + random.choice([-5, 5]), 160), 60)
    return next_bpm, next_intensity, user_id  # Ajout de l'état de l'utilisateur et de l'intensité

# Fonction pour calculer la récompense en fonction du prochain état
def get_reward(user_id, current_bpm, next_bpm):
    if next_bpm > current_bpm:
        return 1  # Récompense de +1 si les BPM augmentent
    elif next_bpm < current_bpm:
        return -1  # Récompense de -1 si les BPM diminuent
    else:
        return 0

# Entraînement du modèle
num_episodes = 1000
for episode in range(num_episodes):
    user_id = random.randint(0, 1)
    current_bpm = random.choice(list(q_table[user_id].keys()))
    current_intensity = 100  # Intensité initiale
    for _ in range(5):  
        action = choose_action(user_id, current_bpm)
        next_bpm, next_intensity, next_user_id = get_next_state(user_id, current_bpm, action, current_intensity)
        reward = get_reward(user_id, current_bpm, next_bpm)
        
        # Vérifie si next_bpm existe dans le Q-table
        if next_bpm not in q_table[user_id]:
            q_table[user_id][next_bpm] = [0] * num_actions
        
        # Met à jour le Q-table
        q_table[user_id][current_bpm][action] += alpha * (reward + gamma * max(q_table[next_user_id][next_bpm]) - q_table[user_id][current_bpm][action])
        current_bpm, current_intensity, user_id = next_bpm, next_intensity, next_user_id

# simuler l'évolution des BPM en fonction des actions
def simulate_bpm_change(user_id, current_bpm, action, current_intensity):
    next_bpm, next_intensity, next_user_id = get_next_state(user_id, current_bpm, action, current_intensity)
    reward = get_reward(user_id, current_bpm, next_bpm)
    return next_bpm, reward, next_intensity


user0_bpm = []
user0_intensity = []
user0_rewards = []
user1_bpm = []
user1_intensity = []
user1_rewards = []

# Intensité initiale 
user0_intensity_value = 100
user1_intensity_value = 100

intensity_variation = []  

# Test du modèle sur les utilisateurs
for _ in range(100):  
    user_id = random.randint(0, 1)
    current_bpm = random.choice(list(q_table[user_id].keys()))
    action = choose_action(user_id, current_bpm)

    if user_id == 0:
        user0_bpm.append(current_bpm)
        if intensity_variation:  # Vérifiez si la liste n'est pas vide
            user0_intensity.append(intensity_variation.pop(0))
        else:
            user0_intensity.append(user0_intensity_value)  # Utilisez la dernière valeur
        user0_rewards.append(q_table[user_id][current_bpm][action])
        current_bpm, reward, user0_intensity_value = simulate_bpm_change(user_id, current_bpm, action, user0_intensity_value)
        user0_rewards[-1] = reward
    else:
        user1_bpm.append(current_bpm)
        if intensity_variation:  
            user1_intensity.append(intensity_variation.pop(0))
        else:
            user1_intensity.append(user1_intensity_value)  
        user1_rewards.append(q_table[user_id][current_bpm][action])
        current_bpm, reward, user1_intensity_value = simulate_bpm_change(user_id, current_bpm, action, user1_intensity_value)
        user1_rewards[-1] = reward

# Affichage des résultats
plt.figure(figsize=(10, 6))
plt.subplot(211)
plt.plot(user0_bpm, label='BPM')
plt.plot(user0_intensity, label='Intensité')
plt.plot(user0_rewards, label='Récompenses')
plt.title('Utilisateur 0')
plt.legend()

plt.subplot(212)
plt.plot(user1_bpm, label='BPM')
plt.plot(user1_intensity, label='Intensité')
plt.plot(user1_rewards, label='Récompenses')
plt.title('Utilisateur 1')
plt.legend()

plt.tight_layout()
plt.show()
