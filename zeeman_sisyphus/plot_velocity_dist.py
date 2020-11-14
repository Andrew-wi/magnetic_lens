# ----------------------------------------------------------------------------
# Propagation, Plot Velocity Distribution
# ----------------------------------------------------------------------------
from dependencies import *
from helpers import *
from init import *
from vector_field import *
from propagation import *

import seaborn as sns
import sys


propagationFig = plt.figure()
propagationAx = plt.subplots()

# initialize variables
n = int(n)
p_pre = np.zeros((n, 3))
v_pre = np.zeros((n, 3))
a_pre = np.zeros((n, 3))
m_s_pre = np.zeros((n, 3))
p, v, a, m_s = generate(n, p_pre, v_pre, a_pre, m_s_pre)
successes_nl = 0
successful_particles_nl = np.zeros(n, dtype=bool)

# plot v distribution without zs decel
pos_nl, vel_nl, acc_nl, successes_nl, successful_particles_nl = \
    propagate(n, p, v, a, successes_nl, successful_particles_nl, l_4k_to_lens_aperture, m_s, decel=False)
print('Success rate for no decelerator: {}'.format(successes_nl/n))
sns.distplot(vel_nl[successful_particles_nl, 2], label='No Decelerator')

# initialize variables
n = int(n)
p_pre = np.zeros((n, 3))
v_pre = np.zeros((n, 3))
a_pre = np.zeros((n, 3))
m_s_pre = np.zeros((n, 3))
p, v, a, m_s = generate(n, p_pre, v_pre, a_pre, m_s_pre)
successes_pp = 0
successful_particles_pp = np.zeros(n, dtype=bool)

# plot distribution without decel
pos_pp, vel_pp, acc_pp, successes_pp, successful_particles_pp = \
    propagate(n, p, v, a, successes_pp, successful_particles_pp, l_4k_to_lens_aperture, m_s, decel=True)
print('Success rate for decelerator: {}'.format(successes_pp/n))
sns.distplot(vel_pp[successful_particles_pp, 2], label='With Decelerator')

# labels
plt.xlabel('v_z (m)')
plt.ylabel('Frequency (arbitrary)')
plt.grid(True)
plt.title('Velocity Distribution of {} Particles, With and Without Decelerator'.format(int(n)))
plt.legend()

# save figure
Path('{}/velocity_distribution_{}'.format(datetime.date.today(), datetime.date.today())).\
    mkdir(parents=True, exist_ok=True)
plt.savefig('{}/velocity_distribution_{}/velocity_distribution_{}_particles{}'.\
    format(datetime.date.today(), datetime.date.today(), int(n), datetime.date.today()))
