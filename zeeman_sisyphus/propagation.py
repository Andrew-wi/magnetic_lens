# ----------------------------------------------------------------------------
# Propagation
# ----------------------------------------------------------------------------
from dependencies import *
from init import *
from vector_field import *

# initialize plotting variables
plotZ = [[] for _ in range(int(n))]
plotX = [[] for _ in range(int(n))]
hexagon = [[R / 2 / 1e3 * np.cos(angle), R / 2 / 1e3 * np.sin(angle)] for angle in np.linspace(0, 2 * np.pi, segs, endpoint=False)]
hexPath = pltPath.Path(hexagon)

for index in range(0, int(n) * 3, 3):
    plotZ[int(index / 3)].append(p[index + 2])
    plotX[int(index / 3)].append(p[index])

# step through time
def propagate(p, v, a, successes, successful_particles, l_4k_to_lens_aperture):
    print('Propagating...')
    for time in np.linspace(0, t_final, num=steps, endpoint=False):
        for index in range(0, int(n) * 3, 3):
            # 4k aperture
            if l_cell_to_4k <= p[index + 2] <= l_cell_to_4k + 0.005 and \
                ((p[index] ** 2 + p[index + 1] ** 2) ** (1/2)) > 0.005:
                v[index:index + 3] = [0, 0, 0]
                a[index:index + 3] = [0, 0, 0]
                continue
            # # Lens ---------------
            # elif l_cell_to_4k + l_4k_to_lens_aperture <= p[index + 2] <= l_cell_to_4k + l_4k_to_lens_aperture + R / 1e3 \
            #     and ((p[index] ** 2 + p[index + 1] ** 2) ** (1/2)) < 0.0107:
            #     # if not hexPath.contains_point((p[index], p[index + 1])):
            #     #     v[index:index + 3] = [0, 0, 0]
            #     #     a[index:index + 3] = [0, 0, 0]
            #     #     continue
            #     l = (R / 1e3) / (m - 1)
            #     xCoord = round(((R / 2) / 1e3 + p[index]) / l)
            #     yCoord = round(((R / 2) / 1e3 + p[index + 1]) / l)
            #     zCoord = round((p[index + 2] - (l_cell_to_4k + l_4k_to_lens_aperture)) / l)
            #     # todo: adjust scaling factor
            #     a[index:index + 3] = force_field[int(yCoord), int(xCoord), int(zCoord)] / mass
            #     continue
            # # Lens ---------------
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
