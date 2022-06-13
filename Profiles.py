# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 10:08:12 2021

@author: alec
"""
#%%
import numpy as np
from matplotlib import pyplot as plt
from boutdata import collect

import matplotlib.cm as cm
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from boututils.datafile import DataFile






#%% Read data

path        = './shared/NORTH/data/'  
field_list  = ['T', 'n', 'phi', 'vort', 'ZMIN','ZMAX', 'dx', 'dy', 'dz']
par_list    = ['t_array']
fast_list   = ['t_array', 'n0', 'phi0', 'n1', 'phi1', 'n2', 'phi2', 'T0', 'T1', 'T2']

data, par, fast = {}, {}, {}


#dmp_files = DataFile("./shared/NORTH/data /BOUT.dmp.0.nc").list()
#fast_files = DataFile("./shared/NORTH/data/BOUT.fast.0.nc").list()

for _field in field_list:
    data[_field] = collect(_field, path = path, xguards = False)

for _par in par_list:
    par[_par] = collect(_par, path = path, xguards = False)

for _fast in fast_list:
    fast[_fast] = collect(_fast, path = path, prefix = 'BOUT.fast', xguards = False)

domain = data['n'].shape

#%% Plot data

probe_pos = [0.80, 0.82, 0.84]

fig, ax = plt.subplots(3)

i = 12

plot0 = ax[0].contourf(np.transpose(data['n'][i, :, 0, :]), 100, cmap = 'hot')
for probe in probe_pos:
    ax[0].plot([int(probe*domain[1])+2], [int(0.50*domain[3])], 'o')
ax[0].set_xlabel('x')
ax[0].set_ylabel('y')
plt.colorbar(plot0, ax=ax[0])

plot1 = ax[1].contourf(np.transpose(data['T'][i, :, 0, :]), 100, cmap = 'hot')
for probe in probe_pos:
    ax[1].plot([int(probe*domain[1])+2], [int(0.50*domain[3])], 'o')
ax[1].set_xlabel('x')
ax[1].set_ylabel('y')
plt.colorbar(plot1, ax=ax[1])

plot2 = ax[2].contourf(np.transpose(data['vort'][i, :, 0, :]), 100, cmap = 'jet')
for probe in probe_pos:
    ax[2].plot([int(probe*domain[1])+2], [int(0.50*domain[3])], 'o')
ax[2].set_xlabel('x')
ax[2].set_ylabel('y')
plt.colorbar(plot2, ax=ax[2])
fig.tight_layout()

plt.show()
#%% density profile

i = 17
density = np.transpose(data['n'][i, :, 0, :])

profile = np.zeros(256)
for x in range(256):
  profile[x] = np.sum(density[:,x])/256

plt.plot(profile)
plt.show


#%% Particle count


Particle_integral = np.zeros(18)
for x in range(18):
  Particle_integral[x] = np.sum(np.transpose(data['n'][x, :, 0, :]))*data['dz']*data['dz']

plt.plot(Particle_integral)

plt.show



