import math

ENV_WIDTH = 100.0
ENV_HEIGHT = 100.0


class Resource:
    def __init__(self, x, y, alpha, rho, gamma):
        self.x = x
        self.y = y
        self.alpha = alpha
        self.rho = rho
        self.gamma = gamma


class Environment:
    def __init__(self, width=ENV_WIDTH, height=ENV_HEIGHT):
        self.width = width
        self.height = height
        self.resources = []
        self.agents = []

    def add_resource(self, resource):
        self.resources.append(resource)

    def add_agent(self, agent):
        self.agents.append(agent)

    def get_resource(self, x, y, sensing_radius):
        """get the closes resource"""
        closest_res = None
        min_dist = float("inf")
        for res in self.resources:
            dist = math.hypot(res.x - x, res.y - y)
            if dist <= sensing_radius and dist < min_dist:
                closest_res = res
                min_dist = dist
        return closest_res

    def get_neighbors(self, agent, communication_radius):
        """get list of neighbors"""
        neighbors = []
        for curr_agent in self.agents:
            if curr_agent is agent:
                continue

            dist = math.hypot(curr_agent.x - agent.x, curr_agent.y - agent.y)
            if dist <= communication_radius:
                neighbors.append(curr_agent)
        return neighbors

    def limit_position(self, x, y):
        """keep position within bounds"""
        limited_x = max(0.0, min(x, self.width))
        limited_y = max(0.0, min(y, self.height))
        return limited_x, limited_y
