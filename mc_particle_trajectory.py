print('Importing dependencies...')
import datetime
import matplotlib.pyplot as plt
import numpy as np

from astropy.io import fits
from scipy.stats import maxwell
print('Done.')

# ----------------------------------------------------------------------------
# Initialize variables
# ----------------------------------------------------------------------------

# Number of particles
n = 3

# Spacing, must be same as variable n in halbach.nb Mathematica
sp = 3

# Time and timestep
t = 0.0
dt = 0.1

# Distance from cell to 4K aperture; will be using mm
l = 100.0

# Physical constants
s = -0.5
g = 2.0
mu_B = 9.274e-24

# Mass of a single CaOCH3 molecule (in kg)
m = 1.1789827e-22

# vectorized velocity and acceleration
p = []
v = []
a = []

# ----------------------------------------------------------------------------
# # Initialize n molecules
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

# Generate particles with velocity distributed standard normally, except
# for in the z-coordinate, distributed Maxwell-Boltzmann
print('Generating particles...')

for i in range(n):
    p.append([0.0, 0.0, 0.0])
    v.append([np.random.standard_normal(), \
        np.random.standard_normal(),\
        np.random.normal(loc=100.0, scale=1.0)])
    a.append([0.0, 0.0, 0.0])
print('Done.')

# convert to numpy array
p = np.array(p)
v = np.array(v)
a = np.array(a)
print('Positions array: \n {} \n'.format(p))
print('Velocities array: \n {} \n'.format(v))
print('Accelerations array: \n {} \n'.format(a))

print('Done.')

# ----------------------------------------------------------------------------
# Deflection by force field
# ----------------------------------------------------------------------------

# Import matrices, source:
# https://mathematica.stackexchange.com/questions/163685/
# export-a-3d-array-from-mathematica-and-import-it-in-python-as-a-numpy-array
hdul = fits.open('/Users/andrewwinnicki/desktop/andrew/2019-2020/Doyle Lab/Modeling Project/B-Matrix/normbMatrix.fits')
normbMatrix = np.array([hdul[i].data for i in range(1)][0])
gradBxMatrix = np.gradient(normbMatrix, axis=0)

# Calculate force field at each spacing
forceField = np.array([[[g * mu_B * s * gradBxMatrix[i][j][k] \
    for k in range(sp)] for j in range(sp)] for i in range(sp)])

print("Old force field: \n {} \n ".format(forceField))

# Add F = 0 for anywhere we're not counting the magnetic lens' effect
# by adding rows and columns to matrix

# Spacing between cell aperture and circular Halbach array is 8x greater than
# spacing within array; 18x greater between array and MOT
for _ in range((sp - 1) * 4):
    # Since the distance from 4K aperture to lens is 8x the length of the lens
    # bore, we must have an additional (sp - 1)*8 points in the force field with
    # value 0
    forceField = np.insert(forceField, 0, [[0.0 for _ in range(sp)]\
        for _ in range(sp)], axis=0)

# Add in 18x 0's in the force field between the lens and the MOT

print("New force field: \n {} \n ".format(forceField))

# ----------------------------------------------------------------------------
# Kinematic propagation
# ----------------------------------------------------------------------------

print('Propagating...')

# Propagate for 5 s, 0.05 s timesteps
for step in np.linspace(0, 1, num=100, endpoint=False):

    # Truncate positions to get approximate indices for force field matrix
    # in acceleration calculations
    positions = np.around(p)

    # Change the accelerations:
    # Find the coordinate in the force field that each particle is closest to.
    for index in range(n):
        position = positions[index]
        try:
            # Attempt to set new acceleration to the F/m given by force field's
            # coordinate
            a[index] = forceField[position] / m
            print('Made it to the break loop. I need to reshape the array.')
            print('I also need to have a force field that uses not the norm,\
                but a vector for the force (need to do gradient on the\
                3d vector')
        except:
            # Set new accelerations to [0, 0, 0] if outside the scope of our
            # Force field's coordinates
            a[index] = [0, 0, 0]
            print('New acceleration is outside scope of calculated coordinates.\
                New acceleration set to [0, 0, 0].')
    print('New accelerations array: {}'.format(a))

    # Change the velocities:

    # Change the positions:

print('Done.')

# print('Plotting...')

# # Trace the trajectories of the particles (just look at x- and z-coordinates)
# for i in range(0, n):
#     z[i].append(particles[i].coords[2])
#     x[i].append(particles[i].coords[0])
#     plt.plot(z[i], x[i], 'r-')

# plt.xlabel('z (mm)')
# plt.ylabel('x (mm)')
# plt.title('Kinematic Propagation of {} particles in the z- and x-coordinates'\
#     .format(n))
# # Save figure
# # plt.savefig('/Users/andrewwinnicki/desktop/andrew/2019-2020/Doyle Lab/Modeling Project/Particle Trajectory Plots/{}_kinematic_{}.png'.format(n, datetime.date.today()))
# plt.show()

# print('Done.')

# ----------------------------------------------------------------------------
# Calculate how many molecules end up in the trap region
# ----------------------------------------------------------------------------

print('Calculating success rate...')
# TODO
print('Done.')

# # ----------------------------------------------------------------------------
# # #############################################################################
# # EXTRAS BELOW
# # #############################################################################
# # ----------------------------------------------------------------------------

# # ----------------------------------------------------------------------------
# # Potential vector definition; phased out in favor of numpy.array
# # ----------------------------------------------------------------------------

# # # Define vector
# # class Vector(list):
# #     def __init__(self, *el):
# #         for e in el:
# #             self.append(e)

# #     # Define addition
# #     def __add__(self, other):
# #         if type(other) is Vector:
# #             assert len(self) == len(other), 'Error 0'
# #             r = Vector()
# #             for i in range(len(self)):
# #                 r.append(self[i] + other[i])
# #             return r

# #     # Define subtraction
# #     def __sub__(self, other):
# #         if type(other) is Vector:
# #             assert len(other) == len(self), 'Error 0'
# #             r = Vector()
# #             for i in range(len(self)):
# #                 r.append(self[i] - other[i])
# #             return r

# #     # Define distance
# #     def __mod__(self, other):
# #         return sum((self - other) ** 2) ** 0.5

# # a = Vector(1, 2, 3)
# # b = Vector(2, 4, 60)
# # print(a + b)
# # print(a - b)
# # print(a % b)
