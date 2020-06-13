# ----------------------------------------------------------------------------
# Kinematic propagation
# ----------------------------------------------------------------------------

print('Propagating...')

# Evolve system through time
for step in np.linspace(0, 1, num=10, endpoint=False):

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

            # I need to reshape the array.
            # I also need to have a force field that uses not the norm,
            # but a vector for the force (need to do gradient on the
            # 3d vector')
            # Todo
        except:
            # Set new accelerations to [0, 0, 0] if outside the scope of our
            # Force field's coordinates
            a[index] = [0, 0, 0]

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
# # Todo: change path
# # plt.savefig('/Users/andrewwinnicki/desktop/andrew/2019-2020/Doyle Lab/Modeling Project/Particle Trajectory Plots/{}_kinematic_{}.png'.format(n, datetime.date.today()))
# plt.show()

# print('Done.')

# ----------------------------------------------------------------------------
# Calculate how many molecules end up in the trap region
# ----------------------------------------------------------------------------

# print('Calculating success rate...')
# # TODO
# print('Done.')
