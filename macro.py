import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# setup values from my report experimental setup
# resource A (High Quality)
A_DISCOVER = 0.1
A_ADOPT = 0.6
A_FORGET = 0.01

# resource B (Low Quality)
B_DISCOVER = 0.1
B_ADOPT = 0.3
B_FORGET = 0.05

TOTAL_TIME = 50


def ode_math_model(
    fractions, time_t, a_disc, a_adopt, a_forget, b_disc, b_adopt, b_forget
):
    # unpack the current values
    frac_a, frac_b = fractions
    frac_u = 1.0 - frac_a - frac_b  # the rest are undecided

    # calculating the derivatives based on Lerman 2002 rate equations
    change_a = (a_disc * frac_u) + (a_adopt * frac_a * frac_u) - (a_forget * frac_a)
    change_b = (b_disc * frac_u) + (b_adopt * frac_b * frac_u) - (b_forget * frac_b)

    return [change_a, change_b]


def solve_and_plot_ode(max_time):
    start_vals = [0.0, 0.0]  # nobody has an opinion at t=0

    # create 1000 smooth points for the chart
    time_points = np.linspace(0, max_time, 1000)

    # run the solver
    results = odeint(
        ode_math_model,
        start_vals,
        time_points,
        args=(A_DISCOVER, A_ADOPT, A_FORGET, B_DISCOVER, B_ADOPT, B_FORGET),
    )

    # slice out the columns
    history_a = results[:, 0]
    history_b = results[:, 1]
    history_u = 1.0 - history_a - history_b

    # draw the plot
    plt.figure(figsize=(10, 6))
    plt.plot(time_points, history_a, label="Resource A", color="blue")
    plt.plot(time_points, history_b, label="Resource B", color="red")
    plt.plot(time_points, history_u, label="Undecided", color="gray")

    plt.xlabel("Time")
    plt.ylabel("Percentage of Swarm")
    plt.title("Macroscopic ODE Model Results")
    plt.legend()
    plt.grid(True)
    plt.ylim(-0.05, 1.05)

    # save it so I can put it in the latex report
    plt.savefig("macro_results.png")


if __name__ == "__main__":
    solve_and_plot_ode(TOTAL_TIME)
