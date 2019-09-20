|# -*- coding: utf-8 -*-
"""

"""
# %%
from control_room import *
import numpy as np

#%%
def generate_sig_generalQi(i=1):
    sigs_general_Qi = [
        signals[f'IC_PCS_interdiction_Q{i}'],
        signals[f'IC_PCS_Power_Q{i}'], 
        #signals[f'IC_P_Q{i}'],
        [signals[f'IC_P_Q{i}_left_fwd'], signals[f'IC_P_Q{i}_left_ref']],
        [signals[f'IC_P_Q{i}_right_fwd'], signals[f'IC_P_Q{i}_right_ref']],
        [signals[f'IC_VSWR_Q{i}_Left'], signals[f'IC_VSWR_Q{i}_Right']],
        [signals[f'IC_Rc_Q{i}_left'], signals[f'IC_Rc_Q{i}_right']],
        [signals[f'IC_Voltage_left_upper_Q{i}'], signals[f'IC_Voltage_left_lower_Q{i}']],
        [signals[f'IC_Voltage_right_upper_Q{i}'], signals[f'IC_Voltage_right_lower_Q{i}']],
        [signals[f'IC_Current_left_upper_Q{i}'], signals[f'IC_Current_left_lower_Q{i}']],
        [signals[f'IC_Current_right_upper_Q{i}'], signals[f'IC_Current_right_lower_Q{i}']],
        #[signals['IC_Phase_Q1 (Pf_Left - Pf_Right)']],
        #signals[f'IC_delta_phi_toro_Q{i}_LmR_FPGA'], 
        [signals[f'IC_delta_phi_toro_Q{i}_Bot_LmR'], signals[f'IC_delta_phi_toro_Q{i}_Top_LmR']],        
        [signals[f'IC_Vacuum_Q{i}_right'], signals[f'IC_Vacuum_Q{i}_left']],
        [signals[f'IC_ErrSig_Q{i}_left_upper'], signals[f'IC_ErrSig_Q{i}_left_lower']],
        [signals[f'IC_ErrSig_Q{i}_right_upper'], signals[f'IC_ErrSig_Q{i}_right_lower']],
    ]
    return sigs_general_Qi


def generate_sig_probes_Qi(i=1):
    sig_probes_Qi = [
    signals[f'IC_P_Q{i}'],
        [signals[f'IC_Rc_Q{i}_left'], signals[f'IC_Rc_Q{i}_right']],
    [signals[f'IC_Voltage_left_upper_Q{i}'], signals[f'IC_Voltage_left_lower_Q{i}']],
    [signals[f'IC_Voltage_right_upper_Q{i}'], signals[f'IC_Voltage_right_lower_Q{i}']],
    [signals[f'IC_Current_left_upper_Q{i}'], signals[f'IC_Current_left_lower_Q{i}']],
    [signals[f'IC_Current_right_upper_Q{i}'], signals[f'IC_Current_right_lower_Q{i}']],
    [signals[f'IC_delta_phi_toro_Q{i}_Bot_LmR'], signals[f'IC_delta_phi_toro_Q{i}_Top_LmR']],
    [signals[f'IC_delta_phi_polo_Q{i}_Left_BmT'], signals[f'IC_delta_phi_polo_Q{i}_Right_BmT']],        
    ]
    return sig_probes_Qi

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
pulses = [55151]


#%%
#sig_generalQ1 = generate_sig_generalQi(1)
#fig, axes = scope(pulses, sig_generalQ1, do_smooth=False)
##axes[-1].set_xlim(3.5, 6.5)
#axes[0].legend()

sig_generalQ2 = generate_sig_generalQi(2)
fig, axes = scope(pulses, sig_generalQ2, do_smooth=False, window_loc=(600,0))
#axes[-1].set_xlim(3.5, 6.5)
axes[0].legend()

sig_generalQ4 = generate_sig_generalQi(4)
fig, axes = scope(pulses, sig_generalQ4, do_smooth=False, window_loc=(1200,0))
#axes[-1].set_xlim(3.5, 6.5)
axes[0].legend()


#%%
#sig_probes_Q1 = generate_sig_probes_Qi(1)
#fig, axes = scope(pulses, sig_probes_Q1, do_smooth=False)
##axes[-1].set_xlim(3.5, 6.5)
#axes[0].legend()

sig_probes_Q2 = generate_sig_probes_Qi(2)
fig, axes = scope(pulses, sig_probes_Q2, do_smooth=False, window_loc=(600,0))
#axes[-1].set_xlim(3.5, 6.5)
axes[0].legend()

sig_probes_Q4 = generate_sig_probes_Qi(4)
fig, axes = scope(pulses, sig_probes_Q4, do_smooth=False, window_loc=(1200,0))
#axes[-1].set_xlim(3.5, 6.5)
axes[0].legend()


#%% capacitors
#sig_capa_Q1 = generate_sig_capas_Qi(1)
#fig, axes = scope(pulses, sig_capa_Q1, do_smooth=False)
##axes[-1].set_xlim(3.5, 6.5)
#axes[0].legend()

sig_capa_Q2 = generate_sig_capas_Qi(2)
fig, axes = scope(pulses, sig_capa_Q2, do_smooth=False, window_loc=(600,0))
#axes[-1].set_xlim(3.5, 6.5)
axes[0].legend()

sig_capa_Q4 = generate_sig_capas_Qi(4)
fig, axes = scope(pulses, sig_capa_Q4, do_smooth=False, window_loc=(1200,0))
#axes[-1].set_xlim(0, 10)
axes[0].legend()


#%% General view and Gaz

sig_general = [
        signals['Ip'],
        signals['nl'],
        signals['Te1'],
        signals['Prad'],
        [signals['Neutron1'], signals['Neutron2']],
        [signals['Rext_median']],
#        [signals['Dext_Q4']],
        #signals['Zgeo'],
        #signals['IC_P_tot'],#[signals['LH_P_LH1'], signals['LH_P_LH2']],
#        signals['LH_P_tot'],
        signals['IC_P_tot'],
        [signals['IC_P_Q1'], signals['IC_P_Q2'], signals['IC_P_Q4']],
        [signals['IC_Rc_Q1_left'], signals['IC_Rc_Q2_left'], signals['IC_Rc_Q4_left']],
        [signals['IC_Rc_Q1_right'], signals['IC_Rc_Q2_right'], signals['IC_Rc_Q4_right']],
#        [signals['Valve11'], ],
        #[signals[f'IC_Vacuum_Q1_right'], signals[f'IC_Vacuum_Q2_right'], signals[f'IC_Vacuum_Q4_right'] ],
        #signals['Cu'],
        ]
fig, axes = scope(pulses, sig_general, do_smooth=True, window_loc=(600,0))
#axes[-1].set_xlim(3.5, 6.5)
axes[0].legend()


#%% Phase differences
sig_phases = [
        [signals['IC_PCS_Phase_Q1'], signals['IC_PCS_Phase_Q2'], signals['IC_PCS_Phase_Q4']],
        [signals['IC_Phase_Q2 (Pf_Left - Pf_Right)'], signals['IC_Phase_Q4 (Pf_Left - Pf_Right)'], ],
        [signals['IC_delta_phi_toro_Q1_Top_LmR'], signals['IC_delta_phi_toro_Q1_Bot_LmR']],
        signals['IC_delta_phi_toro_Q1_LmR_FPGA'],
        [signals['IC_delta_phi_toro_Q2_Top_LmR'], signals['IC_delta_phi_toro_Q2_Bot_LmR']],
        signals['IC_delta_phi_toro_Q2_LmR_FPGA'],
        [signals['IC_delta_phi_toro_Q4_Top_LmR'], signals['IC_delta_phi_toro_Q4_Bot_LmR']],
        signals['IC_delta_phi_toro_Q4_LmR_FPGA'],
        ]
fig, axes = scope(pulses, sig_phases, do_smooth=False, window_loc=(600,0))
#axes[-1].set_xlim(3.5, 6.5)
axes[0].legend()


#%%
sig_currents = [
        [signals['IC_Current_left_upper_Q1'], signals['IC_Current_left_lower_Q1']],
        [signals['IC_Current_right_upper_Q1'], signals['IC_Current_right_lower_Q1']],
        [signals['IC_Current_left_upper_Q2'], signals['IC_Current_left_lower_Q2']],
        [signals['IC_Current_right_upper_Q2'], signals['IC_Current_right_lower_Q2']],
        [signals['IC_Current_left_upper_Q4'], signals['IC_Current_left_lower_Q4']],
        [signals['IC_Current_right_upper_Q4'], signals['IC_Current_right_lower_Q4']],        
        ]
fig, axes = scope(pulses, sig_currents, do_smooth=False, window_loc=(600,0))
#axes[-1].set_xlim(0, 10)
axes[0].legend()


#%% barometry is perturbed by ICRH
sig_baro = [
        signals['IC_P_tot'],
        signals['baro_Q2'],
        signals['baro_Q4']
        ]
fig, axes = scope(pulses, sig_baro, do_smooth=False)
axes[-1].set_xlim(3.5, 6.5)
axes[0].legend()

#%% voltage probes comparaison
sig_voltage_probes = [
    [signals[f'IC_P_Q1_left_fwd'],          signals[f'IC_P_Q2_left_fwd'],           signals[f'IC_P_Q4_left_fwd']            ],
    [signals[f'IC_P_Q1_right_fwd'],         signals[f'IC_P_Q2_right_fwd'],          signals[f'IC_P_Q4_right_fwd']            ],
    [signals[f'IC_VSWR_Q1_Left'],           signals[f'IC_VSWR_Q2_Left'],            signals[f'IC_VSWR_Q4_Left']],
    [signals[f'IC_VSWR_Q1_Right'],          signals[f'IC_VSWR_Q2_Right'],           signals[f'IC_VSWR_Q4_Right']],   
    [signals[f'IC_Voltage_left_upper_Q1'],  signals[f'IC_Voltage_left_upper_Q2'],   signals[f'IC_Voltage_left_upper_Q4']    ],
    [signals[f'IC_Voltage_left_lower_Q1'],  signals[f'IC_Voltage_left_lower_Q2'],   signals[f'IC_Voltage_left_lower_Q4']    ],
    [signals[f'IC_Voltage_right_upper_Q1'], signals[f'IC_Voltage_right_upper_Q2'],  signals[f'IC_Voltage_right_upper_Q4']   ],
    [signals[f'IC_Voltage_right_lower_Q1'], signals[f'IC_Voltage_right_lower_Q2'],  signals[f'IC_Voltage_right_lower_Q4']   ], 
    [signals[f'IC_Rc_Q1_left'],             signals[f'IC_Rc_Q2_left'],              signals[f'IC_Rc_Q4_left']               ],
    [signals[f'IC_Rc_Q1_right'],            signals[f'IC_Rc_Q2_right'],             signals[f'IC_Rc_Q4_right']              ],
        ]
fig, axes = scope(pulses, sig_voltage_probes, do_smooth=False, cycling_mode='color')
axes[0].legend()

#%%
sigs = [
        signals['Ip'],
        signals['nl'],
        signals['Rext_median'],
        signals['IC_P_tot'],
        ]
fig, axes = scope(pulses, sigs, do_smooth=True, lw=2)
axes[0].set_xlim(0, 13)
axes[2].set_ylim(2910, 2950)

#%%

sigs_phase = [
    [signals['IC_P_Q1'], signals['IC_P_Q2'], signals['IC_P_Q4']],
    [signals['IC_Rc_Q1_left'], signals['IC_Rc_Q1_right']],
    [signals['IC_Rc_Q4_left'], signals['IC_Rc_Q4_right']],
    signals['IC_Phase_Q1 (Pf_Left - Pf_Right)'],
    signals['IC_Phase_Q1 (Pr_Left - Pf_Right)'],
    signals['IC_Phase_Q1 (Pr_Right - Pf_Right)'],
    signals['IC_Phase_Q1 (V1 - Pf_Left)'],
    signals['IC_Phase_Q1 (V2 - Pf_Left)'],
    signals['IC_Phase_Q1 (V3 - Pf_Right)'],
    signals['IC_Phase_Q1 (V4 - Pf_Right)'],
        ]
fig, axes = scope([54902], sigs_phase, do_smooth=False, lw=2, cycling_mode='color')

