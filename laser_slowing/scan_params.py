# ----------------------------------------------------------------------------
# Parameter Scan
# ----------------------------------------------------------------------------
from dependencies import *
from init import *
from vector_field import *
from propagation import *

# open/write csv file
with open('{}/lens_variation_{}.csv'.format(datetime.date.today(), datetime.date.today()), 'w+') as file:
    writer = csv.writer(file)
    writer.writerow(['l_cell_to_lens_aperture'] + list(range(trials)))

# set parameters
add_len = lens_range / scan_points

# evolve system through time
for scan_pt in range(scan_points):
    successes_per_run = []
    print('lens distance: {}'.format(l_cell_to_4k + l_4k_to_lens_aperture))
    for trl in range(trials):
        print('Scan {}, trial {}'.format(scan_pt, trl))
        # initialize variables
        p = np.array([])
        v = np.array([])
        a = np.array([])
        successes = 0
        successful_particles = []

        # generate and propagate particles
        p, v, a = generate()
        p, v, a, successes, plotZ, plotX = propagate(p, v, a, successes, successful_particles)

        # log successes
        successes_per_run.append(successes)
        print('Successes so far: {}\n'.format(successes_per_run))
        # memory management
        del p
        del v
        del a
        del plotX
        del plotZ
        del successful_particles
        gc.collect(1)
    # write successes to csv file
    with open('{}/lens_variation_{}.csv'.format(datetime.date.today(), datetime.date.today()), 'a') as file:
        writer = csv.writer(file)
        writer.writerow([l_cell_to_4k + l_4k_to_lens_aperture] + successes_per_run)
    file.close()
    # iterate on distance to lens if it's not the last run
    if scan_pt + 1 != scan_points:
        l_4k_to_lens_aperture += add_len
