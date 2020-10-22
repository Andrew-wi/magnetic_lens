# ----------------------------------------------------------------------------
# Propagation
# ----------------------------------------------------------------------------
from dependencies import *
from helpers import *
from vector_field import *

# step through time
def propagate(p, v, a, successes, successful_particles, l_4k_to_lens_aperture, m_s, plot_prop=None):
    print('Propagating...')
    if plot_prop is not None:
        plotZ, plotX = plot_prop(p)
    for index in range(0, int(n)*3, 3):
        timestep = t_final / steps
        time = 0
        position = p[index:index+3]
        velocity = v[index:index+3]
        acceleration = a[index:index+3]
        ms = m_s[int(index/3)]
        while is_not_dead(position) and time<=t_final:
            if is_in_magnet(position):
                new_acc, new_m_s = magnet_prop(position, velocity, acceleration, ms, ind=int(index/3))
                m_s[int(index/3)] = new_m_s
                a[index:index+3] = new_acc
                v[index:index+3] += new_acc*timestep
                p[index:index+3] += velocity*timestep
            else:
                a[index:index + 3] = 0
                acceleration = 0
                p[index:index+3] += velocity*timestep
            if is_in_mot(position, index, successful_particles):
                successful_particles.append(int(index/3))
                successes += 1
            if plot_prop is not None:
                plotZ[int(index/3)].append(p[index+2])
                plotX[int(index/3)].append(p[index])
            time += timestep
    print('Successful Particles: {}'.format(successful_particles)) # testing
    return p, v, a, successes, plotZ, plotX, successful_particles
