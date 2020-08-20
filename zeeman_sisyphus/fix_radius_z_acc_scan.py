# ----------------------------------------------------------------------------
# Acceleration Profile, Fixed Radius Z-Axis Scan
# ----------------------------------------------------------------------------
from dependencies import *
from vector_field import *

import seaborn as sns

# set seaborn plotting style
sns.set_style("darkgrid")

# initialize values
z_scan = np.linspace(0, R / 1e3, 200)
thetas = np.linspace(0, 2*np.pi, 100)
radius = R / 2 / 2 / 1e3

# initialize arrays for storing acceleration
radial_acc_ind = []
radial_acc_mean = []

# loop through z_scan
for z_val in z_scan:
    for theta in thetas:
        # get x and y values from radius and theta
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)

        # do interpolation
        l = (R / 1e3) / (m - 1)
        xCoord = round(((R / 2) / 1e3 + x) / l)
        yCoord = round(((R / 2) / 1e3 + y) / l)
        zCoord = round(z_val / l)
        print(zCoord)
        # take x, y, z coords and get acc; append to array
        radial_acc_ind.append(np.linalg.norm(force_field[int(yCoord), int(xCoord), int(zCoord)] / mass))
    # take mean of array and append it to the radial acc array
    radial_acc_mean.append(np.mean(radial_acc_ind))

# plot results
fig, ax = plt.subplots(figsize=(20, 10))

sns.lineplot(z_scan, radial_acc_mean, label='Z-Axis Sweep', linewidth=3, color='b')

# formatting
plt.title('Z-Axis Scan of Lens Acceleration Profile at Radius {}'.format(radius), fontsize=25)
plt.ylabel(r'Mean Acceleration $\left( \frac{m}{s^2} \right)$', fontsize=20)
plt.xlabel(r'z-axis distance ($m$)', fontsize=20)
plt.tick_params(axis='both', labelsize=13)

# save to file
Path('{}/acc_mag_plots_{}'.format(datetime.date.today(), datetime.date.today())).mkdir(parents=True, exist_ok=True)
plt.savefig('{}/acc_mag_plots_{}/fix_radius_z_scan_{}'.format(datetime.date.today(), datetime.date.today(), datetime.date.today()))

