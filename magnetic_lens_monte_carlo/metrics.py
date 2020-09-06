# ----------------------------------------------------------------------------
# Propagation
# ----------------------------------------------------------------------------
from dependencies import *
from init import *
from vector_field import *
from propagation import *

# setup
successes = 0
successful_particles = []

# generate particles
p, v, a = generate()

# propagate particles
p_final, v_final, a_final, successes, plotZ, plotX = propagate(p, v, a, successes, successful_particles, l_4k_to_lens_aperture)

def metrics():
