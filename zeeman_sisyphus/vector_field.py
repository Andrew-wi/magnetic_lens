# ----------------------------------------------------------------------------
# Vector Fields
# ----------------------------------------------------------------------------
from dependencies import *

print('Generating vector fields...')

# Import matrices
hf_norm = h5py.File('b_matrix/normbMatrix_{}.h5'.format(mz), 'r')
normBMatrix = hf_norm[('Dataset1')]

# # bMatrix
# hdulBMatrix = fits.open('b_matrix/bMatrix_{}.fits'.format(m))
# bMatrix = np.array([hdulBMatrix[0].data[i] for i in range(m)])
# bMatrix = np.transpose(bMatrix, (1, 0, 2, 3))

# mesh spacing length
l_xy = (r_inner * 2 / 1e3) / (mxy - 1)
l_z = (z_length / 1e3) / (mz - 1)

# coordinates
# xy_coords = np.linspace(-r_inner/1e3, r_inner/1e3, mxy)
# z_coords = np.linspace(-10/1e3, z_length/1e3, mz)

# Generate force field
gradNormBx, gradNormBy, gradNormBz = np.gradient(normBMatrix, l_xy, l_xy, l_z)
gradNormBx = np.transpose(gradNormBx, (1, 0, 2))
gradNormBy = np.transpose(gradNormBy, (1, 0, 2))
# todo: figure out - sign here attenuating v_z
gradNormBz = np.transpose(gradNormBz, (1, 0, 2))

force_field = np.stack([gradNormBx, gradNormBy, gradNormBz], axis=-1) # * -g * mu_B
