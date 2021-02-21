# ----------------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------------
from dependencies import *
from vector_field import *

def is_not_dead(pos, mot_start=mot_left_edge):
    if ((pos[0] ** 2 + pos[1] ** 2) ** (1 / 2)) > r_inner / 1e3 or \
        pos[2] > mot_start + mot_side_length or \
        (pos[2] < l_cell_to_4k and ((pos[0] ** 2 + pos[1] ** 2) ** (1 / 2)) > r_4k_aperture):
        return False
    else:
        return True

def is_in_magnet(pos, zsd_length=z_length):
    if l_cell_to_4k + l_4k_to_lens_aperture <= pos[2] \
        <= l_cell_to_4k + l_4k_to_lens_aperture + zsd_length / 1e3:
        return True
    else:
        return False

def is_in_mot(pos, i, succ_ptcls, mot_start=mot_left_edge):

    if -mot_side_length/2 <= pos[0] <= mot_side_length / 2 and \
        -mot_side_length/2 <= pos[1] <= mot_side_length / 2 and \
        mot_start <= pos[2] <= mot_start + mot_side_length and \
        succ_ptcls[i] == False:
        return True
    else:
        return False

def is_in_gate(gate, z_pos, counted):

    if gate - gate_size / 2 <= z_pos <= gate + gate_size / 2 and counted == 0:
        return True
    else:
        return False

def magnet_prop(pos, vel, acc, ms_prev, zsd_length=z_length, ind=None, flip_check=[True, True, True]):

    # coordinates for interpolation
    xCoord = round((r_inner / 1e3 + pos[0]) / l_xy)
    yCoord = round((r_inner / 1e3 + pos[1]) / l_xy)
    zCoord = round((pos[2] - (l_cell_to_4k + l_4k_to_lens_aperture)) / l_z)
    coords = (xCoord, yCoord, zCoord)

    # flip signs if conditions met
    ms_new, flip_check = sign_change(coords, ms_prev, flip_check)

    # change acceleration
    changed_acceleration = ms_new * force_field[int(yCoord), int(xCoord), int(zCoord)] / mass

    return changed_acceleration, ms_new, flip_check

def sign_change(coords, ms_prev, flip_check):

    # try:
    #     if coords[2] in b_field_maxes and flip_check[np.where(b_field_maxes == coords[2])[0][0]] == False:
    #         ms_change = ms_prev  * -1
    #         flip_check[np.where(b_field_maxes == coords[2])[0][0]] == True
    #     else:
    #         ms_change = ms_prev
    # except:
    #     ms_change == ms_prev

    ms_change = ms_prev * -1 if coords[2] in b_field_maxes else ms_prev

    return ms_change, flip_check

def plot_prop(positions):

    # initialize plotting variables
    pl_z = [[] for _ in range(int(n))]
    pl_x = [[] for _ in range(int(n))]

    # loop through and initialize plotting
    for i in range(0, int(n)*3, 3):
        pl_z[int(i / 3)].append(positions[i + 2])
        pl_x[int(i / 3)].append(positions[i])

    return pl_z, pl_x

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
    ax.vlines(x=l_cell_to_4k, ymin=-10.0, ymax=-r_4k_aperture, color='green', linewidth=3)
    ax.vlines(x=l_cell_to_4k, ymin=r_4k_aperture, ymax=10, color='green', linewidth=3)

    # labels
    ax.set_xlabel('z (m)')
    ax.set_ylabel('x (m)')
    ax.grid(True)
    ax.set_title(f'Propagation of {int(n)} Particles in the z- and x-Coordinates')
    ax.set_xlim(left=0.0, right=mot_left_edge + 0.1)
    ax.set_ylim(bottom=-0.020, top=0.020)

    # save figure
    Path(f'{date}/propagation_plots_{date}').mkdir(parents=True, exist_ok=True)
    fig.savefig(f'{date}/propagation_plots_{date}/propagation_{mol_run}_{int(n)}_particles_{date}')

    return (fig, ax)

def plot_spin(fig, ax):

    # labels
    ax.set_xlabel('z (m)')
    ax.set_ylabel('spin')
    ax.grid(True)
    ax.set_title('Spin Along the z-axis')
    ax.set_xlim(left=0.09, right=mot_left_edge)
    #mot_left_edge + 0.1)
    ax.set_ylim(bottom=-0.7, top=0.7)
    ax.legend()

    # save figure
    Path('{}/tracking_plots_{}'.format(date, date)).mkdir(parents=True, exist_ok=True)
    fig.savefig('{}/tracking_plots_{}/spin_particles_{}'.format(date, date, date))

    return (fig, ax)

# def plot_det(fig, ax):

#     # labels
#     ax.set_xlabel('z (m)')
#     ax.set_ylabel('Detuning')
#     ax.grid(True)
#     ax.set_title('Detuning Along the z-axis')
#     # ax.set_xlim(left=0.0, right=mot_left_edge + 0.1)
#     ax.set_xlim(left=0.14, right=0.25)
#     # ax.set_ylim(bottom=-0.7, top=0.7)
#     ax.legend()

#     # save figure
#     Path('{}/tracking_plots_{}'.format(date, date)).mkdir(parents=True, exist_ok=True)
#     fig.savefig('{}/tracking_plots_{}/detuning_{}'.format(date, date, date))

#     return (fig, ax)

def plot_accel(fig, ax):

    # labels
    ax.set_xlabel('z (m)')
    ax.set_ylabel('Acceleration (m/s)')
    ax.grid(True)
    ax.set_title(f'Acceleration Along the z-axis, {mol_run}, {int(n)} mols')
    # ax.set_xlim(left=0.0, right=mot_left_edge + 0.1)
    ax.set_xlim(left=0.09, right=mot_left_edge)
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
    ax.set_title(f'Velocity Along the z-axis, {mol_run}, {int(n)} mols')
    ax.set_xlim(left=0.0, right=mot_left_edge + 0.1)
    # ax.set_xlim(left=0.58, right=0.62)
    # ax.set_ylim(bottom=117, top=120)
    # ax.legend()

    # save figure
    Path('{}/tracking_plots_{}'.format(date, date)).mkdir(parents=True, exist_ok=True)
    fig.savefig(f'{date}/tracking_plots_{date}/{mol_run}_vel_{date}')

    return (fig, ax)

def plot_vel_long(fig, ax):

    # labels
    ax.set_xlabel('v_z (m/s)')
    ax.set_ylabel('Number')
    ax.grid(True)
    ax.set_title(f'Velocity Distributions At Points Along the z-axis, {mol_run}, {int(n)} mols')
    # ax.set_xlim(left=0.0, right=mot_left_edge + 0.1)
    # ax.set_xlim(left=0.58, right=0.62)
    ax.set_ylim(top=450)
    ax.legend()

    # save figure
    Path('{}/tracking_plots_{}'.format(date, date)).mkdir(parents=True, exist_ok=True)
    fig.savefig(f'{date}/tracking_plots_{date}/{mol_run}_vel_dist_long_{int(n)}_mols_{date}')

    return (fig, ax)

def plot_vel_dist_scan_det(fig, ax, vels, det, index, close=None, successes='n/a'):

    if close == 'close':
        # labels
        ax.set_xlabel('v_z (m/s)')
        ax.set_ylabel('Number')
        ax.grid(True)
        ax.set_title(f'Effect of Strong to Weak Detuning, {mol_run}, {int(n)} mols')
        # ax.set_xlim(left=0.0, right=mot_left_edge + 0.1)
        # ax.set_xlim(left=0.58, right=0.62)
        # ax.set_ylim(top=20)
        ax.legend()

        # save figure
        Path('{}/tracking_plots_{}'.format(date, date)).mkdir(parents=True, exist_ok=True)
        fig.savefig(f'{date}/tracking_plots_{date}/{mol_run}_vel_dist_scan_det_{int(n)}_mols_{date}')

        return (fig, ax)

    else:
        sns.histplot(data=vels, label=f'detuning (GHz) = {det / 1e9}, successes = {successes}', \
            ax=ax, kde=True, stat='count', color=colors[index], binwidth=1, binrange=(0, 215))

def plot_phase_space_acc_reg(fig, ax, vels, pos, det, close=None):

    if close == 'close':
        # labels
        ax.set_xlabel('x (m)')
        ax.set_ylabel('v_x (m/s)')
        ax.grid(True)
        ax.set_title(f'Phase-Space Acceptance at the Detection Region, {mol_run}, {int(n)} mols')
        # ax.set_xlim(left=0.0, right=mot_left_edge + 0.1)
        # ax.set_xlim(left=0.58, right=0.62)
        # ax.set_ylim(top=20)
        ax.legend()

        # save figure
        Path('{}/tracking_plots_{}'.format(date, date)).mkdir(parents=True, exist_ok=True)
        fig.savefig(f'{date}/tracking_plots_{date}/{mol_run}_phase_space_acc_{int(n)}_mols_{date}')

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

def plot_param_scan_heatmap(fig, ax, df, path):

    sns.heatmap(df, annot=True, ax=ax, cmap='mako')

    # labels
    # ax.set_xlabel('del_s2w')
    # ax.set_ylabel('z_length')
    ax.set_title(f'Detuning and Slower Length Optimization, {path}, {mol_run}, {int(n)} mols')

    # save figure
    Path('{}/param_scans_{}'.format(date, date)).mkdir(parents=True, exist_ok=True)
    fig.savefig(f'{date}/param_scans_{date}/{mol_run}_param_scans_det_zlen_{int(n)}_mols_{date}_{path}')

    return (fig, ax)