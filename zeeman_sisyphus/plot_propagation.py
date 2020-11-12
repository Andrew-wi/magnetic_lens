# ----------------------------------------------------------------------------
# Propagation
# ----------------------------------------------------------------------------
from dependencies import *
from helpers import *
from init import *
from vector_field import *
from propagation import *

import sys

# initialize variables
n = int(n)
successes_pp = 0
successful_particles_pp = np.zeros(n, dtype=bool)
p_pre = np.zeros((n, 3))
v_pre = np.zeros((n, 3))
a_pre = np.zeros((n, 3))
m_s_pre = np.zeros((n, 3))
p, v, a, m_s = generate(n, p_pre, v_pre, a_pre, m_s_pre)

# plot v distribution without zs decel
pos_pp, vel_pp, acc_pp, successes_pp, successful_particles_pp = \
    propagate(n, p, v, a, successes_pp, successful_particles_pp, l_4k_to_lens_aperture, m_s, decel=True, plot=True)

print('successes: {}'.format(successes_pp))
print(np.where(successful_particles_pp == True))

# # prune out stray trajectories
# for index in range(0, int(n)):
#     if pos_pp[index, 2] >= l_cell_to_4k and ((pos_pp[index, 0] ** 2 + pos_pp[index, 1] ** 2) ** (1/2)) > 0.01:
#         plotX[int(index / 3)] = 0.0
#         plotZ[int(index / 3)] = 0.0
#     if pos_pp[index, 2] <= l_cell_to_4k + 0.05:
#         plotX[int(index / 3)] = 0.0
#         plotZ[int(index / 3)] = 0.0

# # # save plotz and plotx to files
# # print('Writing to files...')
# # with open('{}/plotZ_{}.csv'.format(datetime.date.today(), datetime.date.today()), 'w+') as plotting:
# #     writer = csv.writer(plotting)
# #     writer.writerows(plotZ)
# # with open('{}/plotX_{}.csv'.format(datetime.date.today(), datetime.date.today()), 'w+') as plotting:
# #     writer = csv.writer(plotting)
# #     writer.writerows(plotX)

# print('Success rate: {}'.format(successes_pp / n))

# # plot trajectories
# print('Plotting trajectories...')

# # plot trajectory of each particle through space
# for index in range(0, int(n)):
#     plt.plot(plotZ[index], plotX[index], 'r-', linewidth=0.5)

# # draw MOT region, magnetic lens, lens, 4k aperture, beam shutter
# motRegion = [[mot_left_edge, mot_side_length / 2], [mot_left_edge + mot_side_length, mot_side_length / 2], \
#     [mot_left_edge + mot_side_length,  -mot_side_length / 2], [mot_left_edge, -mot_side_length / 2]]
# motRegion.append(motRegion[0])
# xMotRegion, yMotRegion = list(zip(*motRegion))

# plt.plot(xMotRegion, yMotRegion, 'k', linewidth=1.0)

# # # magnetic lens
# # magneticLensTop = [[l_cell_to_4k + l_4k_to_lens_aperture, R / 1e3], [l_cell_to_4k + l_4k_to_lens_aperture, R / 1e3 / 2], \
# #     [l_cell_to_4k + l_4k_to_lens_aperture + R / 1e3, R / 1e3 / 2], [l_cell_to_4k + l_4k_to_lens_aperture + R / 1e3, R / 1e3]]
# # magneticLensBottom = [[l_cell_to_4k + l_4k_to_lens_aperture, -R / 1e3], [l_cell_to_4k + l_4k_to_lens_aperture, -R / 1e3 / 2], \
# #     [l_cell_to_4k + l_4k_to_lens_aperture + R / 1e3, -R / 1e3 / 2], [l_cell_to_4k + l_4k_to_lens_aperture + R / 1e3, -R / 1e3]]
# # magneticLensTop.append(magneticLensTop[0])
# # magneticLensBottom.append(magneticLensBottom[0])
# # x1, y1 = list(zip(*magneticLensTop))
# # x2, y2 = list(zip(*magneticLensBottom))

# # 4k aperture and beam shutter
# plt.vlines(x=l_cell_to_4k, ymin = -10.0, ymax=-0.005, color='green', linewidth=3)
# plt.vlines(x=l_cell_to_4k, ymin = 0.005, ymax=10, color='green', linewidth=3)
# # plt.vlines(x=l_cell_to_4k + l_4k_to_beam_shutter, ymin = -10.0, ymax=-0.007, color='green', linewidth=3)
# # plt.vlines(x=l_cell_to_4k + l_4k_to_beam_shutter, ymin = 0.007, ymax=10.0, color='green', linewidth=3)

# # # plot lens
# # plt.plot(x1, y1, 'k')
# # plt.plot(x2, y2, 'k')

# # labels
# plt.xlabel('z (m)')
# plt.ylabel('x (m)')
# plt.grid(True)
# plt.title('Propagation of {} Particles in the z- and x-Coordinates'.format(int(n)))
# plt.axis([0.0, mot_left_edge + 0.1, -0.008, 0.008])

# # save figure
# Path('{}/propagation_plots_{}'.format(datetime.date.today(), datetime.date.today())).mkdir(parents=True, exist_ok=True)
# plt.savefig('{}/propagation_plots_{}/propagation_{}_particles{}'.format(datetime.date.today(), datetime.date.today(), int(n), datetime.date.today()))
