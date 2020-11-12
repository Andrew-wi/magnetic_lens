# ----------------------------------------------------------------------------
# Visualize
# ----------------------------------------------------------------------------
from dependencies import *
from init import *
from vector_field import *

print('Visualizing fields...')

# Path('{}/b_field_plots_{}'.format(datetime.date.today(), datetime.date.today())).mkdir(parents=True, exist_ok=True)
# # plt.savefig('{}/b_field_plots_{}/b_field_3D_{}'.format(datetime.date.today(), datetime.date.today(), datetime.date.today()))

# Plot slice of b-field in two dimensions
# bMatrixFigSlice, bMatrixAxSlice = plt.subplots()
# hexagon = [[r_inner * np.cos(angle), r_inner * np.sin(angle)] for angle in np.linspace(0, 2 * np.pi, segs, endpoint=False)]
# hexagon.append(hexagon[0])
# x, y = list(zip(*hexagon))
# bMatrixAxSlice.plot(x, y, 'k')
# bMatrixAxSlice.axis('equal')

# x2d, y2d = np.meshgrid(np.linspace(-r_inner, r_inner, mxy), np.linspace(-r_inner, r_inner, mxy))

# bxMatrixSlice = bMatrix[:, :, int(mz/2), 0]
# byMatrixSlice = bMatrix[:, :, int(mz/2), 1]

# # # normalize
# # bxMatrixSlice = bxMatrixSlice/np.sqrt(bxMatrixSlice ** 2)
# # byMatrixSlice = byMatrixSlice/np.sqrt(byMatrixSlice ** 2)

# bMatrixAxSlice.quiver(x2d, y2d, bxMatrixSlice, byMatrixSlice)

# bMatrixAxSlice.set_title('2D Slice of Magnetic Field in Circular Halbach Array')
# bMatrixAxSlice.set_ylabel('y (mm)')
# bMatrixAxSlice.set_xlabel('x (mm)')
# plt.savefig('{}/b_field_plots_{}/b_field_2D_slice_{}'.format(datetime.date.today(), datetime.date.today(), datetime.date.today()))

# Plot force field
force_fieldSlice2DFig, force_fieldSlice2DAx = plt.subplots()
# force_fieldSlice2DAx.plot(x, y, 'k')

# forceX = force_field[:, :, 100, 0]
# forceY = force_field[:, :, 100, 1]
forceX = force_field[20:30, 20:30, 20, 0]
forceY = force_field[20:30, 20:30, 20, 1]
# forceX = force_field[10:40, 10:40, 20, 0]
# forceY = force_field[10:40, 10:40, 20, 1]
# forceX = force_field[15:35, 15:35, 20, 0]
# forceY = force_field[15:35, 15:35, 20, 1]

selected_points = forceX.shape[0]

x2d, y2d = np.meshgrid(np.linspace(-r_inner, r_inner, selected_points), np.linspace(-r_inner, r_inner, selected_points))


force_fieldSlice2DAx.quiver(x2d, y2d, forceX, forceY)

force_fieldSlice2DAx.axis('equal')

force_fieldSlice2DAx.set_title(\
    '2D Slice of Force Field in Circular Halbach Array Magnetic Field')
force_fieldSlice2DAx.set_ylabel('y (mm)')
force_fieldSlice2DAx.set_xlabel('x (mm)')

Path('{}/force_field_plots_{}'.format(datetime.date.today(), datetime.date.today())).mkdir(parents=True, exist_ok=True)
plt.savefig('{}/force_field_plots_{}/force_field_2D_slice_{}'.format(datetime.date.today(), datetime.date.today(), datetime.date.today()))

# # Plot magnetization of circular Halbach array
# mMatrixFigSlice, mMatrixAxSlice = plt.subplots()

# hexagonInner = [[R / 2 * np.cos(angle), R / 2 * np.sin(angle)] for angle in np.linspace(0, 2 * np.pi, segs, endpoint=False)]
# hexagonInner.append(hexagonInner[0])
# x1, y1 = list(zip(*hexagonInner))

# hexagonOuter = [[R * np.cos(angle), R * np.sin(angle)] for angle in np.linspace(0, 2 * np.pi, segs, endpoint=False)]
# hexagonOuter.append(hexagonOuter[0])
# x2, y2 = list(zip(*hexagonOuter))

# mMatrixAxSlice.plot(x1, y1, 'k')
# mMatrixAxSlice.plot(x2, y2, 'k')
# mMatrixAxSlice.axis('equal')

# x2d, y2d = np.meshgrid(np.linspace(-R, R, m), np.linspace(-R, R, m))

# mMatrixAxSlice.quiver(x2d, y2d, mxMatrixSlice, myMatrixSlice)

# mMatrixAxSlice.set_title(\
#     '2D Slice of Magnetization in Circular Halbach Array')
# mMatrixAxSlice.set_ylabel('y (mm)')
# mMatrixAxSlice.set_xlabel('x (mm)')

# Path('{}/magnetization_plots_2D_{}'.format(datetime.date.today(), datetime.date.today())).mkdir(parents=True, exist_ok=True)
# plt.savefig('{}/magnetization_plots_2D_{}/magnetization_2D_{}'format(datetime.date.today(), datetime.date.today(), datetime.date.today()))

# # Plot b-field in three dimensions
# bMatrixFig3D = plt.figure()
# bMatrixAx3D = bMatrixFig3D.gca(projection='3d')

# x, y, z = np.meshgrid(np.linspace(-R/2, R/2, m),
#                       np.linspace(-R/2, R/2, m),
#                       np.linspace(-R/2, R/2, m))

# bMatrixAx3D.quiver(x, y, z, bxMatrix, byMatrix, bzMatrix, length=3, \
#     normalize=True)

# bMatrixAx3D.set_title('Magnetic Field in Circular Halbach Array')
# bMatrixAx3D.set_xlabel('x (mm)')
# bMatrixAx3D.set_ylabel('y (mm)')
# bMatrixAx3D.set_zlabel('z (mm)')
