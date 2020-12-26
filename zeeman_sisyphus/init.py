# ----------------------------------------------------------------------------
# # Initialize n molecules
# ----------------------------------------------------------------------------
from dependencies import *

# Create directory for files

Path('{}'.format(datetime.date.today())).mkdir(parents=True, exist_ok=True)

# set random seed; testing
random.seed(30)
np.random.seed(30)

# Generate particles
def generate(n, p, v, a, m_s):
    print('Generating particles...')

    # positions
    p[:, :2] = np.random.normal(loc=0.0, scale=sigma_xy, size=(n, 2)) # <-- CaOH
    # p[:, :2] = np.random.uniform(-unif_xy, unif_xy, size=(n, 2)) # <-- CaF
    p[:, 2] = np.zeros(n)

    # velocities
    v[:, :2] = np.random.normal(loc=0.0, scale=sigma_vxy, size=(n, 2)) # <-- CaOH
    # v[:, :2] = np.random.uniform(-unif_vxy, unif_vxy, size=(n, 2)) # <-- CaF
    v[:, 2] = np.random.normal(loc=mu_vz, scale=sigma_vz, size=n)

    # acceleration and magnetic spin
    m_s = np.random.choice([-0.5, 0.5], size=n)

    for index in range(n):

        while p[index, 0] <= -0.005 or p[index, 0] >= 0.005 or \
            p[index, 1] <= -0.005 or p[index, 1] >= 0.005:
            p[index, :2] = np.random.normal(loc=0.0, scale=sigma_xy, size=2)

        while v[index, 2] < 0:
            v[index, 2] = np.random.normal(loc=mu_vz, scale=sigma_vz)

    return (p, v, a, m_s)
