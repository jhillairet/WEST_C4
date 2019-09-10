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

#%%
P_IC_54902, t_P_IC_54902 = get_sig(54902, signals['IC_P_tot'])
Rc_IC_54902, t_Rc_IC_54902 = get_sig(54902, signals['IC_Rc_avg'])


#%%
# reflectometry timings for average
ts = [(5.0, 5.4),  # before IC
      (6.7, 7.0),  # IC ramp up
      (7.55, 7.75),  # IC plateau
      (8.2, 8.5),  # IC reduced Rc
      (8.68, 8.83),  # IC huge reduced Rc
      ]

#%%
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
ax1.plot(t_P_IC_54902, P_IC_54902, lw=2, label='54902')
ax2.plot(t_Rc_IC_54902, Rc_IC_54902, lw=2, label='54902')

ax2.set_xlabel('t [s]', fontsize=14)
ax2.set_xlim(4, 10)
ax1.set_title(f'WEST #54902 (USN, Q1 + Q4)')
ax1.set_ylabel('Power [kW]', fontsize=14)
ax2.set_ylabel('Rc [Ohm]', fontsize=14)

[a.grid(True, alpha=.4) for a in (ax1, ax2)]
[a.tick_params(labelsize=12) for a in (ax1, ax2)]

for idx, (t_start, t_stop) in enumerate(ts):
    [a.axvspan(t_start, t_stop, alpha=.2, color=f'C{idx}') for a in (ax1, ax2)]


fig.subplots_adjust(hspace=0)


#%%
fig.savefig('WEST_54902_reflectometry_timings.png', dpi=150)

#%%
file_54902 = '../reflectometry/profiles/WEST_54902_prof.mat'

data_54902 = loadmat(file_54902)

#%% plot all profiles
fig, ax = plt.subplots()
#ax.plot(data_54902['RX'], data_54902['NEX'], alpha=.1)
ax.plot(data_54902['RX'][:,idx_t_start:idx_t_stop].mean(axis=1), 
        data_54902['NEX'][:,idx_t_start:idx_t_stop].mean(axis=1))
ax.set_yscale('log')
#%%
def time_averaged_profile(data, t_start, t_stop):
    idx_t_start = argmin(abs(data['tX'] - t_start -32))
    idx_t_stop = argmin(abs(data['tX'] - t_stop -32))
    
    ne_mean = mean(data['NEX'][:,idx_t_start:idx_t_stop], axis=1)
    ne_std = std(data['NEX'][:,idx_t_start:idx_t_stop], axis=1)
    r_mean = mean(data['RX'][:,idx_t_start:idx_t_stop], axis=1)
    r_std = std(data['RX'][:,idx_t_start:idx_t_stop], axis=1)

    return r_mean, r_std, ne_mean, ne_std


# %%
fig, ax = plt.subplots()

for (t_start, t_stop) in ts:
    # ne and r mean, error bar repr with std
    r, rs, ne, nes = time_averaged_profile(data_54902, t_start, t_stop)
    
    ax.fill_betweenx(ne, r-rs, r+rs, alpha=.4)
    ax.plot(r, ne, lw=2, label=f'{t_start}-{t_stop}')


ax.legend()
ax.set_yscale('log')
ax.set_xlim((2.84, 2.98))
ax.grid(True)
ax.grid(True, which='minor', alpha=0.5)
ax.axvline(2.95, color='k')
ax.set_ylabel('Density [$m^{-3}$]', fontsize=12)
ax.set_xlabel('Radius [m]', fontsize=12)
ax.set_title(f'WEST #54902 (USN, Q1 + Q4)')

#%%
fig.savefig('WEST_54902_reflectometry_profiles.png', dpi=150)