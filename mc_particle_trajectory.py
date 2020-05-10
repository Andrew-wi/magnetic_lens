import numpy as np
from scipy.stats import maxwell

# potential vector definition; phased out in favor of numpy.array
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

# initialize variables
n = 10
t = 0

# initialize N molecules with velocity distribution at position 0, t=0

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

ptcls = []

for i in range(n):
    ptcls.append(Point(np.array([0.0, 0.0, 0.0]), maxwell.rvs(), 1.0))
    print(ptcls[i].speed)

# kinematic population

# deflected by force

# calculate how many molecules end up in the trap region
