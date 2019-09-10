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
P_IC_54903, t_P_IC_54903 = get_sig(54903, signals['IC_P_tot'])
Rc_IC_54903, t_Rc_IC_54903 = get_sig(54903, signals['IC_Rc_avg'])





#%%
# reflectometry timings for average
ts = [(5.0, 5.4),  # before IC
      (7.55, 7.75),  # IC plateau
      (8.2, 8.5),  # IC reduced Rc
      (9.30, 9.60),  # IC huge reduced Rc
      ]

#%%
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
ax1.plot(t_P_IC_54903, P_IC_54903, lw=2, label='54903')
ax2.plot(t_Rc_IC_54903, Rc_IC_54903, lw=2, label='54903')

ax2.set_xlabel('t [s]', fontsize=14)
ax2.set_xlim(4, 10)
ax1.set_title(f'WEST #54903 (LSN, Q1 + Q4)')
ax1.set_ylabel('Power [kW]', fontsize=14)
ax2.set_ylabel('Rc [Ohm]', fontsize=14)

[a.grid(True, alpha=.4) for a in (ax1, ax2)]
[a.tick_params(labelsize=12) for a in (ax1, ax2)]

for idx, (t_start, t_stop) in enumerate(ts):
    [a.axvspan(t_start, t_stop, alpha=.2, color=f'C{idx}') for a in (ax1, ax2)]


fig.subplots_adjust(hspace=0)


#%%
fig.savefig('WEST_54903_reflectometry_timings.png', dpi=150)

#%%
file_54903 = '../reflectometry/profiles/WEST_54903_prof.mat'

data_54903 = loadmat(file_54903)


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
    r, rs, ne, nes = time_averaged_profile(data_54903, t_start, t_stop)
    
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
ax.set_title(f'WEST #54903 (LSN, Q1 + Q4)')

#%%
## FW cut off density
#from scipy.constants import c, epsilon_0, e, m_p
#from astropy import units as u
#from plasmapy.physics.parameters import gyrofrequency
#omega_0 = 2*np.pi*55.5e6
#k_0 = omega_0 / c
#k_parallel = 14  # m^-1
## Itor 1250 A, meaning 3.7T at R=2.5 m
#R0 = 2.5
#B0 = 3.7
#omega_ci = gyrofrequency(B=R0/r*B0*u.T, particle='D', Z=2, signed=True).value 
#
#nc_R = epsilon_0/e**2*1/(1/m_p/(omega_0 + omega_ci)/omega_0)*(k_parallel**2/k_0**2 - 1)
#nc_L = epsilon_0/e**2*1/(1/m_p/(omega_0 - omega_ci)/omega_0)*(k_parallel**2/k_0**2 - 1)
#
#ax.axhline(nc_L.mean(), color='r', lw=2, alpha=0.3)
          
#%%
fig.savefig('WEST_54903_reflectometry_profiles.png', dpi=150)