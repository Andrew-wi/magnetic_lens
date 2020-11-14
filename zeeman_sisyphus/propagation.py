# ----------------------------------------------------------------------------
# Propagation
# ----------------------------------------------------------------------------
from dependencies import *
from helpers import *

# step through time
def propagate(n, p, v, a, successes, successful_particles, l_4k_to_lens_aperture,\
    m_s, decel=True, plot=False, spin_tracking=False, spin_tracked_particles=[], pruning=None):

    print('Propagating...')

    successes = successes
    successful_particles = successful_particles

    if plot == True:
        propagation_fig = plt.figure()
        propagation_ax = plt.axes()

    if spin_tracking == True:
        spin_tracking_fig = plt.figure()
        spin_tracking_ax = plt.axes()

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
        spin_tracker = np.zeros((steps, 2))
        detuning_sign_w2s = 1
        detuning_sign_s2w = 1

        while is_not_dead(position) and time <= t_final:

            if plot == True:
                trajectory_z[step_count] = position[2]
                trajectory_x[step_count] = position[0]

            if spin_tracking == True and (index in spin_tracked_particles):
                spin_tracker[step_count, 0] = position[2]
                spin_tracker[step_count, 1] = ms

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
            if pruning == 'to_mot_region':
                if successful_particles[index] == True:
                    trajectory_z = trajectory_z[:step_count]
                    trajectory_x = trajectory_x[:step_count]
                    propagation_ax.plot(trajectory_z, trajectory_x, '-r', linewidth=0.5)
                else:
                    continue
            elif pruning == 'to_magnet':
                if position[2] > l_cell_to_4k + l_4k_to_lens_aperture:
                    trajectory_z = trajectory_z[:step_count]
                    trajectory_x = trajectory_x[:step_count]
                    propagation_ax.plot(trajectory_z, trajectory_x, '-r', linewidth=0.5)
            else:
                trajectory_z = trajectory_z[:step_count]
                trajectory_x = trajectory_x[:step_count]
                propagation_ax.plot(trajectory_z, trajectory_x, '-r', linewidth=0.5)

        if spin_tracking == True and (index in spin_tracked_particles):
            spin_tracker = spin_tracker[:step_count, :]
            print(np.where(spin_tracker[:, 1] == 0.5))
            spin_tracking_ax.plot(spin_tracker[:, 0], spin_tracker[:, 1], linewidth=0.5,\
                label='Molecule {}'.format(index))

    if plot == True:
        propagation_fig, propagation_ax = plot_prop(propagation_fig, propagation_ax)

    if spin_tracking == True:
        spin_tracking_fig, spin_tracking_ax = plot_spin(spin_tracking_fig, spin_tracking_ax)

    return p, v, a, successes, successful_particles
