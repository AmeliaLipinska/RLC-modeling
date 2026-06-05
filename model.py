import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def circuit_model(t,x,u,parameters):
    #state-space model

    L, R2,C,R=parameters

    model_A = np.array([[0, 0],[0,-1/C * (1/R + 1/R2)]])

    model_B = np.array([[1/L],[1/C*R2]])

    model_C = np.array([[0,1]])

    model_D = 0

    # x to wekror stanu x=[x1, x2] 
    # gdzie x1=prąd cewki, 
    # x2=napięcie na rezystorze=y(t)

    dxdt = model_A @ x + model_B.flatten() * u
    y = model_C @ x + model_D

    numerator=R / (R + R2)
    denominator=(R * R2 * C) / (R + R2)

    transmittance = numerator/denominator 

    return dxdt, y, transmittance







