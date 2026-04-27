import sys
from scipy import signal
import numpy as np

##return lambda t zwraca f(t) zamiast wartosci

def signal_sin(amp, freq, offset=0):
     print ("clicked harmoniczny")

     return lambda t: amp * np.sin(2 * np.pi * freq * t ) + offset


def signal_square(amp, freq, duration, offset=0):
     print ("clicked prostokatny")
     
     def logic(t):
          return np.where(
               t <= duration,
               (amp * signal.square(2 * np.pi * freq * t, duty = 0.5) + offset),
               offset
          )
     return logic

def signal_triangle(amp, freq, offset=0):
     print("clicked trojkatny")

     return lambda t: amp * signal.sawtooth(2 * np.pi * freq * t) + offset