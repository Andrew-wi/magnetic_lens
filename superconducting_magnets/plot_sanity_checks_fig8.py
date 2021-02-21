# ----------------------------------------------------------------------------
# Propagation, Plot Sanity Checks Figure 8
# ----------------------------------------------------------------------------
from dependencies import *
from helpers import *
from init import *
from vector_field import *
from propagation_sanity_checks import *

import sys

# initialize variables
start_time_fig_8 = datetime.datetime.now()
print(f'Starting time: {start_time_fig_8}')
print(f'Run: {mol_run}')
n = int(n)
successes_pp = 0
successful_particles_pp = np.zeros(n, dtype=bool)
p_pre = np.zeros((n, 3))
v_pre = np.zeros((n, 3))
a_pre = np.zeros((n, 3))
m_s_pre = np.zeros(n)
p, v, a, m_s = generate(n, p_pre, v_pre, a_pre, m_s_pre)

pos_pp, vel_pp, acc_pp, successes_pp, successful_particles_pp = \
    propagate_sanity(n, p, v, a, successes_pp, successful_particles_pp, \
                     l_4k_to_lens_aperture, m_s, decel=True, plot=False, pruning='to_magnet', \
                     plot_vel=True, plot_vel_particles=mols_tracking,
                     spin_tracking=False, spin_tracked_particles=mols_tracking,
                     plot_long_dist=True, plot_long_dist_particles=mols_tracking)

with open(f'./{date}/data_{date}/run_data_{date}.csv', 'a+') as data_file:
    data_file.write(f'{str(datetime.datetime.now())},{mol_run},')
    str_succ = ','.join(map(str, np.where(successful_particles_pp == True)[0]))
    data_file.write(f'successes_pp={successes_pp},succ_mols_pp=,{str_succ if len(str_succ) > 0 else 0}\n')

print('Successes: {}'.format(successes_pp))
print('Successful particles: {}'.format(np.where(successful_particles_pp == True)))
print(f'Total elapsed time: {datetime.datetime.now() - start_time_fig_8}')