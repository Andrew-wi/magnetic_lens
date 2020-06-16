# ----------------------------------------------------------------------------
# Kinematic propagation
# ----------------------------------------------------------------------------
from dependencies import *
from init import *
from vector_field import *

print('Propagating...\n')

# Evolve system through time
for time in np.linspace(0, tFinal, num=steps, endpoint=False):
    timestep = tFinal / steps

    # Prune out particles not in areas of interest
    for index in range(0, n * 3, 3):
        if p[index + 2] >= lCellTo4k and\
        ((p[index] ** 2 + p[index + 1] ** 2) ** (1/2)) > 0.01

        v[index:index + 3] = [0, 0, 0]

        print('Pruned particle {}'.format())

    # Change accelerations
    for index in range(0, n * 3, 3):
        if -(R / 1e3) / 2 <= p[index] <= (R / 1e3) / 2\
            and -(R / 1e3) / 2 <= p[index + 1] <= (R / 1e3) / 2\
            and lCellTo4k + l4kToAperture <= p[index + 2] <= lCellTo4k + l4kToAperture + R:

            # get spacing
            l = (R / 1e3) / (m - 1)

            print('p[0]: {}'.format(p[index]))
            print('x: {}'.format(abs(-((R / 2) / 1e3) - p[index]) / l))
            print('p[1]: {}'.format(p[index + 1]))
            print('y: {}'.format(abs(-((R / 2) / 1e3) - p[index + 1]) / l))
            print('p[2]: {}'.format(p[index + 2]))
            print('z: {}\n'.format((p[index + 2] - (lCellTo4k + l4kToAperture)) / l))

            # x, y, z direction deviation
            xCoord = round(abs(-((R / 2) / 1e3) - p[index]) / l)
            yCoord = round(abs(-((R / 2) / 1e3) - p[index + 1]) / l)
            zCoord = round((p[index + 2] - (lCellTo4k + l4kToAperture)) / l)

            a[index:index + 3] = gradBMatrix[int(xCoord), int(yCoord),\
                int(zCoord)] / mass
        else:
            a[index:index + 3] = [0, 0, 0]

    v += a * timestep
    p += v * timestep

print('ending positions: {}\n'.format(p))

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
# # todo: change path
# # plt.savefig('/Users/andrewwinnicki/desktop/andrew/2019-2020/Doyle Lab/Modeling Project/Particle Trajectory Plots/{}_kinematic_{}.png'.format(n, datetime.date.today()))
# plt.show()

# print('Done.')

# ----------------------------------------------------------------------------
# Calculate how many molecules end up in the trap region
# ----------------------------------------------------------------------------

# print('Calculating success rate...')
# todo
# print('Done.')
