# -*- coding: utf-8 -*-
"""
Reproducing the load tolerance curve obtained from WEST shot #55589

@author: J.Hillairet
"""
#%% import
from matplotlib.pylab import *
import numpy as np
import skrf as rf

from antenna.conjugate_t import ConjugateT
from antenna.topica import *

import sys
sys.path.append('..')
from control_room import *

#%% pulse
pulse = 55589

#%%  Fetch experimental data
Ip, t_Ip = get_sig(pulse, signals['Ip'])
nl, t_nl = get_sig(pulse, signals['nl'])

P_IC_tot, t_tot = get_sig(pulse, signals['IC_P_tot'])
P_Q1, t_Q1 = get_sig(pulse, signals['IC_P_Q1'])
P_Q2, t_Q2 = get_sig(pulse, signals['IC_P_Q2'])
P_Q4, t_Q4 = get_sig(pulse, signals['IC_P_Q4'])

Prad, trad = get_sig(pulse, signals['Prad'])
Psep, tsep = get_sig(pulse, signals['Separatrix_P'])

# Te, t_Te = get_sig(pulse, signals['Te'])
neutron1, t_neutron1 = get_sig(pulse, signals['Neutron1'])

Rc_Q1, t_Rc_Q1 = get_sig(pulse, signals['IC_Rc_Q1_avg'])
Rc_Q2, t_Rc_Q2 = get_sig(pulse, signals['IC_Rc_Q2_avg'])
Rc_Q4, t_Rc_Q4 = get_sig(pulse, signals['IC_Rc_Q4_avg'])

R_IC, t_R_IC = get_sig(pulse, signals['IC_Positions'])
Rext, t_Rext = get_sig(pulse, signals['Rext_median'])

VSWR_Q1_l, t_VSWR_Q1_l = get_sig(pulse, signals['IC_VSWR_Q1_left'])
VSWR_Q1_r, t_VSWR_Q1_r = get_sig(pulse, signals['IC_VSWR_Q1_right'])
VSWR_Q2_l, t_VSWR_Q2_l = get_sig(pulse, signals['IC_VSWR_Q2_left'])
VSWR_Q2_r, t_VSWR_Q2_r = get_sig(pulse, signals['IC_VSWR_Q2_right'])
VSWR_Q4_l, t_VSWR_Q4_l = get_sig(pulse, signals['IC_VSWR_Q4_left'])
VSWR_Q4_r, t_VSWR_Q4_r = get_sig(pulse, signals['IC_VSWR_Q4_right'])

_Rc_Q1, _ = in_between(Rc_Q1, t_Rc_Q1, 7.0, 8 )
_Rc_Q2, _ = in_between(Rc_Q2, t_Rc_Q2, 5.5, 6.0)
_Rc_Q4, _ = in_between(Rc_Q4, t_Rc_Q4, 7.0, 8 )
_VSWR_Q1_l, _ = in_between(VSWR_Q1_l, t_VSWR_Q1_l[:,0], 7.0, 8 )
_VSWR_Q1_r, _ = in_between(VSWR_Q1_r, t_VSWR_Q1_r[:,0], 7.0, 8 )
_VSWR_Q2_l, _ = in_between(VSWR_Q2_l, t_VSWR_Q2_l[:,0], 5.5, 6.0)
_VSWR_Q2_r, _ = in_between(VSWR_Q2_r, t_VSWR_Q2_r[:,0], 5.5, 6.0)
_VSWR_Q4_r, _ = in_between(VSWR_Q4_r, t_VSWR_Q4_r[:,0], 7.0, 8 )
_VSWR_Q4_l, _ = in_between(VSWR_Q4_l, t_VSWR_Q4_l[:,0], 7.0, 8 )


#%%
def Z(Gamma, Z0=30):
    return Z0*(1 + Gamma)/(1 - Gamma)
    
Z_coupler_left =  Z(Gamma(pulse, 'Q4', 'left', 5.0, 5.2)[0])
Z_coupler_right = Z(Gamma(pulse, 'Q4', 'right', 5.0, 5.2)[0])

print(Z_coupler_left, Z_coupler_right)

#%% Equivalent Q4 antenna model
freqs, _ = get_sig(pulse, signals['IC_Frequencies'])

f_match = freqs[2]*1e6 # Q4 frequency 
Z_match = 30 - 6*1j # matching impedance 
Z_load = 0.65 + 30j
Pin = 1e6 # W

# at a given frequency and loading conditions,
# match capacitance are higher for ideal model, than for equivalent model
# match capacitance are higher for the equivalent model than for the advanced model
# ie : Cideal > Cequivalent > Cadvanced
cap_model = 'advanced'

# Creating the antenna
bridge = rf.Network('../../ICRH/WEST_design/data/Sparameters/WEST/WEST_ICRH_bridge.s3p', f_unit='MHz')
impedance_transformer = rf.Network('../../ICRH/WEST_design/data/Sparameters/WEST/WEST_ICRH_impedance-transformer.s2p', f_unit='MHz')
window = rf.Network('../../ICRH/WEST_design/data/Sparameters/WEST/WEST_ICRH_window.s2p', f_unit='MHz')
idx_f = np.argmin(np.abs(bridge.frequency.f - f_match))

CT = ConjugateT(bridge, impedance_transformer, window, capacitor_model=cap_model)
CT.match(f_match=f_match, z_load=Z_load, z_match=Z_match)

# once having found a match point, change the load impedance to generate 
# a VSWR vs Rc figures
Rcs = np.linspace(0.4, 2.0, 101)
VSWRs = []
for Rc in Rcs:
    VSWRs.append(CT.load(Rc + 30j).s_vswr[idx_f])
    
VSWRs = np.array(VSWRs).squeeze()

fig, ax = plt.subplots()
ax.plot(_Rc_Q4, _VSWR_Q4_l, '.', alpha=0.6, label='Antenna 3 - Experimental')
# ax.plot(_Rc_Q4, _VSWR_Q4_r, '.', alpha=0.6, label='Q4 right')
ax.plot(Rcs, VSWRs, lw=2, color='k',label=f'Antenna 3 - RF Model')
ax.plot(Rcs, Rcs/Z_load.real, ls='--', color='gray', label='Non Resilient')

ax.set_ylim(1, 2.5)
ax.set_xlim(0.35, 2.01)
ax.grid(True, alpha=0.6)
ax.set_xlabel('Rc [$\Omega$]', fontsize=14)
ax.set_ylabel('VSWR', fontsize=14)
ax.set_title(r'WEST #55589 ($t\in[7-8]$s) - Antenna Load Resilience')
ax.legend(fontsize=12)

#%% savefig Q4
fig.savefig(f'WEST_ICRH_{pulse}_load_resilience_Q4.png')

#%% equivalent Q1 antenna model
freqs, _ = get_sig(pulse, signals['IC_Frequencies'])

f_match = freqs[0]*1e6 # Q4 frequency 
# RIGHT SIDE
# Z_match = 30 - 4*1j # matching impedance 
# Z_load = 0.9 + 30j
# LEFT SIDE
Z_match = 30 - 3*1j # matching impedance 
Z_load = 1.2 + 30j
Pin = 1e6 # W

# at a given frequency and loading conditions,
# match capacitance are higher for ideal model, than for equivalent model
# match capacitance are higher for the equivalent model than for the advanced model
# ie : Cideal > Cequivalent > Cadvanced
cap_model = 'advanced'

# Creating the antenna
bridge = rf.Network('../../ICRH/WEST_design/data/Sparameters/WEST/WEST_ICRH_bridge.s3p', f_unit='MHz')
impedance_transformer = rf.Network('../../ICRH/WEST_design/data/Sparameters/WEST/WEST_ICRH_impedance-transformer.s2p', f_unit='MHz')
window = rf.Network('../../ICRH/WEST_design/data/Sparameters/WEST/WEST_ICRH_window.s2p', f_unit='MHz')
idx_f = np.argmin(np.abs(bridge.frequency.f - f_match))


CT = ConjugateT(bridge, impedance_transformer, window, capacitor_model=cap_model)
CT.match(f_match=f_match, z_load=Z_load, z_match=Z_match)

# once having found a match point, change the load impedance to generate 
# a VSWR vs Rc figures
Rcs = np.linspace(0.4, 2.0, 101)
VSWRs = []
for Rc in Rcs:
    VSWRs.append(CT.load(Rc + 30j).s_vswr[idx_f])
    
VSWRs = np.array(VSWRs).squeeze()

fig, ax = plt.subplots()

_Rc_Q1, _ = in_between(Rc_Q1, t_Rc_Q1, 7.0, 8 )
_Rc_Q4, _ = in_between(Rc_Q4, t_Rc_Q4, 7.0, 8 )

ax.plot(_Rc_Q1, _VSWR_Q1_l, '.', alpha=0.6, label='Antenna 1 - Experimental', color='C1')
# ax.plot(_Rc_Q1, _VSWR_Q1_r, '.', alpha=0.6, label='WEST ICRH Antenna', color='C1')
ax.plot(Rcs, VSWRs, lw=2, color="k", label=f'Antenna 1 - RF Model')
ax.plot(Rcs, Rcs/Z_load.real, ls='--', color='gray', label='Non Resilient')

ax.set_ylim(1, 2.5)
ax.set_xlim(0.35, 2.01)
ax.grid(True, alpha=0.6)
ax.set_xlabel('Rc [$\Omega$]', fontsize=14)
ax.set_ylabel('VSWR', fontsize=14)
ax.set_title(r'WEST #55589 ($t\in[7-8]$s) - Antenna Load Resilience')
ax.legend(fontsize=12)

#%% save fig Q1
fig.savefig(f'WEST_ICRH_{pulse}_load_resilience_Q1.png')


#%% equivalent Q2 antenna model
freqs, _ = get_sig(pulse, signals['IC_Frequencies'])

f_match = freqs[1]*1e6 # Q4 frequency 
# RIGHT SIDE
# Z_match = 30 - 4*1j # matching impedance 
# Z_load = 0.9 + 30j
# LEFT SIDE
Z_match = 30 - 3*1j # matching impedance 
Z_load = 0.8 + 30j
Pin = 1e6 # W

# at a given frequency and loading conditions,
# match capacitance are higher for ideal model, than for equivalent model
# match capacitance are higher for the equivalent model than for the advanced model
# ie : Cideal > Cequivalent > Cadvanced
cap_model = 'advanced'

# Creating the antenna
bridge = rf.Network('../../ICRH/WEST_design/data/Sparameters/WEST/WEST_ICRH_bridge.s3p', f_unit='MHz')
impedance_transformer = rf.Network('../../ICRH/WEST_design/data/Sparameters/WEST/WEST_ICRH_impedance-transformer.s2p', f_unit='MHz')
window = rf.Network('../../ICRH/WEST_design/data/Sparameters/WEST/WEST_ICRH_window.s2p', f_unit='MHz')
idx_f = np.argmin(np.abs(bridge.frequency.f - f_match))

CT = ConjugateT(bridge, impedance_transformer, window, capacitor_model=cap_model)
CT.match(f_match=f_match, z_load=Z_load, z_match=Z_match)

# once having found a match point, change the load impedance to generate 
# a VSWR vs Rc figures
Rcs = np.linspace(0.4, 2.0, 101)
VSWRs = []
for Rc in Rcs:
    VSWRs.append(CT.load(Rc + 30j).s_vswr[idx_f])
    
VSWRs = np.array(VSWRs).squeeze()

fig, ax = plt.subplots()

ax.plot(_Rc_Q2, _VSWR_Q2_l, '.', alpha=0.6, label='Antenna 2 - Experimental', color='C1')
# ax.plot(_Rc_Q2, _VSWR_Q2_r, '.', alpha=0.6, label='WEST ICRH Antenna', color='C2')
ax.plot(Rcs, VSWRs, lw=2, color="k", label=f'Antenna 2 - RF Model')
ax.plot(Rcs, Rcs/Z_load.real, ls='--', color='gray', label='Non Resilient')

ax.set_ylim(1, 2.5)
ax.set_xlim(0.35, 2.01)
ax.grid(True, alpha=0.6)
ax.set_xlabel('Rc [$\Omega$]', fontsize=14)
ax.set_ylabel('VSWR', fontsize=14)
ax.set_title(r'WEST #55589 ($t\in[7-8]$s) - Antenna Load Resilience')
ax.legend(fontsize=12)

#%% save fig Q1
fig.savefig(f'WEST_ICRH_{pulse}_load_resilience_Q2.png')