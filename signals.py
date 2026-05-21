import sys
from scipy import signal
import numpy as np

##return lambda t zwraca f(t) zamiast wartosci

def signal_sin(amp, freq, offset=0):
     print ("clicked harmoniczny")

     return lambda t: amp * np.sin(2 * np.pi * freq * t ) + offset


def signal_square(amp, freq, duty, offset=0):
     print ("clicked prostokatny")
     
     #changes amplitude between 0 and amp
     return lambda t: (amp / 2) * signal.square(2 * np.pi * freq * t, duty=duty) + (amp / 2) + offset

def signal_triangle(amp, freq, offset=0):
     print("clicked trojkatny")

     return lambda t: amp * signal.sawtooth(2 * np.pi * freq * t) + offset