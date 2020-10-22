# ----------------------------------------------------------------------------
# # Initialize n molecules
# ----------------------------------------------------------------------------
from dependencies import *

# Create directory for files

Path('{}'.format(datetime.date.today())).mkdir(parents=True, exist_ok=True)

# Generate particles
def generate():
    print('Generating particles...')
    p = np.array([])
    v = np.array([])
    a = np.array([])
    m_s = np.array([])
    for index in range(0, int(n) * 3, 3):
        p = np.append(p, [np.random.normal(loc=0.0, scale=sigma_xy), \
            np.random.normal(loc=0.0, scale=sigma_xy), 0.0])
        v = np.append(v, [np.random.normal(loc=0.0, scale=sigma_vxy), \
            np.random.normal(loc=0.0, scale=sigma_vxy), \
            np.random.normal(loc=mu_vz, scale=sigma_vz)])
        a = np.append(a, [0.0, 0.0, 0.0])
        m_s = np.append(m_s, random.choice([-0.5, 0.5]))

        while p[index] <= -0.005 or p[index] >= 0.005 or \
            p[index + 1] <= -0.005 or p[index + 1] >= 0.005:
            p[index:index + 2] = [np.random.normal(loc=0.0, scale=sigma_xy), \
            np.random.normal(loc=0.0, scale=sigma_xy)]

        while v[index + 2] < 0:
            v[index + 2] = np.random.normal(loc=mu_vz, scale=sigma_vz)
    return (p,v,a, m_s)
