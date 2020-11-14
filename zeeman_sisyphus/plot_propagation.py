# ----------------------------------------------------------------------------
# Propagation, Plot
# ----------------------------------------------------------------------------
from dependencies import *
from helpers import *
from init import *
from vector_field import *
from propagation import *

import sys

# initialize variables
n = int(n)
successes_pp = 0
successful_particles_pp = np.zeros(n, dtype=bool)
p_pre = np.zeros((n, 3))
v_pre = np.zeros((n, 3))
a_pre = np.zeros((n, 3))
m_s_pre = np.zeros((n, 3))
p, v, a, m_s = generate(n, p_pre, v_pre, a_pre, m_s_pre)

pos_pp, vel_pp, acc_pp, successes_pp, successful_particles_pp = \
    propagate(n, p, v, a, successes_pp, successful_particles_pp, l_4k_to_lens_aperture, m_s,\
        decel=True, plot=True, pruning='to_magnet')

print('Successes: {}'.format(successes_pp))
print('Successful particles: {}'.format(np.where(successful_particles_pp == True)))
