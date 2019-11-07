# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 15:50:39 2019

@author: JH218595
"""
#%%
import sys
sys.path.append('..')
from control_room import *
import numpy as np
from matplotlib.pyplot import *


#%%
pulse = 55589

# reflectometry timings for average
ts = [(8.81, 8.88), 
      (8.93, 9.00),   
      ]

ts = [(4.07, 4.70),
      (5.57, 6.03),
      (7.09, 7.59),
      (8.58, 9.02),
      (10.08, 10.45)
      ]

#%%
Ip, t_Ip = get_sig(pulse, signals['Ip'])
nl, t_nl = get_sig(pulse, signals['nl'])

P_IC_tot, t_tot = get_sig(pulse, signals['IC_P_tot'])
P_Q1, t_Q1 = get_sig(pulse, signals['IC_P_Q1'])
P_Q2, t_Q2 = get_sig(pulse, signals['IC_P_Q2'])
P_Q4, t_Q4 = get_sig(pulse, signals['IC_P_Q4'])

Prad, trad = get_sig(pulse, signals['Prad'])
Psep, tsep = get_sig(pulse, signals['Separatrix_P'])

# Te, t_Te = get_sig(pulse, signals['Te'])
neutron1, t_neutron1 = get_sig(pulse, signals['Neutron1'])

Rc_Q1, t_Rc_Q1 = get_sig(pulse, signals['IC_Rc_Q1_avg'])
Rc_Q2, t_Rc_Q2 = get_sig(pulse, signals['IC_Rc_Q2_avg'])
Rc_Q4, t_Rc_Q4 = get_sig(pulse, signals['IC_Rc_Q4_avg'])

R_IC, t_R_IC = get_sig(pulse, signals['IC_Positions'])
Rext, t_Rext = get_sig(pulse, signals['Rext_median'])


VSWR_Q1_l, t_VSWR_Q1_l = get_sig(pulse, signals['IC_VSWR_Q1_Left'])
VSWR_Q1_r, t_VSWR_Q1_r = get_sig(pulse, signals['IC_VSWR_Q1_Right'])
VSWR_Q4_l, t_VSWR_Q4_l = get_sig(pulse, signals['IC_VSWR_Q4_Left'])
VSWR_Q4_r, t_VSWR_Q4_r = get_sig(pulse, signals['IC_VSWR_Q4_Right'])

VSWR_Q1 = (VSWR_Q1_l + VSWR_Q1_r)/2
VSWR_Q4 = (VSWR_Q4_l + VSWR_Q4_r)/2

##%%
### interpolate LH and IC power
#P_LH_tot, t_LH_tot = get_sig(pulse, signals['LH_P_tot'])
#P_LH1, t_LH1 = get_sig(pulse, signals['LH_P_LH1'])
#P_LH2, t_LH2 = get_sig(pulse, signals['LH_P_LH2'])
#
#_P_LH_tot = np.interp(t_tot, t_LH_tot, P_LH_tot)
#_P_LH1 = np.interp(t_tot, t_LH1, P_LH1)
#_P_LH2 = np.interp(t_tot, t_LH2, P_LH2)

#%%
fig, ax = plt.subplots(4,1,sharex=True,  figsize=(10, 8.5))
ax[0].plot(t_Ip, Ip, lw=2)
ax[0].set_ylabel('Ip [kA]', fontsize=14, color='C0')
ax[0].tick_params(color='C0', labelcolor='C0')
ax[0].set_xlim(-0.1, 13)
ax[0].set_title(f'WEST #{pulse} - Preliminary', fontsize=14)

ax0 = ax[0].twinx()
ax0.plot(t_nl, nl, lw=2, color='C1')
ax0.set_ylabel('nl [$10^{19}$ $m^{-3}$]', fontsize=14, color='C1')
ax0.tick_params(color='C1', labelcolor='C1')

ax[1].fill_between(t_Q4, (P_Q1+P_Q4)*1e-3, alpha=0.2, label='Total RF Power')
#ax[1].plot(t_LH1, P_LH1*1e-3, label='LH1', lw=2, color='C1')
#ax[1].plot(t_LH2, P_LH2*1e-3, label='LH2', lw=2, color='C2')
ax[1].plot(t_Q1, P_Q1*1e-3, label='IC Q1', lw=2, color='C3')
#ax[1].plot(t_Q2, P_Q2*1e-3, label='IC Q2', lw=2, color='C4')
ax[1].plot(t_Q4, P_Q4*1e-3, label='IC Q4', lw=2, color='C5')


ax[1].set_ylabel('RF Power [MW]', fontsize=14)
ax[1].legend(fontsize=12, loc='upper left', ncol=1)

ax[2].plot(t_Rc_Q1, Rc_Q1, label='Rc Q1')
ax[2].plot(t_Rc_Q4, Rc_Q4, label='Rc Q4')
ax[2].legend(fontsize=12)
ax[2].set_ylabel('Rc [$\Omega$]', fontsize=14)


#ax[3].plot(t_VSWR_Q1_l, VSWR_Q1_l, lw=2, label='VSWR Q1 - left')
#ax[3].plot(t_VSWR_Q1_r, VSWR_Q1_r, lw=2, label='VSWR Q1 - right')
#ax[3].plot(t_VSWR_Q4_l, VSWR_Q4_l, lw=2, label='VSWR Q4 - left')
#ax[3].plot(t_VSWR_Q4_r, VSWR_Q4_r, lw=2, label='VSWR Q4 - right')
ax[3].plot(t_VSWR_Q1_l, VSWR_Q1, lw=2, label='VSWR Q1')
ax[3].plot(t_VSWR_Q4_l, VSWR_Q4, lw=2, label='VSWR Q4')

ax[3].set_ylim(1, 2.5)
ax[3].set_ylabel('VSWR', fontsize=14)

#ax[3].plot(trad, Prad, lw=2, label='Radiated (total)')
#ax[3].plot(tsep, Psep, lw=2, label='Separatrix')
#ax[3].set_ylim(0, 5)
#ax[3].set_ylabel('Power [MW]', fontsize=14)
#ax[3].legend(fontsize=12, loc='upper left')

# ax2 = ax[2].twinx()
# ax2.plot(t_Te, Te, lw=2, color='C2')
# ax2.set_ylabel('Te [eV]', fontsize=14, color='C2')
# ax2.set_ylim(bottom=0)
# ax2.tick_params(color='C2', labelcolor='C2')

[a.grid(True, alpha=0.2) for a in ax]
[a.tick_params(labelsize=14) for a in ax]
ax[-1].set_xlabel('Time [s]', fontsize=14)

fig.tight_layout()

#%%
for idx, _ts in enumerate(ts):
    ax[0].axvspan(_ts[0], _ts[1], color=f'C2', alpha=0.2)
    ax[1].axvspan(_ts[0], _ts[1], color=f'C2', alpha=0.2)
    ax[2].axvspan(_ts[0], _ts[1], color=f'C2', alpha=0.2)
    ax[3].axvspan(_ts[0], _ts[1], color=f'C2', alpha=0.2)


#%%
fig.savefig(f'WEST_IC_{pulse}_summary_glacons.png', dpi=150)


#%% VSWR vs Rc



fig, ax = plt.subplots()

_Rc_Q1, _ = in_between(Rc_Q1, t_Rc_Q1, 7.0, 8 )
_Rc_Q4, _ = in_between(Rc_Q4, t_Rc_Q4, 7.0, 8 )
_VSWR_Q1, _ = in_between(VSWR_Q1, t_VSWR_Q1_l[:,0], 7.0, 8 )
_VSWR_Q4, _ = in_between(VSWR_Q4, t_VSWR_Q4_l[:,0], 7.0, 8 )

ax.plot(_Rc_Q1, _VSWR_Q1, '.', alpha=0.6, label='Q1')
ax.plot(_Rc_Q4, _VSWR_Q4, '.', alpha=0.6, label='Q4')
ax.legend(fontsize=12)
ax.set_ylim(1, 2.5)
ax.set_xlim(0.35, 2.1)
ax.grid(True, alpha=0.6)
ax.set_xlabel('Rc [$\Omega$]', fontsize=14)
ax.set_ylabel('VSWR', fontsize=14)
ax.set_title(r'Antennas Load Resilience - $t\in[7-8]$s')

#%%
fig.savefig(f'WEST_IC_{pulse}_VSWR_vs_Rc.png', dpi=150)

#%%

##%%
#Rant, _ = get_sig(pulse, signals['IC_Positions'])
#Rant_Q4 = Rant[2]
#
#
#
#
##%%
#file = f'../reflectometry/profiles/WEST_{pulse}_prof.mat'
#
#data = loadmat(file)
#
#
##%%
#def time_averaged_profile(data, t_start, t_stop):
#    idx_t_start = argmin(abs(data['tX'] - t_start -32))
#    idx_t_stop = argmin(abs(data['tX'] - t_stop -32))
#    
#    ne_mean = mean(data['NEX'][:,idx_t_start:idx_t_stop], axis=1)
#    ne_std = std(data['NEX'][:,idx_t_start:idx_t_stop], axis=1)
#    r_mean = mean(data['RX'][:,idx_t_start:idx_t_stop], axis=1)
#    r_std = std(data['RX'][:,idx_t_start:idx_t_stop], axis=1)
#
#    return r_mean, r_std, ne_mean, ne_std
#
#
## %%
#fig, ax = plt.subplots()
#
#for (t_start, t_stop) in ts:
#    # ne and r mean, error bar repr with std
#    r, rs, ne, nes = time_averaged_profile(data, t_start, t_stop)
#    
#    ax.fill_betweenx(ne, r-rs, r+rs, alpha=.4)
#    ax.plot(r, ne, lw=2, label=f'{t_start}-{t_stop}')
#
#
#ax.legend()
#ax.set_yscale('log')
#ax.set_xlim((2.84, 2.98))
#ax.grid(True)
#ax.grid(True, which='minor', alpha=0.5)
#ax.axvline(Rant_Q4, color='k')
#ax.set_ylabel('Density [$m^{-3}$]', fontsize=12)
#ax.set_xlabel('Radius [m]', fontsize=12)
#ax.set_title(f'WEST #{pulse}')
#
##%%
#fig.savefig(f'WEST_{pulse}_reflectometry_profiles.png', dpi=150)
#
##%%
### FW cut off density
##from scipy.constants import c, epsilon_0, e, m_p
##from astropy import units as u
##from plasmapy.physics.parameters import gyrofrequency
##omega_0 = 2*np.pi*55.5e6
##k_0 = omega_0 / c
##k_parallel = 14  # m^-1
### Itor 1250 A, meaning 3.7T at R=2.5 m
##R0 = 2.5
##B0 = 3.7
##omega_ci = gyrofrequency(B=R0/r*B0*u.T, particle='D', Z=2, signed=True).value 
##
##nc_R = epsilon_0/e**2*1/(1/m_p/(omega_0 + omega_ci)/omega_0)*(k_parallel**2/k_0**2 - 1)
##nc_L = epsilon_0/e**2*1/(1/m_p/(omega_0 - omega_ci)/omega_0)*(k_parallel**2/k_0**2 - 1)
##
##ax.axhline(nc_L.mean(), color='r', lw=2, alpha=0.3)
#          

