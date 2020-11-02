# ----------------------------------------------------------------------------
# Propagation
# ----------------------------------------------------------------------------
from dependencies import *
from helpers import *

# step through time
def propagate(n, p, v, a, successes, successful_particles, l_4k_to_lens_aperture, m_s):
    print('Propagating...')

    for index in range(n):

        timestep = t_final / steps
        time = 0
        position = p[index, :]
        velocity = v[index, :]
        acceleration = a[index, :]
        ms = m_s[index, 2]
        plotX = np.zeros(int(n))
        plotZ = np.zeros(int(n))

        while is_not_dead(position) and time<=t_final:

            if is_in_magnet(position):
                new_acc, new_m_s = magnet_prop(position, velocity, acceleration, ms)
                m_s[index, 2] = new_m_s
                a[index, :] = new_acc
                v[index, :] += new_acc * timestep
                p[index, :] += velocity * timestep

            else:
                a[index, :] = 0
                acceleration = 0
                p[index, :] += velocity * timestep

            if is_in_mot(position, index, successful_particles):
                successful_particles[int(index/3)] = 1
                successes += 1

            time += timestep

    return p, v, a, successes, successful_particles, plotX, plotZ
