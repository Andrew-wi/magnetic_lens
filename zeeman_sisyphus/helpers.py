# ----------------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------------
from dependencies import *
from vector_field import *

def is_not_dead(pos):
    if ((pos[0] ** 2 + pos[1] ** 2) ** (1 / 2)) > r_inner / 1e3 or \
        pos[2] > mot_left_edge + mot_side_length:
        return False
    else:
        return True

def is_in_magnet(pos, zsd_length=z_length):
    if l_cell_to_4k + l_4k_to_lens_aperture <= pos[2] \
        <= l_cell_to_4k + l_4k_to_lens_aperture + zsd_length / 1e3:
        return True
    else:
        return False

def magnet_prop(pos, vel, acc, ms_prev, prev_det_sign_w2s_pos, prev_det_sign_w2s_neg, \
    prev_det_sign_s2w_pos, prev_det_sign_s2w_neg, del_0_s2w=del_0_s_to_w, \
    zsd_length=z_length, ind=None):

    # initialize variables
    ms = ms_prev

    # mesh spacing length
    l_xy = (r_inner * 2 / 1e3) / (mxy - 1)
    l_z = (zsd_length / 1e3) / (mz - 1)

    # coordinates for interpolation
    xCoord = round((r_inner / 1e3 + pos[0]) / l_xy)
    yCoord = round((r_inner / 1e3 + pos[1]) / l_xy)
    zCoord = round((pos[2] - (l_cell_to_4k + l_4k_to_lens_aperture)) / l_z)

    # detuning calculation, w -> s and s -> w
    # delta_w_to_s = 2 * np.pi * (-del_0_w_to_s + mu_B * g * ms * \
    #     np.absolute(normBMatrix[int(yCoord), int(xCoord), int(zCoord)]) / h + vel[2] / lambda_trans)
    # delta_s_to_w = 2 * np.pi * (del_0_s2w + mu_B * g * ms * \
    #     np.absolute(normBMatrix[int(yCoord), int(xCoord), int(zCoord)]) / h + vel[2] / lambda_trans)
    # removed ms
    delta_w_to_s_pos = 2 * np.pi * (-del_0_w_to_s + 1/2 * mu_B * g * \
        np.absolute(normBMatrix[int(yCoord), int(xCoord), int(zCoord)]) / h + vel[2] / lambda_trans)
    delta_w_to_s_neg = 2 * np.pi * (-del_0_w_to_s + -1/2 * mu_B * g * \
        np.absolute(normBMatrix[int(yCoord), int(xCoord), int(zCoord)]) / h + vel[2] / lambda_trans)
    delta_s_to_w_pos = 2 * np.pi * (del_0_s2w + 1/2 * mu_B * g * \
        np.absolute(normBMatrix[int(yCoord), int(xCoord), int(zCoord)]) / h + vel[2] / lambda_trans)
    delta_s_to_w_neg = 2 * np.pi * (del_0_s2w + -1/2 * mu_B * g * \
        np.absolute(normBMatrix[int(yCoord), int(xCoord), int(zCoord)]) / h + vel[2] / lambda_trans)

    # flip signs if conditions met
    current_detuning_sign_w2s_pos, current_detuning_sign_w2s_neg, \
        current_detuning_sign_s2w_pos, current_detuning_sign_s2w_neg, ms_new = \
        sign_change(delta_w_to_s_pos, delta_w_to_s_neg, delta_s_to_w_pos, delta_s_to_w_neg, \
            prev_det_sign_w2s_pos, prev_det_sign_w2s_neg, prev_det_sign_s2w_pos, prev_det_sign_s2w_neg, ms)

    # change acceleration
    changed_acceleration = ms_new * force_field[int(yCoord), int(xCoord), int(zCoord)] / mass

    return changed_acceleration, ms_new, \
           current_detuning_sign_w2s_pos, current_detuning_sign_w2s_neg, \
           current_detuning_sign_s2w_pos, current_detuning_sign_s2w_neg, \
           delta_w_to_s_pos, delta_w_to_s_neg, delta_s_to_w_pos, delta_s_to_w_neg

def sign_change(del_w2s_pos, del_w2s_neg, del_s2w_pos, del_s2w_neg, \
    previous_sign_w2s_pos, previous_sign_w2s_neg, previous_sign_s2w_pos, previous_sign_s2w_neg, ms_current):

    # initialize variables
    sign_change_w2s_pos = np.sign(del_w2s_pos)
    sign_change_w2s_neg = np.sign(del_w2s_neg)
    sign_change_s2w_pos = np.sign(del_s2w_pos)
    sign_change_s2w_neg = np.sign(del_s2w_neg)
    ms_change = ms_current

    # test to flip signs
    if np.sign(del_w2s_pos) != previous_sign_w2s_pos and np.sign(ms_current) == 1:
        ms_change *= -1
    elif np.sign(del_w2s_neg) != previous_sign_w2s_neg and np.sign(ms_current) == -1:
        ms_change *= -1
    elif np.sign(del_s2w_pos) != previous_sign_s2w_pos and np.sign(ms_current) == 1:
        ms_change *= -1
    elif np.sign(del_s2w_neg) != previous_sign_s2w_neg and np.sign(ms_current) == -1:
        ms_change *= -1

    # # bootleg spin flipping lol
    # if del_w2s > 2.8e11 and ms_current == 0.5:
    #     ms_change = -0.5
    # elif del_s2w > -0.3e11 and ms_current == -0.5:
    #     ms_change = 0.5

    return sign_change_w2s_pos, sign_change_w2s_neg, sign_change_s2w_pos, sign_change_s2w_neg, ms_change

# def prop(pos, vel, acc, ms):
#     pass
#     return changed_position

def plot_prop(positions):

    # initialize plotting variables
    pl_z = [[] for _ in range(int(n))]
    pl_x = [[] for _ in range(int(n))]

    # loop through and initialize plotting
    for i in range(0, int(n)*3, 3):
        pl_z[int(i / 3)].append(positions[i + 2])
        pl_x[int(i / 3)].append(positions[i])

    return pl_z, pl_x

def is_in_mot(pos, i, succ_ptcls):

    if -mot_side_length/2 <= pos[0] <= mot_side_length / 2 and \
        -mot_side_length/2 <= pos[1] <= mot_side_length / 2 and \
        mot_left_edge <= pos[2] <= mot_left_edge + mot_side_length and \
        succ_ptcls[i] == False:
        return True
    else:
        return False

def is_in_gate(gate, z_pos, counted):

    if gate - gate_size / 2 <= z_pos <= gate + gate_size / 2:# and counted == False:
        return True
    else:
        return False

def plot_prop(fig, ax):

    # draw MOT region, magnetic lens, lens, 4k aperture, beam shutter
    motRegion = [[mot_left_edge, mot_side_length / 2], \
                 [mot_left_edge + mot_side_length, mot_side_length / 2], \
                 [mot_left_edge + mot_side_length,  -mot_side_length / 2], \
                 [mot_left_edge, -mot_side_length / 2]]
    motRegion.append(motRegion[0])
    xMotRegion, yMotRegion = list(zip(*motRegion))

    ax.plot(xMotRegion, yMotRegion, 'k', linewidth=1.0)

    # 4k aperture and beam shutter
    ax.vlines(x=l_cell_to_4k, ymin=-10.0, ymax=-0.003, color='green', linewidth=3)
    ax.vlines(x=l_cell_to_4k, ymin=0.003, ymax=10, color='green', linewidth=3)

    # labels
    ax.set_xlabel('z (m)')
    ax.set_ylabel('x (m)')
    ax.grid(True)
    ax.set_title('Propagation of {} Particles in the z- and x-Coordinates'.format(int(n)))
    ax.set_xlim(left=0.0, right=mot_left_edge + 0.1)
    ax.set_ylim(bottom=-0.008, top=0.008)

    # save figure
    Path('{}/propagation_plots_{}'.format(date, date)).mkdir(parents=True, exist_ok=True)
    fig.savefig('{}/propagation_plots_{}/propagation_{}_particles{}'.format(date, date, int(n), date))

    return (fig, ax)

def plot_spin(fig, ax):

    # labels
    ax.set_xlabel('z (m)')
    ax.set_ylabel('spin')
    ax.grid(True)
    ax.set_title('Spin Along the z-axis')
    ax.set_xlim(left=0.09, right=0.20)
    #mot_left_edge + 0.1)
    ax.set_ylim(bottom=-0.7, top=0.7)
    # ax.legend()

    # save figure
    Path('{}/tracking_plots_{}'.format(date, date)).mkdir(parents=True, exist_ok=True)
    fig.savefig('{}/tracking_plots_{}/spin_particles_{}'.format(date, date, date))

    return (fig, ax)

def plot_det(fig, ax):

    # labels
    ax.set_xlabel('z (m)')
    ax.set_ylabel('Detuning')
    ax.grid(True)
    ax.set_title('Detuning Along the z-axis')
    # ax.set_xlim(left=0.0, right=mot_left_edge + 0.1)
    ax.set_xlim(left=0.14, right=0.25)
    # ax.set_ylim(bottom=-0.7, top=0.7)
    ax.legend()

    # save figure
    Path('{}/tracking_plots_{}'.format(date, date)).mkdir(parents=True, exist_ok=True)
    fig.savefig('{}/tracking_plots_{}/detuning_{}'.format(date, date, date))

    return (fig, ax)

def plot_accel(fig, ax):

    # labels
    ax.set_xlabel('z (m)')
    ax.set_ylabel('Acceleration (m/s)')
    ax.grid(True)
    ax.set_title('Acceleration Along the z-axis')
    # ax.set_xlim(left=0.0, right=mot_left_edge + 0.1)
    ax.set_xlim(left=0.09, right=1.6)
    # ax.set_ylim(bottom=-0.7, top=0.7)
    ax.legend()

    # save figure
    Path('{}/tracking_plots_{}'.format(date, date)).mkdir(parents=True, exist_ok=True)
    fig.savefig('{}/tracking_plots_{}/acc_{}'.format(date, date, date))

    return (fig, ax)

def plot_vel_fig(fig, ax):

    # labels
    ax.set_xlabel('z (m)')
    ax.set_ylabel('Velocity (m/s)')
    ax.grid(True)
    ax.set_title('Velocity Along the z-axis')
    ax.set_xlim(left=0.0, right=mot_left_edge + 0.1)
    # ax.set_xlim(left=0.58, right=0.62)
    # ax.set_ylim(bottom=117, top=120)
    # ax.legend()

    # save figure
    Path('{}/tracking_plots_{}'.format(date, date)).mkdir(parents=True, exist_ok=True)
    fig.savefig(f'{date}/tracking_plots_{date}/vel_{date}_{mol_run}')

    return (fig, ax)

def plot_vel_long(fig, ax):

    # labels
    ax.set_xlabel('v_z (m/s)')
    ax.set_ylabel('Number')
    ax.grid(True)
    ax.set_title('Velocity Distributions At Points Along the z-axis')
    # ax.set_xlim(left=0.0, right=mot_left_edge + 0.1)
    # ax.set_xlim(left=0.58, right=0.62)
    ax.set_ylim(top=200)
    ax.legend()

    # save figure
    Path('{}/tracking_plots_{}'.format(date, date)).mkdir(parents=True, exist_ok=True)
    fig.savefig(f'{date}/tracking_plots_{date}/vel_dist_long_{int(n)}_mols_{date}_{mol_run}')

    return (fig, ax)

def plot_vel_dist_scan_det(fig, ax, vels, det, close=None):

    if close == 'close':
        # labels
        ax.set_xlabel('v_z (m/s)')
        ax.set_ylabel('Number')
        ax.grid(True)
        ax.set_title('Effect of Strong to Weak Detuning')
        # ax.set_xlim(left=0.0, right=mot_left_edge + 0.1)
        # ax.set_xlim(left=0.58, right=0.62)
        # ax.set_ylim(top=20)
        ax.legend()

        # save figure
        Path('{}/tracking_plots_{}'.format(date, date)).mkdir(parents=True, exist_ok=True)
        fig.savefig(f'{date}/tracking_plots_{date}/vel_dist_scan_det_{int(n)}_mols_{date}_{mol_run}')

        return (fig, ax)

    else:
        sns.histplot(data=vels, label='detuning (GHz): {}'.format(det / 1e9), ax=ax, kde=True, \
            stat='count', color=np.random.random(3), binwidth=5)

def plot_phase_space_acc_reg(fig, ax, vels, pos, det, close=None):

    if close == 'close':
        # labels
        ax.set_xlabel('x (m)')
        ax.set_ylabel('v_x (m/s)')
        ax.grid(True)
        ax.set_title('Phase-Space Acceptance at the Detection Region')
        # ax.set_xlim(left=0.0, right=mot_left_edge + 0.1)
        # ax.set_xlim(left=0.58, right=0.62)
        # ax.set_ylim(top=20)
        ax.legend()

        # save figure
        Path('{}/tracking_plots_{}'.format(date, date)).mkdir(parents=True, exist_ok=True)
        fig.savefig(f'{date}/tracking_plots_{date}/phase_space_acc_{int(n)}_mols_{mol_run}_{date}')

        return (fig, ax)

    else:
        sns.scatterplot(x=pos, y=vels, label='detuning (GHz): {}'.format(det / 1e9),\
            ax=ax, color=np.random.random(3))

# def plot_decel_trans_acc(fig, ax, vels, pos, det, close=None):

#     if close == 'close':
#         # labels
#         ax.set_xlabel('detuning (GHz)')
#         ax.set_ylabel('1d transverse phase-space acceptance area (mm * m/s)')
#         ax.grid(True)
#         ax.set_title('Phase-Space Acceptance at the Detection Region')
#         # ax.set_xlim(left=0.0, right=mot_left_edge + 0.1)
#         # ax.set_xlim(left=0.58, right=0.62)
#         # ax.set_ylim(top=20)
#         ax.legend()

#         # save figure
#         Path('{}/tracking_plots_{}'.format(date, date)).mkdir(parents=True, exist_ok=True)
#         fig.savefig('{}/tracking_plots_{}/det_vs_trans_acc_{}'.format(date, date, date))

#         return (fig, ax)

#     else:
#         sns.plot(x=pos, y=vels, label='detuning (GHz): {}'.format(det / 1e9),\
#             ax=ax, color=np.random.random(3))

def plot_param_scan_heatmap(fig, ax, df):

    sns.heatmap(df, annot=True, ax=ax)

    # labels
    # ax.set_xlabel('del_s2w')
    # ax.set_ylabel('z_length')
    ax.set_title('Optimization for Detuning and Slower Length')

    # save figure
    Path('{}/param_scans_{}'.format(date, date)).mkdir(parents=True, exist_ok=True)
    fig.savefig(f'{date}/param_scans_{date}/param_scans_det_slowerlength_{int(n)}_mols_{date}')

    return (fig, ax)