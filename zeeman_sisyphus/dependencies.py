# ----------------------------------------------------------------------------
# Dependencies
# ----------------------------------------------------------------------------
print('Importing dependencies...')

import copy
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
import seaborn as sns

# from astropy.io import fits
# from mpl_toolkits import mplot3d
from pathlib import Path

n = 1e2
t = 0.0
mol_run = 'CaOH_energy_sanity' #'CaOH_no_sel' #'CaF_no_sel' #'CaOH_velclass_sel'
sigma_xy = 0 #0.0042 # <-- CaOH, He3
sigma_vxy = 0 #12.06 # <-- He3 bg #12.0 # <-- CaOH
unif_xy = 0.0025 # <-- CaF
unif_vxy = 7.5 # <-- CaF
sigma_vz = 0 #30.0 # <-- CaOH #2.5 # <-- CaF/CaOH, sanity #39.49 # <-- CaF, real #19.0 # <-- CaOH, He3 bg
mu_vz = 150 #70.0 # <-- CaOH, He3 bg #110.0 # <-- CaOH #150.0 # <-- CaF
l_cell_to_4k = 0.075 # <-- CaOH #0.1 #<-- CaF
l_4k_to_lens_aperture = 0.075 # <-- CaOH #0.0 # <-- CaF
# l_4k_to_beam_shutter = 0.26
g = 2.0
mu_B = 9.274e-24
mass = 9.48671e-26 # <-- CaOH mass (kg) #9.81069e-26 # <-- CaF mass #1.18084e-25 # <-- caoch3 mass
t_final = 0.02
steps = 2000 # for fast runs, set this to 200
mot_left_edge = 1.65 # <-- CaOH #1.3 # <-- CaF, Figure 9 #1.6 # <-- CaF, Figure 8
mot_side_length = 0.01 # <-- CaOH #0.005 # <-- CaF
del_0_w_to_s = 13.75e9 # units: Hz
del_0_s_to_w = 2.5e9 # units: Hz
h = 6.62607004e-34 # units: m^2*kg/s
lambda_trans = 606e-9 # units: m
date = datetime.date.today()
mols_tracking = [1387, 81490]
gate_list = [0, 0.5, 1.0, 1.5]
gate_size = 0.01 # units: m

# parameter scan variables
lens_range = 0.5 # range of values over which we scan the lens. Origin is at l_4k_to_lens_aperture
scan_points = 9 # number of points to scan
trials = 21 # number of trials at each scan_point

# same as in mathematica code
mxy = 50 # mesh spacing in xy directions
mz = 1500 # mesh spacing in z direction
r_inner = 2.5 # inner radius of lens (in mm, as Radia is in mm by default, same as in Mathematica)
r_outer = 20 # outer radius of lens (mm, as in Radia, same as in Mathematica)
dz = 8 # thickness of magnet segments along z-axis
z_length = 1500 # the length along z axis for which b-field is computed
segs = 12 # number of segments
