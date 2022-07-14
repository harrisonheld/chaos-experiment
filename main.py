import dataclasses
import math

DT = 1
G = 6.67e-11
EPSILON = 0.001
MAX_ITER = 1000*1000

SAMPLING_DENSITY = 30


class StaticBody:
    mass = 1.0
    name = ""
    pos_x = pos_y = 0.0

    def __init__(self, name, pos_x, pos_y):
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y


class DynamicBody:
    mass = 1.0
    vel_x = vel_y = 0.0
    pos_x = pos_y = 0.0

    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def apply_force(self, force_x, force_y):
        # f = ma
        ax = force_x / self.mass
        ay = force_y / self.mass
        self.vel_x += ax
        self.vel_y += ay

    def move(self):
        self.pos_x += self.vel_x * DT
        self.pos_y += self.vel_y * DT


class Fg:
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    lightgrey = '\033[37m'
    darkgrey = '\033[90m'
    lightred = '\033[91m'
    lightgreen = '\033[92m'
    yellow = '\033[93m'
    lightblue = '\033[94m'
    pink = '\033[95m'
    lightcyan = '\033[96m'


def simulate(static_bodies, start_x, start_y):

    subject = DynamicBody(start_x, start_y)
    iterations = 0

    while True:
        # apply forces
        for staticBody in static_bodies:
            # F = G * (m_1 * m_2) / d^2

            displacement_x = staticBody.pos_x - subject.pos_x
            displacement_y = staticBody.pos_y - subject.pos_y
            distance_squared = displacement_x ** 2 + displacement_y ** 2
            distance = math.sqrt(distance_squared)

            if distance < EPSILON:
                return staticBody.name

            gravitational_force = G * staticBody.mass * subject.mass
            gravitational_force /= distance_squared

            # find the direction by normalizing
            displacement_x /= distance
            displacement_y /= distance

            subject.apply_force(displacement_x * gravitational_force, displacement_y * gravitational_force)

        subject.move()
        iterations += 1

        if iterations > MAX_ITER:
            return Fg.lightgrey+"-"


static_bodies = [StaticBody(Fg.blue + "A", 0.5, 2*math.sqrt(3.0)/4.0), StaticBody(Fg.red + "B", 0.25, math.sqrt(3.0)/4.0), StaticBody(Fg.pink+"C", 0.75, math.sqrt(3.0)/4.0)]

for y in range(SAMPLING_DENSITY):
    y_pos = y / SAMPLING_DENSITY
    for x in range(SAMPLING_DENSITY):
        x_pos = x / SAMPLING_DENSITY

        print(simulate(static_bodies, x_pos, y_pos), end="")

    print()