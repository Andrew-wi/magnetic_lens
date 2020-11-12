# ----------------------------------------------------------------------------
# X- and Y- Components of Magnetic Field
# ----------------------------------------------------------------------------
from dependencies import *
from vector_field import *

# fig, ax = plt.subplots((2, 2), figsize=(12, 12))
# axes = ax.ravel()

# z = 8 means ~9.6 mm; y = 25 is ~ in the middle; scan along x direction
points_to_plot = range(0, mxy)
x_comps_grad_k2 = [force_field[25, x, 25][0] for x in points_to_plot]
y_comps_grad_k2 = [force_field[25, x, 25][1] for x in points_to_plot]

# x_comps_grad_k6 = [force_field[25, x, 16][0] for x in points_to_plot]
# y_comps_grad_k6 = [force_field[25, x, 16][1] for x in points_to_plot]

print(x_comps_grad_k2)
print(y_comps_grad_k2)
