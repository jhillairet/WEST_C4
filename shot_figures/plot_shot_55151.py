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
pulse = 55151

Ip, t_Ip = get_sig(pulse, signals['Ip'])
nl, t_nl = get_sig(pulse, signals['nl'])

P_IC_tot, t_tot = get_sig(pulse, signals['IC_P_tot'])
P_Q1, t_Q1 = get_sig(pulse, signals['IC_P_Q1'])
P_Q2, t_Q2 = get_sig(pulse, signals['IC_P_Q2'])
P_Q4, t_Q4 = get_sig(pulse, signals['IC_P_Q4'])

P_tot = np.squeeze(P_Q1 + P_Q2 + P_Q4)

#%%
Rc_Q1_left, t_Rc_Q1_left = get_sig(pulse, signals['IC_Rc_Q1_left'])
Rc_Q1_right, t_Rc_Q1_right = get_sig(pulse, signals['IC_Rc_Q1_right'])

Rc_Q2_left, t_Rc_Q2_left = get_sig(pulse, signals['IC_Rc_Q2_left'])
Rc_Q2_right, t_Rc_Q2_right = get_sig(pulse, signals['IC_Rc_Q2_right'])

Rc_Q4_left, t_Rc_Q4_left = get_sig(pulse, signals['IC_Rc_Q4_left'])
Rc_Q4_right, t_Rc_Q4_right = get_sig(pulse, signals['IC_Rc_Q4_right'])

Rc_Q1, t_Rc_Q1 = get_sig(pulse, signals['IC_Rc_Q1_avg'])
Rc_Q2, t_Rc_Q2 = get_sig(pulse, signals['IC_Rc_Q2_avg'])
Rc_Q4, t_Rc_Q4 = get_sig(pulse, signals['IC_Rc_Q4_avg'])

R_IC, t_R_IC = get_sig(pulse, signals['IC_Positions'])
Rext, t_Rext = get_sig(pulse, signals['Rext_median'])

Prad, t_Prad = get_sig(pulse, signals['Prad'])
Prad_b, t_Prad_b = get_sig(pulse, signals['Prad_bulk'])
_Prad = np.interp(t_Q1, t_Prad, Prad*1e3)


phaseQ1, t_phaseQ1 = get_sig(pulse, signals['IC_delta_phi_toro_Q1_Bot_LmR'])
phaseQ2, t_phaseQ2 = get_sig(pulse, signals['IC_delta_phi_toro_Q2_Top_LmR']) 
phaseQ4, t_phaseQ4 = get_sig(pulse, signals['IC_delta_phi_toro_Q4_Top_LmR'])
        
#%%
## interpolate LH and IC power
#P_LH_tot, t_LH_tot = get_sig(pulse, signals['LH_P_tot'])
#_P_LH_tot = np.interp(t_tot.squeeze(), t_LH_tot.squeeze(), P_LH_tot.squeeze())


#%% 
fig, ax = plt.subplots(2,1,sharex=True)
ax[0].plot(t_Ip, Ip, lw=2)
ax[1].fill_between(t_Q4, np.squeeze(P_Q1+P_Q2+P_Q4), alpha=0.2, label='Total RF Power')
#ax[1].plot(t_LH, P_LH_tot, label='LH', lw=2, color='C0')
ax[1].plot(t_Q1, P_Q1, label='IC Q1', lw=2, color='C0')
ax[1].plot(t_Q2, P_Q2, label='IC Q2', lw=2, color='C1')
ax[1].plot(t_Q4, P_Q4, label='IC Q4', lw=2, color='C2')


ax2 = ax[0].twinx()
ax2.plot(t_nl, nl, lw=2, color='C1')

ax[1].set_xlabel('Time [s]', fontsize=14)
ax[0].set_ylabel('Ip [kA]', fontsize=14, color='C0')
ax2.set_ylabel('nl [$10^{19}$ $m^{-3}$]', fontsize=14, color='C1')
ax[1].set_ylabel('IC Power [kW]', fontsize=14)
ax[1].set_ylim(0, 4300)

ax[1].legend(fontsize=12, loc='upper left')
[a.grid(True, alpha=0.2) for a in ax]
[a.tick_params(labelsize=14) for a in ax]
ax[0].tick_params(color='C0', labelcolor='C0')
ax2.tick_params(color='C1', labelcolor='C1')

ax[0].set_xlim(-0.1, 16)

ax[0].set_title(f'WEST #{pulse}', fontsize=14)
fig.tight_layout()

#%%
savefig(f'WEST_IC_{pulse}.png', dpi=150)


#%%
fig, ax = plt.subplots(4,1,sharex=True)
ax[0].plot(t_Ip, Ip, lw=2)
ax[1].fill_between(t_Q4, np.squeeze(P_Q1+P_Q2+P_Q4), alpha=0.2, label='Total RF Power')
#ax[1].plot(t_LH, P_LH_tot, label='LH', lw=2, color='C0')
ax[1].plot(t_Q1, P_Q1, label='IC Q1', lw=2, color='C0')
ax[1].plot(t_Q2, P_Q2, label='IC Q2', lw=2, color='C1')
ax[1].plot(t_Q4, P_Q4, label='IC Q4', lw=2, color='C2')

ax[2].plot(t_phaseQ1, phaseQ1, label='Q1', lw=2, color='C0')
ax[2].plot(t_phaseQ2, phaseQ2, label='Q2', lw=2, color='C1')
ax[2].plot(t_phaseQ4, phaseQ4, label='Q4', lw=2, color='C2')
ax[2].set_ylabel('Toroidal phase [deg]', fontsize=12)
ax[3].plot(t_Prad, Prad, label='Prad', lw=2)
#ax[3].plot(t_Prad_b, Prad_b, label='Prad', lw=2)
ax[3].set_ylabel('Radiated Power (bulk) [MW]', fontsize=12)
#ax[3].plot(t_Q1, _Prad/P_tot, label='Prad/Ptot', lw=2)
#ax[3].set_ylim(0, 2)


ax2 = ax[0].twinx()
ax2.plot(t_nl, nl, lw=2, color='C1')

ax[3].set_xlabel('Time [s]', fontsize=14)
ax[0].set_ylabel('Ip [kA]', fontsize=14, color='C0')
ax2.set_ylabel('nl [$10^{19}$ $m^{-3}$]', fontsize=14, color='C1')
ax[1].set_ylabel('IC Power [kW]', fontsize=14)
ax[1].set_ylim(0, 4300)

ax[1].legend(fontsize=12, loc='upper left')
[a.grid(True, alpha=0.2) for a in ax]
[a.tick_params(labelsize=14) for a in ax]
ax[0].tick_params(color='C0', labelcolor='C0')
ax2.tick_params(color='C1', labelcolor='C1')

ax[0].set_xlim(-0.1, 16)

ax[0].set_title(f'WEST #{pulse}', fontsize=14)
fig.tight_layout()