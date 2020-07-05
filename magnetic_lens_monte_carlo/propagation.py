# ----------------------------------------------------------------------------
# Propagation
# ----------------------------------------------------------------------------
from dependencies import *
from init import *
from vector_field import *

# Initialize variables
propagationFig = plt.figure()
propagationAx = plt.subplots()
plotZ = [[] for _ in range(int(n))]
plotX = [[] for _ in range(int(n))]
hexagon = [[R / 2 / 1e3 * np.cos(angle), R / 2 / 1e3 * np.sin(angle)] for angle in np.linspace(0, 2 * np.pi, segs, endpoint=False)]
hexPath = pltPath.Path(hexagon)

for index in range(0, int(n) * 3, 3):
    plotZ[int(index / 3)].append(p[index + 2])
    plotX[int(index / 3)].append(p[index])

# step through time
def propagate():
    print('Propagating...\n')
    for time in np.linspace(0, t_final, num=steps, endpoint=False):
        for index in range(0, int(n) * 3, 3):
            if l_cell_to_4k <= p[index + 2] <= l_cell_to_4k + 0.005 and \
                ((p[index] ** 2 + p[index + 1] ** 2) ** (1/2)) > 0.005:
                v[index:index + 3] = [0, 0, 0]
                a[index:index + 3] = [0, 0, 0]
                # p[index:index + 3] = [0, 0, 0]
                continue
        # Lens ---------------
            elif l_cell_to_4k + l_4k_to_lens_aperture <= p[index + 2] <= l_cell_to_4k + l_4k_to_lens_aperture + R / 1e3:
                if not hexPath.contains_point((p[index], p[index + 1])):
                    v[index:index + 3] = [0, 0, 0]
                    a[index:index + 3] = [0, 0, 0]
                    continue
                # todo: check all R/2 vs R
                l = (R / 1e3) / (m - 1)
                xCoord = round(abs(-((R / 2) / 1e3) - p[index]) / l)
                yCoord = round(abs(-((R / 2) / 1e3) - p[index + 1]) / l)
                zCoord = round((p[index + 2] - (l_cell_to_4k + l_4k_to_lens_aperture)) / l)
                # todo: adjust mass scaling factor
                a[index:index + 3] = forceField[int(xCoord), int(yCoord), int(zCoord)] / mass
                continue
        # Lens ---------------
            elif l_cell_to_4k + l_4k_to_beam_shutter <= p[index + 2] <= l_cell_to_4k + l_4k_to_beam_shutter + 0.005 and \
                ((p[index] ** 2 + p[index + 1] ** 2) ** (1/2)) > 0.007:
                v[index:index + 3] = [0, 0, 0]
                a[index:index + 3] = [0, 0, 0]
                continue
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
                int(index / 3) not in successfulParticles:
                successfulParticles.append(int(index / 3))
                successes += 1
            plotZ[int(index / 3)].append(p[index + 2])
            plotX[int(index / 3)].append(p[index])
propagate()

# todo: prettify, prune out stray trajectories (visualization)
for index in range(0, int(n) * 3, 3):
    if p[index + 2] >= l_cell_to_4k and \
        ((p[index] ** 2 + p[index + 1] ** 2) ** (1/2)) > 0.006:
        plotZ[int(index / 3)] = [0.0, 0.0]
        plotX[int(index / 3)] = [0.0, 0.0]
    if p[index + 2] <= l_cell_to_4k + l_4k_to_lens_aperture:
        plotZ[int(index / 3)] = [0.0, 0.0]
        plotX[int(index / 3)] = [0.0, 0.0]

print('Ending positions: {}'.format(p))
print('Total particles through MOT region: {}'.format(successes))
print('Success rate: {}\n'.format(successes / n))
print('Done.\n')

print('Plotting trajectories...')

for index in range(0, int(n) * 3, 3):
    plt.plot(plotZ[int(index / 3)], plotX[int(index / 3)], 'r-', linewidth=0.5)

# todo: include accurate MOT region measurements
motRegion = [[mot_left_edge, mot_side_length / 2], [mot_left_edge + mot_side_length, mot_side_length / 2], \
    [mot_left_edge + mot_side_length,  -mot_side_length / 2], [mot_left_edge, -mot_side_length / 2]]
motRegion.append(motRegion[0])
xMotRegion, yMotRegion = list(zip(*motRegion))

# todo: refactor plotting into another file
# todo: export data into files
plt.plot(xMotRegion, yMotRegion, 'k', linewidth=1.0)
plt.vlines(x=l_cell_to_4k, ymin = -10.0, ymax=-0.005, color='green')
plt.vlines(x=l_cell_to_4k, ymin = 0.005, ymax=10, color='green')
plt.vlines(x=l_cell_to_4k + l_4k_to_beam_shutter, ymin = -10.0, ymax=-0.007, color='green')
plt.vlines(x=l_cell_to_4k + l_4k_to_beam_shutter, ymin = 0.007, ymax=10.0, color='green')

magneticLensTop = [[l_cell_to_4k + l_4k_to_lens_aperture, R / 1e3], [l_cell_to_4k + l_4k_to_lens_aperture, R / 1e3 / 2], \
    [l_cell_to_4k + l_4k_to_lens_aperture + R / 1e3, R / 1e3 / 2], [l_cell_to_4k + l_4k_to_lens_aperture + R / 1e3, R / 1e3]]
magneticLensBottom = [[l_cell_to_4k + l_4k_to_lens_aperture, -R / 1e3], [l_cell_to_4k + l_4k_to_lens_aperture, -R / 1e3 / 2], \
    [l_cell_to_4k + l_4k_to_lens_aperture + R / 1e3, -R / 1e3 / 2], [l_cell_to_4k + l_4k_to_lens_aperture + R / 1e3, -R / 1e3]]

magneticLensTop.append(magneticLensTop[0])
magneticLensBottom.append(magneticLensBottom[0])

x1, y1 = list(zip(*magneticLensTop))
x2, y2 = list(zip(*magneticLensBottom))

plt.plot(x1, y1, 'k')
plt.plot(x2, y2, 'k')
plt.xlabel('z (m)')
plt.ylabel('x (m)')
plt.grid(True)
plt.axis([0.0, 0.6, -0.008, 0.008])

plt.title('Propagation of {} Particles in the z- and x-Coordinates'.format(int(n)))
Path('{}/propagation_plots_{}'.format(datetime.date.today(), datetime.date.today())).mkdir(parents=True, exist_ok=True)
plt.savefig('{}/propagation_plots_{}/propagation_{}_particles{}'.format(datetime.date.today(), datetime.date.today(), int(n), datetime.date.today()))

print('Done.\n')
