# ----------------------------------------------------------------------------
# Propagation
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
tracking = [1452, 1630, 1691, 2360, 2614, 4109, 4113, 4231, 5732, 5741, 5812, \
    6373, 6503, 7080, 9940]

pos_pp, vel_pp, acc_pp, successes_pp, successful_particles_pp = \
    propagate(n, p, v, a, successes_pp, successful_particles_pp, \
              l_4k_to_lens_aperture, m_s, decel=True, plot=False, \
              spin_tracking=True, spin_tracked_particles=tracking)

print('Successes: {}'.format(successes_pp))
print('Successful particles: {}'.format(np.where(successful_particles_pp == True)))
