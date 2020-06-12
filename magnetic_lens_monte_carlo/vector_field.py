# ----------------------------------------------------------------------------
# Force Vector Field
# ----------------------------------------------------------------------------

# Import matrices
hdulBxMatrix = fits.open('/Users/andrewwinnicki/Desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/bmatrix/bxMatrix.fits')
hdulByMatrix = fits.open('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/bmatrix/byMatrix.fits')
hdulBzMatrix = fits.open('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/bmatrix/bzMatrix.fits')

bxMatrix = np.array([hdulBxMatrix[0].data[i] for i in range(m)])
byMatrix = np.array([hdulByMatrix[0].data[i] for i in range(m)])
bzMatrix = np.array([hdulBzMatrix[0].data[i] for i in range(m)])

# Plot b-field in three dimensions
bMatrixFig3D = plt.figure()
bMatrixAx3D = bMatrixFig3D.gca(projection='3d')

x, y, z = np.meshgrid(np.linspace(-R/2, R/2, m),
                      np.linspace(-R/2, R/2, m),
                      np.linspace(-R/2, R/2, m))

bMatrixAx3D.quiver(x, y, z, bxMatrix, byMatrix, bzMatrix, length=3, \
    normalize=True)

bMatrixAx3D.set_title('Magnetic Field in Circular Halbach Array')
bMatrixAx3D.set_xlabel('x (mm)')
bMatrixAx3D.set_ylabel('y (mm)')
bMatrixAx3D.set_zlabel('z (mm)')

Path('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/bfield_plots_{}'\
    .format(datetime.date.today())).mkdir(parents=True, exist_ok=True)
plt.savefig('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/bfield_plots_{}/bfield_3D_{}'\
    .format(datetime.date.today(), datetime.date.today()))

# Plot slice of b-field in two dimensions
bMatrixFigSlice = plt.figure()
bMatrixAxSlice = plt.subplot()

x2d, y2d = np.meshgrid(np.linspace(-R/2, R/2, m), np.linspace(-R/2, R/2, m))

bxMatrixSlice = bxMatrix[:, :, int(m/2)]
byMatrixSlice = byMatrix[:, :, int(m/2)]

bMatrixAxSlice.quiver(x2d, y2d, bxMatrixSlice, byMatrixSlice)

bMatrixAxSlice.set_title(\
    '2D Slice of Magnetic Field in Circular Halbach Array')
bMatrixAxSlice.set_ylabel('y (mm)')
bMatrixAxSlice.set_xlabel('x (mm)')
plt.savefig('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/bfield_plots_{}/bfield_2D_slice_{}'\
    .format(datetime.date.today(), datetime.date.today()))

# Generate force field
gradBxMatrix = np.gradient(bxMatrix, axis=0)
gradByMatrix = np.gradient(byMatrix, axis=1)
gradBzMatrix = np.gradient(bzMatrix, axis=2)

gradBMatrix = np.stack([gradBxMatrix, gradByMatrix, gradBzMatrix], axis=3)

# # Add F = 0 for anywhere we're not counting the magnetic lens' effect

# # Spacing between cell aperture and circular Halbach array is 8x greater than
# # spacing within array; 18x greater between array and MOT
# # Todo: fix the '* 1' to be '* 4'
# for _ in range((m - 1) * 1):
#     # Since the distance from 4K aperture to lens is 8x the length of the lens
#     # bore, we must have an additional (m - 1)*8 points in the force field
#     # with value 0
#     forceField = np.insert(forceField, 0, [[0.0 for _ in range(m)]\
#         for _ in range(m)], axis=0)

# # Add in 18x 0's in the force field between the lens and the MOT
# Todo: add the 0's in the force field after the lens

# print("New force field: \n {} \n ".format(forceField))
