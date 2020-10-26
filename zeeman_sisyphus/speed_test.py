# ----------------------------------------------------------------------------
# Speed test
# ----------------------------------------------------------------------------
from dependencies import *
from helpers import *
from init import *
from vector_field import *
from propagation import *

import sys

# initialize variables
successes = 0
successful_particles = []
p, v, a, m_s = generate()

# # change lens distance; comment out these lines when running plot_propagation without testing
# l_4k_to_lens_aperture = float(sys.argv[1])
# print('new lens to 4k distance: {}'.format(l_4k_to_lens_aperture))

# propagate
pos_pp, vel_pp, acc_pp, successes_postrun, successful_particles_postrun = propagate(p, v, a, successes, successful_particles, l_4k_to_lens_aperture, m_s)

print('Number of successes: {}'.format(successes_postrun))
print('Successful particle catalog number: {}'.format(successful_particles_postrun))

