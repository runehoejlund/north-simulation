# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 10:08:12 2021

@author: alec
"""
#%%
import numpy as np
from matplotlib import pyplot as plt
from boutdata import collect



#%% Read data

path        = './shared/NORTH/data/'  
field_list  = ['n', 'phi']
par_list    = ['t_array']
fast_list   = ['t_array', 'n0', 'phi0', 'n1', 'phi1', 'n2', 'phi2']

data, par, fast = {}, {}, {}

for _field in field_list:
    data[_field] = collect(_field, path = path, xguards = False)

for _par in par_list:
    par[_par] = collect(_par, path = path, xguards = False)

for _fast in fast_list:
    fast[_fast] = collect(_fast, path = path, prefix = 'BOUT.fast', xguards = False)

domain = data['n'].shape

#%% Plot data

probe_pos = [0.80, 0.82, 0.84]

fig, ax = plt.subplots()

ax.contourf(np.transpose(data['n'][1, :, 0, :]), 100, cmap = 'inferno')
for probe in probe_pos:
    ax.plot([int(probe*domain[1])+2], [int(0.50*domain[3])], 'o')
ax.set_xlabel('x')
ax.set_ylabel('y')

fig.tight_layout()




fig, ax = plt.subplots(3)

ax[0].plot(fast['t_array'], fast['n0'][:], label = 'fast output')
ax[0].plot(par['t_array' ], data['n' ][:, int(probe_pos[0]*domain[1])+2, 0, int(0.50*domain[3])], 'o', color = 'k', label = 'dmp output')
ax[0].set_xlabel('t')
ax[0].set_ylabel('n')
ax[0].legend()
ax[0].title.set_text('Probe position = {:.2f}'.format(probe_pos[0]))

ax[1].plot(fast['t_array'], fast['n1'][:], label = 'fast output')
ax[1].plot(par['t_array' ], data['n' ][:, int(probe_pos[1]*domain[1])+2, 0, int(0.50*domain[3])], 'o', color = 'k', label = 'dmp output')
ax[1].set_xlabel('t')
ax[1].set_ylabel('n')
ax[1].legend()
ax[1].title.set_text('Probe position = {:.2f}'.format(probe_pos[1]))

ax[2].plot(fast['t_array'], fast['n2'][:], label = 'fast output')
ax[2].plot(par['t_array' ], data['n' ][:, int(probe_pos[2]*domain[1])+2, 0, int(0.50*domain[3])], 'o', color = 'k', label = 'dmp output')
ax[2].set_xlabel('t')
ax[2].set_ylabel('n')
ax[2].legend()
ax[2].title.set_text('Probe position = {:.2f}'.format(probe_pos[2]))


fig.tight_layout()

plt.show()