# ----------------------------------------------------------------------------
# Metrics: Velocity Profile of MOT Successful Particles
# ----------------------------------------------------------------------------
# setting random seed–remove if want to have random runs!
import numpy as np
np.random.seed(13412)

from dependencies import *
from init import *
from vector_field import *
from propagation_velocities import *

# setup
successes = 0
successful_particles = []
today = datetime.date.today()

# get system arguments if doing job scan; comment out if not scanning
l_4k_to_lens_aperture = float(sys.argv[1])

# generate particles
p, v, a = generate()

# # obtain velocities
# v_init = []
# for index in range(0, int(n) * 3, 3):
#     v_init.append(np.linalg.norm(np.array(v[index:index+3])))

# # plot initial v distr
# fig1, ax1 = plt.subplots(figsize=(8*1.62, 8))
# ax1 = sns.distplot(v_init)
# ax1.set_title('Velocity Distribution of Particles At Start')
# ax1.set_ylabel('Frequency')
# ax1.set_xlabel('Magnitude of Velocity (m/s)')

# # save figure
# Path('{}/mot_region_distribution_{}'.format(today, today)).mkdir(parents=True, exist_ok=True)
# plt.savefig('{}/mot_region_distribution_{}/init_v_distr_{}'.format(today, today, today))

# propagate particles
p_final, v_final, a_final, successes, plotZ, plotX, successful_particles = propagate_velocities(p, v, a, successes, successful_particles, l_4k_to_lens_aperture)
print('successful particles: {}'.format(successful_particles))
print('v final: {}'.format(v_final))

# calculate the indices we wish for, extract those from v_final
success_nparr = np.array(successful_particles)
successful_v_indices = [list(range(i, i+3)) for i in success_nparr * 3]
unpacked = [index for index_range in successful_v_indices for index in index_range]

print('particle indices: {}'.format(unpacked))
mot_particle_velocities = v_final[unpacked]

print('particle velocity components: {}'.format(mot_particle_velocities))

# collect real velocities of particles
velocities = []
for index in range(0, len(successful_particles) * 3, 3):
    velocities.append(np.linalg.norm(np.array(mot_particle_velocities[index:index+3])))

print('magnitude of velocity: {}'.format(velocities))

# make histogram
fig2, ax2 = plt.subplots(figsize=(8*1.62, 8))
ax2 = sns.distplot(velocities)
ax2.set_title('Velocity Distribution of Particles in the MOT Region, Lens Position: {}'.format(l_cell_to_4k+l_4k_to_lens_aperture))
ax2.set_ylabel('Frequency')
ax2.set_xlabel('Magnitude of Velocity (m/s)')

Path('{}/mot_region_distribution_{}'.format(today, today)).mkdir(parents=True, exist_ok=True)
plt.savefig('{}/mot_region_distribution_{}/mot_distr_{}_{}'.format(today, today, today, str(l_cell_to_4k+l_4k_to_lens_aperture).replace('.', '')))
