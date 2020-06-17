# ----------------------------------------------------------------------------
# Force Vector Field
# ----------------------------------------------------------------------------
from dependencies import *
from init import *

print('Generating force field...\n')

# Import matrices
hdulBxMatrix = fits.open('/Users/andrewwinnicki/Desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/bmatrix/bxMatrix.fits')
hdulByMatrix = fits.open('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/bmatrix/byMatrix.fits')
hdulBzMatrix = fits.open('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/bmatrix/bzMatrix.fits')
hdulNormBMatrix = fits.open('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/bmatrix/normbMatrix.fits')

bxMatrix = np.array([hdulBxMatrix[0].data[i] for i in range(m)])
byMatrix = np.array([hdulByMatrix[0].data[i] for i in range(m)])
bzMatrix = np.array([hdulBzMatrix[0].data[i] for i in range(m)])
normBMatrix = np.array([hdulNormBMatrix[0].data[i] for i in range(m)])

# Generate force field
gradNormBMatrix = np.gradient(normBMatrix)

gradBMatrix = np.stack([gradNormBMatrix[0], gradNormBMatrix[1], gradNormBMatrix[2]], axis=3)

print('Done.\n')
