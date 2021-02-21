# ----------------------------------------------------------------------------
# Propagation
# ----------------------------------------------------------------------------
from dependencies import *
from helpers import *

def propagate(n, p, v, a, successes_pre, successful_particles_pre, l_4k_to_lens_aperture, \
    m_s, decel=True, deepcopy=True, visual=False, zsd_length=z_length, mot_start=mot_left_edge):

    print('Propagating...')

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
        step_count = 0
        vel_tracker = np.zeros((steps, 4))
        flipped = [False, False, False]

        while is_not_dead(pos_list[index, :], mot_start=mot_start) and time <= t_final:

            if is_in_magnet(pos_list[index, :], zsd_length) and decel == True:
                new_acc, m_s[index], flipped = magnet_prop(pos_list[index, :], vel_list[index, :], acc_list[index, :], m_s[index], ind=index, flip_check=flipped)
                acc_list[index, :] = new_acc
                vel_list[index, :] += new_acc * timestep
                pos_list[index, :] += vel_list[index, :] * timestep

            else:
                acc_list[index, :] = 0
                pos_list[index, :] += vel_list[index, :] * timestep

            if is_in_mot(pos_list[index, :], index, successful_particles, mot_start=mot_start):
                successful_particles[index] = 1
                successes += 1

            step_count += 1
            time += timestep

    return (pos_list, vel_list, acc_list, successes, successful_particles)
