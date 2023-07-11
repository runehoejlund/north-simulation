#  mq submit parameter_scan.py -R 16:xeon16:1h
# %%
import re
import os
import numpy as np
from matplotlib import pyplot as plt
from boutdata import collect
import matplotlib.cm as cm
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from boutdata.data import BoutData

def read_job(job_id):
    print(job_id)
    path        = './shared/NORTH/data_' + job_id + '/'
    bdata = BoutData(path)
    # outputs = bdata['outputs']
    options  =bdata['options']

    # field_keys = bdata['outputs'].keys()

    # %%
    def get_CLI_option(job_id, key):
        for i, line in enumerate(open('./shared/NORTH/slurm_out/north_full_' + job_id + '_ESEL.log', 'r')):
            match = re.search('Command line options for this run.*' + key + '\s*\=\s*(\S*)', line)
            if match:
                try:
                    return eval(match.group(1))
                except:
                    return match.group(1)

    def get_option(*keys):
        cli_option = get_CLI_option(job_id, keys[-1])
        if cli_option == None:
            from numpy import sqrt, pi
            from ast import parse, walk, Name
            val = options
            group = keys[0]
            for key in keys:
                val = val[key]
            try:
                return eval(str(val))
            except:
                # Parse undefined variables from the Bout.inp file:
                val_str = str(val).replace(':', '____') # Replace group indicator ':' with '____' to make string parsable.
                for node in walk(parse(val_str)):
                    if type(node) is Name:
                        missing_keys = node.id.split('____')
                        var = missing_keys[-1]
                        if var not in locals():
                            try:
                                locals()[var] = get_option(*missing_keys)
                            except:
                                missing_keys.insert(0, group)
                                try:
                                    locals()[var] = get_option(*missing_keys)
                                except:
                                    print('Error reading option for keys: ', keys)
                                    return 0
                return eval(str(val))
        else:
            return cli_option

    def get_options(keys_list):
        vals = []
        for keys in keys_list:
            vals.append(get_option(*keys))
        return vals

    # %%
    oci, rho_s, R, n0, Te0, mxg, myg, nx_all, ny_all, nz_all = get_options([
        ('north', 'oci'), ('north', 'rho_s'), ('north', 'R'),
        ('north', 'n0'), ('north', 'Te0'),
        ('mxg',), ('myg',),
        ('mesh', 'nx'),('mesh', 'ny'),('mesh', 'nz')])
    Lx = R/rho_s * rho_s
    nx_inner = nx_all - 2*mxg
    ny_inner = ny_all - 2*myg
    nz_inner = nz_all

    # %%
    try:
        vort_sink_strength = get_option('north', 'vort_sink_strength')
    except:
        if job_id == '5347831' or job_id == '5352599':
            vort_sink_strength = 0.1
        else:
            print('unknown vorticity sink strength')
    print('vorticity sink strength: ' + str(vort_sink_strength))

    #%% Read data

    field_list  = ['T', 'n', 'phi', 'vort', 'source_T','wall_shadow']
    par_list    = ['t_array']
    # fast_list   = ['t_array', 'n0', 'phi0', 'n1', 'phi1', 'n2', 'phi2', 'T0', 'T1', 'T2']
    #%%
    data, par, fast = {}, {}, {}

    for _field in field_list:
        data[_field] = collect(_field, path = path, xguards = False)

    for _par in par_list:
        par[_par] = collect(_par, path = path, xguards = False)
    
    # %%
    thetas = np.linspace(0, 2 * np.pi, nz_inner)
    rhos = np.linspace(Lx/(2*nx_inner), Lx+Lx/(2*nx_inner), nx_inner)
    t = par['t_array']/oci

    # # %% Mean Density
    # n_mean = np.mean(np.mean(data['n'].squeeze(),axis=1), axis=1)

    # plt.figure(figsize=(6,4))
    # plt.plot(t*(10**6),n_mean, 'k-')
    # plt.xlabel(r'$t$  $\mathrm{\mu s}$')
    # plt.ylabel(r'$\left<n\right>$  [norm. unit]')
    # plt.grid()
    # plt.title('With vorticity sink strength: ' + str(vort_sink_strength), pad=20)
    # # plt.show()
    # plt.savefig('plots/' + job_id + '_density_vs_time.png')
    # plt.savefig('plots/' + job_id + '_density_vs_time.pdf')

    # # %% Contained Energy
    # mesh_t, mesh_rhos, mesh_thetas = np.meshgrid(t, rhos, thetas, indexing='ij')

    # Jfun = lambda t, r, theta: np.abs(r*(R + r*np.cos(theta)))
    # def energy():
    #     n = data['n'].squeeze()*n0
    #     T = data['T'].squeeze()*Te0
    #     J = Jfun(mesh_t, mesh_rhos, mesh_thetas)
    #     return 2*np.pi*np.trapz(np.trapz(J*((3/2)*n*T), rhos, axis=1), thetas, axis=1)

    # E = energy()

    # plt.figure(figsize=(6,4))
    # plt.plot(t*(10**6), E, 'k-')
    # plt.xlabel(r'$t$  $\mathrm{\mu s}$')
    # plt.ylabel(r'$E$  $\mathrm{[eV]}$')
    # plt.grid()
    # plt.title('With vorticity sink strength: ' + str(vort_sink_strength), pad=20)
    # # plt.show()
    # plt.savefig('plots/' + job_id + '_energy.png')
    # plt.savefig('plots/' + job_id + '_energy.pdf')

    # %% Animation
    import matplotlib.animation as animation

    def animate_data(field, cmap='inferno', vmin = None, vmax = None):
        field_data = data[field].squeeze()
        if vmin is None:
            vmin = field_data.min()
        if vmax is None:
            vmax = field_data.max()
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        fig.suptitle('With vorticity sink strength: ' + str(vort_sink_strength))

        ax.set_rticks([])
        ax.set_xticks([])
        cont = ax.contourf(thetas, rhos, field_data[0, :, :], 100, cmap = cmap, vmin=vmin, vmax=vmax)    # first image on screen
        fig.colorbar(cont, ax=ax)
        fig.tight_layout()

        # animation function
        def animate(i):
            for c in ax.collections:
                c.remove()  # removes only the contours, leaves the rest intact
            cont = ax.contourf(thetas, rhos, field_data[i, :, :], 100, cmap = cmap, vmin=vmin, vmax=vmax)
            return cont.collections
        
        anim = animation.FuncAnimation(fig, animate, frames=field_data.shape[0], interval=100, blit=True)
        anim.save('./plots/' + job_id + '_animation_' + field +'.gif', fps=4)
        # plt.show()
    
    animate_data('n')
    animate_data('T', vmin=0, vmax=5)
    animate_data('vort', cmap='jet')
    animate_data('phi', cmap='jet')

if __name__ == '__main__':
    job_ids = [re.search('(\d){7}', dir).group() for dir in os.listdir("./shared/NORTH/") if re.search('data_(\d){7}', dir)]
    job_ids.sort()
    n_jobs = 6
    # The last (highest id) job id is the lates job
    job_ids = job_ids[-n_jobs:]
    # job_ids = ['5352599', '5355427']
    for job_id in job_ids:
        read_job(job_id)