# ----------------------------------------------------------------------------
# Propagation, Properties
# ----------------------------------------------------------------------------
from dependencies import *
from helpers import *

# step through time
def propagate_properties(n, p, v, a, successes, successful_particles, l_4k_to_lens_aperture,\
    m_s, decel=True, plot=False, spin_tracking=False, spin_tracked_particles=[], \
    pruning=None, plot_detuning=False, detuning_tracked_particles=[], \
    plot_acc=False, plot_acc_particles=[], visual=False):

    print('Propagating...')

    successes = successes
    successful_particles = successful_particles

    if plot == True:
        propagation_fig = plt.figure()
        propagation_ax = plt.axes()

    if spin_tracking == True:
        spin_tracking_fig = plt.figure()
        spin_tracking_ax = plt.axes()

    if plot_detuning == True:
        detuning_fig = plt.figure()
        detuning_ax = plt.axes()

    if plot_acc == True:
        acc_fig = plt.figure()
        acc_ax = plt.axes()

    for index in range(n):

        if visual == True:
            print('Particle # {}'.format(index))

        timestep = t_final / steps
        time = timestep
        position = p[index, :]
        velocity = v[index, :]
        acceleration = a[index, :]
        ms = m_s[index]
        step_count = 0
        trajectory_z = np.zeros(steps)
        trajectory_x = np.zeros(steps)
        spin_tracker = np.zeros((steps, 2))
        detuning_tracker = np.zeros((steps, 5))
        detuning_sign_w2s_pos = 1
        detuning_sign_w2s_neg = -1
        detuning_sign_s2w_pos = 1
        detuning_sign_s2w_neg = -1
        acc_tracker = np.zeros((steps, 4))

        while is_not_dead(position) and time <= t_final:

            # # testing
            # if index in spin_tracked_particles:
            #     print(time, position[2])

            if plot == True:
                trajectory_z[step_count] = position[2]
                trajectory_x[step_count] = position[0]

            if spin_tracking == True and index in spin_tracked_particles:
                spin_tracker[step_count, 0] = position[2]
                spin_tracker[step_count, 1] = ms

            if is_in_magnet(position) and decel == True:
                new_acc, new_m_s = magnet_prop(position, velocity, acceleration, ms, ind=index)
                ms = new_m_s
                a[index, :] = new_acc
                v[index, :] += new_acc * timestep
                p[index, :] += v[index, :] * timestep

                if plot_detuning == True and index in detuning_tracked_particles:
                    detuning_tracker[step_count, 0] = position[2]
                    detuning_tracker[step_count, 1] = detuning_w2s_pos
                    detuning_tracker[step_count, 2] = detuning_w2s_neg
                    detuning_tracker[step_count, 3] = detuning_s2w_pos
                    detuning_tracker[step_count, 4] = detuning_s2w_neg

            else:
                a[index, :] = 0
                acceleration = 0
                p[index, :] += velocity * timestep

            if plot_acc == True and index in plot_acc_particles:
                acc_tracker[step_count, 0] = position[2]
                acc_tracker[step_count, 1] = a[index, 0]
                acc_tracker[step_count, 2] = a[index, 1]
                acc_tracker[step_count, 3] = a[index, 2]

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

        if spin_tracking == True and index in spin_tracked_particles:

            spin_tracker = spin_tracker[:step_count, :]
            spin_tracking_ax.plot(spin_tracker[:, 0], spin_tracker[:, 1], linewidth=1.0,\
                label='Molecule {}'.format(index))

        if plot_detuning == True and index in detuning_tracked_particles:

            detuning_tracker = detuning_tracker[:step_count - 100, :]
            detuning_ax.plot(detuning_tracker[:, 0], detuning_tracker[:, 1], linewidth=1.0,\
                label='w2s detuning, pos', color='orange')
            detuning_ax.plot(detuning_tracker[:, 0], detuning_tracker[:, 2], linewidth=1.0,\
                label='w2s detuning, neg', color='blue')
            detuning_ax.plot(detuning_tracker[:, 0], detuning_tracker[:, 3], linewidth=1.0,\
                label='s2w detuning, pos', color='green')
            detuning_ax.plot(detuning_tracker[:, 0], detuning_tracker[:, 4], linewidth=1.0,\
                label='s2w detuning, neg', color='red')

        if plot_acc == True and index in plot_acc_particles:

            acc_tracker = acc_tracker[:step_count, :]
            # acc_ax.plot(acc_tracker[:, 0], acc_tracker[:, 1], linewidth=1.0,\
            #     label='x component'.format(index))
            # acc_ax.plot(acc_tracker[:, 0], acc_tracker[:, 2], linewidth=1.0,\
            #     label='y component'.format(index))
            acc_ax.plot(acc_tracker[:, 0], acc_tracker[:, 3], linewidth=1.0,\
                label='z component'.format(index))

    if plot == True:
        propagation_fig, propagation_ax = plot_prop(propagation_fig, propagation_ax)

    if spin_tracking == True:
        spin_tracking_fig, spin_tracking_ax = plot_spin(spin_tracking_fig, spin_tracking_ax)

    if plot_detuning == True:
        detuning_fig, detuning_ax = plot_det(detuning_fig, detuning_ax)

    if plot_acc == True:
        acc_fig, acc_ax = plot_accel(acc_fig, acc_ax)

    return p, v, a, successes, successful_particles
