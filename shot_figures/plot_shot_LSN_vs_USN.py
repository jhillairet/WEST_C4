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
#Plot the differences between USN and LSN plasma
# 700 kA
LSN = [55169]
USN = [55170, 55171, 55172]
# 500 kA
LSN = [55175]
USN = [55174]

USN = [54902]
LSN = [54903]

#%%
#pulses = [54903, 54902]
##%% General view and Gaz
#
#sig_general = [
##        signals['Ip'],
#        signals['nl'],
#        signals['Te1'],
#        signals['Prad'],
##        [signals['Neutron1'], signals['Neutron2']],
##        [signals['Rext_median']],
#        [signals['Dext_Q4']],
#        #signals['Zgeo'],
#        #signals['IC_P_tot'],#[signals['LH_P_LH1'], signals['LH_P_LH2']],
##        signals['LH_P_tot'],
#        signals['IC_P_tot'],
#        [signals['IC_P_Q1'], signals['IC_P_Q2'], signals['IC_P_Q4']],
##        [signals['IC_Rc_Q1_left'], signals['IC_Rc_Q2_left'], signals['IC_Rc_Q4_left']],
##        [signals['IC_Rc_Q1_right'], signals['IC_Rc_Q2_right'], signals['IC_Rc_Q4_right']],
#        [signals['IC_Rc_Q1_avg'], signals['IC_Rc_Q2_avg'], signals['IC_Rc_Q4_avg']],
##        [signals['Valve11'], ],
#        #[signals[f'IC_Vacuum_Q1_right'], signals[f'IC_Vacuum_Q2_right'], signals[f'IC_Vacuum_Q4_right'] ],
#        #signals['Cu'],
#        ]
#fig, axes = scope(pulses, sig_general, do_smooth=True, window_loc=(600,0), cycling_mode='ls')
##axes[-1].set_xlim(3.5, 6.5)
#axes[0].legend()
#
##%%
#Ip, t_Ip = get_sig(pulse, signals['Ip'])
#nl, t_nl = get_sig(pulse, signals['nl'])
#
#P_IC_tot, t_tot = get_sig(pulse, signals['IC_P_tot'])
#P_Q1, t_Q1 = get_sig(pulse, signals['IC_P_Q1'])
#P_Q2, t_Q2 = get_sig(pulse, signals['IC_P_Q2'])
#P_Q4, t_Q4 = get_sig(pulse, signals['IC_P_Q4'])
#
##%%
#Rc_Q1_left, t_Rc_Q1_left = get_sig(pulse, signals['IC_Rc_Q1_left'])
#Rc_Q1_right, t_Rc_Q1_right = get_sig(pulse, signals['IC_Rc_Q1_right'])
#
#Rc_Q2_left, t_Rc_Q2_left = get_sig(pulse, signals['IC_Rc_Q2_left'])
#Rc_Q2_right, t_Rc_Q2_right = get_sig(pulse, signals['IC_Rc_Q2_right'])
#
#Rc_Q4_left, t_Rc_Q4_left = get_sig(pulse, signals['IC_Rc_Q4_left'])
#Rc_Q4_right, t_Rc_Q4_right = get_sig(pulse, signals['IC_Rc_Q4_right'])
#
#Rc_Q1, t_Rc_Q1 = get_sig(pulse, signals['IC_Rc_Q1_avg'])
#Rc_Q2, t_Rc_Q2 = get_sig(pulse, signals['IC_Rc_Q2_avg'])
#Rc_Q4, t_Rc_Q4 = get_sig(pulse, signals['IC_Rc_Q4_avg'])
#
#R_IC, t_R_IC = get_sig(pulse, signals['IC_Positions'])
#Rext, t_Rext = get_sig(pulse, signals['Rext_median'])
#
##%%
### interpolate LH and IC power
##P_LH_tot, t_LH_tot = get_sig(pulse, signals['LH_P_tot'])
##_P_LH_tot = np.interp(t_tot.squeeze(), t_LH_tot.squeeze(), P_LH_tot.squeeze())
#
#
##%% 
#fig, ax = plt.subplots(2,1,sharex=True)
#ax[0].plot(t_Ip, Ip, lw=2)
#ax[1].fill_between(t_Q4, np.squeeze(P_Q1+P_Q2+P_Q4), alpha=0.2, label='Total RF Power')
##ax[1].plot(t_LH, P_LH_tot, label='LH', lw=2, color='C0')
#ax[1].plot(t_Q1, P_Q1, label='IC Q1', lw=2, color='C0')
#ax[1].plot(t_Q2, P_Q2, label='IC Q2', lw=2, color='C1')
#ax[1].plot(t_Q4, P_Q4, label='IC Q4', lw=2, color='C2')
#
#
#ax2 = ax[0].twinx()
#ax2.plot(t_nl, nl, lw=2, color='C1')
#
#ax[1].set_xlabel('Time [s]', fontsize=14)
#ax[0].set_ylabel('Ip [kA]', fontsize=14, color='C0')
#ax2.set_ylabel('nl [$10^{19}$ $m^{-3}$]', fontsize=14, color='C1')
#ax[1].set_ylabel('IC Power [kW]', fontsize=14)
#ax[1].set_ylim(0, 4300)
#
#ax[1].legend(fontsize=12, loc='upper left')
#[a.grid(True, alpha=0.2) for a in ax]
#[a.tick_params(labelsize=14) for a in ax]
#ax[0].tick_params(color='C0', labelcolor='C0')
#ax2.tick_params(color='C1', labelcolor='C1')
#
#ax[0].set_xlim(-0.1, 16)
#
#ax[0].set_title(f'WEST #{pulse}', fontsize=14)
#fig.tight_layout()
#
##%%
#savefig(f'WEST_IC_{pulse}.png', dpi=150)
#






#%%
#%%
# reflectometry timings for average
ts = [(2.9, 3.0),  # before IC
      (3.2, 3.3),  # IC ramp up
      (4.3, 4.4),  # IC plateau
      ]

#%%
pulse = 54902
data = loadmat(f'../reflectometry/profiles/WEST_{pulse}_prof.mat')

Ip, t_Ip = get_sig(pulse, signals['Ip'])
nl, t_nl = get_sig(pulse, signals['nl'])

P_Q1, t_Q1 = get_sig(pulse, signals['IC_P_Q1'])
P_Q2, t_Q2 = get_sig(pulse, signals['IC_P_Q2'])
P_Q4, t_Q4 = get_sig(pulse, signals['IC_P_Q4'])

Rc_Q1, t_Rc_Q1 = get_sig(pulse, signals['IC_Rc_Q1_avg'])
Rc_Q2, t_Rc_Q2 = get_sig(pulse, signals['IC_Rc_Q2_avg'])
Rc_Q4, t_Rc_Q4 = get_sig(pulse, signals['IC_Rc_Q4_avg'])

R_IC, t_R_IC = get_sig(pulse, signals['IC_Positions'])
Rext, t_Rext = get_sig(pulse, signals['Rext_median'])

#%%
# plot R(nco) vs time
nco = 1e19
Rant = R_IC[2]
idx_nco = np.argmin(abs(data['NEX'] - 1e19), axis=0)

Dext = Rant*1e3 - Rext

Dco = (Rant - data['RX'][idx_nco][0] )* 1e3
        

#%%
fig, ax = plt.subplots(4,1,sharex=True)
ax[0].plot(t_Ip, Ip, lw=2)
ax[1].fill_between(t_Q4, np.squeeze(P_Q1+P_Q2+P_Q4), alpha=0.2, label='Total RF Power')
ax[1].plot(t_Q1, P_Q1, label='IC Q1', lw=2, color='C0')
ax[1].plot(t_Q2, P_Q2, label='IC Q2', lw=2, color='C1')
ax[1].plot(t_Q4, P_Q4, label='IC Q4', lw=2, color='C2')

ax[2].plot(t_Rc_Q1, Rc_Q1, label='IC Q1', lw=2, color='C0')
ax[2].plot(t_Rc_Q2, Rc_Q2, label='IC Q2', lw=2, color='C1')
ax[2].plot(t_Rc_Q4, Rc_Q4, label='IC Q4', lw=2, color='C2')
ax[2].set_ylabel('Rc [Ohm]', fontsize=14)
ax[2].set_ylim(0,2)

ax2 = ax[0].twinx()
ax2.plot(t_nl, nl, lw=2, color='C1')


ax[0].set_ylabel('Ip [kA]', fontsize=14, color='C0')
ax2.set_ylabel('nl [$10^{19}$ $m^{-3}$]', fontsize=14, color='C1')
ax[1].set_ylabel('IC Power [kW]', fontsize=14)
ax[1].legend(fontsize=12, loc='upper left')
[a.grid(True, alpha=0.2) for a in ax]
[a.tick_params(labelsize=14) for a in ax]
ax[0].tick_params(color='C0', labelcolor='C0')
ax2.tick_params(color='C1', labelcolor='C1')

ax[0].set_xlim(-0.1, 13.3)

ax[0].set_title(f'WEST #{pulse}', fontsize=14)
fig.tight_layout()

# Max allowable power

ax[3].plot(data['tX'].squeeze() - 32, Dco, label='Dco [mm]')
ax[3].plot(t_Rext, Dext, label='Dext [mm]')

ax[3].set_xlabel('Time [s]', fontsize=14)
ax[3].legend()
ax[3].set_ylim(0, 75)
fig.tight_layout()
fig.subplots_adjust(hspace=0)

#%%
savefig(f'WEST_IC_{pulse}_Dco.png', dpi=150)


#%%#####################
pulse = 54903
data = loadmat(f'../reflectometry/profiles/WEST_{pulse}_prof.mat')

Ip, t_Ip = get_sig(pulse, signals['Ip'])
nl, t_nl = get_sig(pulse, signals['nl'])

P_Q1, t_Q1 = get_sig(pulse, signals['IC_P_Q1'])
P_Q2, t_Q2 = get_sig(pulse, signals['IC_P_Q2'])
P_Q4, t_Q4 = get_sig(pulse, signals['IC_P_Q4'])

Rc_Q1, t_Rc_Q1 = get_sig(pulse, signals['IC_Rc_Q1_avg'])
Rc_Q2, t_Rc_Q2 = get_sig(pulse, signals['IC_Rc_Q2_avg'])
Rc_Q4, t_Rc_Q4 = get_sig(pulse, signals['IC_Rc_Q4_avg'])

R_IC, t_R_IC = get_sig(pulse, signals['IC_Positions'])
Rext, t_Rext = get_sig(pulse, signals['Rext_median'])

#%%
# plot R(nco) vs time
nco = 1e19
Rant = R_IC[2]
idx_nco = np.argmin(abs(data['NEX'] - 1e19), axis=0)

Dext = Rant*1e3 - Rext

Dco = (Rant - data['RX'][idx_nco][0] )* 1e3

#%%
fig, ax = plt.subplots(4,1,sharex=True)
ax[0].plot(t_Ip, Ip, lw=2)
ax[1].fill_between(t_Q4, np.squeeze(P_Q1+P_Q2+P_Q4), alpha=0.2, label='Total RF Power')
ax[1].plot(t_Q1, P_Q1, label='IC Q1', lw=2, color='C0')
ax[1].plot(t_Q2, P_Q2, label='IC Q2', lw=2, color='C1')
ax[1].plot(t_Q4, P_Q4, label='IC Q4', lw=2, color='C2')

ax[2].plot(t_Rc_Q1, Rc_Q1, label='IC Q1', lw=2, color='C0')
ax[2].plot(t_Rc_Q2, Rc_Q2, label='IC Q2', lw=2, color='C1')
ax[2].plot(t_Rc_Q4, Rc_Q4, label='IC Q4', lw=2, color='C2')
ax[2].set_ylabel('Rc [Ohm]', fontsize=14)
ax[2].set_ylim(0,2)
ax2 = ax[0].twinx()
ax2.plot(t_nl, nl, lw=2, color='C1')


ax[0].set_ylabel('Ip [kA]', fontsize=14, color='C0')
ax2.set_ylabel('nl [$10^{19}$ $m^{-3}$]', fontsize=14, color='C1')
ax[1].set_ylabel('IC Power [kW]', fontsize=14)
ax[1].legend(fontsize=12, loc='upper left')
[a.grid(True, alpha=0.2) for a in ax]
[a.tick_params(labelsize=14) for a in ax]
ax[0].tick_params(color='C0', labelcolor='C0')
ax2.tick_params(color='C1', labelcolor='C1')

ax[0].set_xlim(-0.1, 13.3)

ax[0].set_title(f'WEST #{pulse}', fontsize=14)
fig.tight_layout()

# Max allowable power

ax[3].plot(data['tX'].squeeze() - 32, Dco, label='Dco [mm]')
ax[3].plot(t_Rext, Dext, label='Dext [mm]')

ax[3].set_xlabel('Time [s]', fontsize=14)
ax[3].legend()
ax[3].set_ylim(0, 75)
fig.tight_layout()
fig.subplots_adjust(hspace=0)

#%%
savefig(f'WEST_IC_{pulse}_Dco.png', dpi=150)

#%%
#Compare Rext and cut off distances
USN = 54902
LSN = 54903
Rext_USN, t_Rext_USN = get_sig(USN, signals['Rext_median'])
Rext_LSN, t_Rext_LSN = get_sig(LSN, signals['Rext_median'])

R_IC_USN, t_R_IC_USN = get_sig(USN, signals['IC_Positions'])
R_IC_LSN, t_R_IC_LSN = get_sig(LSN, signals['IC_Positions'])

P_Q1_LSN, t_Q1_LSN = get_sig(LSN, signals['IC_P_Q1'])
P_Q2_LSN, t_Q2_LSN = get_sig(LSN, signals['IC_P_Q2'])
P_Q4_LSN, t_Q4_LSN = get_sig(LSN, signals['IC_P_Q4'])
P_Q1_USN, t_Q1_USN = get_sig(USN, signals['IC_P_Q1'])
P_Q2_USN, t_Q2_USN = get_sig(USN, signals['IC_P_Q2'])
P_Q4_USN, t_Q4_USN = get_sig(USN, signals['IC_P_Q4'])

data_USN = loadmat(f'../reflectometry/profiles/WEST_{USN}_prof.mat')
data_LSN = loadmat(f'../reflectometry/profiles/WEST_{LSN}_prof.mat')

Rc_Q1_LSN, t_Rc_Q1_LSN = get_sig(LSN, signals['IC_Rc_Q1_avg'])
Rc_Q2_LSN, t_Rc_Q2_LSN = get_sig(LSN, signals['IC_Rc_Q2_avg'])
Rc_Q4_LSN, t_Rc_Q4_LSN = get_sig(LSN, signals['IC_Rc_Q4_avg'])
Rc_Q1_USN, t_Rc_Q1_USN = get_sig(USN, signals['IC_Rc_Q1_avg'])
Rc_Q2_USN, t_Rc_Q2_USN = get_sig(USN, signals['IC_Rc_Q2_avg'])
Rc_Q4_USN, t_Rc_Q4_USN = get_sig(USN, signals['IC_Rc_Q4_avg'])

#%% clean Rc data and get max
Rc_Q1_LSN[P_Q1_LSN < 1] = 0
Rc_Q2_LSN[P_Q2_LSN < 1] = 0
Rc_Q4_LSN[P_Q4_LSN < 1] = 0
Rc_Q1_USN[P_Q1_USN < 1] = 0
Rc_Q2_USN[P_Q2_USN < 1] = 0
Rc_Q4_USN[P_Q4_USN < 1] = 0


Rc_max_LSN = np.max([Rc_Q1_LSN, Rc_Q2_LSN, Rc_Q4_LSN], axis=0)
Rc_max_USN = np.max([Rc_Q1_USN, Rc_Q2_USN, Rc_Q4_USN], axis=0)

#%%
nco = 1e19
Rant_USN = R_IC_USN[2]
Rant_LSN = R_IC_LSN[2]

idx_nco_USN = np.argmin(abs(data_USN['NEX'] - nco), axis=0)
idx_nco_LSN = np.argmin(abs(data_LSN['NEX'] - nco), axis=0)

Dext_USN = Rant_USN*1e3 - Rext_USN
Dext_LSN = Rant_LSN*1e3 - Rext_LSN

Dco_USN = (Rant_USN - data_USN['RX'][idx_nco_USN][0] )* 1e3
Dco_LSN = (Rant_LSN - data_LSN['RX'][idx_nco_LSN][0] )* 1e3

#%%
fig, ax = plt.subplots(3, 1, sharex=True, figsize=(6,8))
# ax[0].plot(t_Q4_LSN, np.squeeze(P_Q1_LSN+P_Q2_LSN+P_Q4_LSN), label=f'LSN')
# ax[0].plot(t_Q4_USN, np.squeeze(P_Q1_USN+P_Q2_USN+P_Q4_USN), label=f'USN')
# ax[0].set_ylabel('IC Coupled Power [kW]', fontsize=10)
# ax[0].legend(loc=3)
ax[0].plot(t_Rc_Q1_LSN, Rc_max_LSN, label='LSN')
ax[0].plot(t_Rc_Q1_USN, Rc_max_USN, label='USN')
ax[0].set_ylabel('Max Rc ($\Omega$]', fontsize=12)


ax[1].plot(t_Rext_LSN, Dext_LSN, lw=2, label=f'LSN')
ax[1].plot(t_Rext_USN, Dext_USN, lw=2, label=f'USN')
ax[1].set_ylabel('Dist. to Rext [mm]', fontsize=10)
ax[1].set_ylim(0, 34)

ax[2].plot(data_LSN['tX'].squeeze() - 32, Dco_LSN, color='C0', alpha=0.2)
ax[2].plot(data_LSN['tX'].squeeze() - 32, smooth(Dco_LSN), color='C0', label='LSN')

ax[2].plot(data_USN['tX'].squeeze() - 32, Dco_USN, color='C1', alpha=0.2)
ax[2].plot(data_USN['tX'].squeeze() - 32, smooth(Dco_USN), color='C1', label='USN')

ax[2].set_ylabel('Cutoff Dist. [mm]', fontsize=10)
ax[2].set_xlim(5.7, 9.7)
ax[2].set_ylim(0, 100)
ax[2].set_xlabel('Time [s]', fontsize=12)

[a.legend() for a in ax]
fig.suptitle(f'WEST #{LSN}(LSN) vs #{USN}(USN)')
fig.tight_layout()
fig.subplots_adjust(hspace=0)
#%%
fig.savefig(f'WEST_IC_{LSN}_vs_{USN}_Rext_Dco.png', dpi=150)

