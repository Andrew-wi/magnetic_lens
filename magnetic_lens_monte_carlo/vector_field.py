# ----------------------------------------------------------------------------
# Force Vector Field
# ----------------------------------------------------------------------------
from dependencies import *
from init import *

# Import matrices
hdulBxMatrix = fits.open('/Users/andrewwinnicki/Desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/bmatrix/bxMatrix.fits')
hdulByMatrix = fits.open('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/bmatrix/byMatrix.fits')
hdulBzMatrix = fits.open('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/bmatrix/bzMatrix.fits')
hdulNormBMatrix = fits.open('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/bmatrix/normbMatrix.fits')

bxMatrix = np.array([hdulBxMatrix[0].data[i] for i in range(m)])
byMatrix = np.array([hdulByMatrix[0].data[i] for i in range(m)])
bzMatrix = np.array([hdulBzMatrix[0].data[i] for i in range(m)])
normBMatrix = np.array([hdulNormBMatrix[0].data[i] for i in range(m)])

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
gradNormBMatrix = np.gradient(normBMatrix)

gradBMatrix = np.stack([gradNormBMatrix[0], gradNormBMatrix[1], gradNormBMatrix[2]], axis=3)

# Plot force field
forceFieldSlice2DFig, forceFieldSlice2DAx = plt.subplots()
hexagon = [[R / 2 * np.cos(angle), R / 2 * np.sin(angle)] for angle in np.linspace(0, 2 * np.pi, segs, endpoint=False)]
hexagon.append(hexagon[0])
x, y = list(zip(*hexagon))
forceFieldSlice2DAx.plot(x, y, 'k')

x2d, y2d = np.meshgrid(np.linspace(-R/2, R/2, m), np.linspace(-R/2, R/2, m))

gradbxMatrixSlice = gradNormBMatrix[0][:, :, int(m/2)]
gradByMatrixSlice = gradNormBMatrix[1][:, :, int(m/2)]

forceFieldSlice2DAx.quiver(x2d, y2d, gradbxMatrixSlice, gradByMatrixSlice)

forceFieldSlice2DAx.axis('equal')

forceFieldSlice2DAx.set_title(\
    '2D Slice of Force Field in Circular Halbach Array Magnetic Field')
forceFieldSlice2DAx.set_ylabel('y (mm)')
forceFieldSlice2DAx.set_xlabel('x (mm)')

Path('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/force_field_plots_{}'\
    .format(datetime.date.today())).mkdir(parents=True, exist_ok=True)
plt.savefig('/Users/andrewwinnicki/desktop/Andrew/2019-2020/Doyle Lab/Modeling Magnetic Lens/magnetic_lens_monte_carlo/force_field_plots_{}/force_field_2D_slice_{}'\
    .format(datetime.date.today(), datetime.date.today()))
