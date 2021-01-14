# ----------------------------------------------------------------------------
# Propagation, Plot Sanity Checks Figure 9
# ----------------------------------------------------------------------------
from dependencies import *
from helpers import *
from init import *
from vector_field import *
from propagation_sanity_checks import *

import sys

# init
start_time = datetime.datetime.now()
print(f'Start time: {start_time}')
fig9a_fig = plt.figure()
fig9a_ax = plt.axes()
fig9b_fig = plt.figure()
fig9b_ax = plt.axes()
# fig9c_fig = plt.figure()
# fig9c_ax = plt.axes()
# initialize variables
Path(f'./{date}/data_{date}').mkdir(parents=True, exist_ok=True)
n = int(n)
successes_pre = 0
successful_particles_pre = np.zeros(n, dtype=bool)
p_pre = np.zeros((n, 3))
v_pre = np.zeros((n, 3))
a_pre = np.zeros((n, 3))
m_s_pre = np.zeros(n)
p, v, a, m_s = generate(n, p_pre, v_pre, a_pre, m_s_pre)
del_0_s2w_list = [0.5e9, 1.5e9, 2.5e9, 3.5e9, 4.5e9, 5.5e9]

for del_s2w in del_0_s2w_list:

    pos_pp, vel_pp, acc_pp, successes_pp, successful_particles_pp = \
        propagate_sanity(n, p, v, a, successes_pre, successful_particles_pre, \
        l_4k_to_lens_aperture, m_s, decel=True, plot=False, pruning='to_magnet', \
        plot_vel=False, plot_vel_particles=mols_tracking, \
        spin_tracking=False, spin_tracked_particles=mols_tracking, \
        plot_long_dist=False, plot_long_dist_particles=mols_tracking, \
        scan_dets=True, del_0_s2w=del_s2w, visual=False)

    print('Successes: {}'.format(successes_pp))
    print('Successful particles: {}'.format(np.where(successful_particles_pp == True)))

    vel_x = vel_pp[successful_particles_pp, 0]
    vel_z = vel_pp[successful_particles_pp, 2]
    pos_x = pos_pp[successful_particles_pp, 0]

    # fig 9
    plot_vel_dist_scan_det(fig9a_fig, fig9a_ax, vel_z, del_s2w, successes=successes_pp)
    plot_phase_space_acc_reg(fig9b_fig, fig9b_ax, vel_x, pos_x, del_s2w)
    # plot_decel_trans_acc(fig9c_fig, fig9c_ax, vel_x, pos_x, del_s2w)

    with open(f'./{date}/data_{date}/run_data_{date}.csv', 'a+') as data_file:
        data_file.write(f'{str(datetime.datetime.now())},{mol_run},del_s2w_GHz={del_s2w / 1e9},')
        str_success = ','.join(map(str, np.where(successful_particles_pp == True)[0]))
        data_file.write(f'successes_pp={successes_pp},succ_mols_pp=,{str_success if len(str_success) > 0 else 0}\n')

    print(f'Elapsed time so far: {datetime.datetime.now() - start_time}')

plot_vel_dist_scan_det(fig9a_fig, fig9a_ax, vel_x, del_s2w, close='close')
plot_phase_space_acc_reg(fig9b_fig, fig9b_ax, vel_x, pos_x, del_s2w, close='close')
# plot_decel_trans_acc(fig9c_fig, fig9c_ax, vel_x, pos_x, del_s2w, close='close')

print(f'Total elapsed time: {datetime.datetime.now() - start_time}')
