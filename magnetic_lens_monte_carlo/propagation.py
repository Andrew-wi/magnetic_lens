# ----------------------------------------------------------------------------
# Kinematic propagation
# ----------------------------------------------------------------------------
from dependencies import *
from init import *
from vector_field import *

print('Propagating...\n')

# Initialize variables
kinematicPropagationFig = plt.figure()
kinematicPropagationAx = plt.subplots()

plotZ = [[] for _ in range(int(n))]
plotX = [[] for _ in range(int(n))]

hexagon = [[R / 2 / 1e3 * np.cos(angle), R / 2 / 1e3 * np.sin(angle)] for angle in np.linspace(0, 2 * np.pi, segs, endpoint=False)]
path = pltPath.Path(hexagon)

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
            p[index:index + 3] = [0, 0, 0]
            plotZ[int(index / 3)] = [0.0, 0.0]
            plotX[int(index / 3)] = [0.0, 0.0]

        if lCellTo4k + l4kToBeamShutter <= p[index + 2] <= lCellTo4k + l4kToBeamShutter + 0.005 and \
            ((p[index] ** 2 + p[index + 1] ** 2) ** (1/2)) > 0.007:
            v[index:index + 3] = [0, 0, 0]
            a[index:index + 3] = [0, 0, 0]
            p[index:index + 3] = [0, 0, 0]
            plotZ[int(index / 3)] = [0.0, 0.0]
            plotX[int(index / 3)] = [0.0, 0.0]

        if p[index + 2] >= 0.7:
            v[index:index + 3] = [0, 0, 0]
            a[index:index + 3] = [0, 0, 0]

    # Lens
    for index in range(0, int(n) * 3, 3):
        if -(R / 1e3) / 2 <= p[index] <= (R / 1e3) / 2 \
            and -(R / 1e3) / 2 <= p[index + 1] <= (R / 1e3) / 2 \
            and lCellTo4k + l4kToLensAperture <= p[index + 2] <= lCellTo4k + l4kToLensAperture + R / 1e3:

            if not path.contains_point((p[index], p[index + 1])):
                # print('Found a point outside the bore. x, y: {}, {}\n'.format(p[index], p[index + 1]))
                v[index:index + 3] = [0, 0, 0]
                a[index:index + 3] = [0, 0, 0]
                continue

            # get spacing
            l = (R / 1e3) / (m - 1)

            # x, y, z direction deviation
            xCoord = round(abs(-((R / 2) / 1e3) - p[index]) / l)
            yCoord = round(abs(-((R / 2) / 1e3) - p[index + 1]) / l)
            zCoord = round((p[index + 2] - (lCellTo4k + l4kToLensAperture)) / l)

            # print('x position: {}'.format(p[index]))
            # print('x calculation: {}'.format(xCoord))
            # print('y position: {}'.format(p[index + 1]))
            # print('y calculation: {}'.format(yCoord))
            # print('z position: {}'.format(p[index + 2]))
            # print('z calculation: {}\n'.format(zCoord))

            # todo: optimize additional force scaling factor
            a[index:index + 3] = forceField[int(xCoord), int(yCoord), int(zCoord)] / mass * 1e6

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

for index in range(0, int(n) * 3, 3):
    if p[index + 2] >= lCellTo4k and \
        ((p[index] ** 2 + p[index + 1] ** 2) ** (1/2)) > 0.006:
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
xMotRegion, yMotRegion = list(zip(*motRegion))

# todo: refactor plotting into another file
# todo: export data into files
plt.plot(xMotRegion, yMotRegion, 'k', linewidth=2.0)
plt.vlines(x=lCellTo4k, ymin = -10.0, ymax=-0.005, color='green')
plt.vlines(x=lCellTo4k, ymin = 0.005, ymax=10, color='green', label='4K Aperture (1.0 cm)')
plt.vlines(x=lCellTo4k + l4kToBeamShutter, ymin = -10.0, ymax=-0.007, color='green')
plt.vlines(x=lCellTo4k + l4kToBeamShutter, ymin = 0.007, ymax=10.0, color='green', label='Beam Shutter (1.4 cm)')

plt.xlabel('z (m)')
plt.ylabel('x (m)')
plt.grid(True)
plt.axis([0.0, 0.7, -0.008, 0.008])

plt.title('Kinematic Propagation of {} Particles in the z- and x-Coordinates'.format(int(n)))
Path('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/kinematic_propagation_plots_{}'\
    .format(datetime.date.today())).mkdir(parents=True, exist_ok=True)
plt.savefig('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/kinematic_propagation_plots_{}/kinematic_propagation_{}_particles{}'\
    .format(datetime.date.today(), int(n), datetime.date.today()))

print('Done.\n')
