# agentTop.py - Top Layer
# AIFCA Python3 code Version 0.9.3 Documentation at http://aipython.org
# Download the zip file and read aipython.pdf for documentation
import math

# Artificial Intelligence: Foundations of Computational Agents http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017-2021.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from agentMiddle import Rob_middle_layer
from agents import Environment
import matplotlib.pyplot as plt
from agentEnv import Rob_body, Rob_env


class Rob_top_layer(Environment):
    def __init__(self, middle, timeout=200, locations={'mail': (-5, 10),
                                                       'o103': (50, 10), 'o109': (100, 10), 'storage': (101, 51)}):
        """middle is the middle layer
        timeout is the number of steps the middle layer goes before giving up
        locations is a loc:pos dictionary 
            where loc is a named location, and pos is an (x,y) position.
        """
        self.middle = middle
        self.timeout = timeout  # number of steps before the middle layer should give up
        self.locations = locations

    def do(self, plan):
        """carry out actions.
        actions is of the form {'visit':list_of_locations}
        It visits the locations in turn.
        """
        to_do = plan['visit']
        # TODO here implement the ordering, it could decide the path after the location is reached

        locations_to_visit = list(map(lambda l: Location.from_location(self.locations[l], l), to_do))

        while len(locations_to_visit) > 0:
            x, y = self.middle.percepts['rob_x_pos'], self.middle.percepts['rob_y_pos']
            loc = find_closest((x, y), locations_to_visit)
            result = self.middle.do({'go_to': (loc.x, loc.y), 'timeout': self.timeout})
            if result['arrived']:
                locations_to_visit.remove(loc)
                self.display(1, "Arrived at", loc, result)

            else:
                self.display(1, "Failed to arrive at", loc, result)
            if self.middle.env.crashed:
                self.display(1, "Crashed")
                break

class Location:
    def __init__(self, location, x, y):
        self.location = location
        self.x = x
        self.y = y

    @staticmethod
    def from_location(location, name):
        return Location(name, location[0], location[1])

    def __str__(self):
        return self.location + " (" + str(self.x) + ", " + str(self.y) + ")"


def find_closest(pos, locations):
    if len(locations) == 0:
        return None
    px, py = pos
    closest = locations[0]
    closest_distance = math.dist([px, py], [closest.x, closest.y])
    for location in locations:
        distance = math.dist([px, py], [location.x, location.y])
        if distance < closest_distance:
            closest = location
    return closest


class Plot_env(object):
    def __init__(self, body, top):
        """sets up the plot
        """
        self.body = body
        plt.ion()
        plt.clf()
        plt.axes().set_aspect('equal')
        for wall in body.env.walls:
            ((x0, y0), (x1, y1)) = wall
            plt.plot([x0, x1], [y0, y1], "-k", linewidth=3)
        for loc in top.locations:
            (x, y) = top.locations[loc]
            plt.plot([x], [y], "k<")
            plt.text(x + 1.0, y + 0.5, loc)  # print the label above and to the right
        plt.plot([body.rob_x], [body.rob_y], "go")
        plt.draw()
        plt.show()

    def plot_run(self):
        """plots the history after the agent has finished.
        This is typically only used if body.plotting==False
        """
        xs, ys = zip(*self.body.history)
        plt.plot(xs, ys, "go")
        wxs, wys = zip(*self.body.wall_history)
        plt.plot(wxs, wys, "ro")
        plt.draw()


"""
"""

env = Rob_env({
    ((5, 0), (25, 25)),
    ((25, 25), (40, 20)),
    ((40, 30), (60, 30)),
    ((80, 5), (80, 40)),
})
body = Rob_body(env)
middle = Rob_middle_layer(body)
top = Rob_top_layer(middle)

# try:
pl = Plot_env(body, top)
top.do({
    'visit': ['o109', 'storage', 'o109', 'o103'],
})
pl.plot_run()
# You can directly control the middle layer:
# middle.do({'go_to': (30, -10), 'timeout': 200})
# Can you make it crash?

# Robot Trap for which the current controller cannot escape:
trap_env = Rob_env({((10, -21), (10, 0)), ((10, 10), (10, 31)), ((30, -10), (30, 0)),
                    ((30, 10), (30, 20)), ((50, -21), (50, 31)), ((10, -21), (50, -21)),
                    ((10, 0), (30, 0)), ((10, 10), (30, 10)), ((10, 31), (50, 31))})
trap_body = Rob_body(trap_env, init_pos=(-1, 0, 90))
trap_middle = Rob_middle_layer(trap_body)
trap_top = Rob_top_layer(trap_middle, locations={'goal': (71, 0)})

# Robot trap exercise:
# pl = Plot_env(trap_body, trap_top)
# trap_top.do({'visit': ['goal']})
