## Files
* `micro.py`: The swarm-based simulation.
* `macro.py`: The mathematical ODE model which predicts average swarm behavior.
* `swarm.py`:  Swarm features.
* `environment.py`: The 2D space containing the FoodSite class and environment features.

## Run
Run the robot simulation:
```bash
uv run micro.py
```

Plot the math model:
```bash
uv run macro.py
```