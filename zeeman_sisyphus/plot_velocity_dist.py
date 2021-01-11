# ----------------------------------------------------------------------------
# Propagation, Plot Velocity Distribution
# ----------------------------------------------------------------------------
from dependencies import *
from helpers import *
from init import *
from vector_field import *
from propagation import *

import sys

propagationFig = plt.figure()
propagationAx = plt.subplots()

# initialize variables
starting_time_plot_vel = datetime.datetime.now()
print(f'Starting time: {starting_time_plot_vel}')
n = int(n)
p_pre = np.zeros((n, 3))
v_pre = np.zeros((n, 3))
a_pre = np.zeros((n, 3))
m_s_pre = np.zeros(n)
p, v, a, m_s = generate(n, p_pre, v_pre, a_pre, m_s_pre)
successes_no_decel = 0
successful_particles_no_decel = np.zeros(n, dtype=bool)
sucesses_with_decel = 0
successful_particles_with_decel = np.zeros(n, dtype=bool)

# plot v distribution without zs decel
pos_nl, vel_nl, acc_nl, successes_no_decel, successful_particles_no_decel = \
    propagate(n, p, v, a, successes_no_decel, successful_particles_no_decel, \
    	l_4k_to_lens_aperture, m_s, decel=False, deepcopy=True, visual=False)
print(f'Success rate for no decelerator: {successes_no_decel / n}')
sns.histplot(data=vel_nl[successful_particles_no_decel, 2], \
	label=f'No Decelerator = {successes_no_decel}', stat='count', \
    kde=True, color=np.random.random(3), binwidth=2)

# plot distribution with decel
pos_pp, vel_pp, acc_pp, sucesses_with_decel, successful_particles_with_decel = \
    propagate(n, p, v, a, sucesses_with_decel, successful_particles_with_decel, \
    	l_4k_to_lens_aperture, m_s, decel=True, deepcopy=True, visual=False)
print(f'Success rate for decelerator: {sucesses_with_decel / n}')
sns.histplot(data=vel_pp[successful_particles_with_decel, 2], \
	label=f'With Decelerator = {sucesses_with_decel}', stat='count', \
    kde=True, color=np.random.random(3), binwidth=2)

# labels
plt.xlabel('v_z (m)')
plt.ylabel('Count')
plt.grid(True)
plt.title('Velocity Distribution of {} Particles, With and Without Decelerator'.format(int(n)))
plt.legend()

# save figure
Path('{}/velocity_distribution_{}'.format(date, date)).\
    mkdir(parents=True, exist_ok=True)
plt.savefig('{}/velocity_distribution_{}/velocity_distribution_{}_particles_{}_{}_{}'.\
    format(date, date, int(n), str(successes_no_decel / n).replace('.', 'p'), \
    str(sucesses_with_decel / n).replace('.', 'p'), date))

print(f'Total elapsed time: {datetime.datetime.now() - starting_time_plot_vel}')