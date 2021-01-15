# ----------------------------------------------------------------------------
# Parameter Scan
# ----------------------------------------------------------------------------
from dependencies import *
from init import *
from vector_field import *
from propagation import *

# open/write csv file
with open('{}/lens_variation_{}_{}.csv'.format(datetime.date.today(), datetime.date.today(), int(n)), 'w+') as file:
    writer = csv.writer(file)
    writer.writerow(['l_cell_to_lens_aperture'] + list(range(trials)))

# set parameters
add_len = lens_range / scan_points

# evolve system through time
for scan_pt in range(scan_points):

    successes_per_run = []
    print('Decelerator distance: {}'.format(l_cell_to_4k + l_4k_to_lens_aperture))

    for trl in range(trials):
        print('Scan {}, trial {}'.format(scan_pt, trl))

        # initialize variables
        n = int(n)
        successes = 0
        successful_particles = np.zeros(n, dtype=bool)
        p_pre = np.zeros((n, 3))
        v_pre = np.zeros((n, 3))
        a_pre = np.zeros((n, 3))
        m_s_pre = np.zeros((n, 3))
        p, v, a, m_s = generate(n, p_pre, v_pre, a_pre, m_s_pre)

        # generate and propagate particles
        pos_pp, vel_pp, acc_pp, successes_pp, successful_particles_pp = \
            propagate(n, p, v, a, successes, successful_particles, \
                      l_4k_to_lens_aperture, m_s, decel=True)

        # log successes
        successes_per_run.append(successes_pp)
        print('Successes so far: {}\n'.format(successes_per_run))

    # write successes to csv file
    with open('{}/lens_variation_{}.csv'.format(datetime.date.today(), datetime.date.today()), 'a') as file:
        writer = csv.writer(file)
        writer.writerow([l_cell_to_4k + l_4k_to_lens_aperture] + successes_per_run)
    file.close()

    # iterate on distance to lens if it's not the last run
    if scan_pt + 1 != scan_points:
        l_4k_to_lens_aperture += add_len
