# ----------------------------------------------------------------------------
# Sanity Checks
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

# calculate initial angular momentum
# L_init = np.array([0.0, 0.0, 0.0])
L_init = np.cross(v[0:2], p[0:2])
E_init = 0
for index in range(0, int(n) * 3, 3):
    L_init = L_init + mass * np.cross(v[index:index + 2], p[index:index + 2])
    E_init += 1/2 * mass * np.linalg.norm(v[index:index + 3])**2

# propagate particles
p_final, v_final, a_final, successes, plotZ, plotX = propagate(p, v, a, successes, successful_particles, l_4k_to_lens_aperture)

# calculate final angular momentum
# L_final = np.array([0.0, 0.0, 0.0])
L_final = np.cross(v[0:2], p[0:2])
E_final = 0
for index in range(0, int(n) * 3, 3):
    L_final = L_init + mass * np.cross(v_final[index:index + 2], p_final[index:index + 2])
    E_final += 1/2 * mass * np.linalg.norm(v[index:index + 3])**2

print('Initial angular momentum: {}'.format(L_init))
print('Final angular momentum: {}'.format(L_final))
print('Initial energy: {}'.format(E_init))
print('Final energy: {}'.format(E_final))

