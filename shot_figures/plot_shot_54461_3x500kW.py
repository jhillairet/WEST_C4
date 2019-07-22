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
pulse = 54461

P_tot, t_tot = get_sig(pulse, signals['IC_P_tot'])
P_Q1, t_Q1 = get_sig(pulse, signals['IC_P_Q1'])
P_Q2, t_Q2 = get_sig(pulse, signals['IC_P_Q2'])
P_Q4, t_Q4 = get_sig(pulse, signals['IC_P_Q4'])

RC_Q1, t_RC_Q1 = get_sig(pulse, signals['IC_Rc_Q1_avg'])
RC_Q2, t_RC_Q2 = get_sig(pulse, signals['IC_Rc_Q2_avg'])
RC_Q4, t_RC_Q4 = get_sig(pulse, signals['IC_Rc_Q4_avg'])

#%%
fig, ax = subplots(2, 1, sharex=True)
ax[0].fill_between(t_tot, P_tot.squeeze(), alpha=0.2, label='IC Total')
ax[0].plot(t_Q1, P_Q1, label='IC Q1', lw=2)
ax[0].plot(t_Q2, P_Q2, label='IC Q2', lw=2)
ax[0].plot(t_Q4, P_Q4, label='IC Q4', lw=2)

ax[0].set_title(f'WEST #{pulse}', fontsize=14)

ax[0].set_ylabel('Coupled Power \n [kW]', fontsize=12)
ax[0].set_ylim(0, 2e3)

ax[0].legend(fontsize=12)

ax[1].plot(t_RC_Q1, RC_Q1, label='IC Q1', lw=2)
ax[1].plot(t_RC_Q2, RC_Q2, label='IC Q2', lw=2)
ax[1].plot(t_RC_Q4, RC_Q4, label='IC Q4', lw=2)
ax[1].set_ylabel('Coupling Resistance \n [$\Omega$]', fontsize=12)
ax[1].legend(fontsize=12)


[a.grid(True, alpha=0.2) for a in ax]
ax[0].set_xlim(3, 4.2)
ax[1].set_xlabel('Time [s]', fontsize=12)
fig.subplots_adjust(hspace=0.1)

[a.tick_params(labelsize=14) for a in ax]
fig.tight_layout()

#%%
fig.savefig('WEST_IC_54461_Power_Rc.png', dpi=150)


#%%
V_left_max_Q2, t_V_left_max_Q2 = get_sig(pulse, signals['IC_Voltage_left_max_Q2'])
V_right_max_Q2, t_V_right_max_Q2 = get_sig(pulse, signals['IC_Voltage_right_max_Q2'])

I_left_max_Q2, t_I_left_max_Q2 = get_sig(pulse, signals['IC_Current_left_max_Q2'])
I_right_max_Q2, t_I_right_max_Q2 = get_sig(pulse, signals['IC_Current_right_max_Q2'])

#%%
fig, ax = subplots(2,1,sharex=True)
ax[0].plot(t_V_left_max_Q2, V_left_max_Q2, label='Q2 Left')
ax[0].plot(t_V_right_max_Q2, V_right_max_Q2, label='Q2 Right')
ax[0].axhline(27, color='C3')
ax[0].set_ylabel('Max Cap. Voltage [kV]', fontsize=12)
ax[0].set_title(f'WEST #{pulse}', fontsize=14)
  
ax[1].plot(t_I_left_max_Q2, I_left_max_Q2, label='Q2 Left')
ax[1].plot(t_I_right_max_Q2, I_right_max_Q2, label='Q2 Right')
ax[1].axhline(915, color='C3')
ax[1].set_ylabel('Max Cap. Current [A]', fontsize=12)

ax[1].legend(fontsize=12)

[a.grid(True, alpha=0.2) for a in ax]
ax[0].set_xlim(3, 4.2)
ax[1].set_xlabel('Time [s]', fontsize=12)
fig.subplots_adjust(hspace=0.1)
[a.tick_params(labelsize=14) for a in ax]
[a.legend() for a in ax]
fig.tight_layout()


#%%
fig.savefig('WEST_IC_54461_VI.png', dpi=150)

