# ----------------------------------------------------------------------------
# Dependencies
# ----------------------------------------------------------------------------

print('Importing dependencies...')
import datetime
import matplotlib.pyplot as plt
import numpy as np

from astropy.io import fits
from mpl_toolkits import mplot3d
from pathlib import Path
from scipy.stats import maxwell
print('Done.')

# Number of particles
n = 3

# Mesh spacing, must be same as variable m in halbach.nb Mathematica code
m = 18

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

# Generate particles
print('Generating particles...')

for i in range(n):
    p = np.append(p, [0.0, 0.0, 0.0])
    v = np.append(v, [np.random.standard_normal(), \
        np.random.standard_normal(),\
        np.random.normal(loc=100.0, scale=1.0)])
    a = np.append(a, [0.0, 0.0, 0.0])
print('Done.')

print('Positions array: \n {} \n'.format(p))
print('Velocities array: \n {} \n'.format(v))
print('Accelerations array: \n {} \n'.format(a))

# ----------------------------------------------------------------------------
# Force Vector Field
# ----------------------------------------------------------------------------

# Import matrices
hdulBxMatrix = fits.open('/Users/andrewwinnicki/Desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/bmatrix/bxMatrix.fits')
hdulByMatrix = fits.open('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/bmatrix/byMatrix.fits')
hdulBzMatrix = fits.open('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/bmatrix/bzMatrix.fits')

bxMatrix = np.array([hdulBxMatrix[0].data[i] for i in range(m)])
byMatrix = np.array([hdulByMatrix[0].data[i] for i in range(m)])
bzMatrix = np.array([hdulBzMatrix[0].data[i] for i in range(m)])

# Plot b-field in three dimensions
bMatrixFig3D = plt.figure()
bMatrixAx3D = bMatrixFig3D.gca(projection='3d')

x, y, z = np.meshgrid(np.linspace(-R/2, R/2, m),
                      np.linspace(-R/2, R/2, m),
                      np.linspace(-R/2, R/2, m))

bMatrixAx3D.quiver(x, y, z, bxMatrix, byMatrix, bzMatrix, length=3, \
    normalize=True)

bMatrixAx3D.set_title('Magnetic Field in Circular Halbach Array')
bMatrixAx3D.set_xlabel('x (mm)')
bMatrixAx3D.set_ylabel('y (mm)')
bMatrixAx3D.set_zlabel('z (mm)')

Path('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/bfield_plots_{}'\
    .format(date())).mkdir(parents=True, exist_ok=True)
plt.savefig('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/bfield_plots_{}/bfield_3D_{}'\
    .format(date(), date()))

# Plot slice of b-field in two dimensions
bMatrixFigSlice = plt.figure()
bMatrixAxSlice = plt.subplot()

x2d, y2d = np.meshgrid(np.linspace(-R/2, R/2, m), np.linspace(-R/2, R/2, m))

bxMatrixSlice = bxMatrix[:, :, int(m/2)]
byMatrixSlice = byMatrix[:, :, int(m/2)]

bMatrixAxSlice.quiver(x2d, y2d, bxMatrixSlice, byMatrixSlice)

bMatrixAxSlice.set_title(\
    '2D Slice of Magnetic Field in Circular Halbach Array')
bMatrixAxSlice.set_ylabel('y (mm)')
bMatrixAxSlice.set_xlabel('x (mm)')
plt.savefig('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/bfield_plots_{}/bfield_2D_slice_{}'\
    .format(date(), date()))

# Generate force field
gradBxMatrix = np.gradient(bxMatrix, axis=0)
gradByMatrix = np.gradient(byMatrix, axis=1)
gradBzMatrix = np.gradient(bzMatrix, axis=2)

gradBMatrix = np.stack([gradBxMatrix, gradByMatrix, gradBzMatrix], axis=3)

# # Add F = 0 for anywhere we're not counting the magnetic lens' effect

# # Spacing between cell aperture and circular Halbach array is 8x greater than
# # spacing within array; 18x greater between array and MOT
# # Todo: fix the '* 1' to be '* 4'
# for _ in range((m - 1) * 1):
#     # Since the distance from 4K aperture to lens is 8x the length of the lens
#     # bore, we must have an additional (m - 1)*8 points in the force field
#     # with value 0
#     force_field = np.insert(force_field, 0, [[0.0 for _ in range(m)]\
#         for _ in range(m)], axis=0)

# # Add in 18x 0's in the force field between the lens and the MOT
# Todo: add the 0's in the force field after the lens

# print("New force field: \n {} \n ".format(force_field))

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
#             a[index] = force_field[position] / m

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
# Todo: change path
# # plt.savefig('/Users/andrewwinnicki/desktop/andrew/2019-2020/Doyle Lab/Modeling Project/Particle Trajectory Plots/{}_kinematic_{}.png'.format(n, date()))
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
