import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def circuit_model(t,x,u,parameters):
    #state-space model

    L, R2,C,R=parameters

    model_A = np.array([[0,-1/L],[1/C,-1/C * (1/R + 1/R2)]])

    model_B = np.array([[1/L],[0]])

    model_C = np.array([[0,1]])

    model_D = 0

    # x to wekror stanu x=[x1, x2] 
    # gdzie x1=prąd cewki, 
    # x2=napięcie na rezystorze=y(t)

    # @-operator mnożenia macierzy 

    dxdt = model_A @ x + model_B.flatten() * u
    y = model_C @ x + model_D

    #transmittance G(s)

    #numerator = R
    #denominator = [C*R*R2,R2+R]
    numerator=2
    denominator=2

    transmittance = numerator/denominator #do poprawki


    return dxdt, y, transmittance







