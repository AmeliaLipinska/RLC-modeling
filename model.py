import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def circuit_model(L,R2,C,R,x0):
    model_A = [[0,0],[0,-1/C * (1/R + 1/R2)]]

    model_B = [[1/L],[1/(C*R2)]]

    model_C = [0,1]

    model_D = 0

    return







