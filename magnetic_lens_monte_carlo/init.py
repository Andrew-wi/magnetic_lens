# ----------------------------------------------------------------------------
# # Initialize n molecules
# ----------------------------------------------------------------------------
from dependencies import *

# Generate particles
print('Generating particles...')

for index in range(0, int(n) * 3, 3):
    p = np.append(p, [np.random.normal(loc=0.0, scale=sigmaXY), \
        np.random.normal(loc=0.0, scale=sigmaXY), 0.0])
    v = np.append(v, [np.random.normal(loc=0.0, scale=sigmaVxy), \
        np.random.normal(loc=0.0, scale=sigmaVxy), \
        np.random.normal(loc=muVz, scale=sigmaVz)])
    a = np.append(a, [0.0, 0.0, 0.0])

    while p[index] <= -0.005 or p[index] >= 0.005 or \
        p[index + 1] <= -0.005 or p[index + 1] >= 0.005:
        p[index:index + 2] = [np.random.normal(loc=0.0, scale=sigmaXY), \
        np.random.normal(loc=0.0, scale=sigmaXY)]

    while v[index + 2] < 0:
        v[index + 2] = np.random.normal(loc=muVz, scale=sigmaVz)
print('Done.\n')

print('====================================== Initial Conditions ======================================')
print('Positions array: \n {} \n'.format(p))
print('Velocities array: \n {} \n'.format(v))
print('Accelerations array: \n {}'.format(a))
print('================================================================================================\n')
