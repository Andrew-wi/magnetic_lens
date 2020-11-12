# ----------------------------------------------------------------------------
# Propagation
# ----------------------------------------------------------------------------
from dependencies import *
from helpers import *

# step through time
def propagate(n, p, v, a, successes, successful_particles, l_4k_to_lens_aperture, m_s, decel=True, plot=False):
    print('Propagating...')

    successes = successes
    successful_particles = successful_particles

    if plot == True:
        propagationFig = plt.figure()
        propagationAx = plt.axes()

    for index in range(n):

        timestep = t_final / steps
        time = timestep
        position = p[index, :]
        velocity = v[index, :]
        acceleration = a[index, :]
        ms = m_s[index, 2]
        step_count = 0
        trajectory_z = np.zeros(steps)
        trajectory_x = np.zeros(steps)
        detuning_sign_w2s = 1
        detuning_sign_s2w = 1

        while is_not_dead(position) and time <= t_final:

            if plot == True:
                trajectory_z[step_count] = position[2]
                trajectory_x[step_count] = position[0]

            if is_in_magnet(position) and decel == True:
                new_acc, new_m_s, det_sign_change_w2s, det_sign_change_s2w = \
                    magnet_prop(position, velocity, acceleration, ms, detuning_sign_w2s, detuning_sign_s2w, ind=index)
                detuning_sign_w2s = det_sign_change_w2s
                detuning_sign_s2w = det_sign_change_s2w
                m_s[index, 2] = new_m_s
                a[index, :] = new_acc
                v[index, :] += new_acc * timestep
                p[index, :] += velocity * timestep

            else:
                a[index, :] = 0
                acceleration = 0
                p[index, :] += velocity * timestep

            if is_in_mot(position, index, successful_particles):
                successful_particles[index] = 1
                successes += 1

            step_count += 1
            time += timestep

        if plot == True:
            trajectory_z = trajectory_z[:step_count]
            trajectory_x = trajectory_x[:step_count]
            propagationAx.plot(trajectory_z, trajectory_x, '-r', linewidth=0.5)

    if plot == True:
        propagationFig, propagationAx = plot_prop(propagationFig, propagationAx)

    return p, v, a, successes, successful_particles
