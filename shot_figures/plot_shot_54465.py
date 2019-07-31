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
pulse = 54565

P_tot, t_tot = get_sig(pulse, signals['IC_P_tot'])
P_Q1, t_Q1 = get_sig(pulse, signals['IC_P_Q1'])
#P_Q2, t_Q2 = get_sig(pulse, signals['IC_P_Q2'])
P_Q4, t_Q4 = get_sig(pulse, signals['IC_P_Q4'])

P_LH_tot, t_LH_tot = get_sig(pulse, signals['LH_P_tot'])
P_LH1, t_LH1 = get_sig(pulse, signals['LH_P_LH1'])
P_LH2, t_LH2 = get_sig(pulse, signals['LH_P_LH2'])


#%%
fig, ax = plt.subplots(2, 1, sharex=True)

ax[0].fill_between(t_LH_tot, 1e3*P_LH_tot.squeeze(), alpha=0.2, label='LH Total')
ax[0].plot(t_LH1, P_LH1, label='LH1', lw=2)
ax[0].plot(t_LH2, P_LH2, label='LH2', lw=2)


ax[1].fill_between(t_tot, P_tot.squeeze(), alpha=0.2, label='IC Total')
ax[1].plot(t_Q1, P_Q1, label='IC Q1', lw=2)
#ax[1].plot(t_Q2, P_Q2, label='IC Q2', lw=2)
ax[1].plot(t_Q4, P_Q4, label='IC Q4', lw=2)

ax[0].set_title(f'WEST #{pulse}', fontsize=14)
ax[1].set_xlabel('Time [s]', fontsize=14)

[a.set_ylabel('Coupled Power [kW]', fontsize=14) for a in ax]

ax[1].set_xlim(2.7, 11)
[a.grid(True, alpha=0.2) for a in ax]
[a.legend(fontsize=14) for a in ax]
[a.tick_params(labelsize=14) for a in ax]
fig.tight_layout()

#%%
savefig('WEST_IC_54565.png', dpi=150)