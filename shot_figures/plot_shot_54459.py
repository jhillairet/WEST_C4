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
pulse = 54459

P_tot, t_tot = get_sig(pulse, signals['IC_P_tot'])
P_Q1, t_Q1 = get_sig(pulse, signals['IC_P_Q1'])
P_Q2, t_Q2 = get_sig(pulse, signals['IC_P_Q2'])
P_Q4, t_Q4 = get_sig(pulse, signals['IC_P_Q4'])

figure(1, clear=True)
fill_between(t_tot, P_tot.squeeze(), alpha=0.2, label='IC Total')
plot(t_Q1, P_Q1, label='IC Q1', lw=2)
plot(t_Q2, P_Q2, label='IC Q2', lw=2)
plot(t_Q4, P_Q4, label='IC Q4', lw=2)

title(f'WEST #{pulse}', fontsize=14)
xlabel('Time [s]', fontsize=14)
ylabel('Coupled Power [kW]', fontsize=14)
xlim(3, 3.7)
grid(True, alpha=0.2)
legend(fontsize=14)
tick_params(labelsize=14)
tight_layout()

#%%
savefig('WEST_IC_54459.png', dpi=150)