import random
import matplotlib.pyplot as plt
from environment import GridWorld, FoodSite, ENV_WIDTH, ENV_HEIGHT
from swarm import SwarmAnt

# resource A (good quality)
A_POS_X, A_POS_Y = 25.0, 25.0
A_ALPHA = 0.1  # detection rate
A_RHO = 0.6  # adoption probability
A_GAMMA = 0.01  # abandonment rate

# resource B (bad quality)
B_POS_X, B_POS_Y = 75.0, 75.0
B_ALPHA = 0.1
B_RHO = 0.3
B_GAMMA = 0.05

# test configuration
TEST_COUNTS = [20, 50, 100, 200]
REPETITIONS = 10
MAX_STEPS = 1500
AGREE_LIMIT = 0.80


def do_swarm_sim(num_ants, total_steps):
    world = GridWorld()

    # spawn the food
    good_food = FoodSite(A_POS_X, A_POS_Y, A_ALPHA, A_RHO, A_GAMMA)
    bad_food = FoodSite(B_POS_X, B_POS_Y, B_ALPHA, B_RHO, B_GAMMA)

    world.put_food(good_food)
    world.put_food(bad_food)

    # scatter the ants randomly around the box
    bug_list = []
    for _ in range(num_ants):
        spawn_x = random.uniform(0, ENV_WIDTH)
        spawn_y = random.uniform(0, ENV_HEIGHT)
        new_ant = SwarmAnt(world, spawn_x, spawn_y)
        world.put_ant(new_ant)
        bug_list.append(new_ant)

    # tracking lists for the plot
    tracker = {"A": [], "B": [], "U": []}

    for step_num in range(total_steps):
        # everybody moves and talks
        for bug in bug_list:
            bug.tick()

        # count up what everyone is thinking right now
        c_a = 0
        c_b = 0
        c_u = 0
        for bug in bug_list:
            if bug.current_idea is None:
                c_u += 1
            elif bug.current_idea is good_food:
                c_a += 1
            elif bug.current_idea is bad_food:
                c_b += 1

        # save the fractions
        tracker["A"].append(c_a / num_ants)
        tracker["B"].append(c_b / num_ants)
        tracker["U"].append(c_u / num_ants)

        # print so I can see the process
        if step_num % 100 == 0:
            print(
                f"Step {step_num} -> A: {int((c_a / num_ants) * 100)}% | B: {int((c_b / num_ants) * 100)}%"
            )

    return tracker


def main_experiment_loop():
    saved_graphs = {}

    for ant_count in TEST_COUNTS:
        steps_taken_list = []
        wins = 0

        for run_id in range(REPETITIONS):
            # lock the seed so the plots look the same every time I run it
            random.seed(42 + run_id)

            run_data = do_swarm_sim(ant_count, MAX_STEPS)

            # save the first run of the 10 for the plot images
            if run_id == 0:
                saved_graphs[ant_count] = run_data

            end_a = run_data["A"][-1]
            end_b = run_data["B"][-1]
            if end_a > end_b and end_a > 0.5:
                wins += 1

            # find how fast they reached the threshold
            finished_at = -1
            for idx, a_ratio in enumerate(run_data["A"]):
                if a_ratio >= AGREE_LIMIT:
                    finished_at = idx
                    break

            if finished_at != -1:
                steps_taken_list.append(finished_at)

        # find the averages for the report table
        win_rate = (wins / REPETITIONS) * 100.0

        # print to see the process
        if steps_taken_list:
            average_time = sum(steps_taken_list) / len(steps_taken_list)
            time_text = f"{average_time:.1f} steps"
        else:
            time_text = "> max steps"

        print(f"\n--- Swarm Size {ant_count} ---")
        print(f"Average Time: {time_text} | Accuracy: {win_rate}%\n")

    # generate the png files for report
    time_x = range(MAX_STEPS)

    for ant_count in TEST_COUNTS:
        data = saved_graphs[ant_count]

        plt.figure(figsize=(10, 6))
        plt.plot(time_x, data["A"], label="Resource A", color="blue")
        plt.plot(time_x, data["B"], label="Resource B", color="red")
        plt.plot(time_x, data["U"], label="Undecided", color="gray")

        plt.title(f"Microscopic Results (Size: {ant_count} agents)")
        plt.xlabel("Simulation Steps")
        plt.ylabel("Swarm Percentage")
        plt.ylim(-0.05, 1.05)
        plt.grid(True)
        plt.legend()

        file_name = f"micro_results_{ant_count}.png"
        plt.savefig(file_name)
        plt.close()


if __name__ == "__main__":
    main_experiment_loop()
