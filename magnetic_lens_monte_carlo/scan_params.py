# ----------------------------------------------------------------------------
# Parameter Scan
# ----------------------------------------------------------------------------
from dependencies import *
from init import *
from vector_field import *

with open('./lens_variation_{}.csv'.format(datetime.date.today()), 'w+') as file:
    writer = csv.writer(file)
    writer.writerow(['l_4k_to_lens_aperture', 'successes'])

# Evolve system through time
for i, add_len in enumerate(np.linspace(scan_l_4k_to_lens_aperture_start, scan_l_4k_to_lens_aperture, scan_points, endpoint=False)):
    # set global variables for scan through parameters and initialize
    global l_4k_to_lens_aperture
    global successes
    global successfulParticles
    successes = 0
    successfulParticles = []
    generate()
    propagate()
    # write successes to csv file
    with open('./lens_variation_{}.csv'.format(datetime.date.today()), 'a') as file:
        writer = csv.writer(file)
        writer.writerow([l_cell_to_4k + l_4k_to_lens_aperture, successes])
    # iterate on distance to lens
    l_4k_to_lens_aperture += add_len
    print('l_4k_to_lens_aperture: {}'.format(l_4k_to_lens_aperture))
    print('successes: {}\n'.format(successes))
