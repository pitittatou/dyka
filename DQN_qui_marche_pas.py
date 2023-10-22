import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

# Créer un environnement personnalisé pour simuler les préférences de l'utilisateur
class UserPreferenceEnv:
    def __init__(self, user_type):
        self.user_type = user_type
        self.bpm = 100
        self.intensity = 100

    def step(self, action):
        if self.user_type == 1:
            if action == 0:  # Diminuer l'intensité
                self.bpm -= 5
            else:  # Augmenter l'intensité
                self.bpm += 5
        else:
            if action == 0:  # Diminuer l'intensité
                self.bpm += 5
            else:  # Augmenter l'intensité
                self.bpm -= 5

        self.bpm = np.clip(self.bpm, 60, 160)
        self.intensity = np.clip(self.intensity, 60, 160)
        state = (self.bpm, self.intensity)
        return state

    def reset(self):
        self.bpm = 100
        self.intensity = 100
        return (self.bpm, self.intensity)

# Créer l'environnement pour les utilisateurs de type 1 et 2
env_user_type_1 = UserPreferenceEnv(user_type=1)
env_user_type_2 = UserPreferenceEnv(user_type=2)

# Créer le modèle d'apprentissage par renforcement
model = keras.Sequential([
    keras.layers.Input(shape=(2,)),  # Deux états : BPM et intensité
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(2, activation='linear')  # Deux actions : diminuer, augmenter
])

optimizer = keras.optimizers.Adam(learning_rate=0.001)
model.compile(optimizer=optimizer, loss='mean_squared_error')

# Fonction pour choisir une action en utilisant epsilon-greedy
def choose_action(state, epsilon=0.1):
    if np.random.rand() < epsilon:
        return np.random.choice(2)  # Exploration aléatoire entre deux actions (0, 1)
    else:
        q_values = model.predict(np.array(state).reshape(1, -1))[0]
        return np.argmax(q_values)

# Fonction d'apprentissage par renforcement
def train_rl_model(env, num_episodes, epsilon=0.1, discount_factor=0.9):
    for _ in range(num_episodes):
        state = env.reset()
        total_reward = 0

        for _ in range(50):  # Nombre maximal d'étapes par épisode
            action = choose_action(state, epsilon)
            next_state = env.step(action)

            target = state[0] - next_state[0]  # Récompense basée sur la différence de BPM
            q_values = model.predict(np.array(state).reshape(1, -1))
            q_values[0][action] = target
            model.fit(np.array(state).reshape(1, -1), q_values, epochs=1, verbose=0)

            total_reward += target
            state = next_state

train_rl_model(env_user_type_1, num_episodes=10)
train_rl_model(env_user_type_2, num_episodes=10)

# Fonction pour afficher les performances
def plot_performance(user_type, num_steps=100):  # Modifier le nombre de pas ici
    bpm_values = []
    intensity_values = []

    for step in range(num_steps):  # Utilisez le nombre fixe de pas ici
        state = env_user_type_1.reset() if user_type == 1 else env_user_type_2.reset()

        while step < num_steps:
            action = choose_action(state, epsilon=0)  # Pas d'exploration
            state = env_user_type_1.step(action) if user_type == 1 else env_user_type_2.step(action)
            bpm_values.append(state[0])
            intensity_values.append(state[1])
            step += 1  # Incrémenter le nombre d'étapes

    plt.plot(bpm_values, label="BPM")
    plt.plot(intensity_values, label="Intensité")
    plt.xlabel("Pas")
    plt.title(f"Performance pour le Type d'Utilisateur {user_type}")
    plt.legend()
    plt.show()

# Afficher les performances pour les deux types d'utilisateurs
plot_performance(1, num_steps=100)  # Spécifier le nombre de pas
plot_performance(2, num_steps=100)  # Spécifier le nombre de pas
