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
from scipy.io import loadmat

from matplotlib.pyplot import *


#%%
pulse = 54719

#%%
# reflectometry timings for average
ts = [(09.1, 09.3),  # during LH, before IC
      (11.8, 11.9),  # during LH, during IC
      ]



#%%
P_IC_tot, t_tot = get_sig(pulse, signals['IC_P_tot'])
P_Q1, t_Q1 = get_sig(pulse, signals['IC_P_Q1'])
P_Q2, t_Q2 = get_sig(pulse, signals['IC_P_Q2'])
P_Q4, t_Q4 = get_sig(pulse, signals['IC_P_Q4'])


P_LH_tot, t_LH_tot = get_sig(pulse, signals['LH_P_tot'])
P_LH1, t_LH1 = get_sig(pulse, signals['LH_P_LH1'])
P_LH2, t_LH2 = get_sig(pulse, signals['LH_P_LH2'])
Rc_Q4, t_Rc_Q4 = get_sig(pulse, signals['IC_Rc_Q4_avg'])
Rc_Q4_left, t_Rc_Q4_left = get_sig(pulse, signals['IC_Rc_Q4_left'])
Rc_Q4_right, t_Rc_Q4_right = get_sig(pulse, signals['IC_Rc_Q4_right'])

Rext, t_Rext = get_sig(pulse, signals['Rext_median'])

#%%
I_max = 915

I, t_I = pw.tsbase(pulse, 'GICHICAPA', nargout=2)
I_Q1_max = np.amax(I[:,1:4])
I_Q2_max = np.amax(I[:,4:8])
I_Q4_max = np.amax(I[:,8:12]) 

P_Q1_max = P_Q1 * (I_max/I_Q1_max)**2 
P_Q2_max = P_Q2 * (I_max/I_Q2_max)**2 
P_Q4_max = P_Q4 * (I_max/I_Q4_max)**2 
P_max =  P_Q4_max

# interpolate LH and IC power
_P_LH_tot = np.interp(t_tot.squeeze(), t_LH_tot.squeeze(), P_LH_tot.squeeze())


R_IC, t_R_IC = get_sig(pulse, signals['IC_Positions'])


#%% 
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
ax1.fill_between(t_tot, _P_LH_tot*1e3 + P_IC_tot.squeeze(), alpha=0.2, label='Total RF Power')
ax1.plot(t_LH1, P_LH1, label='LH1', lw=2)
ax1.plot(t_LH2, P_LH2, label='LH2', lw=2)
ax1.plot(t_Q4, P_Q4, label='IC Q4', lw=2)
ax1.plot(t_Q4, P_max, color='r')
ax1.set_ylabel('P RF [kW]')

#ax2.plot(t_Rc_Q4, Rc_Q4)
ax2.plot(t_Rc_Q4_left, Rc_Q4_left, label='Rc Q4 left', lw=2)
ax2.plot(t_Rc_Q4_right, Rc_Q4_right, label='Rc Q4 right', lw=2)
ax2.set_ylabel('Rc [Ohm]')
ax2.legend(fontsize=12, loc='upper right') 

ax3.plot(t_Rext, R_IC[2]*1e3 - Rext)
ax3.set_ylim(8, 45)
ax3.set_title('R_ant - R_ext_median')
ax3.set_ylabel('[mm]')

ax1.set_xlim(3.5, 13)
[ax.grid(True, alpha=0.2) for ax in (ax1, ax2, ax3)]
[ax.tick_params(labelsize=14) for ax in (ax1, ax2, ax3)]
ax1.legend(fontsize=12, loc='upper right') 

ax1.set_title(f'WEST #{pulse}', fontsize=12)
ax3.set_xlabel('Time [s]', fontsize=12)

#for idx, (t_start, t_stop) in enumerate(ts):
#    [a.axvspan(t_start, t_stop, alpha=.2, color=f'C{idx}') for a in (ax1, ax2)]


fig.subplots_adjust(hspace=0)

fig.tight_layout()
#%%
savefig(f'WEST_IC_{pulse}.png', dpi=150)




