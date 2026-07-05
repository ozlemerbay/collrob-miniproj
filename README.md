Simulation of how a swarm of robots chooses between two resources.

## Files
* `micro.py`: The agent-based simulation. Tracks individual robots.
* `macro.py`: The mathematical ODE model. Predicts average swarm behavior.
* `agent.py`: Rules for a single robot (`move`, `discover_resource`, `abandon_opinion`, `communicate_and_switch`).
* `environment.py`: The 2D space containing the `Environment` (agents, resources) and the `Resource` class (quality, alpha, rho, gamma).

## Run

Run the robot simulation:
```bash
uv run micro.py
```

Plot the math model:
```bash
uv run macro.py
```