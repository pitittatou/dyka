import serial
import time

port = 'COM3'
baudrate = 9600

# Initialise la connexion série
arduino = serial.Serial(port, baudrate, timeout=1)

# Attendez que la connexion soit établie
time.sleep(2)

def regler_intensite(valeur):
    # Envoyer la valeur à l'Arduino
    arduino.write(f'{valeur}\n'.encode())
    print(f'Intensité réglée à {valeur}')

while(True):
    #regler_intensite(input("Quelle valeur de vibration ? [0,255] : "))
    for i in range(20,255):
        regler_intensite(i)

# Ferme la connexion série
arduino.close()