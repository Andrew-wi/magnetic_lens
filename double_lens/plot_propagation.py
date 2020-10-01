# ----------------------------------------------------------------------------
# Propagation
# ----------------------------------------------------------------------------
from dependencies import *
from init import *
from vector_field import *
from propagation import *

import sys

propagationFig = plt.figure()
propagationAx = plt.subplots()

# array of paths that the i-th particle takes (by index) in the z and x directions
plotZ = [[] for _ in range(int(n))]
plotX = [[] for _ in range(int(n))]

# initialize variables
successes = 0
successful_particles = []
p, v, a = generate()

# store positions of the particles in plotZ and plotX
for index in range(0, int(n) * 3, 3):
    plotZ[int(index / 3)].append(p[index + 2])
    plotX[int(index / 3)].append(p[index])

# # change lens distance
# l_4k_to_lens_aperture = float(sys.argv[1])
# l_4k_to_lens_aperture_2 = float(sys.argv[2])
# print('new lens to 4k distances: {}, {}'.format(l_4k_to_lens_aperture, l_4k_to_lens_aperture_2))

# propagate
p, v, a, successes, plotZ, plotX = propagate(p, v, a, successes, successful_particles, l_4k_to_lens_aperture, l_4k_to_lens_aperture_2)

# prune out stray trajectories
for index in range(0, int(n) * 3, 3):
    if p[index + 2] >= l_cell_to_4k and \
        ((p[index] ** 2 + p[index + 1] ** 2) ** (1/2)) > 0.01: # todo: make 0.008
        plotZ[int(index / 3)] = [0.0, 0.0]
        plotX[int(index / 3)] = [0.0, 0.0]
    elif p[index + 2] <= l_cell_to_4k + l_4k_to_beam_shutter + 0.05:
        plotZ[int(index / 3)] = [0.0, 0.0]
        plotX[int(index / 3)] = [0.0, 0.0]

# save plotz and plotx to files
print('Writing to files...')
with open('{}/plotZ_{}.csv'.format(datetime.date.today(), datetime.date.today()), 'w+') as plotting:
    writer = csv.writer(plotting)
    writer.writerows(plotZ)
with open('{}/plotX_{}.csv'.format(datetime.date.today(), datetime.date.today()), 'w+') as plotting:
    writer = csv.writer(plotting)
    writer.writerows(plotX)

print('Success rate: {}'.format(successes / n))

# plot trajectories
print('Plotting trajectories...')

# plot trajectory of each particle through space
for index in range(0, int(n) * 3, 3):
    plt.plot(plotZ[int(index / 3)], plotX[int(index / 3)], 'r-', linewidth=0.5)

# draw MOT region, magnetic lens, lens, 4k aperture, beam shutter
motRegion = [[mot_left_edge, mot_side_length / 2], [mot_left_edge + mot_side_length, mot_side_length / 2], \
    [mot_left_edge + mot_side_length,  -mot_side_length / 2], [mot_left_edge, -mot_side_length / 2]]
motRegion.append(motRegion[0])
xMotRegion, yMotRegion = list(zip(*motRegion))

plt.plot(xMotRegion, yMotRegion, 'k', linewidth=1.0)

# magnetic lens
magneticLensTop = [[l_cell_to_4k + l_4k_to_lens_aperture, R / 1e3], [l_cell_to_4k + l_4k_to_lens_aperture, R / 1e3 / 2], \
    [l_cell_to_4k + l_4k_to_lens_aperture + R / 1e3, R / 1e3 / 2], [l_cell_to_4k + l_4k_to_lens_aperture + R / 1e3, R / 1e3]]
magneticLensBottom = [[l_cell_to_4k + l_4k_to_lens_aperture, -R / 1e3], [l_cell_to_4k + l_4k_to_lens_aperture, -R / 1e3 / 2], \
    [l_cell_to_4k + l_4k_to_lens_aperture + R / 1e3, -R / 1e3 / 2], [l_cell_to_4k + l_4k_to_lens_aperture + R / 1e3, -R / 1e3]]
magneticLensTop.append(magneticLensTop[0])
magneticLensBottom.append(magneticLensBottom[0])
x1, y1 = list(zip(*magneticLensTop))
x2, y2 = list(zip(*magneticLensBottom))

# 4k aperture and beam shutter
plt.vlines(x=l_cell_to_4k, ymin = -10.0, ymax=-0.005, color='green', linewidth=3)
plt.vlines(x=l_cell_to_4k, ymin = 0.005, ymax=10, color='green', linewidth=3)
plt.vlines(x=l_cell_to_4k + l_4k_to_beam_shutter, ymin = -10.0, ymax=-0.007, color='green', linewidth=3)
plt.vlines(x=l_cell_to_4k + l_4k_to_beam_shutter, ymin = 0.007, ymax=10.0, color='green', linewidth=3)

# plot lens
plt.plot(x1, y1, 'k')
plt.plot(x2, y2, 'k')

# labels
plt.xlabel('z (m)')
plt.ylabel('x (m)')
plt.grid(True)
plt.title('Propagation of {} Particles in the z- and x-Coordinates'.format(int(n)))

# # ylims to show lens
# plt.axis([0.0, 0.6, -0.02, 0.02])
# ylims close-up
plt.axis([0.0, 0.70, -0.008, 0.008])

# save figure
Path('{}/propagation_plots_{}'.format(datetime.date.today(), datetime.date.today())).mkdir(parents=True, exist_ok=True)
plt.savefig('{}/propagation_plots_{}/propagation_{}_particles{}'.format(datetime.date.today(), datetime.date.today(), int(n), datetime.date.today()))
