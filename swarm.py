import random
import math

ANT_SPEED = 1.0
SENSE_RAD = 2.0
TALK_RAD = 5.0


class SwarmAnt:
    def __init__(self, world, start_x, start_y):
        self.world = world
        self.x = start_x
        self.y = start_y
        self.current_idea = None  # None means the ant is undecided

        self.speed = ANT_SPEED
        self.sense_range = SENSE_RAD
        self.talk_range = TALK_RAD

    def do_random_walk(self):
        # pick a random angle and walk
        random_angle = random.uniform(0, 2 * math.pi)
        next_x = self.x + math.cos(random_angle) * self.speed
        next_y = self.y + math.sin(random_angle) * self.speed

        # apply the walls
        self.x, self.y = self.world.keep_in_bounds(next_x, next_y)

    def maybe_forget(self):
        # check if ant forgets opinion
        if self.current_idea is not None:
            if random.random() < self.current_idea.gamma:
                self.current_idea = None  # go back to undecided

    def try_discover(self):
        # only look for food if ant doesn't have an idea
        if self.current_idea is None:
            nearby_food = self.world.find_nearest_food(self.x, self.y, self.sense_range)
            if nearby_food is not None:
                # check if ant  actually detect it
                if random.random() < nearby_food.alpha:
                    self.current_idea = nearby_food

    def chat_with_neighbors(self):
        # see who is around the ant
        nearby_ants = self.world.get_buddies(self, self.talk_range)
        if len(nearby_ants) == 0:
            return

        # pick one random ant
        speaker = random.choice(nearby_ants)

        # only copy them if we are undecided and they actually have an opinion
        if self.current_idea is None and speaker.current_idea is not None:
            if random.random() < speaker.current_idea.rho:
                self.current_idea = speaker.current_idea

    def tick(self):
        # execute the biological loop
        self.do_random_walk()
        self.try_discover()
        self.maybe_forget()
        self.chat_with_neighbors()
