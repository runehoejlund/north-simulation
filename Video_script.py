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
field_list  = ['T', 'n', 'phi', 'vort']
par_list    = ['t_array']
fast_list   = ['t_array', 'n0', 'phi0', 'n1', 'phi1', 'n2', 'phi2', 'T0', 'T1', 'T2']

data, par, fast = {}, {}, {}


dmp_files = DataFile("./shared/NORTH/data/BOUT.dmp.0.nc").list()
fast_files = DataFile("./shared/NORTH/data/BOUT.fast.0.nc").list()

for _field in field_list:
    data[_field] = collect(_field, path = path, xguards = False)

for _par in par_list:
    par[_par] = collect(_par, path = path, xguards = False)

for _fast in fast_list:
    fast[_fast] = collect(_fast, path = path, prefix = 'BOUT.fast', xguards = False)

domain = data['n'].shape

#%% Plot data

probe_pos = [0.80, 0.82, 0.84]
dmp_nr = 80

fig, ax = plt.subplots(3)

plot0 = ax[0].contourf(np.transpose(data['n'][dmp_nr, :, 0, :]), 100, cmap = 'inferno')
for probe in probe_pos:
    ax[0].plot([int(probe*domain[1])+2], [int(0.50*domain[3])], 'o')
ax[0].set_xlabel('x')
ax[0].set_ylabel('y')
plt.colorbar(plot0, ax=ax[0])

plot1 = ax[1].contourf(np.transpose(data['T'][dmp_nr, :, 0, :]), 100, cmap = 'inferno')
for probe in probe_pos:
    ax[1].plot([int(probe*domain[1])+2], [int(0.50*domain[3])], 'o')
ax[1].set_xlabel('x')
ax[1].set_ylabel('y')
plt.colorbar(plot1, ax=ax[1])

plot2 = ax[2].contourf(np.transpose(data['vort'][dmp_nr, :, 0, :]), 100, cmap = 'jet')
for probe in probe_pos:
    ax[2].plot([int(probe*domain[1])+2], [int(0.50*domain[3])], 'o')
ax[2].set_xlabel('x')
ax[2].set_ylabel('y')
plt.colorbar(plot2, ax=ax[2])
fig.tight_layout()


plt.show(block=False)

#%%

fig, ax = plt.subplots(3)

ax[0].plot(fast['t_array'], fast['T0'][:], label = 'fast output')
ax[0].plot(par['t_array' ], data['T' ][:, int(probe_pos[0]*domain[1])+2, 0, int(0.50*domain[3])], 'o', color = 'k', label = 'dmp output')
ax[0].set_xlabel('t')
ax[0].set_ylabel('n')
ax[0].legend()
ax[0].title.set_text('Probe position = {:.2f}'.format(probe_pos[0]))

ax[1].plot(fast['t_array'], fast['T1'][:], label = 'fast output')
ax[1].plot(par['t_array' ], data['T' ][:, int(probe_pos[1]*domain[1])+2, 0, int(0.50*domain[3])], 'o', color = 'k', label = 'dmp output')
ax[1].set_xlabel('t')
ax[1].set_ylabel('n')
ax[1].legend()
ax[1].title.set_text('Probe position = {:.2f}'.format(probe_pos[1]))

ax[2].plot(fast['t_array'], fast['T2'][:], label = 'fast output')
ax[2].plot(par['t_array' ], data['T' ][:, int(probe_pos[2]*domain[1])+2, 0, int(0.50*domain[3])], 'o', color = 'k', label = 'dmp output')
ax[2].set_xlabel('t')
ax[2].set_ylabel('n')
ax[2].legend()
ax[2].title.set_text('Probe position = {:.2f}'.format(probe_pos[2]))

fig.tight_layout()

plt.show()

#%%

plt.rcParams["figure.figsize"] = [7.0, 7.0]
plt.rcParams["figure.autolayout"] = True

# Create a figure and a set of subplots
fig, ax = plt.subplots()

# Method to change the contour data points
def animate(i):
    ax.clear()
    #ax.contourf(np.transpose(data['vort'][i, :, 0, :]), 100, cmap = 'jet', vmin=-0.6, vmax=0.6)
    ax.contourf(np.transpose(data['n'][i, :, 0, :]), 100, cmap = 'inferno', vmin=5.5, vmax=10.5)
    #plot_vid = ax.contourf(np.transpose(data['T'][i, :, 0, :]), 100, cmap = 'hot', vmin=0.85, vmax=1.25)
    for probe in probe_pos:
        ax.plot([int(probe*domain[1])+2], [int(0.50*domain[3])], 'o')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    fig.tight_layout()

# Call animate method
ani = animation.FuncAnimation(fig, animate, frames=81, interval=100, blit=False)

ani.save('plots/animation_ne_2.mp4',
          writer = 'ffmpeg', fps = 10)

plt.show()
# %%
