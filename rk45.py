import numpy as np

tol = 1e-6 #tolerancja
s = 0.9 #współczynnik bezpieczeństwa
p = 4 #rząd metody niższej

def model(t,x,u,parameters):
    #parameters = [L,R2,C,R]
    L, R2, C, R = parameters
    
    model_A = np.array([[0,-1/L],[1/C,-1/C * (1/R + 1/R2)]])
    model_B = np.array([[1/L],[0]])

    #x~ = A*x + B*u
    dxdt = model_A @ x + model_B.flatten() * u
    
    return dxdt

def new_h(h,error):
    hnew = s*h*(tol/abs(np.linalg.norm(error)))**(1/(p+1))
    hnew = min(hnew,0.01) #dodatkowe ograniczenie
    
    return hnew

def rk45_step(t,x,h,u,parameters):
    #parameters = [L,R2,C,R]
    k1 = model(t,x,u(t), parameters)

    k2 = model(t + h/5 ,x + h/5*k1, u(t+ h/5), parameters)

    k3 = model(t + 3/10*h, x + h*(3/40*k1 + 9/40*k2), u(t + 3/10*h), parameters)

    k4 = model(t + 4/5*h, x + h*(44/45*k1 - 56/15*k2 +32/9*k3), u(t + 4/5*h), parameters)

    k5 = model(t + 8/9*h, x + h*(19372/6561*k1 - 25360/2187*k2 + 64448/6561*k3 - 212/729*k4), u(t + 8/9*h), parameters)

    k6 = model(t + h, x + h*(9017/3168*k1 - 355/33*k2 + 46732/5247*k3 + 49/176*k4 - 5103/18656*k5), u(t + h), parameters)

    k7 = model(t + h, x + h*(35/384*k1 + 500/1113*k3 + 125/192*k4 - 2187/6784*k5 + 11/84*k6), u(t + h), parameters)

    x_5 = x + h*(35/384*k1 + 500/1113*k3 + 125/192*k4 - 2187/6784*k5 + 11/84*k6)

    x_4 = x + h*(5179/57600*k1 + 7571/16695*k3 + 393/640*k4 - 92097/339200*k5 + 187/2100*k6 + 1/40*k7)
    
    error_comp = x_5 - x_4
    
    return x_5, error_comp