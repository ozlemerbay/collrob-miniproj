import math

ENV_WIDTH = 100.0
ENV_HEIGHT = 100.0


class FoodSite:
    # this is a specific resource area
    def __init__(self, x, y, alpha, rho, gamma):
        self.x = x
        self.y = y
        self.alpha = alpha  # discovery
        self.rho = rho  # adoption
        self.gamma = gamma  # forgetting


class GridWorld:
    # 2d empty box where the ants walk around
    def __init__(self, width=ENV_WIDTH, height=ENV_HEIGHT):
        self.width = width
        self.height = height
        self.food_sites = []
        self.ants = []

    def put_food(self, site):
        self.food_sites.append(site)

    def put_ant(self, ant):
        self.ants.append(ant)

    def find_nearest_food(self, x, y, radius):
        # find the closest food source to the ant
        best_site = None
        shortest = float("inf")
        for site in self.food_sites:
            distance = math.hypot(site.x - x, site.y - y)
            if distance <= radius and distance < shortest:
                best_site = site
                shortest = distance
        return best_site

    def get_buddies(self, current_ant, comm_dist):
        # find all other ants inside the talking circle
        buddies = []
        for other_ant in self.ants:
            if other_ant is current_ant:
                continue  # dont talk to yourself

            distance = math.hypot(
                other_ant.x - current_ant.x, other_ant.y - current_ant.y
            )
            if distance <= comm_dist:
                buddies.append(other_ant)
        return buddies

    def keep_in_bounds(self, x, y):
        # stops ants from walking off the edge of the world
        safe_x = max(0.0, min(x, self.width))
        safe_y = max(0.0, min(y, self.height))
        return safe_x, safe_y
