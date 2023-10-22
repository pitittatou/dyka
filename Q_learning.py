import random
import matplotlib.pyplot as plt

# Définition de l'environnement
num_actions = 2  # Actions : "augmenter l'intensité" (1) et "diminuer l'intensité" (0)
num_users = 2    # Deux types d'utilisateurs (0 et 1)

# Initialisation du Q-table (état-action)
q_table = {}
for user_id in range(num_users):
    q_table[user_id] = {}
    q_table[user_id][80] = [0] * num_actions  # Les BPM commencent à 80
    for bpm in range(60, 180, 5):
        q_table[user_id][bpm] = [0] * num_actions

# Définition des paramètres du Q-learning
alpha = 0.1  # Taux d'apprentissage
gamma = 0.9  # Facteur de réduction
epsilon = 0.2  # Probabilité d'exploration

# Fonction pour choisir une action en utilisant epsilon-greedy
def choose_action(user_id, current_bpm):
    if random.uniform(0, 1) < epsilon:
        return random.randint(0, num_actions - 1)  # Exploration
    else:
        return q_table[user_id][current_bpm].index(max(q_table[user_id][current_bpm]))  # Exploitation

# Fonction pour obtenir le prochain état en fonction de l'action choisie
def get_next_state(user_id, current_bpm, action, current_intensity):
    next_bpm = current_bpm

    if user_id == 0:
        if action == 1:  # Action : Augmenter l'intensité
            next_bpm = max(current_bpm - 5, 60)
    elif user_id == 1:
        if action == 1:  # Action : Augmenter l'intensité
            next_bpm = min(current_bpm + 5, 160)

    # next_bpm doit rester dans la plage souhaitée (60-180)
    next_bpm = max(60, min(180, next_bpm))

    # La valeur de l'intensité change déterministiquement
    next_intensity = current_intensity + 5 if action == 1 else current_intensity - 5
    next_intensity = max(60, min(180, next_intensity))

    return next_bpm, next_intensity, user_id

# Fonction pour calculer la récompense en fonction du prochain état
def get_reward(user_id, current_bpm, next_bpm):
    if next_bpm > current_bpm:
        return 1  # Récompense de +1 si les BPM augmentent
    elif next_bpm < current_bpm:
        return -1  # Récompense de -1 si les BPM diminuent
    else:
        return 0

# Entraînement du modèle
num_episodes = 10000
for episode in range(num_episodes):
    user_id = random.randint(0, 1)
    current_bpm = 80  # Les BPM commencent à 80
    current_intensity = 100  # Intensité initiale
    for _ in range(5):  # 5 actions par épisode
        action = choose_action(user_id, current_bpm)
        next_bpm, next_intensity, next_user_id = get_next_state(user_id, current_bpm, action, current_intensity)
        reward = get_reward(user_id, current_bpm, next_bpm)
        
        # Mise à jour de la variable current_bpm pour refléter le nouveau BPM
        current_bpm = next_bpm
        
        # Vérifie si next_bpm existe dans le Q-table,
        if next_bpm not in q_table[user_id]:
            q_table[user_id][next_bpm] = [0] * num_actions
        
        # Met à jour le Q-table
        q_table[user_id][current_bpm][action] += alpha * (reward + gamma * max(q_table[next_user_id][next_bpm]) - q_table[user_id][current_bpm][action])
        current_intensity, user_id = next_intensity, next_user_id

# Fonction pour simuler l'évolution des BPM en fonction des actions
def simulate_bpm_change(user_id, current_bpm, action, current_intensity):
    next_bpm, next_intensity, next_user_id = get_next_state(user_id, current_bpm, action, current_intensity)
    reward = get_reward(user_id, current_bpm, next_bpm)
    return next_bpm, reward, next_intensity

# Variables pour stocker les résultats
user0_bpm = []
user0_intensity = []
user0_rewards = []
user1_bpm = []
user1_intensity = []
user1_rewards = []

# Intensité initiale pour les graphiques
user0_intensity_value = 100
user1_intensity_value = 100
current_bpm_user0 = 80
current_bpm_user1 = 80

# Test du modèle sur les utilisateurs
for _ in range(1000):  # Simuler 1000 étapes
    user_id = random.randint(0, 1)
    action = choose_action(user_id, current_bpm_user0 if user_id == 0 else current_bpm_user1)

    if user_id == 0:
        user0_bpm.append(current_bpm_user0)
        user0_intensity.append(user0_intensity_value)
        user0_rewards.append(q_table[user_id][current_bpm_user0][action])
        current_bpm_user0, reward, user0_intensity_value = simulate_bpm_change(user_id, current_bpm_user0, action, user0_intensity_value)
        user0_rewards[-1] = reward
    else:
        user1_bpm.append(current_bpm_user1)
        user1_intensity.append(user1_intensity_value)
        user1_rewards.append(q_table[user_id][current_bpm_user1][action])
        current_bpm_user1, reward, user1_intensity_value = simulate_bpm_change(user_id, current_bpm_user1, action, user1_intensity_value)
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

