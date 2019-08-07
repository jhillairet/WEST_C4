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
pulse = 54721

P_IC_tot, t_tot = get_sig(pulse, signals['IC_P_tot'])
P_Q1, t_Q1 = get_sig(pulse, signals['IC_P_Q1'])
P_Q2, t_Q2 = get_sig(pulse, signals['IC_P_Q2'])
P_Q4, t_Q4 = get_sig(pulse, signals['IC_P_Q4'])

P_LH_tot, t_LH_tot = get_sig(pulse, signals['LH_P_tot'])
P_LH1, t_LH1 = get_sig(pulse, signals['LH_P_LH1'])
P_LH2, t_LH2 = get_sig(pulse, signals['LH_P_LH2'])

#%%
# interpolate LH and IC power
_P_LH_tot = np.interp(t_tot.squeeze(), t_LH_tot.squeeze(), P_LH_tot.squeeze())


#%% 
fig, ax = plt.subplots()
ax.fill_between(t_tot, _P_LH_tot*1e3 + P_IC_tot.squeeze(), alpha=0.2, label='Total RF Power')
ax.plot(t_LH1, P_LH1, label='LH1', lw=2)
ax.plot(t_LH2, P_LH2, label='LH2', lw=2)
#ax.plot(t_Q1, P_Q1, label='IC Q1', lw=2)
#ax.plot(t_Q2, P_Q2, label='IC Q2', lw=2)
ax.plot(t_Q4, P_Q4, label='IC Q4', lw=2)

ax.set_xlim(2, 16)
ax.grid(True, alpha=0.2) 
ax.legend(fontsize=14, loc='upper left') 
ax.tick_params(labelsize=14) 
ax.set_title(f'WEST #{pulse}', fontsize=14)
ax.set_xlabel('Time [s]', fontsize=14)


fig.tight_layout()
#%%
savefig('WEST_IC_54721.png', dpi=150)

