# ----------------------------------------------------------------------------
# Vector Fields
# ----------------------------------------------------------------------------
from dependencies import *
from init import *

print('Generating vector fields...\n')

# Import matrices
hdulBxMatrix = fits.open('/Users/andrewwinnicki/Desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/b_matrix/bxMatrix_{}.fits'.format(m))
hdulByMatrix = fits.open('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/b_matrix/byMatrix_{}.fits'.format(m))
hdulBzMatrix = fits.open('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/b_matrix/bzMatrix_{}.fits'.format(m))
hdulNormBMatrix = fits.open('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/b_matrix/normbMatrix_{}.fits'.format(m))
hdulMxMatrixSlice = fits.open('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/m_matrix/mxMatrix_{}.fits'.format(m))
hdulMyMatrixSlice = fits.open('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/m_matrix/myMatrix_{}.fits'.format(m))

bxMatrix = np.array([hdulBxMatrix[0].data[i] for i in range(m)])
byMatrix = np.array([hdulByMatrix[0].data[i] for i in range(m)])
bzMatrix = np.array([hdulBzMatrix[0].data[i] for i in range(m)])
mxMatrixSlice = np.array([hdulMxMatrixSlice[0].data[i] for i in range(m)])
myMatrixSlice = np.array([hdulMyMatrixSlice[0].data[i] for i in range(m)])
normBMatrix = np.array([hdulNormBMatrix[0].data[i] for i in range(m)])

# Generate force field
gradNormBMatrix = np.gradient(normBMatrix)

forceField = s * g * mu_B * np.stack([gradNormBMatrix[0], gradNormBMatrix[1], gradNormBMatrix[2]], axis=3)

print('Done.\n')
