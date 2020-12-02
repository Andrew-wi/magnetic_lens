# ----------------------------------------------------------------------------
# Dependencies
# ----------------------------------------------------------------------------
print('Importing dependencies...')

import csv
import datetime
import gc
import h5py
import matplotlib.pyplot as plt
import matplotlib.path as pltPath
import math
import numpy as np
import pprint
import random

# from astropy.io import fits
# from mpl_toolkits import mplot3d
from pathlib import Path

n = 1e4
t = 0.0
sigma_xy = 0.0042
sigma_vxy = 12.0
sigma_vz = 30.0
mu_vz = 110.0
l_cell_to_4k = 0.1
l_4k_to_lens_aperture = 0.05 # origin is at l_cell_to_4k. Can be negative to scan behind the 4k
# l_4k_to_beam_shutter = 0.26
g = 2.0
mu_B = 9.274e-24
mass = 9.48671e-26 # caoh mass # 1.18084e-25 # caoch3 mass
t_final = 0.02
steps = 2000 # for fast runs, set this to 200
mot_left_edge = 1.35
mot_side_length = 0.01
del_0_w_to_s = 13.75e9 # units: Hz
del_0_s_to_w = 2.5e9 # units: Hz
h = 6.62607004e-34 # units: m^2*kg/s
lambda_trans = 606e-9 # units: m
date = datetime.date.today()
mols_tracking = [485]

# parameter scan variables
lens_range = 0.5 # range of values over which we scan the lens. Origin is at l_4k_to_lens_aperture
scan_points = 9 # number of points to scan
trials = 21 # number of trials at each scan_point

# same as in mathematica code
mxy = 50 # mesh spacing in xy directions
mz = 1200 # mesh spacing in z direction
r_inner = 3 # inner radius of lens (in mm, as Radia is in mm by default, same as in Mathematica)
r_outer = 20 # outer radius of lens (mm, as in Radia, same as in Mathematica)
dz = 8 # thickness of magnet segments along z-axis
z_length = 1200 # the length along z axis for which b-field is computed
segs = 12 # number of segments
