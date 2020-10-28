# ----------------------------------------------------------------------------
# Magnitude of Force at
# ----------------------------------------------------------------------------
from vector_field import *

# initialize force magnitude arrays
force_x = []
force_y = []

# initialize mesh values
mesh = range(0, mxy)

# loop through mesh grid of force field
z_pos = 10

for i in mesh:
    print('coords: {}'.format((i, 0, z_pos)))
    print(force_field[i, 0, z_pos]/mass)
    force_x.append(force_field[i, 0, z_pos])

# transform to numpy arrays
force_x = np.array(force_x)

# get components of vectors
force_x_plt = [force_x[i, 0] for i in range(len(mesh))]
force_y_plt = [force_x[i, 1] for i in range(len(mesh))]

# plot results
fig, ax = plt.subplots(2, 1, figsize=(20, 10))
ax = ax.ravel()

ax[0].plot(mesh, force_x_plt, label='x-component scan', linewidth=3, color='b')
ax[1].plot(mesh, force_y_plt, label='y-component scan', linewidth=3, color='r')

# formatting
ax[0].legend()
ax[1].legend()

# title
fig.suptitle('Force Field Scan Along y-Axis, z_pos={}'.format(z_pos), fontsize=15)

# save to file
Path('{}/force_mag_plots_{}'.format(datetime.date.today(), datetime.date.today())).mkdir(parents=True, exist_ok=True)
plt.savefig('{}/force_mag_plots_{}/force_mag_{}'.format(datetime.date.today(), datetime.date.today(), datetime.date.today()))
