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


#%%  Q4 scan phase
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 55222
pulse = 55222

Ip, t_Ip = get_sig(pulse, signals['Ip'])
nl, t_nl = get_sig(pulse, signals['nl'])

P_IC_tot, t_tot = get_sig(pulse, signals['IC_P_tot'])
P_Q1, t_Q1 = get_sig(pulse, signals['IC_P_Q1'])
P_Q2, t_Q2 = get_sig(pulse, signals['IC_P_Q2'])
P_Q4, t_Q4 = get_sig(pulse, signals['IC_P_Q4'])

#%%
Rc_Q1_left, t_Rc_Q1_left = get_sig(pulse, signals['IC_Rc_Q1_left'])
Rc_Q1_right, t_Rc_Q1_right = get_sig(pulse, signals['IC_Rc_Q1_right'])

Rc_Q2_left, t_Rc_Q2_left = get_sig(pulse, signals['IC_Rc_Q2_left'])
Rc_Q2_right, t_Rc_Q2_right = get_sig(pulse, signals['IC_Rc_Q2_right'])

Rc_Q4_left, t_Rc_Q4_left = get_sig(pulse, signals['IC_Rc_Q4_left'])
Rc_Q4_right, t_Rc_Q4_right = get_sig(pulse, signals['IC_Rc_Q4_right'])

Rc_Q1, t_Rc_Q1 = get_sig(pulse, signals['IC_Rc_Q1_avg'])
Rc_Q2, t_Rc_Q2 = get_sig(pulse, signals['IC_Rc_Q2_avg'])
Rc_Q4, t_Rc_Q4 = get_sig(pulse, signals['IC_Rc_Q4_avg'])

R_IC, t_R_IC = get_sig(pulse, signals['IC_Positions'])
Rext, t_Rext = get_sig(pulse, signals['Rext_median'])

Prad, t_Prad = get_sig(pulse, signals['Prad'])
Prad_bulk, t_Prad_bulk = get_sig(pulse, signals['Prad_bulk'])

# phaseQ2, t_phaseQ2 = get_sig(pulse, signals['IC_delta_phi_toro_Q2_Top_LmR'], do_smooth=True) 
# phaseQ4, t_phaseQ4 = get_sig(pulse, signals['IC_delta_phi_toro_Q4_Top_LmR'], do_smooth=True)
phaseQ2, t_phaseQ2 = get_sig(pulse, signals['IC_Phase_Q2']) 
phaseQ4, t_phaseQ4 = get_sig(pulse, signals['IC_Phase_Q4'])

#%% 
fig, ax = plt.subplots(3,1,sharex=True)
ax[0].plot(t_Ip, Ip, lw=2)
ax2 = ax[0].twinx()
ax[0].set_ylabel('Ip [kA]', fontsize=14, color='C0')
ax[0].tick_params(color='C0', labelcolor='C0')
ax[0].set_xlim(-0.1, 16)
ax[0].set_title(f'WEST #{pulse}', fontsize=14)

ax2.plot(t_nl, nl, lw=2, color='C1')
ax2.set_ylabel('nl [$10^{19}$ $m^{-3}$]', fontsize=14, color='C1')
ax2.tick_params(color='C1', labelcolor='C1')

ax[1].plot(t_Q4, P_Q4, label='IC Q4', lw=2, color='C2')
ax[1].plot(t_Prad, Prad*1e3, label='Prad (tot)')
ax[1].plot(t_Prad_bulk, Prad_bulk*1e3, label='Prad (bulk)')

ax[1].set_ylim(0, 1300)
ax[1].set_xlabel('Time [s]', fontsize=14)
ax[1].set_ylabel('Power [kW]', fontsize=14)
ax[1].legend(fontsize=12, loc='upper right')

ax[2].plot(t_Rc_Q4, Rc_Q4, label='Rc Q4', lw=2, color='C2')
ax[2].set_ylabel('Rc [Ohm]', fontsize=14)
_ax = ax[2].twinx()
_ax.plot(t_phaseQ4, phaseQ4, lw=2, color='C1')
_ax.set_ylabel('Tor.Phase [deg]', fontsize=14, color='C1')
_ax.tick_params(color='C1', labelcolor='C1')
_ax.set_ylim(0, 360)
[a.grid(True, alpha=0.2) for a in ax]
[a.tick_params(labelsize=14) for a in ax]

fig.tight_layout()

#%%
savefig(f'WEST_IC_{pulse}.png', dpi=150)

#%%
# 
ts = (5.83, 8.34)
_ph, _t = in_between(phaseQ4, t_phaseQ4, t_start=ts[0], t_end=ts[1])
_p, _t_p = in_between(P_Q4, t_Q4, t_start=ts[0], t_end=ts[1])
_prad, _t_prad = in_between(Prad_bulk*1e3, t_Prad_bulk, t_start=ts[0], t_end=ts[1])

_prad = np.interp(_t, _t_prad, _prad.squeeze())
_p = np.interp(_t, _t_p, _p.squeeze())

fig, ax = plt.subplots()
ax.plot(_ph, _prad/_p, '.')
ax.grid(True)
ax.set_xlabel('Phase [deg]', fontsize=14)
ax.set_ylabel('Prad (bulk) / P_RF', fontsize=14)
ax.set_title(f'WEST #{pulse} - Q4', fontsize=14)

#%%
savefig(f'WEST_IC_{pulse}_Prad_vs_phase.png', dpi=150)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 55226
pulse = 55226

Ip, t_Ip = get_sig(pulse, signals['Ip'])
nl, t_nl = get_sig(pulse, signals['nl'])

P_IC_tot, t_tot = get_sig(pulse, signals['IC_P_tot'])
P_Q1, t_Q1 = get_sig(pulse, signals['IC_P_Q1'])
P_Q2, t_Q2 = get_sig(pulse, signals['IC_P_Q2'])
P_Q4, t_Q4 = get_sig(pulse, signals['IC_P_Q4'])

#%%
Rc_Q1_left, t_Rc_Q1_left = get_sig(pulse, signals['IC_Rc_Q1_left'])
Rc_Q1_right, t_Rc_Q1_right = get_sig(pulse, signals['IC_Rc_Q1_right'])

Rc_Q2_left, t_Rc_Q2_left = get_sig(pulse, signals['IC_Rc_Q2_left'])
Rc_Q2_right, t_Rc_Q2_right = get_sig(pulse, signals['IC_Rc_Q2_right'])

Rc_Q4_left, t_Rc_Q4_left = get_sig(pulse, signals['IC_Rc_Q4_left'])
Rc_Q4_right, t_Rc_Q4_right = get_sig(pulse, signals['IC_Rc_Q4_right'])

Rc_Q1, t_Rc_Q1 = get_sig(pulse, signals['IC_Rc_Q1_avg'])
Rc_Q2, t_Rc_Q2 = get_sig(pulse, signals['IC_Rc_Q2_avg'])
Rc_Q4, t_Rc_Q4 = get_sig(pulse, signals['IC_Rc_Q4_avg'])

R_IC, t_R_IC = get_sig(pulse, signals['IC_Positions'])
Rext, t_Rext = get_sig(pulse, signals['Rext_median'])

Prad, t_Prad = get_sig(pulse, signals['Prad'])
Prad_bulk, t_Prad_bulk = get_sig(pulse, signals['Prad_bulk'])

Pohmic, t_Pohmic = get_sig(pulse, signals['Ohmic_P'])

phaseQ2, t_phaseQ2 = get_sig(pulse, signals['IC_delta_phi_toro_Q2_Top_LmR'], do_smooth=True) 
phaseQ4, t_phaseQ4 = get_sig(pulse, signals['IC_delta_phi_toro_Q4_Top_LmR'], do_smooth=True)

V1_Q2, t_V1_Q2 = get_sig(pulse, signals['IC_Voltage_left_upper_Q2'])
V2_Q2, t_V2_Q2 = get_sig(pulse, signals['IC_Voltage_left_lower_Q2'])
V3_Q2, t_V3_Q2 = get_sig(pulse, signals['IC_Voltage_right_upper_Q2'])
V4_Q2, t_V4_Q2 = get_sig(pulse, signals['IC_Voltage_right_lower_Q2'])
Vmax_Q2 = np.max([V1_Q2, V2_Q2, V3_Q2, V4_Q2], axis=0)
Vmin_Q2 = np.min([V1_Q2, V2_Q2, V3_Q2, V4_Q2], axis=0)
Vdelta_Q2 = Vmax_Q2 - Vmin_Q2

dV1V2 = np.abs(V1_Q2 - V2_Q2)
dV3V4 = np.abs(V3_Q2 - V4_Q2)


#%% remove data points where power is 0
idx_P = P_Q2 < 1
idx_V = V4_Q2 < 1

#%% 
fig, ax = plt.subplots(5,1,sharex=True, figsize=(6,8))
# ax[0].plot(t_Ip, Ip, lw=2)
# ax[0].set_ylabel('Ip [kA]', fontsize=14, color='C0')
# ax[0].tick_params(color='C0', labelcolor='C0')
ax[0].set_xlim(4.4, 10)
ax[0].set_title(f'WEST #{pulse}', fontsize=14)
ax[-1].set_xlabel('Time [s]', fontsize=12)

# ax2 = ax[0].twinx()
ax[0].plot(t_nl, nl, lw=2, color='C1')
ax[0].set_ylabel('nl [$10^{19}$ $m^{-3}$]', fontsize=12)
# ax2.tick_params(color='C1', labelcolor='C1')
ax[0].set_ylim(4, 4.6)


ax[1].plot(t_Q2, smooth(P_Q2), label='IC Q2', lw=2, color='C2')
ax[1].plot(t_Prad, Prad*1e3, label='Prad (tot)')
ax[1].set_ylim(0, 1300)
ax[1].set_ylabel('Power [kW]', fontsize=12)
ax[1].legend(fontsize=12, loc='upper right', ncol=1)

ax[2].plot(t_Rc_Q2, smooth(Rc_Q2_left), label='Rc Q4 left', lw=2, color='C0')
ax[2].plot(t_Rc_Q2, smooth(Rc_Q2_right), label='Rc Q4 right', lw=2, color='C1')
ax[2].set_ylabel('Rc [Ohm]', fontsize=12)
ax[2].set_ylim(0, 1)
ax[2].legend(ncol=1)

ax[3].plot(t_phaseQ2, phaseQ2, lw=2, color='C1')
ax[3].set_ylabel('Tor.Phase [deg]', fontsize=12)
ax[3].set_ylim(0, 360)

ax[4].plot(t_V1_Q2, smooth(V1_Q2), label='V1', lw=2)
ax[4].plot(t_V2_Q2, smooth(V2_Q2), label='V2', lw=2)
ax[4].plot(t_V3_Q2, smooth(V3_Q2), label='V3', lw=2)
ax[4].plot(t_V4_Q2, smooth(V4_Q2), label='V4', lw=2)
# # ax[3].plot(t_V4_Q2, Vmax_Q2, label='Vmax', lw=1)
# ax[3].plot(t_V1_Q2, smooth(dV1V2) )
# ax[3].plot(t_V1_Q2, smooth(dV3V4) )
ax[4].legend(ncol=2)
ax[4].set_ylabel('Voltage [kV]', fontsize=12)

[a.grid(True, alpha=0.2) for a in ax]
[a.tick_params(labelsize=14) for a in ax]

fig.tight_layout()
fig.subplots_adjust(hspace=0)
fig.show()

#%%
savefig(f'WEST_IC_{pulse}.png', dpi=150)



#%% filter times where there is not IC power
ts = ((6, 8.35), (8.64, 9.07))
_Prad, _t_Prad = filter_times(Prad, t_Prad, ts)
_Prad_bulk, _t_Prad_bulk = filter_times(Prad_bulk, t_Prad_bulk, ts)
_Pohmic, _t_Pohmic = filter_times(Pohmic, t_Pohmic, ts)

_Vmax, _t_Vmax = filter_times(Vmax_Q2, t_V1_Q2, ts)
_Vdelta, _t_Vdelta = filter_times(Vdelta_Q2, t_V1_Q2, ts)
_P_Q2, _t_P_Q2 = filter_times(P_Q2, t_Q2, ts)
_phaseQ2, _t_phaseQ2  = filter_times(phaseQ2, t_phaseQ2, ts)

_dV1V2, _t_dV1V2 = filter_times(dV1V2, t_V1_Q2, ts)
_dV3V4, _t_dV3V4 = filter_times(dV3V4, t_V3_Q2, ts)


#%%
# smoothing data
__dV1V2 = smooth(_dV1V2)
__dV3V4 = smooth(_dV3V4)
__P_Q2 = smooth(_P_Q2)

# radiated power and voltage does not use the same time base
_Prad_interp = np.interp(_t_Vmax, _t_Prad, _Prad)
_Prad_bulk_interp = np.interp(_t_Vmax, _t_Prad_bulk, _Prad_bulk)
_Pohmic = np.interp(_t_Vmax, _t_Pohmic, _Pohmic)
_P_Q2_interp =  np.interp(_t_Vmax, _t_P_Q2, __P_Q2)
_phaseQ2_interp = np.interp(_t_Vmax, _t_phaseQ2, _phaseQ2)
_nl_interp = np.interp(_t_Vmax, t_nl, nl)

#%%
fig, ax = plt.subplots(5,1,sharex=True)
ax[0].set_xlim(4.4, 10)
ax[0].plot(_t_P_Q2, smooth(_P_Q2), label='IC Q2', lw=2, color='C2')
ax[0].plot(_t_Prad, _Prad*1e3, label='Prad (tot)')
ax[0].plot(_t_Prad_bulk, _Prad_bulk*1e3, label='Prad (bulk)')

ax[0].set_ylim(0, 1300)
ax[0].set_xlabel('Time [s]', fontsize=14)
ax[0].set_ylabel('Power [kW]', fontsize=14)
ax[0].legend(fontsize=12, loc='upper right', ncol=3)

ax[1].plot(_t_phaseQ2, _phaseQ2, lw=2, color='C1')
ax[1].set_ylabel('Tor.Phase [deg]', fontsize=12)
ax[1].set_ylim(0, 360)

#ax[2].plot(_t_Vmax, _Vmax, label='Vmax', lw=1)
ax[2].plot(_t_dV1V2, smooth(_dV1V2), label='|V1-V2|', lw=1)
ax[2].plot(_t_dV3V4, smooth(_dV3V4), label='|V3-V4|', lw=1)
ax[2].legend(ncol=4)

ax[3].plot(t_nl, nl)
ax[3].set_ylabel('nl')
ax[3].set_ylim(4, 4.5)

ax[4].plot(_t_Vmax, _Prad_bulk_interp/(_P_Q2_interp*1e-3 + _Pohmic))
ax[4].set_ylabel('frad (bulk')

[a.grid(True, alpha=0.2) for a in ax]
[a.tick_params(labelsize=14) for a in ax]

fig.tight_layout()
fig.subplots_adjust(hspace=0)
fig.show()


#%%
fig, ax = plt.subplots(1, 2, sharey=True)
cb=ax[0].scatter(__dV1V2, _Prad_bulk_interp/(_P_Q2_interp*1e-3 + _Pohmic), alpha=0.2, c=_phaseQ2_interp)
cb=ax[1].scatter(__dV3V4, _Prad_bulk_interp/(_P_Q2_interp*1e-3 + _Pohmic), alpha=0.2, c=_phaseQ2_interp)
ax[0].set_xlabel('Poloidal Voltage difference |V1-V2| [kV]', fontsize=12)
ax[1].set_xlabel('Poloidal Voltage difference |V3-V4| [kV]', fontsize=12)
        
for a in ax:
    a.set_ylabel('Radiated fraction (P_rad/P_IC)', fontsize=12)
    a.grid()

fig.colorbar(cb)
fig.show()

#%%
fig, ax = plt.subplots()
cb=ax.scatter(_phaseQ2_interp, _Prad_interp/(_P_Q2_interp*1e-3 + _Pohmic), alpha=0.2, c=__dV1V2)
#cb=ax.scatter(_phaseQ2_interp, _Prad_bulk_interp/(_P_Q2_interp*1e-3 + _Pohmic), alpha=0.2, c=__dV3V4)
        
ax.set_xlabel('Toroidal Phase [deg]', fontsize=12)
ax.set_ylabel('Radiated fraction ($P_\mathrm{rad}$/($P_\mathrm{IC}$+$P_\Omega$)', fontsize=12)

fig.colorbar(cb)
fig.show()
fig.savefig(f'WEST_IC_{pulse}_radiatedfraction_vs_toroidal_phase.png', dpi=150)