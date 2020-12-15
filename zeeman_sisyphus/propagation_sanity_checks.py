# ----------------------------------------------------------------------------
# Propagation Sanity Checks
# ----------------------------------------------------------------------------
from dependencies import *
from helpers import *

# step through time
def propagate_sanity(n, p, v, a, successes_pre, successful_particles_pre, l_4k_to_lens_aperture,\
    m_s, decel=True, plot=False, spin_tracking=False, spin_tracked_particles=[], \
    pruning=None, plot_vel=False, plot_vel_particles=[], \
    plot_long_dist=False, plot_long_dist_particles=[],
    scan_s2w=False, scan_s2w_detunings=[], \
    scan_dets=False, del_0_s2w=del_0_s_to_w, deepcopy=True):

    print('Propagating...')

    if deepcopy == True:
        # init, allocate new memory for copied variables
        pos_list=copy.deepcopy(p)
        vel_list=copy.deepcopy(v)
        acc_list=copy.deepcopy(a)
        successes = copy.deepcopy(successes_pre)
        successful_particles = copy.deepcopy(successful_particles_pre)
        gate_tracker = np.zeros((len(gate_list), n))
    else:
        # init, reference to value
        pos_list=p
        vel_list=v
        acc_list=a
        successes = successes_pre
        successful_particles = successful_particles_pre
        gate_tracker = np.zeros((len(gate_list), n))

    if plot == True:
        propagation_fig = plt.figure()
        propagation_ax = plt.axes()

    if spin_tracking == True:
        spin_tracking_fig = plt.figure()
        spin_tracking_ax = plt.axes()

    if plot_vel == True:
        vel_fig = plt.figure()
        vel_ax = plt.axes()

    if plot_long_dist == True:
        vel_long_fig = plt.figure()
        vel_long_ax = plt.axes()

    for index in range(n):

        timestep = t_final / steps
        time = timestep
        position = pos_list[index, :]
        velocity = vel_list[index, :]
        acceleration = acc_list[index, :]
        ms = m_s[index]
        step_count = 0
        trajectory_z = np.zeros(steps)
        trajectory_x = np.zeros(steps)
        spin_tracker = np.zeros((steps, 2))
        detuning_sign_w2s_pos = 1
        detuning_sign_w2s_neg = -1
        detuning_sign_s2w_pos = 1
        detuning_sign_s2w_neg = -1
        vel_tracker = np.zeros((steps, 4))
        counted = np.zeros(len(gate_list))

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

            if plot_long_dist == True:
                for i, gate_pos in enumerate(gate_list):
                    if is_in_gate(gate_pos, position[2], counted[i]):
                        counted[i] = 1
                        gate_tracker[i, index] = velocity[2]

            if is_in_magnet(position) and decel == True:
                new_acc, new_m_s, \
                    det_sign_change_w2s_pos, det_sign_change_w2s_neg, \
                    det_sign_change_s2w_pos, det_sign_change_s2w_neg, \
                    detuning_w2s_pos, detuning_w2s_neg, detuning_s2w_pos, detuning_s2w_neg = \
                    magnet_prop(position, velocity, acceleration, ms, detuning_sign_w2s_pos, \
                    detuning_sign_w2s_neg, detuning_sign_s2w_pos, detuning_sign_s2w_neg, \
                    del_0_s2w, ind=index)
                detuning_sign_w2s_pos = det_sign_change_w2s_pos
                detuning_sign_w2s_neg = det_sign_change_w2s_neg
                detuning_sign_s2w_pos = det_sign_change_s2w_pos
                detuning_sign_s2w_neg = det_sign_change_s2w_neg

                # # testing
                # if index in spin_tracked_particles:
                #     print(ms)

                ms = new_m_s
                acc_list[index, :] = new_acc
                vel_list[index, :] += new_acc * timestep
                pos_list[index, :] += velocity * timestep

            else:
                acc_list[index, :] = 0
                acceleration = 0
                pos_list[index, :] += velocity * timestep

            if plot_vel == True and index in plot_vel_particles:
                vel_tracker[step_count, 0] = position[2]
                vel_tracker[step_count, 1] = vel_list[index, 0]
                vel_tracker[step_count, 2] = vel_list[index, 1]
                vel_tracker[step_count, 3] = vel_list[index, 2]

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
            spin_tracking_ax.plot(spin_tracker[:, 0], spin_tracker[:, 1], linewidth=1.0, \
                label='Molecule {}'.format(index))

        if plot_vel == True and index in plot_vel_particles:
            vel_tracker = vel_tracker[:step_count, :]
            # vel_ax.plot(vel_tracker[:, 0], vel_tracker[:, 1], linewidth=1.0,\
            #     label='x component')
            # vel_ax.plot(vel_tracker[:, 0], vel_tracker[:, 2], linewidth=1.0,\
            #     label='y component')
            vel_ax.plot(vel_tracker[:, 0], vel_tracker[:, 3], linewidth=1.0, \
                label='velocity z-component')

    if plot == True:
        propagation_fig, propagation_ax = plot_prop(propagation_fig, propagation_ax)

    if spin_tracking == True:
        spin_tracking_fig, spin_tracking_ax = plot_spin(spin_tracking_fig, spin_tracking_ax)

    if plot_vel == True:
        vel_fig, vel_ax = plot_vel_fig(vel_fig, vel_ax)

    if plot_long_dist == True:
        for row in range(len(gate_list)):
            sns.histplot(gate_tracker[row, :][np.where(gate_tracker[row, :] != 0)], \
                label='gate: {}'.format(gate_list[row]), ax=vel_long_ax, kde=True, \
                stat='count', color=np.random.random(3))

        vel_long_fig, vel_long_ax = plot_vel_long(vel_long_fig, vel_long_ax)

    return (pos_list, vel_list, acc_list, successes, successful_particles)
