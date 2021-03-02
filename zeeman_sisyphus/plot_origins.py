# ----------------------------------------------------------------------------
# Propagation, Plot Origins
# ----------------------------------------------------------------------------
from dependencies import *
from helpers import *
from init import *
from vector_field import *
from propagation import *

# initialize variables
starting_time_plot_vel = datetime.datetime.now()
print(f'Starting time: {starting_time_plot_vel}')
print(f'Run: {mol_run}')
Path(f'{date}/origins_plot_{date}').mkdir(parents=True, exist_ok=True)
n = int(n)
p_pre = np.zeros((n, 3))
v_pre = np.zeros((n, 3))
a_pre = np.zeros((n, 3))
m_s_pre = np.zeros(n)
p, v, a, m_s = generate(n, p_pre, v_pre, a_pre, m_s_pre)
successes = 0
successful_particles = np.zeros(n, dtype=bool)
run_data = pd.DataFrame(columns=['mol_index', 'v_zi', 'v_zf'])

# plot distribution with decel
pos_pp, vel_pp, acc_pp, successes, successful_particles = \
    propagate(n, p, v, a, successes, successful_particles, \
    	l_4k_to_lens_aperture, m_s, decel=True, deepcopy=True, visual=False)
print(f'Success rate: {successes / n}')

for index in range(n):
    if index in np.where(successful_particles == True)[0]:
        run_data = run_data.append({'mol_index': index,
                         'v_zi': v[index][2],
                         'v_zf': vel_pp[index][2]}, ignore_index=True)
    else:
        continue

fig_origins = plt.figure(figsize=(10 * 1.62, 10))
ax_origins = plt.axes()
sns.histplot(data=run_data, x='v_zi', y='v_zf', cbar=True, ax=ax_origins)
fig_origins.savefig(f'{date}/origins_plot_{date}/{mol_run}_origins_plot_{date}_{n}')
run_data.to_csv(path_or_buf=f'{date}/origins_plot_{date}/{mol_run}_run_data_{date}_{n}.csv')

print(f'Total elapsed time: {datetime.datetime.now() - starting_time_plot_vel}')
