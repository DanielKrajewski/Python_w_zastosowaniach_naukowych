import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.animation import FuncAnimation
import IPython.display as display

def sir_model(y, t, beta, gamma):
    S, I, R = y
    dS_dt = -beta * S * I
    dI_dt = beta * S * I - gamma * I
    dR_dt = gamma * I
    return [dS_dt, dI_dt, dR_dt]

def simulate_sir(beta, gamma, S0, I0, R0, t_max):
    
    dt = 0.1 
    t = np.arange(0, t_max + dt, dt)

    y0 = [S0, I0, R0]

    solution = odeint(sir_model, y0, t, args=(beta, gamma))
    S, I, R = solution.T

    return S, I, R, t

def plot_sir(t, S, I, R , gamma,beta):
    plt.figure(figsize=(10, 6))
    plt.plot(t, S, label='Susceptible', color='blue')
    plt.plot(t, I, label='Infected', color='red')
    plt.plot(t, R, label='Removed', color='green')
    plt.xlabel('Time')
    plt.ylabel('Population Fraction')
    plt.title('SIR Model Simulation: gamma = {}'.format(gamma) + ' beta = {}'.format(beta))
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":

    beta = 0.3
    gamma = 0.1
    S0 = 0.99
    I0 = 0.01
    R0 = 0.0
    t_max = 100

    S, I, R, t = simulate_sir(beta, gamma, S0, I0, R0, t_max)
    plot_sir(t, S, I, R, gamma, beta)
    gamma =  0.3
    S, I, R, t = simulate_sir(beta, gamma, S0, I0, R0, t_max)
    plot_sir(t, S, I, R, gamma, beta)
        