# ----------------------------------------------------------------------------
# Dependencies
# ----------------------------------------------------------------------------

print('Importing dependencies...')
import datetime
import matplotlib.pyplot as plt
import numpy as np

from astropy.io import fits
from mpl_toolkits import mplot3d
from pathlib import Path
from scipy.stats import maxwell
print('Done.')

# Number of particles
n = 3

# Mesh spacing, must be same as variable m in halbach.nb Mathematica code
m = 5

# Radius of circular Halbach array, same as in halbach.nb code; units of mm
R = 25.4

# Time and timestep
t = 0.0
dt = 0.1

# Distance from cell to 4K aperture; will be using mm
l = 100.0

# Physical constants
s = -0.5
g = 2.0
mu_B = 9.274e-24

# Mass of a single CaOCH3 molecule (in kg)
mass = 1.1789827e-22

# Vectorized velocity and acceleration
p = np.array([])
v = np.array([])
a = np.array([])

# Propagation
tFinal = 0.01
steps = 10
