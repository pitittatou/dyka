import time
import serial

from window import Window


class Demo():
    def __init__(self, user, bandit, it_per_click, arduino_connected):
        self.user = user
        self.bandit = bandit
        self.window = Window(self)
        self.next = False
        self.it_per_click = it_per_click

        if arduino_connected:
            self.arduino = serial.Serial('COM3', 9600, timeout=1)
            time.sleep(2)
        else:
            self.arduino = None


    def button_pressed(self):
        self.next = True


    def run(self):
        heart_rates = []
        vibro_freqs = []
        i = 0

        while(True):
            # Wait for button press
            if i % self.it_per_click == 0:
                while not self.next:
                    self.window.root.update()
                    if self.arduino:
                        self.arduino.write(f'{self.user.freq}\n'.encode())
                self.next = False

            prev_hr = self.user.get_state()
            action = self.bandit.act()
            new_hr = self.user.get_next_state(action)
            reward = new_hr - prev_hr

            if reward == 0:
                if new_hr == self.user.max_heart_rate:
                    reward = 10
                elif new_hr == self.user.min_heart_rate:
                    reward = -10

            self.bandit.step(action, reward)

            heart_rates.append(new_hr)
            vibro_freqs.append(self.user.freq)
            self.window.update_figs(heart_rates, vibro_freqs)

            if self.arduino:
                self.arduino.write(f'{self.user.freq}\n'.encode())

            i += 1
