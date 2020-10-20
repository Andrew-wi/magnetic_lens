# ----------------------------------------------------------------------------
# Dependencies
# ----------------------------------------------------------------------------
print('Importing dependencies...')

import csv
import datetime
import gc
import matplotlib.pyplot as plt
import matplotlib.path as pltPath
import math
import numpy as np
import h5py

# from astropy.io import fits
# from mpl_toolkits import mplot3d
from pathlib import Path

n = 1e2
t = 0.0
sigma_xy = 0.001 #0.0042
sigma_vxy = 20.0 #12.0
sigma_vz = 0.0 #30.0
mu_vz = 100.0 #110.0
l_cell_to_4k = 0.1
l_4k_to_lens_aperture = 0.1 # origin is at l_cell_to_4k. Can be negative to scan behind the 4k
l_4k_to_beam_shutter = 0.26
m_s = 0.5
g = 2.0
mu_B = 9.274e-24
mass = 9.48671e-26 # caoh mass # 1.18084e-25 # caoch3 mass
t_final = 0.02
steps = 200
mot_left_edge = 1.50
mot_side_length = 0.01

# parameter scan variables
lens_range = 0.5 # range of values over which we scan the lens. Origin is at l_4k_to_lens_aperture
scan_points = 9 # number of points to scan
trials = 21 # number of trials at each scan_point

# same as in mathematica code
mxy = 50 # mesh spacing in xy directions
mz = 250 # mesh spacing in z direction
r_inner = 3 # inner radius of lens (in mm, as Radia is in mm by default, same as in Mathematica)
r_outer = 20 # outer radius of lens (mm, as in Radia, same as in Mathematica)
dz = 8 # thickness of magnet segments along z-axis
z_length = 140 # the length along z axis for which b-field is computed
segs = 12 # number of segments
