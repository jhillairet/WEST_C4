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
pulse = 54891

Ip, t_Ip = get_sig(pulse, signals['Ip'])
nl, t_nl = get_sig(pulse, signals['nl'])

P_IC_tot, t_tot = get_sig(pulse, signals['IC_P_tot'])
#P_Q1, t_Q1 = get_sig(pulse, signals['IC_P_Q1'])
#P_Q2, t_Q2 = get_sig(pulse, signals['IC_P_Q2'])
P_Q4, t_Q4 = get_sig(pulse, signals['IC_P_Q4'])

#P_LH_tot, t_LH_tot = get_sig(pulse, signals['LH_P_tot'])
#P_LH1, t_LH1 = get_sig(pulse, signals['LH_P_LH1'])
#P_LH2, t_LH2 = get_sig(pulse, signals['LH_P_LH2'])

#%%
# interpolate LH and IC power
#_P_LH_tot = np.interp(t_tot.squeeze(), t_LH_tot.squeeze(), P_LH_tot.squeeze())


#%% 
fig, ax = plt.subplots(2,1,sharex=True)
ax[0].plot(t_Ip, Ip, lw=2)
ax[1].plot(t_Q4, P_Q4, label='IC Q4', lw=2, color='C2')
ax2 = ax[0].twinx()
ax2.plot(t_nl, nl, lw=2, color='C1')

ax[1].set_xlabel('Time [s]', fontsize=14)
ax[0].set_ylabel('Ip [kA]', fontsize=14, color='C0')
ax2.set_ylabel('nl [$10^{19}$ $m^{-3}$]', fontsize=14, color='C1')
ax[1].set_ylabel('IC Power [kW]', fontsize=14)
ax[1].legend(('IC Q4',), fontsize=12)
[a.grid(True, alpha=0.2) for a in ax]
[a.tick_params(labelsize=14) for a in ax]
ax[0].tick_params(color='C0', labelcolor='C0')
ax2.tick_params(color='C1', labelcolor='C1')

ax[0].set_xlim(-0.1, 12.3)

ax[0].set_title(f'WEST #{pulse}', fontsize=14)
fig.tight_layout()

#%%
savefig('WEST_IC_54891.png', dpi=150)

