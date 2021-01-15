# ----------------------------------------------------------------------------
# Propagation, Scan Zeeman-Sisyphus Decelerator Length and Detunings
# ----------------------------------------------------------------------------
from dependencies import *
from helpers import *
from init import *
from vector_field import *
from propagation import *

import pandas as pd

start_time_scan_len_dets = datetime.datetime.now()
print(f'Start time: {start_time_scan_len_dets}')

# init
scan_fig = plt.figure()
scan_ax = plt.axes()
n = int(n)
# successes_pre = 0
# successful_particles_pre = np.zeros(n, dtype=bool)
p_pre = np.zeros((n, 3))
v_pre = np.zeros((n, 3))
a_pre = np.zeros((n, 3))
m_s_pre = np.zeros(n)
p, v, a, m_s = generate(n, p_pre, v_pre, a_pre, m_s_pre)
del_0_s2w_list = np.array([0.5e9, 1.5e9, 2.5e9, 3.5e9, 4.5e9, 5.5e9]) # units: Hz
z_lens_list = np.array([250, 500, 750, 1000, 1250, 1500]) # units: mm
desired_vel_class_vz = 50 # units: m/s
desired_populations_dict_list = []

# initial population run
pos_pp, vel_pp, acc_pp, successes_pp, successful_particles_pp = \
    propagate(n, p, v, a, 0, np.zeros(n, dtype=bool), \
    l_4k_to_lens_aperture, m_s, decel=False, visual=False)

print('Successes, no decel: {}'.format(successes_pp))
print('Successful particles, no decel: {}'.format(np.where(successful_particles_pp == True)))

for i, del_s2w in enumerate(del_0_s2w_list):

    for j, z_len in enumerate(z_lens_list):

        pos_pp, vel_pp, acc_pp, successes_pp, successful_particles_pp = \
            propagate(n, p, v, a, 0, np.zeros(n, dtype=bool), \
            l_4k_to_lens_aperture, m_s, decel=True, del_0_s2w=del_s2w, zsd_length=z_len, visual=False)

        print('Successes, del2w = {} and z_len = {}: {}'.format(del_s2w / 1e9, z_len / 1e3, successes_pp))
        print('Successful particles, del2w = {} and z_len = {}: {}'.format(del_s2w  / 1e9, z_len / 1e3, \
            np.where(successful_particles_pp == True)))

        desired_molecules = (vel_pp[successful_particles_pp, 2] < desired_vel_class_vz).sum()
        print('Number of molecules in desired velocity class: {}'.format(desired_molecules))

        # save results to new dict, add to dict list
        results_dict = {'del_s2w': del_s2w / 1e9, 'z_len': z_len, 'desired_vel_class': desired_molecules}
        desired_populations_dict_list.append(results_dict)

        print(f'Elapsed time so far: {datetime.datetime.now() - start_time_scan_len_dets}')

# dataframe
desired_pop_df = pd.DataFrame(desired_populations_dict_list)
Path('{}/param_scans_{}'.format(date, date)).mkdir(parents=True, exist_ok=True)
desired_pop_df.to_csv('{}/param_scans_{}/param_scans_{}.csv'.format(date, date, date))

pivoted_df = desired_pop_df.pivot(index='del_s2w', columns='z_len', values='desired_vel_class')
plot_param_scan_heatmap(scan_fig, scan_ax, pivoted_df)

print('Total elapsed time: {}'.format(datetime.datetime.now() - start_time_scan_len_dets))