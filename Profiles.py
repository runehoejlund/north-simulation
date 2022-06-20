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

path        = './shared/NORTH/data'  
field_list  = ['T', 'n', 'phi', 'vort', 'ZMIN','ZMAX', 'dx', 'dy', 'dz','source_n', 'Wall_shadow']
par_list    = ['t_array']
fast_list   = ['t_array', 'n0', 'phi0', 'n1', 'phi1', 'n2', 'phi2', 'T0', 'T1', 'T2']

data, par, fast = {}, {}, {}


#dmp_files = DataFile("./shared/NORTH/data copy/BOUT.dmp.1.nc").list()
#fast_files = DataFile("./shared/NORTH/data copy/BOUT.fast.1.nc").list()

for _field in field_list:
    data[_field] = collect(_field, path = path, xguards = False)

for _par in par_list:
    par[_par] = collect(_par, path = path, xguards = False)

#for _fast in fast_list:
#    fast[_fast] = collect(_fast, path = path, prefix = 'BOUT.fast', xguards = False)

domain = data['n'].shape

#%% Plot data
i = 300

probe_pos = [0.80, 0.82, 0.84]

fig, ax = plt.subplots(2,2)

fig.set_size_inches(15, 12)

plot0 = ax[0,0].contourf(np.transpose(data['n'][i, :, 0, :]), 100, cmap = 'inferno')
for probe in probe_pos:
    ax[0,0].plot([int(probe*domain[1])+2], [int(0.50*domain[3])], 'o')
ax[0,0].set_xlabel('x')
ax[0,0].set_ylabel('y')
plt.colorbar(plot0, ax=ax[0,0])

plot1 = ax[0,1].contourf(np.transpose(data['T'][i, :, 0, :]), 100, cmap = 'inferno')
for probe in probe_pos:
    ax[0,1].plot([int(probe*domain[1])+2], [int(0.50*domain[3])], 'o')
ax[0,1].set_xlabel('x')
ax[0,1].set_ylabel('y')
plt.colorbar(plot1, ax=ax[0,1])

plot2 = ax[1,0].contourf(np.transpose(data['vort'][i, :, 0, :]), 100, cmap = 'jet', vmin=-1, vmax=1)
for probe in probe_pos:
    ax[1,0].plot([int(probe*domain[1])+2], [int(0.50*domain[3])], 'o')
ax[1,0].set_xlabel('x')
ax[1,0].set_ylabel('y')
plt.colorbar(plot2, ax=ax[1,0])

plot3 = ax[1,1].contourf(np.transpose(data['phi'][i, :, 0, :]), 100, cmap = 'jet')
for probe in probe_pos:
    ax[1,1].plot([int(probe*domain[1])+2], [int(0.50*domain[3])], 'o')
ax[1,1].set_xlabel('x')
ax[1,1].set_ylabel('y')
plt.colorbar(plot3, ax=ax[1,1])
fig.tight_layout()


plt.show()
plt.savefig('plots/contours.png', dpi=100)


#%%

fig, ax = plt.subplots(2)

fig.set_size_inches(8, 8)

plot0 = ax[0].contourf(np.transpose(data['source_n'][ :, 0, :]), 100, cmap = 'hot')
for probe in probe_pos:
    ax[0].plot([int(probe*domain[1])+2], [int(0.50*domain[3])], 'o')
ax[0].set_xlabel('x')
ax[0].set_ylabel('y')
plt.colorbar(plot0, ax=ax[0])

plot1 = ax[1].contourf(np.transpose(data['Wall_shadow'][ :, 0, :]), 100, cmap = 'hot')
for probe in probe_pos:
    ax[1].plot([int(probe*domain[1])+2], [int(0.50*domain[3])], 'o')
ax[1].set_xlabel('x')
ax[1].set_ylabel('y')
plt.colorbar(plot1, ax=ax[1])


plt.show()
plt.savefig('plots/System.png', dpi=100)

#%% density profile

density = np.transpose(data['n'][i, :, 0, :])
density_0 = np.transpose(data['n'][0, :, 0, :])
source = np.transpose(data['source_n'][:, 0,:])

profile = np.zeros(256)
profile_0 = np.zeros(256)
for x in range(256):
  profile[x] = np.sum(density[:,x])/256
  profile_0[x] = np.sum(density_0[:,x])/256

fig, ax = plt.subplots(1)
plt.plot(profile)
plt.plot(profile_0)
#plt.plot(sum(source)/256/10)
plt.show()
plt.savefig('plots/profile.png')


#%% Particle count


Particle_integral = np.zeros(i)
for x in range(i):
  Particle_integral[x] = np.sum(np.transpose(data['n'][x, :, 0, :]))/(256*256)

fig, ax = plt.subplots(1)
plt.plot(Particle_integral)
plt.show()
plt.savefig('plots/Avg_n.png')



#%% Temperature


Temperature_integral = np.zeros(i)
for x in range(i):
  Temperature_integral[x] = np.sum(np.transpose(data['T'][x, :, 0, :]))/(256*256)

fig, ax = plt.subplots(1)
plt.plot(Temperature_integral)
plt.show()
plt.savefig('plots/tAvg_Temperature.png')


