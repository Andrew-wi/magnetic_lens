import numpy as np
import time
import threading
import sys

from scipy.stats import maxwell

# -----------------------------------------------------------------------------
# initialize variables
# -----------------------------------------------------------------------------

# number of particles
n = 10

# time and timestep
t = 0
dt = 0.1

# distance from cell to 4K aperture; will be using mm
l = 100

# particle collection
ptcls = []

# -----------------------------------------------------------------------------
# # initialize N molecules with velocity distribution at position 0, t=0
# -----------------------------------------------------------------------------

class Point():
    def __init__(self, coords, speed, mass):
        self.coords = coords
        self.speed = speed
        self.mass = mass
        self.acc = np.array([0, 0, 0])

    # define movement
    def move(self, dt):
        self.coords = self.coords + self.speed * dt

    def accelerate(self, dt):
        self.speed = self.speed + self.acc * dt

print('Generating {} particles...'.format(n))

for i in range(n):
    ptcls.append(Point(np.array([0.0, 0.0, 0.0]), np.array([maxwell.rvs(), \
        maxwell.rvs(), maxwell.rvs()]), 1.0))
    print('Particle {} has coordinates, speed, mass: '.format(i), \
        ptcls[i].coords, ', ', ptcls[i].speed, ', ', ptcls[i].mass)

# -----------------------------------------------------------------------------
# kinematic propagation
# -----------------------------------------------------------------------------

# will propagate for 100 mm, 0.1 s timesteps

# -----------------------------------------------------------------------------
# deflected by force
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# calculate how many molecules end up in the trap region
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# #######################
# EXTRAS BELOW
# #######################
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# potential vector definition; phased out in favor of numpy.array
# -----------------------------------------------------------------------------

# # define vector
# class Vector(list):
#     def __init__(self, *el):
#         for e in el:
#             self.append(e)

#     # define addition
#     def __add__(self, other):
#         if type(other) is Vector:
#             assert len(self) == len(other), 'Error 0'
#             r = Vector()
#             for i in range(len(self)):
#                 r.append(self[i] + other[i])
#             return r

#     # define subtraction
#     def __sub__(self, other):
#         if type(other) is Vector:
#             assert len(other) == len(self), 'Error 0'
#             r = Vector()
#             for i in range(len(self)):
#                 r.append(self[i] - other[i])
#             return r

#     # define distance
#     def __mod__(self, other):
#         return sum((self - other) ** 2) ** 0.5

# a = Vector(1, 2, 3)
# b = Vector(2, 4, 60)
# print(a + b)
# print(a - b)
# print(a % b)
