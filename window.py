import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Window():
    def __init__(self, demo):
        self.demo = demo

        self.root = tk.Tk()
        self.root.title('Deeka')

        self.fig, (self.fig1, self.fig2) = plt.subplots(1, 2)

        self.line1, = self.fig1.plot([], [])
        self.fig1.set_title('Fréquence de vibration')
        self.fig1.set_xlabel('Temps (s)')
        self.fig1.set_ylabel('Fréquence de vibration (Hz)')

        self.line2, = self.fig2.plot([], [])
        self.fig2.set_title('Fréquence cardiaque')
        self.fig2.set_xlabel('Temps (s)')
        self.fig2.set_ylabel('Fréquence cardiaque (bpm)')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.button = tk.Button(self.root, text='Continuer', command=self.demo.button_pressed)
        self.button.pack()

    def update_figs(self, heart_rates, vibro_freqs):
        x = np.arange(len(vibro_freqs))
        self.line1.set_data(x, vibro_freqs)
        self.line2.set_data(x, heart_rates)

        self.fig1.relim()
        self.fig2.relim()
        self.fig1.autoscale_view()
        self.fig2.autoscale_view()

        self.fig.canvas.draw()
