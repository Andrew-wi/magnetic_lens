import datetime
import matplotlib.pyplot as plt
import numpy as np

from astropy.io import fits
from scipy.stats import maxwell

# -----------------------------------------------------------------------------
# Initialize variables
# -----------------------------------------------------------------------------

# Number of particles
n = 1000

# Spacing, same as variable n in halbach.nb Mathematica
sp = 4

# Time and timestep
t = 0.0
dt = 0.1

# Distance from cell to 4K aperture; will be using mm
l = 100.0

# Particle collection
particles = []

# Physical constants
s = -0.5
g = 2.0
mu_B = 9.274e-24

# -----------------------------------------------------------------------------
# # Initialize N molecules
# -----------------------------------------------------------------------------

class Point():
    def __init__(self, coords, speed, mass):
        self.coords = coords
        self.speed = speed
        self.mass = mass
        self.acc = np.array([0, 0, 0])

    def move(self, dt):
        self.coords = self.coords + self.speed * dt

    def accelerate(self, dt):
        self.speed = self.speed + self.acc * dt

# Generate particles with velocity distributed standard normally, except
# for in the z-coordinate, distributed Maxwell-Boltzmann
for i in range(n):
    particles.append(Point(np.array([0.0, 0.0, 0.0]), \
        np.array([np.random.standard_normal(), \
        np.random.standard_normal(), maxwell.rvs()]), 1.0))

# Store original points in x- and y-coordinates
z = []
x = []
for i in range(n):
    z.append([particles[i].coords[2]])
    x.append([particles[i].coords[0]])

# -----------------------------------------------------------------------------
# Kinematic propagation
# -----------------------------------------------------------------------------

# Will propagate for 5 s, 0.1 s timesteps
for step in np.linspace(0, 1, num=100, endpoint=False):
    for i in range(0, n):
        particles[i].move(dt)

# Trace the trajectories of the particles (just look at x- and y-coordinates)
for i in range(0, n):
    z[i].append(particles[i].coords[2])
    x[i].append(particles[i].coords[0])
    plt.plot(z[i], x[i], 'r-')

plt.xlabel('z (mm)')
plt.ylabel('x (mm)')
plt.title('Kinematic Propagation of {} particles in the z- and x-coordinates'\
    .format(n))
plt.savefig('/Users/andrewwinnicki/desktop/andrew/2019-2020/Doyle Lab/Modeling Project/Particle Trajectory Plots/{}_kinematic_{}.png'.format(n, datetime.date.today()))

# -----------------------------------------------------------------------------
# Deflection by force field
# -----------------------------------------------------------------------------

# Import matrices, source:
# https://mathematica.stackexchange.com/questions/163685/
# export-a-3d-array-from-mathematica-and-import-it-in-python-as-a-numpy-array
hdul = fits.open('/Users/andrewwinnicki/desktop/andrew/2019-2020/Doyle Lab/Modeling Project/B-Matrix/bxMatrix.fits')
bxMatrix = np.array([hdul[i].data for i in range(1)][0])
gradBxMatrix = np.gradient(bxMatrix, axis=0)

# Calculate force field at each spacing
forceField = np.array([[[g * mu_B * s * gradBxMatrix[i][j][k] \
    for k in range(sp)] for j in range(sp)] for i in range(sp)])

# -----------------------------------------------------------------------------
# Calculate how many molecules end up in the trap region
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# #############################################################################
# EXTRAS BELOW
# #############################################################################
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Potential vector definition; phased out in favor of numpy.array
# -----------------------------------------------------------------------------

# # Define vector
# class Vector(list):
#     def __init__(self, *el):
#         for e in el:
#             self.append(e)

#     # Define addition
#     def __add__(self, other):
#         if type(other) is Vector:
#             assert len(self) == len(other), 'Error 0'
#             r = Vector()
#             for i in range(len(self)):
#                 r.append(self[i] + other[i])
#             return r

#     # Define subtraction
#     def __sub__(self, other):
#         if type(other) is Vector:
#             assert len(other) == len(self), 'Error 0'
#             r = Vector()
#             for i in range(len(self)):
#                 r.append(self[i] - other[i])
#             return r

#     # Define distance
#     def __mod__(self, other):
#         return sum((self - other) ** 2) ** 0.5

# a = Vector(1, 2, 3)
# b = Vector(2, 4, 60)
# print(a + b)
# print(a - b)
# print(a % b)
