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
#ax1.plot(t_Q4, P_max, color='r')
ax1.set_ylabel('P RF [kW]')

#ax2.plot(t_Rc_Q4, Rc_Q4)
ax2.plot(t_Rc_Q4_left, Rc_Q4_left, label='Rc Q4 left', lw=2)
ax2.plot(t_Rc_Q4_right, Rc_Q4_right, label='Rc Q4 right', lw=2)
ax2.set_ylabel('Rc [Ohm]')
ax2.legend(fontsize=12, loc='upper left') 

ax3.plot(t_Rext, R_IC[2]*1e3 - Rext)
ax3.set_ylim(8, 45)
ax3.set_title('R_ant - R_ext_median')
ax3.set_ylabel('[mm]')

ax1.set_xlim(3.5, 13)
[ax.grid(True, alpha=0.2) for ax in (ax1, ax2, ax3)]
[ax.tick_params(labelsize=14) for ax in (ax1, ax2, ax3)]
ax1.legend(fontsize=12, loc='upper left') 

ax1.set_title(f'WEST #{pulse}', fontsize=12)
ax3.set_xlabel('Time [s]', fontsize=12)

#for idx, (t_start, t_stop) in enumerate(ts):
#    [a.axvspan(t_start, t_stop, alpha=.2, color=f'C{idx}') for a in (ax1, ax2)]


fig.subplots_adjust(hspace=0)
fig.tight_layout()
fig.show()
#%%
savefig(f'WEST_IC_{pulse}.png', dpi=150)


#%% Display electric field 
do_smooth=False
P_Q4, t_Q4 = get_sig(pulse, signals['IC_P_Q4'])
P_Q4_PCS, P_Q4_PCS_t = get_sig(pulse, signals['IC_PCS_Power_Q4'])

Q4_V1, Q4_V1_t = get_sig(pulse, signals['IC_Voltage_left_upper_Q4'], do_smooth=do_smooth)
Q4_V2, Q4_V2_t = get_sig(pulse, signals['IC_Voltage_left_lower_Q4'], do_smooth=do_smooth)
Q4_V3, Q4_V3_t = get_sig(pulse, signals['IC_Voltage_right_upper_Q4'], do_smooth=do_smooth)
Q4_V4, Q4_V4_t = get_sig(pulse, signals['IC_Voltage_right_lower_Q4'], do_smooth=do_smooth)

Q4_I1, Q4_I1_t = get_sig(pulse, signals['IC_Current_left_upper_Q4'], do_smooth=do_smooth)
Q4_I2, Q4_I2_t = get_sig(pulse, signals['IC_Current_left_lower_Q4'], do_smooth=do_smooth)
Q4_I3, Q4_I3_t = get_sig(pulse, signals['IC_Current_right_upper_Q4'], do_smooth=do_smooth)
Q4_I4, Q4_I4_t = get_sig(pulse, signals['IC_Current_right_lower_Q4'], do_smooth=do_smooth)

max_I, max_V = 915, 27.8

Q4_VSWR_L, Q4_VSWR_L_t = get_sig(pulse, signals['IC_VSWR_Q4_left'])
Q4_VSWR_R, Q4_VSWR_R_t = get_sig(pulse, signals['IC_VSWR_Q4_right'])

limit = (Q4_V1 > max_V) | (Q4_V2 > max_V) | (Q4_V3 > max_V) | (Q4_V4 > max_V)
idx_limit = np.where(limit)


#%%
alpha = 0.4
color='gray'
fig, ax = plt.subplots(3,1, sharex=True, figsize=(6,8))
ax[0].plot(t_Q4, P_Q4/1e3, label='IC Q4 Coupled', lw=2)
ax[0].plot(P_Q4_PCS_t, P_Q4_PCS/1e3, label='IC Q4 Request', 
           lw=2, ls='--', color='DarkBlue')
# make shading when voltage higher than limit (power feedback)
ax[0].fill_between(Q4_V1_t,  np.full_like(Q4_V1, 3), where=limit, color=color, alpha=alpha)
ax[0].set_ylim(0,2.05)
ax[0].set_ylabel('Power [MW]', fontsize=12)
ax[0].set_xlim(8.5, 12.5)
ax[0].legend()

ax[1].axhline(max_V, color='k', lw=2, alpha=0.5)
# ax[1].plot(Q4_V1_t, Q4_V1, label='V1')
# ax[1].plot(Q4_V2_t, Q4_V2, label='V2')
# ax[1].plot(Q4_V3_t, Q4_V3, label='V3')
# ax[1].plot(Q4_V4_t, Q4_V4, label='V4')
ax[1].plot(Q4_V1_t, np.max((Q4_V1,Q4_V2,Q4_V3,Q4_V4),axis=0), 
           label='Max Voltage', color='C3')

ax[1].fill_between(Q4_V1_t,  np.full_like(Q4_V1, 40), where=limit, color=color, alpha=alpha)
ax[1].set_ylabel('Voltage [kV]', fontsize=12)
ax[1].legend(loc='upper left', ncol=2)

ax[2].plot(t_Rc_Q4_left, Rc_Q4_left, label='Rc Q4 left', lw=2)
ax[2].plot(t_Rc_Q4_right, Rc_Q4_right, label='Rc Q4 right', lw=2)
ax[2].fill_between(Q4_V1_t,  np.full_like(Q4_V1, 2), where=limit, color=color, alpha=alpha)
ax[2].set_ylabel('Rc [Ohm]')
ax[2].set_ylim(0.5, 1.4)
ax[2].legend(loc='upper left') 
ax[2].set_ylabel('Rc [$\Omega$]', fontsize=12)

fig.tight_layout()
fig.subplots_adjust(hspace=0)
fig.show()
#%%
fig.savefig(f'WEST_IC_{pulse}_2.png', dpi=150)

#%%
# impurities
P_Ohmic, P_Ohmic_t = get_sig(pulse, signals['Ohmic_P'])
P_IC_tot, P_IC_tot_t = get_sig(pulse, signals['IC_P_tot'])
P_LH_tot, P_LH_tot_t = get_sig(pulse, signals['LH_P_tot'])
P_rad, P_rad_t = get_sig(pulse, signals['Prad'])
P_rad_bulk, P_rad_bulk_t = get_sig(pulse, signals['Prad_bulk'])
# radiated fraction
Ptot = np.interp(P_rad_bulk_t, P_Ohmic_t, P_Ohmic) +\
        np.interp(P_rad_bulk_t, P_IC_tot_t, P_IC_tot/1e3) +\
        np.interp(P_rad_bulk_t, P_LH_tot_t, P_LH_tot) 
frad_bulk = P_rad_bulk / Ptot
frad = P_rad / Ptot

#%%
fig, ax = plt.subplots()
ax.plot(P_rad_bulk_t, frad_bulk)
ax.plot(P_rad_t, frad)
ax.set_ylim(0,1)

#%%
fig, ax = plt.subplots()
ax.plot(P_Ohmic_t, P_Ohmic, label='Ohmic')
ax.plot(P_LH_tot_t, P_LH_tot, label='LH')
ax.plot(P_IC_tot_t, P_IC_tot/1e3, label='IC')
ax.plot(P_rad_t, P_rad, label='radiated')
ax.plot(P_rad_bulk_t, P_rad_bulk, label='radiated bulk')
ax.set_ylim(0,6)
ax.legend()
