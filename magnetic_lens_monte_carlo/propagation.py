# ----------------------------------------------------------------------------
# Propagation
# ----------------------------------------------------------------------------
from dependencies import *
from init import *
from vector_field import *

print('Propagating...\n')

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

# Evolve system through time
for time in np.linspace(0, tFinal, num=steps, endpoint=False):

    for index in range(0, int(n) * 3, 3):

        if lCellTo4k <= p[index + 2] <= lCellTo4k + 0.005 and \
            ((p[index] ** 2 + p[index + 1] ** 2) ** (1/2)) > 0.005:
            v[index:index + 3] = [0, 0, 0]
            a[index:index + 3] = [0, 0, 0]
            # p[index:index + 3] = [0, 0, 0]
            # Prettify
            plotZ[int(index / 3)] = [0.0, 0.0]
            plotX[int(index / 3)] = [0.0, 0.0]
            continue

    # Lens ---------------
        elif lCellTo4k + l4kToLensAperture <= p[index + 2] <= lCellTo4k + l4kToLensAperture + R / 1e3:

            if not hexPath.contains_point((p[index], p[index + 1])):
                v[index:index + 3] = [0, 0, 0]
                a[index:index + 3] = [0, 0, 0]
                continue

            # temp, todo: remove
            if ((p[index] ** 2 + p[index + 1] ** 2) ** (1/2)) > 0.010:
                v[index:index + 3] = [0, 0, 0]
                a[index:index + 3] = [0, 0, 0]
                p[index:index + 3] = [0, 0, 0]
                continue


            # todo: check all R/2 vs R
            l = (R / 1e3) / (m - 1)
            xCoord = round(abs(-((R / 2) / 1e3) - p[index]) / l)
            yCoord = round(abs(-((R / 2) / 1e3) - p[index + 1]) / l)
            zCoord = round((p[index + 2] - (lCellTo4k + l4kToLensAperture)) / l)
            # todo: adjust mass scaling factor
            a[index:index + 3] = forceField[int(xCoord), int(yCoord), int(zCoord)] / mass
            continue
    # Lens ---------------

        elif lCellTo4k + l4kToBeamShutter <= p[index + 2] <= lCellTo4k + l4kToBeamShutter + 0.005 and \
            ((p[index] ** 2 + p[index + 1] ** 2) ** (1/2)) > 0.007:
            v[index:index + 3] = [0, 0, 0]
            a[index:index + 3] = [0, 0, 0]
            # p[index:index + 3] = [0, 0, 0]
            # Prettify
            plotZ[int(index / 3)] = [0.0, 0.0]
            plotX[int(index / 3)] = [0.0, 0.0]
            continue

        elif p[index + 2] >= 0.7:
            v[index:index + 3] = [0, 0, 0]
            a[index:index + 3] = [0, 0, 0]
            continue

        else:
            a[index:index + 3] = [0, 0, 0]

    timestep = tFinal / steps
    v += a * timestep
    p += v * timestep

    for index in range(0, int(n) * 3, 3):
        # todo: include accurate MOT region measurements
        if -motSideLength / 2 <= p[index] <= motSideLength / 2 and \
            -motSideLength / 2 <= p[index + 1] <= motSideLength / 2 and \
            motLeftEdge <= p[index + 2] <= motLeftEdge + motSideLength and \
            int(index / 3) not in successfulParticles:
            successfulParticles.append(int(index / 3))
            successes += 1
        plotZ[int(index / 3)].append(p[index + 2])
        plotX[int(index / 3)].append(p[index])

# todo: prettify, prune out stray trajectories
for index in range(0, int(n) * 3, 3):
    if p[index + 2] >= lCellTo4k and \
        ((p[index] ** 2 + p[index + 1] ** 2) ** (1/2)) > 0.006:
        plotZ[int(index / 3)] = [0.0, 0.0]
        plotX[int(index / 3)] = [0.0, 0.0]
    if p[index + 2] <= lCellTo4k + l4kToLensAperture:
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
motRegion = [[motLeftEdge, motSideLength / 2], [motLeftEdge + motSideLength, motSideLength / 2], \
    [motLeftEdge + motSideLength,  -motSideLength / 2], [motLeftEdge, -motSideLength / 2]]
motRegion.append(motRegion[0])
xMotRegion, yMotRegion = list(zip(*motRegion))

# todo: refactor plotting into another file
# todo: export data into files
plt.plot(xMotRegion, yMotRegion, 'k', linewidth=1.0)
plt.vlines(x=lCellTo4k, ymin = -10.0, ymax=-0.005, color='green')
plt.vlines(x=lCellTo4k, ymin = 0.005, ymax=10, color='green')
plt.vlines(x=lCellTo4k + l4kToBeamShutter, ymin = -10.0, ymax=-0.007, color='green')
plt.vlines(x=lCellTo4k + l4kToBeamShutter, ymin = 0.007, ymax=10.0, color='green')

magneticLensTop = [[lCellTo4k + l4kToLensAperture, R / 1e3], [lCellTo4k + l4kToLensAperture, R / 1e3 / 2], \
    [lCellTo4k + l4kToLensAperture + R / 1e3, R / 1e3 / 2], [lCellTo4k + l4kToLensAperture + R / 1e3, R / 1e3]]
magneticLensBottom = [[lCellTo4k + l4kToLensAperture, -R / 1e3], [lCellTo4k + l4kToLensAperture, -R / 1e3 / 2], \
    [lCellTo4k + l4kToLensAperture + R / 1e3, -R / 1e3 / 2], [lCellTo4k + l4kToLensAperture + R / 1e3, -R / 1e3]]

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
# plt.axis([0.0, 0.6, -0.015, 0.015])

plt.title('Propagation of {} Particles in the z- and x-Coordinates'.format(int(n)))
Path('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/propagation_plots_{}'\
    .format(datetime.date.today())).mkdir(parents=True, exist_ok=True)
plt.savefig('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/propagation_plots_{}/propagation_{}_particles{}'\
    .format(datetime.date.today(), int(n), datetime.date.today()))

print('Done.\n')
