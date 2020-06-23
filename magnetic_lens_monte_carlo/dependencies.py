# ----------------------------------------------------------------------------
# Dependencies
# ----------------------------------------------------------------------------
print('\nImporting dependencies...')

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
dt = 0.1
sigmaXY = 0.005
sigmaVxy = 1.5
sigmaVz = 30.0
muVz = 100.0
lCellTo4k = 0.1
l4kToLensAperture = 0.1
l4kToBeamShutter = 0.26
s = -0.5
g = 2.0
mu_B = 9.274e-24
mass = 1.1789827e-22
p = np.array([])
v = np.array([])
a = np.array([])
tFinal = 0.02
steps = 1000
successfulParticles = []
successes = 0
motLeftEdge = 0.5500
motSideLength = 0.0025

# As in mathematica code
m = 16
R = 25.4
segs = 12

print('Done.\n')
