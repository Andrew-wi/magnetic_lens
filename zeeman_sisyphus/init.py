# ----------------------------------------------------------------------------
# # Initialize n molecules
# ----------------------------------------------------------------------------
from dependencies import *

# Create directory for files

Path('{}'.format(datetime.date.today())).mkdir(parents=True, exist_ok=True)

# Generate particles
def generate():
    print('Generating particles...')
    # positions
    p_xy = np.random.normal(loc=0.0, scale=sigma_xy, size=2*int(n))
    p_z = np.zeros(int(n))
    # velocities
    v_xy = np.random.normal(loc=0.0, scale=sigma_vxy, size=2*int(n))
    v_z = np.random.normal(loc=mu_vz, scale=sigma_vz, size=int(n))
    # acceleration and magnetic spin
    a = np.zeros(3*int(n))
    m_s = np.random.choice([-0.5, 0.5], size=3*int(n))
    # interleave arrays
    p = np.empty((p_xy.size + p_z.size), dtype=p_xy.dtype)
    v = np.empty((v_xy.size + v_z.size), dtype=v_xy.dtype)
    p[0::3] = p_xy[0::2]
    p[1::3] = p_xy[1::2]
    p[2::3] = p_z
    v[0::3] = v_xy[0::2]
    v[1::3] = v_xy[1::2]
    v[2::3] = v_z
    for index in np.arange(0, int(n)*3, 3):
        while p[index] <= -0.005 or p[index] >= 0.005 or \
            p[index + 1] <= -0.005 or p[index + 1] >= 0.005:
            p[index:index + 2] = np.array([np.random.normal(loc=0.0, scale=sigma_xy), \
            np.random.normal(loc=0.0, scale=sigma_xy)])
        while v[index + 2] < 0:
            v[index + 2] = np.random.normal(loc=mu_vz, scale=sigma_vz)
    return (p, v, a, m_s)
