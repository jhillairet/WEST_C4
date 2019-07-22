# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 10:52:25 2019

@author: JH218595
"""

#%%
from control_room import *
import matplotlib.pyplot as plt

#%%
pulse = 54413

#%%
P_Q1, t_P_Q1 = get_sig(pulse, signals['IC_P_Q1'])
P_Q2, t_P_Q2 = get_sig(pulse, signals['IC_P_Q2'])
P_Q4, t_P_Q4 = get_sig(pulse, signals['IC_P_Q4'])
# Rc_Q2, t_Rc_Q2 = get_sig(pulse, signals['IC_Rc_Q2_avg'])
# Rc_Q4, t_Rc_Q4 = get_sig(pulse, signals['IC_Rc_Q2_avg'])
#%%
P_LH1, t_P_LH1 = get_sig(pulse, signals['LH_P_LH1'])
P_LH2, t_P_LH2 = get_sig(pulse, signals['LH_P_LH2'])

#%%
fig, ax = plt.subplots()
#ax.fill_between(t_P_Q2, np.squeeze(P_Q2 + P_Q4)/1e3, alpha=0.2, label='Total')

ax.plot(t_P_LH1, P_LH1, lw=2, label='LH1', c='C0')
ax.plot(t_P_LH2, P_LH2, lw=2, label='LH2', c='g')

ax.plot(t_P_Q1, P_Q1, lw=2, color='r', label="Q1")
ax.plot(t_P_Q2, P_Q2, lw=2, color='gold', label='Q2')
ax.plot(t_P_Q4, P_Q4, lw=2, color='salmon', label='Q4')
ax.set_xlabel('Time [s]', fontsize=14)
ax.set_ylabel('Coupled Power [kW]', fontsize=14)
ax.set_xlim(2, 14)
ax.legend(fontsize=14, loc='upper left')
ax.set_title(f'WEST #{pulse}')
ax.tick_params(labelsize=12)
ax.grid(True, alpha=.5)


#%%
fig.savefig('WEST_54413_P_IC_LH.png', dpi=150)
