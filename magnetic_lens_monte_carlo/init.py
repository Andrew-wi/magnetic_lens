# ----------------------------------------------------------------------------
# # Initialize n molecules
# ----------------------------------------------------------------------------
from dependencies import *

# Generate particles
print('Generating particles...')

for i in range(n):
    p = np.append(p, [0.0, 0.0, 0.0])
    v = np.append(v, [np.random.normal(loc=0.0, scale=2.0), \
        np.random.normal(loc=0.0, scale=2.0),\
        np.random.normal(loc=40.0, scale=1.0)])
    a = np.append(a, [0.0, 0.0, 0.0])
print('Done.\n')

print('====================================== Initial Conditions ======================================')
print('Positions array: \n {} \n'.format(p))
print('Velocities array: \n {} \n'.format(v))
print('Accelerations array: \n {}'.format(a))
print('================================================================================================\n')
