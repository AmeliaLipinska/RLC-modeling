import numpy as np

def model(t,x,u,parameters):
    L, R2, C, R = parameters
    
    model_A = np.array([[0,0],[0,-1/C * (1/R + 1/R2)]])
    model_B = np.array([[1/L],[1/(C*R2)]])

    dxdt = model_A @ x + model_B.flatten() * u
    
    return dxdt

def rk4_step(t, x, h, u, parameters):
    k1 = model(t,           x,                 u(t),         parameters)
    k2 = model(t + h/2,     x + h/2 * k1,      u(t + h/2),   parameters)
    k3 = model(t + h/2,     x + h/2 * k2,      u(t + h/2),   parameters)
    k4 = model(t + h,       x + h   * k3,      u(t + h),     parameters)

    x_next = x + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
    return x_next