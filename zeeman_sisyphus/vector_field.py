# ----------------------------------------------------------------------------
# Vector Fields
# ----------------------------------------------------------------------------
from dependencies import *
# from init import *

print('Generating vector fields...')

# Import matrices
# hdulBxMatrix = fits.open('b_matrix/bxMatrix_{}.fits'.format(m))
# hdulByMatrix = fits.open('b_matrix/byMatrix_{}.fits'.format(m))
# hdulBzMatrix = fits.open('b_matrix/bzMatrix_{}.fits'.format(m))
# hdulNormBMatrix = fits.open('b_matrix/normbMatrix_{}.fits'.format(m))
# hdulMxMatrixSlice = fits.open('m_matrix/mxMatrix_{}.fits'.format(m))
# hdulMyMatrixSlice = fits.open('m_matrix/myMatrix_{}.fits'.format(m))

# bxMatrix = np.array([hdulBxMatrix[0].data[i] for i in range(m)])
# byMatrix = np.array([hdulByMatrix[0].data[i] for i in range(m)])
# bzMatrix = np.array([hdulBzMatrix[0].data[i] for i in range(m)])
# mxMatrixSlice = np.array([hdulMxMatrixSlice[0].data[i] for i in range(m)])
# myMatrixSlice = np.array([hdulMyMatrixSlice[0].data[i] for i in range(m)])
hf_norm = h5py.File('b_matrix/normbMatrix_{}.h5'.format(mz), 'r')
normBMatrix = hf_norm[('Dataset1')]

# # bMatrix
# hdulBMatrix = fits.open('b_matrix/bMatrix_{}.fits'.format(m))
# bMatrix = np.array([hdulBMatrix[0].data[i] for i in range(m)])
# bMatrix = np.transpose(bMatrix, (1, 0, 2, 3))

# mesh spacing length
l_xy = (r_inner*2/1e3)/(mxy-1)
l_z = (z_length/1e3)/(mz-1)

# Generate force field
gradNormBx, gradNormBy, gradNormBz = np.gradient(normBMatrix, l_xy, l_xy, l_z)
gradNormBx = np.transpose(gradNormBx, (1, 0, 2))
gradNormBy = np.transpose(gradNormBy, (1, 0, 2))
gradNormBz = np.transpose(gradNormBz, (1, 0, 2))

# force_field = -m_s * g * mu_B * 1/l * np.stack([gradNormBx, gradNormBy, gradNormBz], axis=3)
force_field = g * mu_B * np.stack([gradNormBx, gradNormBy, gradNormBz], axis=3)
# print(force_field)
