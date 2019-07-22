# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 10:52:25 2019

@author: JH218595
"""

#%%
from control_room import *
import matplotlib.pyplot as plt

#%%
pulse = 54455

#%%

P_Q2, t_P_Q2 = get_sig(pulse, signals['IC_P_Q2'])
P_Q4, t_P_Q4 = get_sig(pulse, signals['IC_P_Q4'])
Rc_Q2, t_Rc_Q2 = get_sig(pulse, signals['IC_Rc_Q2_avg'])
Rc_Q4, t_Rc_Q4 = get_sig(pulse, signals['IC_Rc_Q2_avg'])

#%%
fig, ax = plt.subplots()
ax.fill_between(t_P_Q2, np.squeeze(P_Q2 + P_Q4)/1e3, alpha=0.2, label='Total')
ax.plot(t_P_Q2, P_Q2/1e3, lw=2, label='Q2')
ax.plot(t_P_Q4, P_Q4/1e3, lw=2, label='Q4')
ax.set_xlabel('Time [s]', fontsize=14)
ax.set_ylabel('Transmitted Power [MW]', fontsize=14)
ax.set_xlim(3.9, 5.2)
ax.legend(fontsize=14, loc='upper left')
ax.set_title(f'WEST #{pulse}')
ax.tick_params(labelsize=12)
#%%
fig.savefig('WEST_54455_P_IC.png', dpi=150)
