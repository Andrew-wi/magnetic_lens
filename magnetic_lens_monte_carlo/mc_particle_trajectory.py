print('Importing dependencies...')
import datetime
import matplotlib.pyplot as plt
import numpy as np

from astropy.io import fits
from mpl_toolkits import mplot3d
from scipy.stats import maxwell
print('Done.')

# ----------------------------------------------------------------------------
# Initialize variables
# ----------------------------------------------------------------------------

# Number of particles
n = 3

# Mesh spacing, must be same as variable m in halbach.nb Mathematica code
m = 6

# Radius of circular Halbach array, same as in halbach.nb code
R = 25.4

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
mass = 1.1789827e-22

# vectorized velocity and acceleration
p = np.array([])
v = np.array([])
a = np.array([])

# ----------------------------------------------------------------------------
# # Initialize n molecules
# ----------------------------------------------------------------------------

# Generate particles with velocity distributed standard normally, except
# for in the z-coordinate, distributed Maxwell-Boltzmann
print('Generating particles...')

for i in range(n):
    p = np.append(p, [0.0, 0.0, 0.0])
    v = np.append(v, [np.random.standard_normal(), \
        np.random.standard_normal(),\
        np.random.normal(loc=100.0, scale=1.0)])
    a = np.append(a, [0.0, 0.0, 0.0])
print('Done.')

# convert to numpy array
print('Positions array: \n {} \n'.format(p))
print('Velocities array: \n {} \n'.format(v))
print('Accelerations array: \n {} \n'.format(a))

# ----------------------------------------------------------------------------
# Force Field
# ----------------------------------------------------------------------------

# Import matrices, source:
# https://mathematica.stackexchange.com/questions/163685/
# export-a-3d-array-from-mathematica-and-import-it-in-python-as-a-numpy-array
hdulBxMatrix = fits.open('/Users/andrewwinnicki/desktop/andrew/2019-2020/Doyle Lab/Modeling Project/B-Matrix/bxMatrix.fits')
hdulByMatrix = fits.open('/Users/andrewwinnicki/desktop/andrew/2019-2020/Doyle Lab/Modeling Project/B-Matrix/byMatrix.fits')
hdulBzMatrix = fits.open('/Users/andrewwinnicki/desktop/andrew/2019-2020/Doyle Lab/Modeling Project/B-Matrix/bzMatrix.fits')

bxMatrix = np.array([hdulBxMatrix[0].data[i] for i in range(m)])
byMatrix = np.array([hdulByMatrix[0].data[i] for i in range(m)])
bzMatrix = np.array([hdulBzMatrix[0].data[i] for i in range(m)])

# Take gradients of all matrices in x, y, z coordinates respectively
gradBxMatrix = np.gradient(bxMatrix, axis=0)
gradByMatrix = np.gradient(byMatrix, axis=1)
gradBzMatrix = np.gradient(bzMatrix, axis=2)

# Splice together gradients of all matrices here to get force field w/ vectors
gradBMatrix = np.stack([gradBxMatrix, gradByMatrix, gradBzMatrix], axis=3)

# Plot the 3D Matrix to visualize force field in space
gradBMatrixFig = plt.figure()
gradBMatrixAx = gradBMatrixFig.gca(projection='3d')

# Create mesh grid in 3D space for visualization purposes
x, y, z = np.meshgrid(np.linspace(-R/2, R/2, m),
                      np.linspace(-R/2, R/2, m),
                      np.linspace(-R/2, R/2, m))

gradBMatrixAx.quiver(x, y, z, bxMatrix, byMatrix, bzMatrix, length=3, \
    normalize=True)
plt.show()

# # Add F = 0 for anywhere we're not counting the magnetic lens' effect
# # by adding rows and columns to matrix

# # Spacing between cell aperture and circular Halbach array is 8x greater than
# # spacing within array; 18x greater between array and MOT
# # Todo: fix the '* 1' to be '* 4'
# for _ in range((m - 1) * 1):
#     # Since the distance from 4K aperture to lens is 8x the length of the lens
#     # bore, we must have an additional (m - 1)*8 points in the force field with
#     # value 0
#     forceField = np.insert(forceField, 0, [[0.0 for _ in range(m)]\
#         for _ in range(m)], axis=0)

# # Add in 18x 0's in the force field between the lens and the MOT
# Todo: add the 0's in the force field after the lens

# print("New force field: \n {} \n ".format(forceField))

# ----------------------------------------------------------------------------
# Kinematic propagation
# ----------------------------------------------------------------------------

# print('Propagating...')

# # Evolve system through time
# for step in np.linspace(0, 1, num=10, endpoint=False):

#     # Truncate positions to get approximate indices for force field matrix
#     # in acceleration calculations
#     positions = np.around(p)

#     # Change the accelerations:
#     # Find the coordinate in the force field that each particle is closest to.
#     for index in range(n):
#         position = positions[index]
#         try:
#             # Attempt to set new acceleration to the F/m given by force field's
#             # coordinate
#             a[index] = forceField[position] / m

#             # I need to reshape the array.
#             # I also need to have a force field that uses not the norm,
#             # but a vector for the force (need to do gradient on the
#             # 3d vector')
#             # Todo
#         except:
#             # Set new accelerations to [0, 0, 0] if outside the scope of our
#             # Force field's coordinates
#             a[index] = [0, 0, 0]

#     # Change the velocities:

#     # Change the positions:

# print('Done.')

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

# print('Calculating success rate...')
# # TODO
# print('Done.')

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
