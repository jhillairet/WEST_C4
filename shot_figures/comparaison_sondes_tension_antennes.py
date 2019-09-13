# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 16:08:41 2019

@author: JH218595
"""
#%%
import sys
sys.path.append('..')
from control_room import *
import numpy as np

from matplotlib.pyplot import *
#%%
pulse = 54414

#%%
sigs_power=[

        [signals['IC_P_Q1_left_fwd'], signals['IC_P_Gen6_fwd'], signals['IC_P_Q1_left_ref'], signals['IC_P_Gen6_ref']], # Q1L: G6
        [signals['IC_P_Q1_right_fwd'], signals['IC_P_Gen5_fwd'], signals['IC_P_Q1_right_ref'], signals['IC_P_Gen5_ref']], # Q1R: G5
        
        [signals['IC_P_Q2_left_fwd'], signals['IC_P_Gen2_fwd'], signals['IC_P_Q2_left_ref'], signals['IC_P_Gen2_ref']], # Q2L: G2
        [signals['IC_P_Q2_right_fwd'], signals['IC_P_Gen1_fwd'], signals['IC_P_Q2_right_ref'], signals['IC_P_Gen1_ref']], # Q2R: G1
        
        [signals['IC_P_Q4_left_fwd'], signals['IC_P_Gen3_fwd'], signals['IC_P_Q4_left_ref'], signals['IC_P_Gen3_ref']], # Q4L: G3
        [signals['IC_P_Q4_right_fwd'], signals['IC_P_Gen4_fwd'], signals['IC_P_Q4_right_ref'], signals['IC_P_Gen4_ref']], # Q4R: G4
        ]

fig, axes = scope([pulse], sigs_power, do_smooth=True, cycling_mode='color')


#%%

sigs = [
        [signals['IC_P_Q1'], signals['IC_P_Q2'], signals['IC_P_Q4']],
        signals['Rext_median'],
        [signals['IC_VSWR_Q1_Left'],  signals['IC_VSWR_Q2_Left'],  signals['IC_VSWR_Q4_Left'] ],
        [signals['IC_VSWR_Q1_Right'], signals['IC_VSWR_Q2_Right'], signals['IC_VSWR_Q4_Right'] ],
        ]

fig, axes = scope([pulse], sigs, do_smooth=True, cycling_mode='color')
axes[0].legend(('Q1', 'Q2', 'Q4'))


#%%
sigs = [
        [signals['IC_P_Q1'], signals['IC_P_Q2'], signals['IC_P_Q4']],
        signals['Rext_median'],
        [signals['IC_Rc_Q1_left'], signals['IC_Rc_Q2_left'], signals['IC_Rc_Q4_left']],
        [signals['IC_Rc_Q1_right'], signals['IC_Rc_Q2_right'], signals['IC_Rc_Q4_right']],
        [signals[f'IC_delta_phi_toro_Q1_Bot_LmR'], signals[f'IC_delta_phi_toro_Q2_Bot_LmR'], signals[f'IC_delta_phi_toro_Q4_Bot_LmR']],
        [signals[f'IC_delta_phi_toro_Q1_Top_LmR'], signals[f'IC_delta_phi_toro_Q2_Top_LmR'], signals[f'IC_delta_phi_toro_Q4_Top_LmR']],
        ]

fig, axes = scope([pulse], sigs, do_smooth=True, cycling_mode='color')
axes[0].legend(('Q1', 'Q2', 'Q4'))


#%%

# compare voltages
V_left_upper_Q1, t_V_left_upper_Q1 = get_sig(pulse, signals['IC_Voltage_left_upper_Q1'], do_smooth=True)
V_right_upper_Q1, t_V_right_upper_Q1 = get_sig(pulse, signals['IC_Voltage_right_upper_Q1'], do_smooth=True)
V_left_lower_Q1, t_V_left_lower_Q1 = get_sig(pulse, signals['IC_Voltage_left_lower_Q1'], do_smooth=True)
V_right_lower_Q1, t_V_right_lower_Q1 = get_sig(pulse, signals['IC_Voltage_right_lower_Q1'], do_smooth=True)

V_left_upper_Q2, t_V_left_upper_Q2 = get_sig(pulse, signals['IC_Voltage_left_upper_Q2'], do_smooth=True)
V_right_upper_Q2, t_V_right_upper_Q2 = get_sig(pulse, signals['IC_Voltage_right_upper_Q2'], do_smooth=True)
V_left_lower_Q2, t_V_left_lower_Q2 = get_sig(pulse, signals['IC_Voltage_left_lower_Q2'], do_smooth=True)
V_right_lower_Q2, t_V_right_lower_Q2 = get_sig(pulse, signals['IC_Voltage_right_lower_Q2'], do_smooth=True)

V_left_upper_Q4, t_V_left_upper_Q4 = get_sig(pulse, signals['IC_Voltage_left_upper_Q4'], do_smooth=True)
V_right_upper_Q4, t_V_right_upper_Q4 = get_sig(pulse, signals['IC_Voltage_right_upper_Q4'], do_smooth=True)
V_left_lower_Q4, t_V_left_lower_Q4 = get_sig(pulse, signals['IC_Voltage_left_lower_Q4'], do_smooth=True)
V_right_lower_Q4, t_V_right_lower_Q4 = get_sig(pulse, signals['IC_Voltage_right_lower_Q4'], do_smooth=True)

#%%
fig, ax = plt.subplots(2,2,sharex=True, sharey=True)
ax[0,0].plot(t_V_left_upper_Q1, V_left_upper_Q1)
ax[0,0].plot(t_V_left_upper_Q2, V_left_upper_Q2)
ax[0,0].plot(t_V_left_upper_Q4, V_left_upper_Q4)
ax[0,0].set_title('left upper')

ax[1,0].plot(t_V_left_lower_Q1, V_left_lower_Q1)
ax[1,0].plot(t_V_left_lower_Q2, V_left_lower_Q2)
ax[1,0].plot(t_V_left_lower_Q4, V_left_lower_Q4)
ax[1,0].set_title('left lower')

ax[0,1].plot(t_V_right_upper_Q1, V_right_upper_Q1)
ax[0,1].plot(t_V_right_upper_Q2, V_right_upper_Q2)
ax[0,1].plot(t_V_right_upper_Q4, V_right_upper_Q4)
ax[0,1].set_title('right upper')

ax[1,1].plot(t_V_right_lower_Q1, V_right_lower_Q1)
ax[1,1].plot(t_V_right_lower_Q2, V_right_lower_Q2)
ax[1,1].plot(t_V_right_lower_Q4, V_right_lower_Q4)
ax[1,1].set_title('right lower')

[a.set_xlim(3.8, 9.2) for a in ax.flatten()]
ax[0,0].legend(('Q1', 'Q2', 'Q4'))
fig.suptitle(f'WEST #{pulse}')

##%%
#fig, ax = plt.subplots(2,2,sharex=True, sharey=True)
#ax[0,0].plot(t_V_left_upper_Q4, 100*(V_left_upper_Q1 - V_left_upper_Q4)/V_left_upper_Q4, label='$(V_{1} - V_{4})/V_4$')
#ax[0,0].plot(t_V_left_upper_Q4, 100*(V_left_upper_Q2 - V_left_upper_Q4)/V_left_upper_Q4, label='$(V_{2} - V_{4})/V_4$')
#ax[0,0].set_title('left upper')
#
#ax[1,0].plot(t_V_left_lower_Q4, 100*(V_left_lower_Q1 - V_left_lower_Q4)/V_left_lower_Q4, label='$(V_{1} - V_{4})/V_4$')
#ax[1,0].plot(t_V_left_lower_Q4, 100*(V_left_lower_Q2 - V_left_lower_Q4)/V_left_lower_Q4, label='$(V_{2} - V_{4})/V_4$')
#ax[1,0].set_title('left lower')
#
#ax[0,1].plot(t_V_right_upper_Q4, 100*(V_right_upper_Q1 - V_right_upper_Q4)/V_right_upper_Q4, label='$(V_{1} - V_{4})/V_4$')
#ax[0,1].plot(t_V_right_upper_Q4, 100*(V_right_upper_Q2 - V_right_upper_Q4)/V_right_upper_Q4, label='$(V_{2} - V_{4})/V_4$')
#ax[0,1].set_title('right upper')
#
#ax[1,1].plot(t_V_right_lower_Q4, 100*(V_right_lower_Q1 - V_right_lower_Q4)/V_right_lower_Q4, label='$(V_{1} - V_{4})/V_4$')
#ax[1,1].plot(t_V_right_lower_Q4, 100*(V_right_lower_Q2 - V_right_lower_Q4)/V_right_lower_Q4, label='$(V_{2} - V_{4})/V_4$')
#ax[1,1].set_title('right lower')
#
#[a.set_ylim(-100, 100) for a in ax.flatten()]
#[a.set_xlim(3.8, 9.2) for a in ax.flatten()]

#%%
# moyennage des données
# WEST 54629
t_Q1 = (5.83, 6.07)
t_Q2 = (8.47, 8.73)
t_Q4 = (3.12, 3.62)
Q1_upper_left_avg, Q1_upper_left_std = mean_std_in_between(V_left_upper_Q1, t_V_left_upper_Q1, t_start=t_Q1[0], t_end=t_Q1[1])
Q2_upper_left_avg, Q2_upper_left_std = mean_std_in_between(V_left_upper_Q2, t_V_left_upper_Q2, t_start=t_Q2[0], t_end=t_Q2[1])
Q4_upper_left_avg, Q4_upper_left_std = mean_std_in_between(V_left_upper_Q4, t_V_left_upper_Q4, t_start=t_Q4[0], t_end=t_Q4[1])

Q1_lower_left_avg, Q1_lower_left_std = mean_std_in_between(V_left_lower_Q1, t_V_left_lower_Q1, t_start=t_Q1[0], t_end=t_Q1[1])
Q2_lower_left_avg, Q2_lower_left_std = mean_std_in_between(V_left_lower_Q2, t_V_left_lower_Q2, t_start=t_Q2[0], t_end=t_Q2[1])
Q4_lower_left_avg, Q4_lower_left_std = mean_std_in_between(V_left_lower_Q4, t_V_left_lower_Q4, t_start=t_Q4[0], t_end=t_Q4[1])

Q1_upper_right_avg, Q1_upper_right_std = mean_std_in_between(V_right_upper_Q1, t_V_right_upper_Q1, t_start=t_Q1[0], t_end=t_Q1[1])
Q2_upper_right_avg, Q2_upper_right_std = mean_std_in_between(V_right_upper_Q2, t_V_right_upper_Q2, t_start=t_Q2[0], t_end=t_Q2[1])
Q4_upper_right_avg, Q4_upper_right_std = mean_std_in_between(V_right_upper_Q4, t_V_right_upper_Q4, t_start=t_Q4[0], t_end=t_Q4[1])

Q1_lower_right_avg, Q1_lower_right_std = mean_std_in_between(V_right_lower_Q1, t_V_right_lower_Q1, t_start=t_Q1[0], t_end=t_Q1[1])
Q2_lower_right_avg, Q2_lower_right_std = mean_std_in_between(V_right_lower_Q2, t_V_right_lower_Q2, t_start=t_Q2[0], t_end=t_Q2[1])
Q4_lower_right_avg, Q4_lower_right_std = mean_std_in_between(V_right_lower_Q4, t_V_right_lower_Q4, t_start=t_Q4[0], t_end=t_Q4[1])






#%%
pulse = 55015

#%%

sigs = [
        [signals['IC_P_Q1'], signals['IC_P_Q2'], signals['IC_P_Q4']],
        signals['Rext_median'],
        [signals['IC_VSWR_Q1_Left'],  signals['IC_VSWR_Q2_Left'],  signals['IC_VSWR_Q4_Left'] ],
        [signals['IC_VSWR_Q1_Right'], signals['IC_VSWR_Q2_Right'], signals['IC_VSWR_Q4_Right'] ],
        ]

fig, axes = scope([pulse], sigs, do_smooth=True, cycling_mode='color')
axes[0].legend(('Q1', 'Q2', 'Q4'))


#%%
sigs = [
        [signals['IC_P_Q1'], signals['IC_P_Q2'], signals['IC_P_Q4']],
        signals['Rext_median'],
        [signals['IC_Rc_Q1_left'], signals['IC_Rc_Q2_left'], signals['IC_Rc_Q4_left']],
        [signals['IC_Rc_Q1_right'], signals['IC_Rc_Q2_right'], signals['IC_Rc_Q4_right']],
        [signals[f'IC_delta_phi_toro_Q1_Bot_LmR'], signals[f'IC_delta_phi_toro_Q2_Bot_LmR'], signals[f'IC_delta_phi_toro_Q4_Bot_LmR']],
        [signals[f'IC_delta_phi_toro_Q1_Top_LmR'], signals[f'IC_delta_phi_toro_Q2_Top_LmR'], signals[f'IC_delta_phi_toro_Q4_Top_LmR']],
        ]

fig, axes = scope([pulse], sigs, do_smooth=True, cycling_mode='color')
axes[0].legend(('Q1', 'Q2', 'Q4'))


#%%

# compare voltages
V_left_upper_Q1, t_V_left_upper_Q1 = get_sig(pulse, signals['IC_Voltage_left_upper_Q1'], do_smooth=True)
V_right_upper_Q1, t_V_right_upper_Q1 = get_sig(pulse, signals['IC_Voltage_right_upper_Q1'], do_smooth=True)
V_left_lower_Q1, t_V_left_lower_Q1 = get_sig(pulse, signals['IC_Voltage_left_lower_Q1'], do_smooth=True)
V_right_lower_Q1, t_V_right_lower_Q1 = get_sig(pulse, signals['IC_Voltage_right_lower_Q1'], do_smooth=True)

V_left_upper_Q2, t_V_left_upper_Q2 = get_sig(pulse, signals['IC_Voltage_left_upper_Q2'], do_smooth=True)
V_right_upper_Q2, t_V_right_upper_Q2 = get_sig(pulse, signals['IC_Voltage_right_upper_Q2'], do_smooth=True)
V_left_lower_Q2, t_V_left_lower_Q2 = get_sig(pulse, signals['IC_Voltage_left_lower_Q2'], do_smooth=True)
V_right_lower_Q2, t_V_right_lower_Q2 = get_sig(pulse, signals['IC_Voltage_right_lower_Q2'], do_smooth=True)

V_left_upper_Q4, t_V_left_upper_Q4 = get_sig(pulse, signals['IC_Voltage_left_upper_Q4'], do_smooth=True)
V_right_upper_Q4, t_V_right_upper_Q4 = get_sig(pulse, signals['IC_Voltage_right_upper_Q4'], do_smooth=True)
V_left_lower_Q4, t_V_left_lower_Q4 = get_sig(pulse, signals['IC_Voltage_left_lower_Q4'], do_smooth=True)
V_right_lower_Q4, t_V_right_lower_Q4 = get_sig(pulse, signals['IC_Voltage_right_lower_Q4'], do_smooth=True)

#%%
fig, ax = plt.subplots(2,2,sharex=True, sharey=True)
ax[0,0].plot(t_V_left_upper_Q1, V_left_upper_Q1)
ax[0,0].plot(t_V_left_upper_Q2, V_left_upper_Q2)
ax[0,0].plot(t_V_left_upper_Q4, V_left_upper_Q4)
ax[0,0].set_title('left upper')

ax[1,0].plot(t_V_left_lower_Q1, V_left_lower_Q1)
ax[1,0].plot(t_V_left_lower_Q2, V_left_lower_Q2)
ax[1,0].plot(t_V_left_lower_Q4, V_left_lower_Q4)
ax[1,0].set_title('left lower')

ax[0,1].plot(t_V_right_upper_Q1, V_right_upper_Q1)
ax[0,1].plot(t_V_right_upper_Q2, V_right_upper_Q2)
ax[0,1].plot(t_V_right_upper_Q4, V_right_upper_Q4)
ax[0,1].set_title('right upper')

ax[1,1].plot(t_V_right_lower_Q1, V_right_lower_Q1)
ax[1,1].plot(t_V_right_lower_Q2, V_right_lower_Q2)
ax[1,1].plot(t_V_right_lower_Q4, V_right_lower_Q4)
ax[1,1].set_title('right lower')

[a.set_xlim(3.8, 9.2) for a in ax.flatten()]
ax[0,0].legend(('Q1', 'Q2', 'Q4'))
fig.suptitle(f'WEST #{pulse}')

##%%
#fig, ax = plt.subplots(2,2,sharex=True, sharey=True)
#ax[0,0].plot(t_V_left_upper_Q4, 100*(V_left_upper_Q1 - V_left_upper_Q4)/V_left_upper_Q4, label='$(V_{1} - V_{4})/V_4$')
#ax[0,0].plot(t_V_left_upper_Q4, 100*(V_left_upper_Q2 - V_left_upper_Q4)/V_left_upper_Q4, label='$(V_{2} - V_{4})/V_4$')
#ax[0,0].set_title('left upper')
#
#ax[1,0].plot(t_V_left_lower_Q4, 100*(V_left_lower_Q1 - V_left_lower_Q4)/V_left_lower_Q4, label='$(V_{1} - V_{4})/V_4$')
#ax[1,0].plot(t_V_left_lower_Q4, 100*(V_left_lower_Q2 - V_left_lower_Q4)/V_left_lower_Q4, label='$(V_{2} - V_{4})/V_4$')
#ax[1,0].set_title('left lower')
#
#ax[0,1].plot(t_V_right_upper_Q4, 100*(V_right_upper_Q1 - V_right_upper_Q4)/V_right_upper_Q4, label='$(V_{1} - V_{4})/V_4$')
#ax[0,1].plot(t_V_right_upper_Q4, 100*(V_right_upper_Q2 - V_right_upper_Q4)/V_right_upper_Q4, label='$(V_{2} - V_{4})/V_4$')
#ax[0,1].set_title('right upper')
#
#ax[1,1].plot(t_V_right_lower_Q4, 100*(V_right_lower_Q1 - V_right_lower_Q4)/V_right_lower_Q4, label='$(V_{1} - V_{4})/V_4$')
#ax[1,1].plot(t_V_right_lower_Q4, 100*(V_right_lower_Q2 - V_right_lower_Q4)/V_right_lower_Q4, label='$(V_{2} - V_{4})/V_4$')
#ax[1,1].set_title('right lower')
#
#[a.set_ylim(-100, 100) for a in ax.flatten()]
#[a.set_xlim(3.8, 9.2) for a in ax.flatten()]

#%%
# moyennage des données
# WEST 54629
t_Q1 = (5.7, 7.2)
t_Q2 = (5.7, 7.2)
t_Q4 = (5.7, 7.2)
Q1_upper_left_avg, Q1_upper_left_std = mean_std_in_between(V_left_upper_Q1, t_V_left_upper_Q1, t_start=t_Q1[0], t_end=t_Q1[1])
Q2_upper_left_avg, Q2_upper_left_std = mean_std_in_between(V_left_upper_Q2, t_V_left_upper_Q2, t_start=t_Q2[0], t_end=t_Q2[1])
Q4_upper_left_avg, Q4_upper_left_std = mean_std_in_between(V_left_upper_Q4, t_V_left_upper_Q4, t_start=t_Q4[0], t_end=t_Q4[1])

Q1_lower_left_avg, Q1_lower_left_std = mean_std_in_between(V_left_lower_Q1, t_V_left_lower_Q1, t_start=t_Q1[0], t_end=t_Q1[1])
Q2_lower_left_avg, Q2_lower_left_std = mean_std_in_between(V_left_lower_Q2, t_V_left_lower_Q2, t_start=t_Q2[0], t_end=t_Q2[1])
Q4_lower_left_avg, Q4_lower_left_std = mean_std_in_between(V_left_lower_Q4, t_V_left_lower_Q4, t_start=t_Q4[0], t_end=t_Q4[1])

Q1_upper_right_avg, Q1_upper_right_std = mean_std_in_between(V_right_upper_Q1, t_V_right_upper_Q1, t_start=t_Q1[0], t_end=t_Q1[1])
Q2_upper_right_avg, Q2_upper_right_std = mean_std_in_between(V_right_upper_Q2, t_V_right_upper_Q2, t_start=t_Q2[0], t_end=t_Q2[1])
Q4_upper_right_avg, Q4_upper_right_std = mean_std_in_between(V_right_upper_Q4, t_V_right_upper_Q4, t_start=t_Q4[0], t_end=t_Q4[1])

Q1_lower_right_avg, Q1_lower_right_std = mean_std_in_between(V_right_lower_Q1, t_V_right_lower_Q1, t_start=t_Q1[0], t_end=t_Q1[1])
Q2_lower_right_avg, Q2_lower_right_std = mean_std_in_between(V_right_lower_Q2, t_V_right_lower_Q2, t_start=t_Q2[0], t_end=t_Q2[1])
Q4_lower_right_avg, Q4_lower_right_std = mean_std_in_between(V_right_lower_Q4, t_V_right_lower_Q4, t_start=t_Q4[0], t_end=t_Q4[1])

