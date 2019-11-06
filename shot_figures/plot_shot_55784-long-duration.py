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
pulse = 55784

#%%
Ip, t_Ip = get_sig(pulse, signals['Ip'])
nl, t_nl = get_sig(pulse, signals['nl'])
Vloop, t_Vloop = get_sig(pulse, signals['Vloop'], do_smooth=True)

Prad, trad = get_sig(pulse, signals['Prad'])
# Psep, tsep = get_sig(pulse, signals['Separatrix_P'])

#%%
Te, t_Te = get_sig(pulse, signals['Te1'])

#%%
## interpolate LH and IC power
# P_LH_tot, t_LH_tot = get_sig(pulse, signals['LH_P_tot'])
P_LH1, t_LH1 = get_sig(pulse, signals['LH_P_LH1'])
P_LH2, t_LH2 = get_sig(pulse, signals['LH_P_LH2'])

#%%
fig, ax = plt.subplots(3,1,sharex=True,  figsize=(10, 8.5))
ax[0].plot(t_Ip, Ip, lw=2)
ax[0].set_ylabel('Ip [kA]', fontsize=14, color='C0')
ax[0].tick_params(color='C0', labelcolor='C0')
ax[0].set_xlim(-0.1, 50)
ax[0].set_title(f'WEST #{pulse} - Preliminary', fontsize=14)

ax0 = ax[0].twinx()
ax0.plot(t_nl, nl, lw=2, color='C1')
ax0.set_ylabel('nl [$10^{19}$ $m^{-3}$]', fontsize=14, color='C1')
ax0.tick_params(color='C1', labelcolor='C1')

ax[1].fill_between(t_LH1, P_LH1+P_LH2, alpha=0.2, label='Total')
ax[1].plot(t_LH1, P_LH1, label='LH1', lw=2, color='C1')
ax[1].plot(t_LH2, P_LH2, label='LH2', lw=2, color='C2')
ax[1].set_ylabel('RF Power [MW]', fontsize=14)
ax[1].legend(fontsize=12, loc='upper left', ncol=1)

ax[2].plot(trad, Prad, lw=2, label='Radiated (total)')
# ax[2].plot(tsep, Psep, lw=2, label='Separatrix')

ax[2].set_ylim(0, 5)
ax[2].set_ylabel('Power [MW]', fontsize=14)
ax[2].legend(fontsize=12, loc='upper left')

ax2 = ax[2].twinx()
ax2.plot(t_Vloop, Vloop, lw=2, color='C2', alpha=0.5)
ax2.set_ylabel('Vloop [V]', fontsize=14, color='C2')
ax2.tick_params(color='C2', labelcolor='C2')
ax2.set_ylim(0, 1)

[a.grid(True, alpha=0.2) for a in ax]
[a.tick_params(labelsize=14) for a in ax]
ax[-1].set_xlabel('Time [s]', fontsize=14)

fig.tight_layout()

#%%
fig.savefig(f'WEST_LH_{pulse}_prelim.png', dpi=150)




