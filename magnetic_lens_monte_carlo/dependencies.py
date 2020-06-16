# ----------------------------------------------------------------------------
# Dependencies
# ----------------------------------------------------------------------------
print('Importing dependencies...')
import datetime
import matplotlib.pyplot as plt
import math
import numpy as np

from astropy.io import fits
from mpl_toolkits import mplot3d
from pathlib import Path
from scipy.stats import maxwell
print('Done.')

# Number of particles
n = 5

# Mesh spacing, must be same as variable m in halbach.nb Mathematica code
m = 5

# Radius of circular Halbach array, as in halbach.nb code, units of mm
R = 25.4

# Time and timestep, units of s
t = 0.0
dt = 0.1

# Distance parameters, units of m
lCellTo4k = 0.1
l4kToAperture = 0.1

# Physical constants
s = -0.5
g = 2.0
mu_B = 9.274e-24

# Mass of a single CaOCH3 molecule, units of kg
mass = 1.1789827e-22

# Vectorized velocity and acceleration
p = np.array([])
v = np.array([])
a = np.array([])

# Propagation
tFinal = 0.01
steps = 1000
