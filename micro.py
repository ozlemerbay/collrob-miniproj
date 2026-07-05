import random
import matplotlib.pyplot as plt
from environment import Environment, Resource, ENV_WIDTH, ENV_HEIGHT
from agent import Agent

# resource A
RES_A_X, RES_A_Y = 25.0, 25.0
RES_A_ALPHA = 0.1  # detection rate
RES_A_RHO = 0.6  # adoption probability
RES_A_GAMMA = 0.01  # abandonment rate

# resource B
RES_B_X, RES_B_Y = 75.0, 75.0
RES_B_ALPHA = 0.1
RES_B_RHO = 0.3
RES_B_GAMMA = 0.05

# simulation
SWARM_SIZES = [20, 50, 100, 200]
NUM_RUNS_PER_SIZE = 10
SIMULATION_STEPS = 1500
CONSENSUS_THRESHOLD = 0.80


def run_simulation(swarm_size, steps):
    env = Environment()

    res_A = Resource(
        x=RES_A_X,
        y=RES_A_Y,
        alpha=RES_A_ALPHA,
        rho=RES_A_RHO,
        gamma=RES_A_GAMMA,
    )
    res_B = Resource(
        x=RES_B_X,
        y=RES_B_Y,
        alpha=RES_B_ALPHA,
        rho=RES_B_RHO,
        gamma=RES_B_GAMMA,
    )

    env.add_resource(res_A)
    env.add_resource(res_B)

    # initialize agents with random positions
    agents = []
    for _ in range(swarm_size):
        x = random.uniform(0, ENV_WIDTH)
        y = random.uniform(0, ENV_HEIGHT)
        agent = Agent(env, x, y)
        env.add_agent(agent)
        agents.append(agent)

    history = {"A": [], "B": [], "U": []}

    for step in range(steps):
        for agent in agents:
            agent.step()

        count_A = 0
        count_B = 0
        count_U = 0
        for agent in agents:
            if agent.preferred_resource is None:
                count_U += 1
            elif agent.preferred_resource is res_A:
                count_A += 1
            elif agent.preferred_resource is res_B:
                count_B += 1

        history["A"].append(count_A / swarm_size)
        history["B"].append(count_B / swarm_size)
        history["U"].append(count_U / swarm_size)

        if step % 100 == 0:
            pct_A = int(history["A"][-1] * 100)
            pct_B = int(history["B"][-1] * 100)
            pct_U = int(history["U"][-1] * 100)
            print(f"Step {step} | A: {pct_A}% | B: {pct_B}% | U: {pct_U}%")

    return history


def run_experiments():
    sample_histories = {}
    for swarm_size in SWARM_SIZES:
        consensus_steps = []
        correct_decisions = 0

        for run_idx in range(NUM_RUNS_PER_SIZE):
            random.seed(42 + run_idx)
            history = run_simulation(swarm_size, SIMULATION_STEPS)

            if run_idx == 0:
                sample_histories[swarm_size] = history

            final_A = history["A"][-1]
            final_B = history["B"][-1]

            if final_A > final_B and final_A > 0.5:
                correct_decisions += 1

            # check when swarm reaches consensus
            steps_to_consensus = -1
            for step, ratio_A in enumerate(history["A"]):
                if ratio_A >= CONSENSUS_THRESHOLD:
                    steps_to_consensus = step
                    break

            if steps_to_consensus != -1:
                consensus_steps.append(steps_to_consensus)

        accuracy = (correct_decisions / NUM_RUNS_PER_SIZE) * 100.0

        if consensus_steps:
            avg_steps = sum(consensus_steps) / len(consensus_steps)
            step_str = f"{avg_steps:.1f} steps"
        else:
            step_str = "> max steps"

        print(
            f"Swarm Size: {swarm_size} | Avg Steps: {step_str} | Accuracy: {accuracy}%"
        )

    # plots
    t = range(SIMULATION_STEPS)

    for swarm_size in SWARM_SIZES:
        hist = sample_histories[swarm_size]

        plt.figure(figsize=(10, 6))
        plt.plot(t, hist["A"], label="Resource A", color="blue")
        plt.plot(t, hist["B"], label="Resource B", color="red")
        plt.plot(t, hist["U"], label="Undecided", color="gray")

        plt.title(f"Swarm Size: {swarm_size}")
        plt.xlabel("Time")
        plt.ylabel("Percentage")
        plt.ylim(-0.05, 1.05)
        plt.grid(True)
        plt.legend()

        plt.savefig(f"micro_results_{swarm_size}.png")
        plt.close()


if __name__ == "__main__":
    run_experiments()
