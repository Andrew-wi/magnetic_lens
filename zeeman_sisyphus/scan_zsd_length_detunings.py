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
scan_fig_absolute_number = plt.figure(figsize=(10*1.62, 10))
scan_ax_absolute_number = plt.axes()
scan_fig_desired_vel_class = plt.figure(figsize=(10*1.62, 10))
scan_ax_desired_vel_class = plt.axes()
scan_fig_enhancement = plt.figure(figsize=(10*1.62, 10))
scan_ax_enhancement = plt.axes()
scan_fig_enhancement_desired_molecules = plt.figure(figsize=(10*1.62, 10))
scan_ax_enhancement_desired_molecules = plt.axes()
scan_fig_enhancement_number_successes_1m = plt.figure(figsize=(10*1.62, 10))
scan_ax_enhancement_number_successes_1m = plt.axes()
scan_fig_enhancement_desired_molecules_1m = plt.figure(figsize=(10*1.62, 10))
scan_ax_enhancement_desired_molecules_1m = plt.axes()
scan_fig_mean_velocity = plt.figure(figsize=(10*1.62, 10))
scan_ax_mean_velocity = plt.axes()
scan_fig_mean_velocity_reduction = plt.figure(figsize=(10*1.62, 10))
scan_ax_mean_velocity_reduction = plt.axes()
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
results_dict_list = []
initial_nodecel_list = []

# initial population runs
for i, z_len in enumerate(z_lens_list):

    mot_region_distance = l_cell_to_4k + l_4k_to_lens_aperture + z_len / 1e3

    _, vel_pp_no_decel, _, successes_pp_no_decel, successful_mols_pp_no_decel = \
        propagate(n, p, v, a, 0, np.zeros(n, dtype=bool), l_4k_to_lens_aperture, m_s, \
                  decel=False, visual=False, mot_start=mot_region_distance)

    successes_pp_no_decel_desired = (vel_pp_no_decel[successful_mols_pp_no_decel, 2] < \
        desired_vel_class_vz).sum()

    no_decel_results_dict = {
        'z_len': z_len,
        'successes_pp_no_decel': successes_pp_no_decel,
        'successes_pp_no_decel_desired': successes_pp_no_decel_desired,
        'mean_velocity': np.mean(vel_pp_no_decel[successful_mols_pp_no_decel, 2])
    }
    initial_nodecel_list.append(no_decel_results_dict)

    succ_pp = initial_nodecel_list[i]['successes_pp_no_decel']
    succ_pp_desired = initial_nodecel_list[i]['successes_pp_no_decel_desired']
    mean_vel = initial_nodecel_list[i]['mean_velocity']
    print(f'Successes, no decel, z_len = {z_lens_list[i] / 1e3}: {succ_pp}')
    print(f'Successful particles, no decel, desired velocity class, z_len = ' + \
          f'{z_lens_list[i] / 1e3}: {succ_pp_desired}')
    print(f'Mean successful particle velocity: {mean_vel}')

    print(f'Elapsed time so far: {datetime.datetime.now() - start_time_scan_len_dets}')

# change if 1m is no longer at index 3 in z_lens_list
successes_pp_no_decel_1m = initial_nodecel_list[3]['successes_pp_no_decel']
successes_pp_no_decel_desired_1m = initial_nodecel_list[3]['successes_pp_no_decel_desired']
mean_velocity_1m = initial_nodecel_list[3]['mean_velocity']

for i, del_s2w in enumerate(del_0_s2w_list):

    for j, z_len in enumerate(z_lens_list):

        mot_region_distance = l_cell_to_4k + l_4k_to_lens_aperture + z_len / 1e3
        successes_pp_no_decel = initial_nodecel_list[j]['successes_pp_no_decel']
        successes_pp_no_decel_desired = initial_nodecel_list[j]['successes_pp_no_decel_desired']

        _, vel_pp, _, successes_pp, successful_mols_pp = \
            propagate(n, p, v, a, 0, np.zeros(n, dtype=bool), \
            l_4k_to_lens_aperture, m_s, decel=True, del_0_s2w=del_s2w, zsd_length=z_len, \
            visual=False, mot_start=mot_region_distance)

        desired_molecules = (vel_pp[successful_mols_pp, 2] < desired_vel_class_vz).sum()
        enhancement_number_successes = successes_pp / np.float64(successes_pp_no_decel)
        enhancement_desired_molecules = desired_molecules / np.float64(successes_pp_no_decel_desired)
        enhancement_number_successes_1m = successes_pp / np.float64(successes_pp_no_decel_1m)
        enhancement_desired_molecules_1m = desired_molecules / np.float64(successes_pp_no_decel_desired_1m)
        mean_velocity = np.mean(vel_pp[successful_mols_pp, 2])
        mean_velocity_reduction = mean_velocity / mean_velocity_1m

        print(f'Successes, del2w = {del_s2w / 1e9} and z_len = {z_len / 1e3}: {successes_pp}')
        print(f'Successful particles, del2w = {del_s2w / 1e9} and z_len = {z_len / 1e3}: ' + \
              f'{np.where(successful_mols_pp == True)}')
        print(f'Number of molecules in MOT region: {successes_pp}')
        print(f'Number of molecules in desired velocity class: {desired_molecules}')
        print(f'Enhancement, successes: {enhancement_number_successes}')
        print(f'Enhancement, desired velocity class: {enhancement_desired_molecules}')
        print(f'Enhancement from 1m, successes: {enhancement_number_successes_1m}')
        print(f'Enhancement from 1m, desired velocity class: {enhancement_desired_molecules_1m}')
        print(f'Mean velocity: {mean_velocity}')
        print(f'Mean velocity reduction from 1m no decel: {mean_velocity_reduction}')

        # save results to new dict, add to dict list
        results_dict = {
            'del_s2w': del_s2w / 1e9,
            'z_len': z_len,
            'absolute_number': successes_pp,
            'desired_vel_class': desired_molecules,
            'enhancement_successes': enhancement_number_successes,
            'enhancement_desired_molecules': enhancement_desired_molecules,
            'enhancement_number_successes_1m': enhancement_number_successes_1m,
            'enhancement_desired_molecules_1m': enhancement_desired_molecules_1m,
            'mean_velocity': mean_velocity,
            'mean_velocity_reduction': mean_velocity_reduction
        }
        results_dict_list.append(results_dict)

        print(f'Elapsed time so far: {datetime.datetime.now() - start_time_scan_len_dets}')

# dataframe
results_df = pd.DataFrame(results_dict_list)
Path('{}/param_scans_{}'.format(date, date)).mkdir(parents=True, exist_ok=True)
results_df.to_csv('{}/param_scans_{}/param_scans_{}.csv'.format(date, date, date))

# pivot
pivoted_df_absolute_number = results_df.pivot(index='del_s2w', \
    columns='z_len', values='absolute_number')
pivoted_df_desired_vel_class = results_df.pivot(index='del_s2w', \
    columns='z_len', values='desired_vel_class')
pivoted_df_enhancement = results_df.pivot(index='del_s2w', columns='z_len', \
    values='enhancement_successes')
pivoted_df_enhancement_desired_molecules = results_df.pivot(index='del_s2w', \
    columns='z_len', values='enhancement_desired_molecules')
pivoted_df_enhancement_number_successes_1m = results_df.pivot(index='del_s2w', columns='z_len', \
    values='enhancement_number_successes_1m')
pivoted_df_enhancement_desired_molecules_1m = results_df.pivot(index='del_s2w', columns='z_len', \
    values='enhancement_desired_molecules_1m')
pivoted_df_mean_velocity = results_df.pivot(index='del_s2w', columns='z_len', \
    values='mean_velocity')
pivoted_df_mean_velocity_reduction = results_df.pivot(index='del_s2w', columns='z_len', \
    values='mean_velocity_reduction')

# plot
plot_param_scan_heatmap(scan_fig_absolute_number, scan_ax_absolute_number, \
    pivoted_df_absolute_number, path='absolute_number')
plot_param_scan_heatmap(scan_fig_desired_vel_class, scan_ax_desired_vel_class, \
    pivoted_df_desired_vel_class, path='desired_vel_class')
plot_param_scan_heatmap(scan_fig_enhancement, scan_ax_enhancement, \
    pivoted_df_enhancement, path='enhancement_successes')
plot_param_scan_heatmap(scan_fig_enhancement_desired_molecules, scan_ax_enhancement_desired_molecules, \
    pivoted_df_enhancement_desired_molecules, path='enhancement_desired_molecules')
plot_param_scan_heatmap(scan_fig_enhancement_number_successes_1m, \
    scan_ax_enhancement_number_successes_1m, \
    pivoted_df_enhancement_number_successes_1m, path='enhancement_number_successes_1m')
plot_param_scan_heatmap(scan_fig_enhancement_desired_molecules_1m, \
    scan_ax_enhancement_desired_molecules_1m, \
    pivoted_df_enhancement_desired_molecules_1m, path='enhancement_desired_molecules_1m')
plot_param_scan_heatmap(scan_fig_mean_velocity, scan_ax_mean_velocity, \
    pivoted_df_mean_velocity, path='mean_velocity')
plot_param_scan_heatmap(scan_fig_mean_velocity_reduction, scan_ax_mean_velocity_reduction, \
    pivoted_df_mean_velocity_reduction, path='mean_velocity_reduction')

print('Total elapsed time: {}'.format(datetime.datetime.now() - start_time_scan_len_dets))