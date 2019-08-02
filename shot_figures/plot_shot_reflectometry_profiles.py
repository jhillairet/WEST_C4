# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 10:27:26 2019

@author: JH218595
"""
#%%
import sys; sys.path.append('..')
from control_room import *
from numpy import *
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from scipy.io import loadmat
import pywed as pw

#%%
pulse = 54600

P_IC, t_P_IC= get_sig(pulse, signals['IC_P_tot'])
P_LH, t_P_LH= get_sig(pulse, signals['LH_P_tot'])
nl, t_nl = get_sig(pulse, signals['nl'])
ip, t_ip = get_sig(pulse, signals['Ip'])

#%%
(td1, tf1) = (4.7, 4.8)
(td2, tf2) = (7.0, 7.1)
(td3, tf3) = (10.15, 10.25)

#%%
fig, ax = plt.subplots(2, 1, sharex=True)
ax[0].plot(t_nl, nl, lw=2, label=f'nl')
ax[0].plot(t_ip, ip/1e3, lw=2, label=f'Ip')
ax[1].plot(t_P_IC, P_IC/1e3, lw=2, label=f'IC' )
ax[1].plot(t_P_LH, P_LH, lw=2, label=f'LH')
         
ax[1].set_xlabel('t [s]', fontsize=14)
ax[0].set_title(f'WEST #{pulse}')
ax[1].set_ylabel('Power [kW]', fontsize=14) 
ax[0].set_xlim(0, 16)
[a.grid(True, alpha=.4) for a in ax]
[a.tick_params(labelsize=12) for a in ax]

[a.axvspan(td1, tf1, color='C0', alpha=.2) for a in ax]
[a.axvspan(td2, tf2, color='C1', alpha=.2) for a in ax]
[a.axvspan(td3, tf3, color='C2', alpha=.2) for a in ax]
[a.legend() for a in ax]
fig.subplots_adjust(hspace=0)

#%%
fig.savefig('WEST_54600_reflecto_times.png', dpi=150)

#%%
file = f'../reflectometry/profiles/WEST_{pulse}_prof.mat'
data = loadmat(file)

#%%
# correct data time from ignitron
t_ignitron = pw.tsmat(pulse, 'IGNITRON|1')
data['tX'] -= t_ignitron

#%%
def time_averaged_profile(data, t_start, t_end):
    idx_t_start = argmin(abs(data['tX'] - t_start))
    idx_t_stop = argmin(abs(data['tX'] - t_end))
    
    ne_mean = mean(data['NEX'][:,idx_t_start:idx_t_stop], axis=1)
    ne_std = std(data['NEX'][:,idx_t_start:idx_t_stop], axis=1)
    r_mean = mean(data['RX'][:,idx_t_start:idx_t_stop], axis=1)
    r_std = std(data['RX'][:,idx_t_start:idx_t_stop], axis=1)

    return r_mean, r_std, ne_mean, ne_std

#%% ne and r mean, error bar repr with std
r1, rs1, ne1, nes1 = time_averaged_profile(data, td1, tf1)
r2, rs2, ne2, nes2 = time_averaged_profile(data, td2, tf2)
r3, rs3, ne3, nes3 = time_averaged_profile(data, td3, tf3)


# %%
fig, ax = plt.subplots()

ax.fill_betweenx(ne1, r1-rs1, r1+rs1, alpha=.4)
ax.plot(r1, ne1, lw=2, label=f'#{pulse} - {td1}-{tf1} s')
ax.fill_betweenx(ne3, r3-rs3, r3+rs3, alpha=.4)
ax.plot(r3, ne3, lw=2, label=f'#{pulse} - {td2}-{tf2} s')
        
ax.fill_betweenx(ne2, r2-rs2, r2+rs2, alpha=.4)
ax.plot(r2, ne2, lw=2, label=f'#{pulse} - {td3}-{tf3} s')


ax.legend()
ax.set_yscale('log')
ax.set_xlim((2.89, 2.96))
ax.grid(True)
ax.grid(True, which='minor', alpha=0.5)
ax.axvline(2.951, color='k')
ax.axvline(2.955, color='grey')
ax.axvline(2.957, color='darkgrey')
ax.set_ylabel('Density [$m^{-3}$]', fontsize=12)
ax.set_xlabel('Radius [m]', fontsize=12)



#%%
fig.savefig('WEST_54600_reflecto_density_profiles.png', dpi=150)
