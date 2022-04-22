# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 10:08:12 2021

@author: alec
"""
#%%
import numpy as np
from matplotlib import pyplot as plt
from boutdata import collect

print(1)
#%% Read data

path        = './shared/NORTH/data/'  
field_list  = ['n', 'phi']
par_list    = ['t_array']
fast_list   = ['t_array', 'n0', 'phi0']

data, par, fast = {}, {}, {}

for _field in field_list:
    data[_field] = collect(_field, path = path, xguards = False)

for _par in par_list:
    par[_par] = collect(_par, path = path, xguards = False)

for _fast in fast_list:
    fast[_fast] = collect(_fast, path = path, prefix = 'BOUT.fast', xguards = False)

domain = data['n'].shape

#%% Plot data

print(123)

fig, ax = plt.subplots(2)

ax[0].contourf(np.transpose(data['n'][-1, :, 0, :]), 100, cmap = 'inferno')
for probe in [0.80, 0.85, 0.90]:
    ax[0].plot([int(probe*domain[1])+2], [int(0.50*domain[3])], 'o')
ax[0].set_xlabel('x')
ax[0].set_ylabel('y')
    
ax[1].plot(fast['t_array'], fast['n0'][:], label = 'fast output')
ax[1].plot(par['t_array' ], data['n' ][:, int(0.80*domain[1])+2, 0, int(0.50*domain[3])], 'o', color = 'k', label = 'dmp output')
ax[1].set_xlabel('t')
ax[1].set_ylabel('n')
ax[1].legend()


fig.tight_layout()

plt.show()
# %%
