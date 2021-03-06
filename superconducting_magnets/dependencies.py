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
import pandas as pd
import pprint
import random
import seaborn as sns

from pathlib import Path

t = 0.0
n = 1e6 # < -- CaOH/CaF number of molecules
mol_run = 'CaOH_origins'
desired_vel_class_vz = 30 # units: m/s
sigma_xy = 0.0042 # <-- CaOH
# sigma_vxy = 12.06 # <-- CaOH, He3 bg
sigma_vxy = 12.0 # <-- CaOH, regparams
# sigma_vz = 2.5 # <-- CaF/CaOH, velocity class selection
sigma_vz = 30.0 # <-- CaOH, regparams
# sigma_vz = 19.0 # <-- CaOH, He3 bg
# mu_vz = 110.0 # <-- CaOH, regparams
#mu_vz = 70.0 # <-- CaOH, He3 bg
mu_vz = 110.0 # <-- CaOH, velocity class selection
l_cell_to_4k = 0.075 # <-- CaOH
l_4k_to_lens_aperture = 0.075 # <-- CaOH
r_4k_aperture = 0.005
# l_4k_to_beam_shutter = 0.26
g = 2.0
mu_B = 9.274e-24
mass = 9.48671e-26 # <-- CaOH mass (kg) 
#mass = 1.18084e-25 # <-- caoch3 mass
t_final = 0.02
steps = 2000 # for fast runs, set this to 200
# mot_left_edge = 1.15 # <-- CaOH, optimal
# mot_left_edge = 1.65 # <-- CaOH, full length
mot_left_edge = 0.5 # <-- CaOH, superconducting magnets
mot_side_length = 0.01 # <-- CaOH
del_0_w_to_s = 13.75e9 # units: Hz
del_0_s_to_w = 2.5e9 #2.5e9 # units: Hz
h = 6.62607004e-34 # units: m^2*kg/s
lambda_trans = 606e-9 # units: m
date = datetime.date.today()
mols_tracking = [61, 485, 534, 887]
# gate_list = [0.15, 0.65, 1.15, 1.65] # <-- CaOH
gate_list = np.linspace(0.15, 0.50, 4) # <-- CaOH
colors = ['red', 'green', 'blue', 'purple', 'orange', 'maroon', 'skyblue', 'peru']
gate_size = 0.01 # units: m
l_xy = 0.0001818182 # mesh spacing length, as in file_read_testing.ipynb
l_z = 0.0007518999999999998 # mesh spacing length
b_field_maxes = [153, 200, 246]
branching_ratios = {'A000,X000': 0.9, 'A000,X100': 0.05, 'A000,dark': 0.05}
zeeman_effect = {'X000': np.linspace(0, 0.009, 400), 'X100': np.linspace(-0.3, -0.1, 400)}


# parameter scan variables
lens_range = 0.5 # range of values over which we scan the lens. Origin is at l_4k_to_lens_aperture
scan_points = 9 # number of points to scan
trials = 21 # number of trials at each scan_point

# same as in mathematica code
mxy = 200 # mesh grid density in xy directions
mz = 400 # mesh grid density in z direction
r_inner = 18 # inner radius of lens (in mm, as Radia is in mm by default, same as in Mathematica)
r_outer = 18 # outer radius of lens (mm, as in Radia, same as in Mathematica)
dz = 8 # thickness of magnet segments along z-axis
z_length = 300 # the length along z axis for which b-field is computed
segs = 12 # number of segments
