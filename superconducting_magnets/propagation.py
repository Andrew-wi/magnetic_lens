# ----------------------------------------------------------------------------
# Propagation
# ----------------------------------------------------------------------------
from dependencies import *
from helpers import *

def propagate(n, p, v, a, successes_pre, successful_particles_pre, l_4k_to_lens_aperture,\
    m_s, decel=True, deepcopy=True, visual=False, del_0_s2w=del_0_s_to_w, \
    zsd_length=z_length, mot_start=mot_left_edge):

    print('Propagating...')

    mot_starting_point = mot_start

    if deepcopy == True:
        # init, allocate new memory for copied variables (don't change original, passed-in values)
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

    for index in range(n):

        if visual == True:
            print('Particle # {}'.format(index))

        timestep = t_final / steps
        time = timestep
        position = pos_list[index, :]
        velocity = vel_list[index, :]
        acceleration = acc_list[index, :]
        ms = m_s[index]
        step_count = 0
        detuning_sign_w2s_pos = 1
        detuning_sign_w2s_neg = -1
        detuning_sign_s2w_pos = 1
        detuning_sign_s2w_neg = -1
        vel_tracker = np.zeros((steps, 4))

        while is_not_dead(position, mot_start=mot_starting_point) and time <= t_final:

            if is_in_magnet(position, zsd_length) and is_in_beam_aperture(position) and decel == True:
                new_acc, new_m_s = magnet_prop(position, velocity, acceleration, ms, ind=index)
                ms = new_m_s
                acc_list[index, :] = new_acc
                vel_list[index, :] += new_acc * timestep
                pos_list[index, :] += velocity * timestep

            else:
                acc_list[index, :] = 0
                acceleration = 0
                pos_list[index, :] += velocity * timestep

            if is_in_mot(position, index, successful_particles, mot_start=mot_starting_point):
                successful_particles[index] = 1
                successes += 1

            step_count += 1
            time += timestep

    return (pos_list, vel_list, acc_list, successes, successful_particles)
