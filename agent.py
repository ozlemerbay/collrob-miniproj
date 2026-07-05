import random
import math

AGENT_SPEED = 1.0
AGENT_SENSING_RADIUS = 2.0
AGENT_COMM_RADIUS = 5.0


class Agent:
    def __init__(self, env, x, y):
        self.env = env
        self.x = x
        self.y = y
        self.preferred_resource = None  # none means undecided

        self.speed = AGENT_SPEED
        self.sensing_radius = AGENT_SENSING_RADIUS
        self.communication_radius = AGENT_COMM_RADIUS

    def move(self):
        angle = random.uniform(0, 2 * math.pi)
        new_x = self.x + math.cos(angle) * self.speed
        new_y = self.y + math.sin(angle) * self.speed

        self.x, self.y = self.env.limit_position(new_x, new_y)

    def abandon_opinion(self):
        if self.preferred_resource is not None:
            if random.random() < self.preferred_resource.gamma:
                self.preferred_resource = None

    def discover_resource(self):
        if self.preferred_resource is None:
            found_resource = self.env.get_resource(self.x, self.y, self.sensing_radius)
            if found_resource is not None:
                if random.random() < found_resource.alpha:
                    self.preferred_resource = found_resource

    def communicate_and_switch(self):
        neighbors = self.env.get_neighbors(self, self.communication_radius)
        if not neighbors:
            return

        neighbor = random.choice(neighbors)
        if self.preferred_resource is None and neighbor.preferred_resource is not None:
            if random.random() < neighbor.preferred_resource.rho:
                self.preferred_resource = neighbor.preferred_resource

    def step(self):
        self.move()
        self.discover_resource()
        self.abandon_opinion()
        self.communicate_and_switch()
