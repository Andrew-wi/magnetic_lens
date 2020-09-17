# ----------------------------------------------------------------------------
# Acceleration Profile, Z-Axis Scan, Mean Acceleration
# ----------------------------------------------------------------------------
from dependencies import *
from vector_field import *

import seaborn as sns

# set seaborn plotting style
sns.set_style("darkgrid")

# initialize values
z_scan = np.linspace(0, 2*R/1e3, 50)

# initialize arrays for storing acceleration
radial_acc_mean = []

# loop through z_scan
for z_val in z_scan:
    # create zCoord
    zCoord = round(z_val / l)

    # take slice of magnet
    mag_slice = np.linalg.norm(force_field[:, :, int(zCoord)] / mass, axis=2)

    # take mean of array and append it to the radial acc array
    radial_acc_mean.append(np.mean(mag_slice))

# plot results
fig, ax = plt.subplots(figsize=(20, 10))

sns.lineplot(z_scan, radial_acc_mean, label='Z-Axis Sweep', linewidth=3, color='b')

# formatting
plt.title('Z-Axis Scan of Lens Acceleration Profile', fontsize=25)
plt.ylabel(r'Mean Acceleration $\left( \frac{m}{s^2} \right)$', fontsize=20)
plt.xlabel(r'z-axis distance ($m$)', fontsize=20)
plt.tick_params(axis='both', labelsize=13)

# save to file
Path('{}/acc_mag_plots_{}'.format(datetime.date.today(), datetime.date.today())).mkdir(parents=True, exist_ok=True)
plt.savefig('{}/acc_mag_plots_{}/z_scan_{}'.format(datetime.date.today(), datetime.date.today(), datetime.date.today()))

