# ----------------------------------------------------------------------------
# Acceleration Profile, Fixed Radius Z-Axis Scan
# ----------------------------------------------------------------------------
from dependencies import *
from vector_field import *

import seaborn as sns

# set seaborn plotting style
sns.set_style("darkgrid")

# initialize values
z_scan = np.linspace(0, z_length / 1e3, mz)
thetas = np.linspace(0, 2 * np.pi, 100)
radius = r_inner / 2 /1e3
theta = np.pi / 2

# initialize arrays for storing acceleration
radial_acc = []

# loop through z_scan
for z_val in z_scan:

    x = radius * np.cos(theta)
    y = radius * np.sin(theta)

    # mesh spacing length
    l_xy = (r_inner*2/1e3)/(mxy-1)
    l_z = (z_length/1e3)/(mz-1)

    # interpolation
    xCoord = round((r_inner / 1e3 + x) / l_xy)
    yCoord = round((r_inner / 1e3 + y) / l_xy)
    zCoord = round(z_val / l_z)

    # take mean of array and append it to the radial acc array
    radial_acc.append(force_field[int(yCoord), int(xCoord), int(zCoord)][2] / mass)

# plot results
fig, ax = plt.subplots(figsize=(20, 10))

sns.lineplot(z_scan, radial_acc, label='Z-Axis Sweep', linewidth=3, color='b')

# formatting
plt.title('Z-Axis Scan of Lens Acceleration Profile at Radius {}'.format(radius), fontsize=25)
plt.ylabel(r'Mean Acceleration $\left( \frac{m}{s^2} \right)$', fontsize=20)
plt.xlabel(r'z-axis distance ($m$)', fontsize=20)
plt.tick_params(axis='both', labelsize=13)
plt.xlim(left=0, right=0.05)

# save to file
Path('{}/acc_mag_plots_{}'.format(datetime.date.today(), datetime.date.today())).mkdir(parents=True, exist_ok=True)
plt.savefig('{}/acc_mag_plots_{}/fix_radius_z_scan_{}'.format(datetime.date.today(), datetime.date.today(), datetime.date.today()))

