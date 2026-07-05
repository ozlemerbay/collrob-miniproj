import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# resource A
ALPHA_A = 0.1
RHO_A = 0.6
GAMMA_A = 0.01

# resource B
ALPHA_B = 0.1
RHO_B = 0.3
GAMMA_B = 0.05

# simulation
SIMULATION_TIME = 50


def collective_decision_model(
    population_fractions, t, alpha_A, rho_A, gamma_A, alpha_B, rho_B, gamma_B
):
    fraction_A, fraction_B = population_fractions
    fraction_U = 1.0 - fraction_A - fraction_B

    rate_of_change_A = (
        alpha_A * fraction_U + rho_A * fraction_A * fraction_U - gamma_A * fraction_A
    )
    rate_of_change_B = (
        alpha_B * fraction_U + rho_B * fraction_B * fraction_U - gamma_B * fraction_B
    )

    return [rate_of_change_A, rate_of_change_B]


def run_macroscopic_model(simulation_time):
    initial_fractions = [0.0, 0.0]
    t = np.linspace(0, simulation_time, 1000)

    solution = odeint(
        collective_decision_model,
        initial_fractions,
        t,
        args=(ALPHA_A, RHO_A, GAMMA_A, ALPHA_B, RHO_B, GAMMA_B),
    )

    history_A = solution[:, 0]
    history_B = solution[:, 1]
    history_U = 1.0 - history_A - history_B

    plt.figure(figsize=(10, 6))
    plt.plot(t, history_A, label="Resource A", color="blue")
    plt.plot(t, history_B, label="Resource B", color="red")
    plt.plot(t, history_U, label="Undecided", color="gray")
    plt.xlabel("Time")
    plt.ylabel("Percentage of Swarm")
    plt.title("ODE Model: Swarm Decision Making")
    plt.legend()
    plt.grid(True)
    plt.ylim(-0.05, 1.05)
    plt.savefig("macro_results.png")


if __name__ == "__main__":
    run_macroscopic_model(SIMULATION_TIME)
