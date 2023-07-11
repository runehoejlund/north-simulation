# -*- coding: utf-8 -*-

# %%
import re
import os
job_ids = [re.search('(\d){7}', dir).group() for dir in os.listdir("./shared/NORTH/") if re.search('data_(\d){7}', dir)]
job_ids.sort()

# The last (highest id) job id is the lates job
job_id = job_ids[-1]
print('job_id', job_id)

# %%
import numpy as np
from matplotlib import pyplot as plt
from boutdata import collect
import matplotlib.cm as cm
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from boutdata.data import BoutData

path        = './shared/NORTH/data_' + job_id + '/'
bdata = BoutData(path)
outputs = bdata['outputs']
options  =bdata['options']

field_keys = bdata['outputs'].keys()

print('field_keys', field_keys)

# %%
from matplotlib import rcParams
rcParams.update({
    "font.size": 16})
rcParams['axes.titlepad'] = 20

# %%
def get_option(*keys):
    from numpy import sqrt
    val = options
    try:
        for key in keys:
            val = val[key]
        return eval(str(val))
    except:
        print('Error reading option for keys: ', keys)
        return 0

def get_options(keys_list):
    vals = []
    for keys in keys_list:
        vals.append(get_option(*keys))
    return vals

R, Te0, N_nuclei, mp, B0, e, mxg, myg = get_options([
    ('north', 'R'), ('north', 'Te0'), ('north', 'N_nuclei'),
    ('north', 'mp'), ('north', 'B0'), ('north', 'e'),
    (['mxg']), (['myg'])])
R, Te0, N_nuclei, mp, B0, e, mxg, myg

print('nx: ', options['mesh']['nx'])
print('ny: ', options['mesh']['ny'])
print('nz: ', options['mesh']['nz'])
print('Lx: ', options['mesh']['Lx'])
print('rho_s: ', options['north']['rho_s'])
print('oci: ', options['north']['oci'])

nx_all, ny_all, nz_all = get_options([('mesh', 'nx'),('mesh', 'ny'),('mesh', 'nz')])
oci = get_option('north', 'oci')
rho_s = get_option('north', 'rho_s')
Lx = R/rho_s * rho_s
nx_inner = nx_all - 2*mxg
ny_inner = ny_all - 2*myg
nz_inner = nz_all

#%% Read data

field_list  = ['T', 'n', 'phi', 'vort','source_n', 'source_T','wall_shadow']
par_list    = ['t_array']
# fast_list   = ['t_array', 'n0', 'phi0', 'n1', 'phi1', 'n2', 'phi2', 'T0', 'T1', 'T2']
#%%
data, par, fast = {}, {}, {}

for _field in field_list:
    data[_field] = collect(_field, path = path, xguards = False)

for _par in par_list:
    par[_par] = collect(_par, path = path, xguards = False)

dmp_nr = 4

thetas = np.linspace(0, 2 * np.pi, nz_inner)
rhos = np.linspace(1/(2*nx_inner), Lx+1/(2*nx_inner), nx_inner)

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

# %% 
# Polar plot test
plot0 = ax.contourf(thetas, rhos, data['n'][dmp_nr, :, :, :].squeeze(), 100, cmap = 'inferno')
ax.set_rticks([])
ax.set_xticks([])
plt.colorbar(plot0, ax=ax)
# plt.save('n_dmp_nr_' + str(dmp_nr) + '.png')

# %%
# Method to change the contour data points
def plot_field(field, i, cmap='inferno'):
    vmin = data[field].min()
    vmax = data[field].max()
    # ax.clear()
    contour_set = ax.contourf(thetas, rhos, data[field][i, :, :, :].squeeze(), 100, cmap = cmap, vmin=vmin, vmax=vmax)
    ax.set_rticks([])
    ax.set_xticks([])
    fig.tight_layout()
    return contour_set

def animate_n(i):
    plot_field('n',i)
def animate_T(i):
    plot_field('T',i)
def animate_vort(i):
    plot_field('vort',i, cmap='jet')

# %%
# Density animation
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

plt.colorbar(plot_field('n',0), ax=ax)
ani = animation.FuncAnimation(fig, animate_n, frames=data['n'].shape[0], interval=100, blit=False)
ani.save('plots/' + job_id + '_animation_n.gif', fps = 4)
# plt.show()

# %%
# Temperature animation
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

plt.colorbar(plot_field('T',-1), ax=ax)
ani = animation.FuncAnimation(fig, animate_T, frames=data['T'].shape[0], interval=100, blit=False)
ani.save('./plots/' + job_id + 'animation_T.gif', fps = 4)
# plt.show()

# %%
# Vorticity animation
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

plt.colorbar(plot_field('vort',-1), ax=ax)
ani = animation.FuncAnimation(fig, animate_vort, frames=data['vort'].shape[0], interval=100, blit=False)
ani.save('plots/' + job_id + 'animation_vort.gif', fps = 4)
# plt.show()