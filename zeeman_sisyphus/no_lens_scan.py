# ----------------------------------------------------------------------------
# No Lens Paramter Scan
# ** Remember to comment out the lens in propagation.py **
# ----------------------------------------------------------------------------
from dependencies import *
from init import *
from vector_field import *
from propagation import *

# create/open csv file to write results to
with open('{}/no_lens_{}.csv'.format(datetime.date.today(), datetime.date.today()), 'w+') as file:
    writer = csv.writer(file)
    writer.writerow(['l_cell_to_lens_aperture'] + list(range(trials)))

# evolve system through time
successes_per_run = []
for trl in range(trials):
    print('Trial: {}'.format(trl))
    # initialize variables
    p = np.array([])
    v = np.array([])
    a = np.array([])
    successes = 0
    successful_particles = []

    # generate and propagate particles
    p, v, a = generate()
    p, v, a, successes, plotZ, plotX, _ = propagate(p, v, a, successes, successful_particles, l_4k_to_lens_aperture)

    # log successes
    successes_per_run.append(successes)
    print('Successes so far: {}\n'.format(successes_per_run))
# write successes to csv file
with open('{}/no_lens_{}.csv'.format(datetime.date.today(), datetime.date.today()), 'a') as file:
    writer = csv.writer(file)
    writer.writerow([l_cell_to_4k + l_4k_to_lens_aperture] + successes_per_run)
