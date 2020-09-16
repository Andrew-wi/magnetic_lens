# ----------------------------------------------------------------------------
# Propagation
# ----------------------------------------------------------------------------
from dependencies import *
from init import *

# ======================== analytical lens ========================

print('Generating vector fields...')

# create fake b matrix
force_x = np.linspace(-1, 1, m)
force_y = np.linspace(-1, 1, m)
force_z = np.zeros((m, m))

# take components and multiply by absolute value of themselves, make into matrix
force_x = np.tile(force_x, (m, 1))
force_y = np.tile(force_y, (m, 1))

# reshape y components
force_y = force_y.transpose()

# stack components to make force_matrix
force_matrix = np.stack([force_x, force_y, force_z], axis=2)

# expand axis dimensions
force_matrix = np.expand_dims(force_matrix, axis=2)

# repeat along 0-th axis
force_matrix = np.repeat(force_matrix, m, axis=2)

force_field = -m_s * g * mu_B * force_matrix

print(force_field)

# ======================== propagation ========================

# initialize plotting variables
plotZ = [[] for _ in range(int(n))]
plotX = [[] for _ in range(int(n))]
hexagon = [[R / 2 / 1e3 * np.cos(angle), R / 2 / 1e3 * np.sin(angle)] for angle in np.linspace(0, 2 * np.pi, segs, endpoint=False)]
hexPath = pltPath.Path(hexagon)

for index in range(0, int(n) * 3, 3):
    plotZ[int(index / 3)].append(p[index + 2])
    plotX[int(index / 3)].append(p[index])

# step through time
def propagate(p, v, a, successes, successful_particles):
    print('Propagating...')
    for time in np.linspace(0, t_final, num=steps, endpoint=False):
        for index in range(0, int(n) * 3, 3):
            # 4k aperture
            if l_cell_to_4k <= p[index + 2] <= l_cell_to_4k + 0.005 and \
                ((p[index] ** 2 + p[index + 1] ** 2) ** (1/2)) > 0.005:
                v[index:index + 3] = [0, 0, 0]
                a[index:index + 3] = [0, 0, 0]
                continue
            # Lens ---------------
            elif l_cell_to_4k + l_4k_to_lens_aperture <= p[index + 2] <= l_cell_to_4k + l_4k_to_lens_aperture + R / 1e3 \
                and ((p[index] ** 2 + p[index + 1] ** 2) ** (1/2)) < 0.0107:
                # if not hexPath.contains_point((p[index], p[index + 1])):
                #     v[index:index + 3] = [0, 0, 0]
                #     a[index:index + 3] = [0, 0, 0]
                #     continue
                l = (R / 1e3) / (m - 1)
                xCoord = round(((R / 2) / 1e3 + p[index]) / l)
                yCoord = round(((R / 2) / 1e3 + p[index + 1]) / l)
                zCoord = round((p[index + 2] - (l_cell_to_4k + l_4k_to_lens_aperture)) / l)
                # todo: adjust scaling factor
                a[index:index + 3] = force_field[int(yCoord), int(xCoord), int(zCoord)] / mass * m*1e3/R
                continue
            # Lens ---------------
            # beam shutter
            elif l_cell_to_4k + l_4k_to_beam_shutter <= p[index + 2] <= l_cell_to_4k + l_4k_to_beam_shutter + 0.005 and \
                ((p[index] ** 2 + p[index + 1] ** 2) ** (1/2)) > 0.007:
                v[index:index + 3] = [0, 0, 0]
                a[index:index + 3] = [0, 0, 0]
                continue
            # maximum distance, for simplicity
            elif p[index + 2] >= 0.7:
                v[index:index + 3] = [0, 0, 0]
                a[index:index + 3] = [0, 0, 0]
                continue
            else:
                a[index:index + 3] = [0, 0, 0]
        timestep = t_final / steps
        v += a * timestep
        p += v * timestep
        for index in range(0, int(n) * 3, 3):
            # todo: include accurate MOT region measurements
            if -mot_side_length / 2 <= p[index] <= mot_side_length / 2 and \
                -mot_side_length / 2 <= p[index + 1] <= mot_side_length / 2 and \
                mot_left_edge <= p[index + 2] <= mot_left_edge + mot_side_length and \
                int(index / 3) not in successful_particles:
                successful_particles.append(int(index / 3))
                successes += 1
            plotZ[int(index / 3)].append(p[index + 2])
            plotX[int(index / 3)].append(p[index])
    return p, v, a, successes, plotZ, plotX

# ======================== plotting ========================

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

# propagate
p, v, a, successes, plotZ, plotX = propagate(p, v, a, successes, successful_particles)

# # prune out stray trajectories
# for index in range(0, int(n) * 3, 3):
#     if p[index + 2] >= l_cell_to_4k and \
#         ((p[index] ** 2 + p[index + 1] ** 2) ** (1/2)) > 0.01: # todo: make 0.008
#         plotZ[int(index / 3)] = [0.0, 0.0]
#         plotX[int(index / 3)] = [0.0, 0.0]
#     elif p[index + 2] <= l_cell_to_4k + l_4k_to_beam_shutter + 0.05:
#         plotZ[int(index / 3)] = [0.0, 0.0]
#         plotX[int(index / 3)] = [0.0, 0.0]

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
plt.axis([0.0, 0.6, -0.008, 0.008])

# save figure
Path('{}/propagation_plots_{}'.format(datetime.date.today(), datetime.date.today())).mkdir(parents=True, exist_ok=True)
plt.savefig('{}/propagation_plots_{}/propagation_{}_particles{}'.format(datetime.date.today(), datetime.date.today(), int(n), datetime.date.today()))
