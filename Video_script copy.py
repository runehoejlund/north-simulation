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
i = 300


path        = './shared/NORTH/data/'  
field_list  = ['T', 'n', 'phi', 'vort', 'ZMIN','ZMAX', 'dx', 'dy', 'dz']
par_list    = ['t_array']
fast_list   = ['t_array', 'n0', 'phi0', 'n1', 'phi1', 'n2', 'phi2', 'T0', 'T1', 'T2']

data, par, fast = {}, {}, {}

for _field in field_list:
    data[_field] = collect(_field, path = path, xguards = False)

for _par in par_list:
    par[_par] = collect(_par, path = path, xguards = False)

#for _fast in fast_list:
#    fast[_fast] = collect(_fast, path = path, prefix = 'BOUT.fast', xguards = False)

domain = data['n'].shape


plt.rcParams["figure.figsize"] = [10.0, 10.0]
plt.rcParams["figure.autolayout"] = True


# Create a figure and a set of subplots
fig, ax = plt.subplots()
# Method to change the contour data points
def animate(i):
    ax.clear()
    ax.contourf(np.transpose(data['vort'][i, :, 0, :]), 100, cmap = 'jet', vmin=-0.5, vmax=0.5)
    #ax.contourf(np.transpose(data['n'][i, :, 0, :]), 100, cmap = 'inferno', vmin=0, vmax=1.4)
    #ax.contourf(np.transpose(data['T'][i, :, 0, :]), 100, cmap = 'inferno', vmin=0, vmax=1.2)

    
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    fig.tight_layout()

# Call animate method
ani = animation.FuncAnimation(fig, animate, frames=i, interval=10, blit=False)

ani.save('plots/animation_vort.gif', fps = 10)

