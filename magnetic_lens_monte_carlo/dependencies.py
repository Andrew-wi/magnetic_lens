# ----------------------------------------------------------------------------
# Dependencies
# ----------------------------------------------------------------------------
print('\nImporting dependencies...')

import csv
import datetime
import matplotlib.pyplot as plt
import matplotlib.path as pltPath
import math
import numpy as np

from astropy.io import fits
from mpl_toolkits import mplot3d
from pathlib import Path
from scipy.stats import maxwell

n = 1e3
t = 0.0
sigma_xy = 0.005
sigma_vxy = 1.0
sigma_vz = 10.0
mu_vz = 100.0
l_cell_to_4k = 0.1
l_4k_to_lens_aperture = 0.0
l_4k_to_beam_shutter = 0.26
s = -0.5
g = 2.0
mu_B = 9.274e-24
mass = 1.18084e-25
p = np.array([])
v = np.array([])
a = np.array([])
t_final = 0.02
steps = 3000
mot_left_edge = 0.5500
mot_side_length = 0.0025
scan_l_4k_to_lens_aperture = 0.1
scan_points = 3
scan_l_4k_to_lens_aperture_start = 0.0
successfulParticles = []
successes = 0

# As in mathematica code
m = 50
R = 25.4
segs = 12

print('Done.\n')
