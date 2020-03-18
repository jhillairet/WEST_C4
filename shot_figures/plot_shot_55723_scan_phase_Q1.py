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


#%%  Q1 scan phase
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 55222
pulse = 55723

Ip, t_Ip = get_sig(pulse, signals['Ip'])
nl, t_nl = get_sig(pulse, signals['nl'])

P_IC_tot, t_tot = get_sig(pulse, signals['IC_P_tot'])
P_Q1, t_Q1 = get_sig(pulse, signals['IC_P_Q1'])
P_Q2, t_Q2 = get_sig(pulse, signals['IC_P_Q2'])
P_Q4, t_Q4 = get_sig(pulse, signals['IC_P_Q4'])

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
Prad_bulk, t_Prad_bulk = get_sig(pulse, signals['Prad_bulk'])

#%%
phaseQ1, t_phaseQ1 = get_sig(pulse, signals['IC_delta_phi_toro_Q1_Bot_LmR'], do_smooth=True) 
# phaseQ2, t_phaseQ2 = get_sig(pulse, signals['IC_delta_phi_toro_Q2_Top_LmR'], do_smooth=True) 
# phaseQ4, t_phaseQ4 = get_sig(pulse, signals['IC_delta_phi_toro_Q4_Top_LmR'], do_smooth=True)


#%% 
fig, ax = plt.subplots(3, 1, sharex=True)
ax[0].plot(t_Ip, Ip, lw=2)
ax2 = ax[0].twinx()
ax[0].set_ylabel('Ip [kA]', fontsize=14, color='C0')
ax[0].tick_params(color='C0', labelcolor='C0')
ax[0].set_xlim(-0.1, 9)
ax[0].set_title(f'WEST #{pulse}', fontsize=14)

ax2.plot(t_nl, nl, lw=2, color='C1')
ax2.set_ylabel('nl [$10^{19}$ $m^{-3}$]', fontsize=14, color='C1')
ax2.tick_params(color='C1', labelcolor='C1')

ax[1].plot(t_Q1, P_Q1, label='IC Q1', lw=2, color='C0')
# ax[1].plot(t_Q4, P_Q4, label='IC Q4', lw=2, color='C2')
ax[1].plot(t_Prad, Prad*1e3, label='Prad (tot)')
ax[1].plot(t_Prad_bulk, Prad_bulk*1e3, label='Prad (bulk)')

ax[1].set_ylim(0, 1300)
ax[1].set_xlabel('Time [s]', fontsize=14)
ax[1].set_ylabel('Power [kW]', fontsize=14)
ax[1].legend(fontsize=12, loc='upper left')

ax[2].plot(t_Rc_Q1, Rc_Q1, label='Rc Q1', lw=2, color='C2')
ax[2].set_ylabel('Rc [Ohm]', fontsize=14)
_ax = ax[2].twinx()
_ax.plot(t_phaseQ1, phaseQ1, lw=2, color='C1', label='Phase Q1')
# _ax.plot(t_phaseQ4, phaseQ4, lw=2, color='C4', label='Phase Q4')

_ax.set_ylabel('Tor.Phase [deg]', fontsize=14, color='C1')
_ax.tick_params(color='C1', labelcolor='C1')
_ax.set_ylim(0, 360)
[a.grid(True, alpha=0.2) for a in ax]
[a.tick_params(labelsize=14) for a in ax]

fig.tight_layout()

#%%
savefig(f'WEST_IC_{pulse}.png', dpi=150)

#%%
# 
ts = (4.68, 7.63)  # 55723

_ph, _t = in_between(phaseQ1, t_phaseQ1, t_start=ts[0], t_end=ts[1])
_p, _t_p = in_between(P_Q1, t_Q1, t_start=ts[0], t_end=ts[1])
_prad, _t_prad = in_between(Prad_bulk*1e3, t_Prad_bulk, t_start=ts[0], t_end=ts[1])

_prad = np.interp(_t, _t_prad, _prad.squeeze())
_p = np.interp(_t, _t_p, _p.squeeze())

fig, ax = plt.subplots()
ax.plot(_ph, _prad/_p, '.')
ax.grid(True)
ax.set_xlabel('Phase [deg]', fontsize=14)
ax.set_ylabel('Prad (bulk) / P_RF', fontsize=14)
ax.set_title(f'WEST #{pulse} - Q1', fontsize=14)

#%%
savefig(f'WEST_IC_{pulse}_Prad_vs_phase.png', dpi=150)


