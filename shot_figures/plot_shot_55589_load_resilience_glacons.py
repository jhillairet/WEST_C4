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

# maximum voltages in DFCI
max_Vs = pw.tsmat(pulse, 'AFCI ;+VME_FCI ;V_limite')
max_Is = pw.tsmat(pulse, 'AFCI ;+VME_FCI ;I_limite')

#%%
do_smooth=True
Ip, t_Ip = get_sig(pulse, signals['Ip'])
nl, t_nl = get_sig(pulse, signals['nl'])

P_IC_tot, t_tot = get_sig(pulse, signals['IC_P_tot'], do_smooth)
P_Q1, t_Q1 = get_sig(pulse, signals['IC_P_Q1'], do_smooth)
P_Q2, t_Q2 = get_sig(pulse, signals['IC_P_Q2'], do_smooth)
P_Q4, t_Q4 = get_sig(pulse, signals['IC_P_Q4'], do_smooth)

Prad, trad = get_sig(pulse, signals['Prad'])
Psep, tsep = get_sig(pulse, signals['Separatrix_P'])

# Te, t_Te = get_sig(pulse, signals['Te'])
neutron1, t_neutron1 = get_sig(pulse, signals['Neutron1'])

Rc_Q1, t_Rc_Q1 = get_sig(pulse, signals['IC_Rc_Q1_avg'], do_smooth)
Rc_Q2, t_Rc_Q2 = get_sig(pulse, signals['IC_Rc_Q2_avg'], do_smooth)
Rc_Q4, t_Rc_Q4 = get_sig(pulse, signals['IC_Rc_Q4_avg'], do_smooth)

R_IC, t_R_IC = get_sig(pulse, signals['IC_Positions'])
Rext, t_Rext = get_sig(pulse, signals['Rext_median'])


VSWR_Q1_l, t_VSWR_Q1_l = get_sig(pulse, signals['IC_VSWR_Q1_left'], do_smooth)
VSWR_Q1_r, t_VSWR_Q1_r = get_sig(pulse, signals['IC_VSWR_Q1_right'], do_smooth)
VSWR_Q4_l, t_VSWR_Q4_l = get_sig(pulse, signals['IC_VSWR_Q4_left'], do_smooth)
VSWR_Q4_r, t_VSWR_Q4_r = get_sig(pulse, signals['IC_VSWR_Q4_right'], do_smooth)

VSWR_Q1 = (VSWR_Q1_l + VSWR_Q1_r)/2
VSWR_Q4 = (VSWR_Q4_l + VSWR_Q4_r)/2

Rant, _ = get_sig(pulse, signals['IC_Positions'])
Rant_Q1 = Rant[0]
Rant_Q4 = Rant[2]

#%% corrige valeur de repli 
Rc_Q4[P_Q4 < 1] = 0
Rc_Q1[P_Q1 < 1] = 0

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
fig, ax = plt.subplots(4,1, sharex=True,  figsize=(6, 8))
ax[0].plot(t_Ip, Ip, lw=2)
ax[0].set_ylabel('Ip [kA]', fontsize=14, color='C0')
ax[0].tick_params(color='C0', labelcolor='C0')
ax[0].set_xlim(-0.1, 13)
ax[0].set_title(f'WEST #{pulse}', fontsize=14)

ax0 = ax[0].twinx()
ax0.plot(t_nl, nl, lw=2, color='C1')
ax0.set_ylabel('nl [$10^{19}$ $m^{-3}$]', fontsize=14, color='C1')
ax0.tick_params(color='C1', labelcolor='C1')

ax[1].fill_between(t_Q4, (P_Q2+P_Q1+P_Q4)*1e-3, alpha=0.2, label='IC Total')
ax[1].plot(t_Q1, P_Q1*1e-3, label='IC Q1', lw=2, color='C0')
ax[1].plot(t_Q2, P_Q2*1e-3, label='IC Q2', lw=2, color='C1')
ax[1].plot(t_Q4, P_Q4*1e-3, label='IC Q4', lw=2, color='C2')
ax[1].set_ylabel('RF Power [MW]', fontsize=14)
ax[1].legend(fontsize=10, loc='upper left', ncol=1)

ax[2].plot(t_Rc_Q1, Rc_Q1, label=r'$\overline{R}_c$ Q1', color='C0')
ax[2].plot(t_Rc_Q4, Rc_Q4, label=r'$\overline{R}_c$ Q4', color='C2')
ax[2].legend(fontsize=10)
ax[2].set_ylabel('Rc [$\Omega$]', fontsize=14)


#ax[3].plot(t_VSWR_Q1_l, VSWR_Q1_l, lw=2, label='VSWR Q1 - left')
#ax[3].plot(t_VSWR_Q1_r, VSWR_Q1_r, lw=2, label='VSWR Q1 - right')
#ax[3].plot(t_VSWR_Q4_l, VSWR_Q4_l, lw=2, label='VSWR Q4 - left')
#ax[3].plot(t_VSWR_Q4_r, VSWR_Q4_r, lw=2, label='VSWR Q4 - right')
ax[3].plot(t_VSWR_Q1_l[:,0], VSWR_Q1, lw=2, label=r'$\overline{VSWR}$ Q1', color='C0')
ax[3].plot(t_VSWR_Q4_l[:,0], VSWR_Q4, lw=2, label=r'$\overline{VSWR}$ Q4', color='C2')
ax[3].legend(fontsize=10)
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
fig.show()
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

ax.plot(_Rc_Q1, _VSWR_Q1, '.', alpha=0.6, label='Q1', color='C1')
ax.plot(_Rc_Q4, _VSWR_Q4, '.', alpha=0.6, label='Q4', color='C2')
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
file = f'../reflectometry/profiles/WEST_{pulse}_prof.mat'
data = loadmat(file)
t_ignitron = pw.tsmat(pulse, 'IGNITRON|1')

#%%
def time_averaged_profile(data, t_start, t_stop):
    idx_t_start = np.argmin(abs(data['tX'] - t_start -t_ignitron))
    idx_t_stop = np.argmin(abs(data['tX'] - t_stop -t_ignitron))
    
    ne_mean = np.mean(data['NEX'][:,idx_t_start:idx_t_stop], axis=1)
    ne_std = np.std(data['NEX'][:,idx_t_start:idx_t_stop], axis=1)
    r_mean = np.mean(data['RX'][:,idx_t_start:idx_t_stop], axis=1)
    r_std = np.std(data['RX'][:,idx_t_start:idx_t_stop], axis=1)

    return r_mean, r_std, ne_mean, ne_std

#%%
fig, ax = plt.subplots()

# before pellet
r, rs, ne, nes = time_averaged_profile(data, 6.4, 6.5)
ax.fill_betweenx(ne, r-rs, r+rs, alpha=.4)
ax.plot(r, ne, lw=2, label=f'3.6-3.7')

for (t_start, t_stop) in ts:
    # ne and r mean, error bar repr with std
    r, rs, ne, nes = time_averaged_profile(data, t_start, t_stop)
    
    ax.fill_betweenx(ne, r-rs, r+rs, alpha=.4)
    ax.plot(r, ne, lw=2, label=f'{t_start}-{t_stop}')
   
ax.legend()
ax.set_yscale('log')
ax.set_xlim((2.84, 2.98))
ax.grid(True)
ax.grid(True, which='minor', alpha=0.5)
ax.axvline(Rant_Q4, color='k')
ax.set_ylabel('Density [$m^{-3}$]', fontsize=12)
ax.set_xlabel('Radius [m]', fontsize=12)
ax.set_title(f'WEST #{pulse}')

#%%
fig.savefig(f'WEST_{pulse}_reflectometry_profiles.png', dpi=150)

#%%
### FW cut off density
from scipy.constants import c, epsilon_0, e, m_p
from astropy import units as u
from plasmapy.formulary.parameters import gyrofrequency
omega_0 = 2*np.pi*55.5e6
k_0 = omega_0 / c
k_parallel = 14  # m^-1
# Itor 1250 A, meaning 3.7T at R=2.5 m
R0 = 2.5
B0 = 3.7
omega_ci = gyrofrequency(B=R0/r*B0*u.T, particle='D', Z=2, signed=True).value 
# TODO : check cutoff density
nc_R = epsilon_0/e**2*1/(1/m_p/(omega_0 + omega_ci)/omega_0)*(k_parallel**2/k_0**2 - 1)
nc_L = epsilon_0/e**2*1/(1/m_p/(omega_0 - omega_ci)/omega_0)*(k_parallel**2/k_0**2 - 1)

#%% distance to cutoff vs time
idx_Rco = np.argmin(np.abs(data['NEX'] -  1e19), axis=0)  # (nb_t,)
d_co = 1e3*(Rant_Q4 - data['RX'][idx_Rco].diagonal()) # (nb_t,)
# Distance to Rext median vs time
d_Rext = (Rant_Q4*1e3 - Rext)

# difference between cutoff distance and distance to Rext: 
# lower values means strongest gradient
dd = np.interp(t_Rext, data['tX'].squeeze() - t_ignitron, d_co) - d_Rext

#%% Voltages and Currents
do_smooth=False

Q1_V1, Q1_V1_t = get_sig(pulse, signals['IC_Voltage_left_upper_Q1'], do_smooth=do_smooth)
Q1_V2, Q1_V2_t = get_sig(pulse, signals['IC_Voltage_left_lower_Q1'], do_smooth=do_smooth)
Q1_V3, Q1_V3_t = get_sig(pulse, signals['IC_Voltage_right_upper_Q1'], do_smooth=do_smooth)
Q1_V4, Q1_V4_t = get_sig(pulse, signals['IC_Voltage_right_lower_Q1'], do_smooth=do_smooth)

Q1_I1, Q1_I1_t = get_sig(pulse, signals['IC_Current_left_upper_Q1'], do_smooth=do_smooth)
Q1_I2, Q1_I2_t = get_sig(pulse, signals['IC_Current_left_lower_Q1'], do_smooth=do_smooth)
Q1_I3, Q1_I3_t = get_sig(pulse, signals['IC_Current_right_upper_Q1'], do_smooth=do_smooth)
Q1_I4, Q1_I4_t = get_sig(pulse, signals['IC_Current_right_lower_Q1'], do_smooth=do_smooth)

Q4_V1, Q4_V1_t = get_sig(pulse, signals['IC_Voltage_left_upper_Q4'], do_smooth=do_smooth)
Q4_V2, Q4_V2_t = get_sig(pulse, signals['IC_Voltage_left_lower_Q4'], do_smooth=do_smooth)
Q4_V3, Q4_V3_t = get_sig(pulse, signals['IC_Voltage_right_upper_Q4'], do_smooth=do_smooth)
Q4_V4, Q4_V4_t = get_sig(pulse, signals['IC_Voltage_right_lower_Q4'], do_smooth=do_smooth)

Q4_I1, Q4_I1_t = get_sig(pulse, signals['IC_Current_left_upper_Q4'], do_smooth=do_smooth)
Q4_I2, Q4_I2_t = get_sig(pulse, signals['IC_Current_left_lower_Q4'], do_smooth=do_smooth)
Q4_I3, Q4_I3_t = get_sig(pulse, signals['IC_Current_right_upper_Q4'], do_smooth=do_smooth)
Q4_I4, Q4_I4_t = get_sig(pulse, signals['IC_Current_right_lower_Q4'], do_smooth=do_smooth)


#%%
fig, ax = plt.subplots(5,1, sharex=True,  figsize=(6, 8))

ax[0].plot(t_Ip, Ip, lw=2)
ax[0].set_ylabel('Ip [kA]', fontsize=12, color='C0')
ax[0].tick_params(color='C0', labelcolor='C0')
ax[0].set_xlim(0, 11)
ax[0].set_title(f'WEST #{pulse}', fontsize=14)

ax0 = ax[0].twinx()
ax0.plot(t_nl, nl, lw=2, color='C1')
ax0.set_ylabel('nl [$10^{19}$ $m^{-3}$]', fontsize=12, color='C1')
ax0.tick_params(color='C1', labelcolor='C1')
ax0.set_ylim(2, 7.5)

Q1_V_max = np.max((Q1_V1,Q1_V2,Q1_V3,Q1_V4),axis=0)
Q1_V_min = np.min((Q1_V1,Q1_V2,Q1_V3,Q1_V4),axis=0)
Q4_V_max = np.max((Q4_V1,Q4_V2,Q4_V3,Q4_V4),axis=0)
Q4_V_min = np.min((Q4_V1,Q4_V2,Q4_V3,Q4_V4),axis=0)

ax[1].axhline(max_Vs[0], color='gray', alpha=0.8, ls='--')
ax[1].fill_between(Q1_V1_t, Q1_V_min, Q1_V_max, label='Q1 min/max', alpha=0.3, color='C0')
ax[1].fill_between(Q4_V1_t, Q4_V_min, Q4_V_max, label='Q4 min/max', alpha=0.3, color='C2')
ax[1].set_ylabel('Voltage [kV]', fontsize=12)
ax[1].set_ylim(10,30)
ax[1].legend(ncol=1, loc='upper left')

# ax[2].fill_between(t_Q4, (P_Q1+P_Q4)*1e-3, alpha=0.2, label='Total RF Power')
ax[2].plot(t_Q1, P_Q1*1e-3, label='IC Q1', lw=2, color='C0')
# ax[2].plot(t_Q2, P_Q2*1e-3, label='IC Q2', lw=2, color='C1')
ax[2].plot(t_Q4, P_Q4*1e-3, label='IC Q4', lw=2, color='C2')
ax[2].set_ylabel('RF Power [MW]', fontsize=12)
ax[2].legend(fontsize=10, loc='upper left', ncol=1)

ax[3].plot(t_Rc_Q1, Rc_Q1, label=r'$\overline{R}_c$ Q1', color='C0')
ax[3].plot(t_Rc_Q4, Rc_Q4, label=r'$\overline{R}_c$ Q4', color='C2')
ax[3].legend(fontsize=10, ncol=2)
ax[3].set_ylabel('Rc [$\Omega$]', fontsize=12)

# ax[4].plot(t_Rext, Rext, label='Rext median')
# ax[4].set_ylim(2910, 2970)
# ax[4].set_ylabel('R [mm]', fontsize=12)
# ax[4].legend(fontsize=10)

ax[4].plot(t_Rext, d_Rext, lw=2, label=r'$d_{\mathrm{R_{ex}}}$')
ax[4].plot(data['tX'].squeeze() - t_ignitron, smooth(d_co), lw=2, label=r'$d_{\mathrm{cutoff}}$')
ax[4].set_ylabel('Distance [mm]', fontsize=12)

ax[4].plot(t_Rext, smooth(dd), lw=2, label=r'$d_{\mathrm{cutoff}} -d_{\mathrm{R_{ex}}}$',
           color='gray')
#ax[5].legend(fontsize=10, ncol=2, loc='upper left')
ax[4].legend(fontsize=10, ncol=1, loc='upper left')
ax[4].set_ylim(-10, 50)



[a.grid(True, alpha=0.2) for a in ax]
[a.tick_params(labelsize=14) for a in ax]
ax[-1].set_xlabel('Time [s]', fontsize=14)


fig.tight_layout()
fig.subplots_adjust(hspace=0)
fig.show()

color='darkgray'
for idx, _ts in enumerate(ts):
    for axe in ax:
        axe.axvspan(_ts[0], _ts[1], color=color, alpha=0.2)

    
#%%
fig.savefig(f'WEST_{pulse}_distances.png', dpi=150)

