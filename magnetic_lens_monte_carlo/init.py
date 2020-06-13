# ----------------------------------------------------------------------------
# # Initialize n molecules
# ----------------------------------------------------------------------------
from dependencies import *

# Generate particles
print('Generating particles...')

for i in range(n):
    p = np.append(p, [0.0, 0.0, 0.0])
    v = np.append(v, [np.random.standard_normal(), \
        np.random.standard_normal(),\
        np.random.normal(loc=100.0, scale=1.0)])
    a = np.append(a, [0.0, 0.0, 0.0])
print('Done.')

print('Positions array: \n {} \n'.format(p))
print('Velocities array: \n {} \n'.format(v))
print('Accelerations array: \n {} \n'.format(a))
