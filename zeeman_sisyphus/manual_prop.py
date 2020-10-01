# ----------------------------------------------------------------------------
# Manual Propagation
# ----------------------------------------------------------------------------
from dependencies import *
from init import *
from vector_field import *
from propagation import *

import sys

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

# set dependencies
l_4k_to_lens_aperture = float(sys.argv[1])

# propagate
p, v, a, successes, plotZ, plotX, _ = propagate(p, v, a, successes, successful_particles, l_4k_to_lens_aperture)

print('Success rate: {}'.format(successes / n))
