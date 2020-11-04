# ----------------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------------
from dependencies import *
from vector_field import *

def is_not_dead(pos):
    if ((pos[0] ** 2 + pos[1] ** 2) ** (1 / 2)) > 0.003:
        return False
    else:
        return True

def is_in_magnet(pos):
    if l_cell_to_4k + l_4k_to_lens_aperture - 0.006 <= pos[2] \
        <= l_cell_to_4k + l_4k_to_lens_aperture + -0.006 + z_length / 1e3:
        return True
    else:
        return False

def magnet_prop(pos, vel, acc, ms, ind=None):
    ms = ms
    # mesh spacing length
    l_xy = (r_inner * 2 / 1e3) / (mxy - 1)
    l_z = (z_length / 1e3) / (mz - 1)
    # coordinates for interpolation
    xCoord = round((r_inner/1e3 + pos[0]) / l_xy)
    yCoord = round((r_inner/1e3 + pos[1]) / l_xy)
    zCoord = round((pos[2] - (l_cell_to_4k + l_4k_to_lens_aperture - 0.006)) / l_z)
    # detuning calculation, w->s and s->w
    delta_w_to_s = 2 * np.pi * (-del_0_w_to_s + mu_B * g * ms * np.absolute(normBMatrix[int(yCoord), int(xCoord), int(zCoord)]) / h + vel[2] / lambda_trans)
    delta_s_to_w = 2 * np.pi * (del_0_s_to_w + mu_B * g * ms * np.absolute(normBMatrix[int(yCoord), int(xCoord), int(zCoord)]) / h + vel[2] / lambda_trans)
    # flip sign accordingly
    if -10e6 < delta_w_to_s < 10e6 and ms == -0.5:
        ms = 0.5
        print('Flipped state to +')
    elif -10e6 < delta_s_to_w < 10e6 and ms == 0.5:
        ms = -0.5
        print('Flipped state to -')
    # change acceleration
    changed_acceleration = ms*force_field[int(yCoord), int(xCoord), int(zCoord)]/mass
    changed_m_s = ms
    return changed_acceleration, changed_m_s

def prop(pos, vel, acc, ms):
    pass
    return changed_position

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
        int(i / 3) not in succ_ptcls:
        return True
    else:
        return False

def plot_prop(fig, ax):

    # draw MOT region, magnetic lens, lens, 4k aperture, beam shutter
    motRegion = [[mot_left_edge, mot_side_length / 2], [mot_left_edge + mot_side_length, mot_side_length / 2], \
        [mot_left_edge + mot_side_length,  -mot_side_length / 2], [mot_left_edge, -mot_side_length / 2]]
    motRegion.append(motRegion[0])
    xMotRegion, yMotRegion = list(zip(*motRegion))

    ax.plot(xMotRegion, yMotRegion, 'k', linewidth=1.0)

    # 4k aperture and beam shutter
    ax.vlines(x=l_cell_to_4k, ymin = -10.0, ymax=-0.005, color='green', linewidth=3)
    ax.vlines(x=l_cell_to_4k, ymin = 0.005, ymax=10, color='green', linewidth=3)

    # labels
    ax.set_xlabel('z (m)')
    ax.set_ylabel('x (m)')
    ax.grid(True)
    ax.set_title('Propagation of {} Particles in the z- and x-Coordinates'.format(int(n)))
    ax.set_xlim(left = 0.0, right = mot_left_edge + 0.1)
    ax.set_ylim(bottom = -0.008, top = 0.008)

    # save figure
    Path('{}/propagation_plots_{}'.format(datetime.date.today(), datetime.date.today())).mkdir(parents = True, exist_ok = True)
    fig.savefig('{}/propagation_plots_{}/propagation_{}_particles{}'.format(datetime.date.today(), datetime.date.today(), int(n), datetime.date.today()))

    return (fig, ax)
