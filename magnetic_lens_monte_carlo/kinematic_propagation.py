# ----------------------------------------------------------------------------
# Kinematic propagation
# ----------------------------------------------------------------------------
from dependencies import *
from init import *
from vector_field import *

print('Propagating...')

# Evolve system through time
for time in np.linspace(0, tFinal, num=steps, endpoint=False):
    timestep = tFinal / steps

    # Prune out particles not in areas of interest
    # todo

    # Change accelerations
    for index in range(0, n, 3):
        position = p[index:index + 3]
        if -0.0125 <= position[0] <= 0.0125 and -0.0125 <= position[1] <= \
            0.0125 and 0.2 <= position[2] <= 0.225:
            a[index:index + 3] = gradBMatrix[position[0], position[1],\
                position[2]] / mass
        else:
            a[index:index + 3] = [0, 0, 0]

    print('a at time {}: \n {}'.format(time + timestep, a))

    # Change the velocities:
    v += a * timestep

    print('v at time {}: \n {}'.format(time + timestep, v))

    # Change the positions:
    p += v * timestep

    print('p at time {}: \n {} \n'.format(time + timestep, p))

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
