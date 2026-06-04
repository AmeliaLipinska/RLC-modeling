import sys
from scipy import signal
import numpy as np

##return lambda t zwraca f(t) zamiast wartosci

def signal_sin(amp, freq, offset=0):
     print ("clicked harmoniczny")

     return lambda t: amp * np.sin(2 * np.pi * freq * t ) + offset


def signal_square(amp, freq, duty, start_time, offset=0):
     print ("clicked prostokatny")
     
     duration = duty/freq
     end_time = start_time + duration

     #changes amplitude between 0 and amp
     def logic(t):
          return np.where(
               (t >= start_time) & (t <= end_time),
               amp,
               offset
          )
     return logic

def signal_triangle(amp, freq, offset=0):
     print("clicked trojkatny")

     return lambda t: amp * signal.sawtooth(2 * np.pi * freq * t, width=0.5) + offset