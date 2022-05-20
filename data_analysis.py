# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 10:08:12 2021

@author: alec
"""
# %%
import numpy as np
from matplotlib import pyplot as plt
from boutdata import collect

path        = './shared/NORTH/data/'  
field_list  = ['n', 'vort', 'phi']
par_list    = ['t_array']

data, par, fast = {}, {}, {}

for _field in field_list:
    data[_field] = collect(_field, path = path, xguards = False)

for _par in par_list:
    par[_par] = collect(_par, path = path, xguards = False)

domain = data['n'].shape

#%%
fig, ax = plt.subplots(2)
ax[0].contourf(np.transpose(data['n'][-1, :, 0, :]), 100, cmap = 'inferno')
ax[1].contourf(np.transpose(data['phi'][-1, :, 0, :]), 100, cmap = 'inferno')
plt.show()

# %%
fig2 = plt.figure()
plt.contourf(np.transpose(data['n'][-1, :, 0, :]), 100, cmap = 'inferno')
plt.colorbar()
plt.show()
# %%
