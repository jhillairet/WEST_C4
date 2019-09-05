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
pulse = 54902

Ip, t_Ip = get_sig(pulse, signals['Ip'])
nl, t_nl = get_sig(pulse, signals['nl'])

P_IC_tot, t_tot = get_sig(pulse, signals['IC_P_tot'])
P_Q1, t_Q1 = get_sig(pulse, signals['IC_P_Q1'])
P_Q2, t_Q2 = get_sig(pulse, signals['IC_P_Q2'])
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
ax[1].fill_between(t_Q4, np.squeeze(P_Q1+P_Q4), alpha=0.2, label='Total RF Power')
ax[1].plot(t_Q1, P_Q1, label='IC Q1', lw=2, color='C0')
ax[1].plot(t_Q4, P_Q4, label='IC Q4', lw=2, color='C2')


ax2 = ax[0].twinx()
ax2.plot(t_nl, nl, lw=2, color='C1')

ax[1].set_xlabel('Time [s]', fontsize=14)
ax[0].set_ylabel('Ip [kA]', fontsize=14, color='C0')
ax2.set_ylabel('nl [$10^{19}$ $m^{-3}$]', fontsize=14, color='C1')
ax[1].set_ylabel('IC Power [kW]', fontsize=14)
ax[1].legend(fontsize=12, loc='upper left')
[a.grid(True, alpha=0.2) for a in ax]
[a.tick_params(labelsize=14) for a in ax]
ax[0].tick_params(color='C0', labelcolor='C0')
ax2.tick_params(color='C1', labelcolor='C1')

ax[0].set_xlim(-0.1, 12.3)

ax[0].set_title(f'WEST #{pulse}', fontsize=14)
fig.tight_layout()

# Max allowable power


fig.tight_layout()
#%%
savefig('WEST_IC_54902.png', dpi=150)


#%%
def generate_sig_capas_Qi(i=1):
    sig_probes_Qi = [
        [signals[f'IC_P_Q{i}_left_fwd'], signals[f'IC_P_Q{i}_left_ref']],    
        [signals[f'IC_P_Q{i}_right_fwd'], signals[f'IC_P_Q{i}_right_ref']],
        [signals[f'IC_Rc_Q{i}_left'], signals[f'IC_Rc_Q{i}_right']],
                        [signals[f'IC_VSWR_Q{i}_Left'], signals[f'IC_VSWR_Q{i}_Right']],
        [signals[f'IC_ErrSig_Q{i}_left_upper'], signals[f'IC_ErrSig_Q{i}_left_lower']],
        [signals[f'IC_ErrSig_Q{i}_right_upper'], signals[f'IC_ErrSig_Q{i}_right_lower']],  
        [signals[f'IC_Capa_Q{i}_left_upper'], signals[f'IC_Capa_Q{i}_left_lower']],
        [signals[f'IC_Capa_Q{i}_right_upper'], signals[f'IC_Capa_Q{i}_right_lower']],
    ]
    return sig_probes_Qi

#%%
sigs = generate_sig_capas_Qi(1)
fig, axes = scope([pulse], sigs, do_smooth=False)
#axes[-1].set_xlim(3.5, 6.5)
axes[0].legend()

