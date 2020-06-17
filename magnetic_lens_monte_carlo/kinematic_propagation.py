# ----------------------------------------------------------------------------
# Kinematic propagation
# ----------------------------------------------------------------------------
from dependencies import *
from init import *
from vector_field import *

print('Propagating...\n')

# Initialize variables
kinematicPropagationFig = plt.figure()
kinematicPropagationAx = plt.subplot()

plotZ = [[] for _ in range(int(n))]
plotX = [[] for _ in range(int(n))]

hexagon = [[R / 2 / 1e3 * np.cos(angle), R / 2 / 1e3 * np.sin(angle)] for angle in np.linspace(0, 2 * np.pi, segs, endpoint=False)]
path = pltPath.Path(hexagon)

for index in range(0, int(n) * 3, 3):
    plotZ[int(index / 3)].append(p[index + 2])
    plotX[int(index / 3)].append(p[index])

# Evolve system through time
for time in np.linspace(0, tFinal, num=steps, endpoint=False):
    timestep = tFinal / steps
    for index in range(0, int(n) * 3, 3):
        if p[index + 2] >= lCellTo4k and\
        ((p[index] ** 2 + p[index + 1] ** 2) ** (1/2)) > 0.005:
            v[index:index + 3] = [0, 0, 0]
            a[index:index + 3] = [0, 0, 0]
        elif v[index + 2] < 0:
            v[index:index + 3] = [0, 0, 0]
            a[index:index + 3] = [0, 0, 0]

    for index in range(0, int(n) * 3, 3):
        if -(R / 1e3) / 2 <= p[index] <= (R / 1e3) / 2\
            and -(R / 1e3) / 2 <= p[index + 1] <= (R / 1e3) / 2\
            and lCellTo4k + l4kToAperture <= p[index + 2] <= lCellTo4k + l4kToAperture + R / 1e3:

            if not path.contains_point((p[index], p[index + 1])):
                print('Found a point outside the bore. x, y: {}, {}\n'.format(p[index], p[index + 1]))
                v[index:index + 3] = [0, 0, 0]
                a[index:index + 3] = [0, 0, 0]
                continue

            # get spacing
            l = (R / 1e3) / (m - 1)

            # x, y, z direction deviation
            xCoord = round(abs(-((R / 2) / 1e3) - p[index]) / l)
            yCoord = round(abs(-((R / 2) / 1e3) - p[index + 1]) / l)
            zCoord = round((p[index + 2] - (lCellTo4k + l4kToAperture)) / l)

            print('x position: {}'.format(p[index]))
            print('x calculation: {}'.format(xCoord))
            print('y position: {}'.format(p[index + 1]))
            print('y calculation: {}'.format(yCoord))
            print('z position: {}'.format(p[index + 2]))
            print('z calculation: {}\n'.format(zCoord))

            # todo: include mass factor
            a[index:index + 3] = gradBMatrix[int(xCoord), int(yCoord), int(zCoord)] / mass * 1e5
        else:
            a[index:index + 3] = [0, 0, 0]

    v += a * timestep
    p += v * timestep

    for index in range(0, int(n) * 3, 3):
        if -0.0125 <= p[index] <= 0.0125 and -0.0125 <= p[index + 1] <= 0.0125 and \
            (0.57 + lCellTo4k - 0.0125) <= p[index + 2] <= (0.57 + lCellTo4k + 0.0125):
            success += 1
        plotZ[int(index / 3)].append(p[index + 2])
        plotX[int(index / 3)].append(p[index])

print('Ending positions: {}'.format(p))
print('Total particles through MOT region: {}'.format(success))
print('Success rate: {}\n'.format(success / n))
print('Done.\n')

print('Plotting trajectories...')

for index in range(0, int(n) * 3, 3):
    plt.plot(plotZ[int(index / 3)], plotX[int(index / 3)], 'r-', linewidth=0.5)

plt.xlabel('z (m)')
plt.ylabel('x (m)')
plt.grid(True)

plt.title('Kinematic Propagation of {} Particles in the z- and x-Coordinates'.format(int(n)))
Path('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/kinematic_propagation_plots_{}'\
    .format(datetime.date.today())).mkdir(parents=True, exist_ok=True)
plt.savefig('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/kinematic_propagation_plots_{}/kinematic_propagation_{}_particles{}'\
    .format(datetime.date.today(), int(n), datetime.date.today()))

print('Done.\n')

# ----------------------------------------------------------------------------
# Calculate how many molecules end up in the trap region
# ----------------------------------------------------------------------------

# print('Calculating success rate...')
# todo
# print('Done.')
