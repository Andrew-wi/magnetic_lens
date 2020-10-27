# ----------------------------------------------------------------------------
# Acceleration Profile, Radial Scan
# ----------------------------------------------------------------------------
from dependencies import *
from vector_field import *

import seaborn as sns

# set seaborn plotting style
sns.set_style("darkgrid")

# initialize values
radii = np.linspace(0, r_inner/1e3, 100)
thetas = np.linspace(0, 2*np.pi, 100)

# initialize arrays for storing acceleration
radial_acc_ind = []
radial_acc_mean = []

# loop through radii
for radius in radii:
    for theta in thetas:
        # get x and y values from radius and theta
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        # mesh spacing length
        l_xy = (r_inner*2/1e3)/(mxy-1)
        # interpolation
        xCoord = round((r_inner/1e3 + x) / l_xy)
        yCoord = round((r_inner/1e3 + y) / l_xy)
        zCoord = round(60)
        # take x, y, z coords and get acc; append to array
        radial_acc_ind.append(np.linalg.norm(force_field[int(yCoord), int(xCoord), int(zCoord)] / mass))
    # take mean of array and append it to the radial acc array
    radial_acc_mean.append(np.mean(radial_acc_ind))

# plot results
fig, ax = plt.subplots(figsize=(20, 10))

sns.lineplot(radii, radial_acc_mean, label='Radial Sweep', linewidth=3, color='b')

# formatting
plt.title('Radial Scan of Lens Acceleration Profile', fontsize=25)
plt.ylabel(r'Acceleration $\left( \frac{m}{s^2} \right)$', fontsize=20)
plt.xlabel(r'Radial distance from z-axis ($m$)', fontsize=20)
plt.tick_params(axis='both', labelsize=13)

# save to file
Path('{}/acc_mag_plots_{}'.format(datetime.date.today(), datetime.date.today())).mkdir(parents=True, exist_ok=True)
plt.savefig('{}/acc_mag_plots_{}/acc_mag_{}'.format(datetime.date.today(), datetime.date.today(), datetime.date.today()))

