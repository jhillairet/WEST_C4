# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 10:52:25 2019

@author: JH218595
"""

#%%
import sys; sys.path.append('..')
from control_room import *
import matplotlib.pyplot as plt
from scipy.io import loadmat

#%%
pulse = 54453 

#%%
P_Q2, t_P_Q2 = get_sig(pulse, signals['IC_P_Q2'])
P_Q4, t_P_Q4 = get_sig(pulse, signals['IC_P_Q4'])
Rc_Q2, t_Rc_Q2 = get_sig(pulse, signals['IC_Rc_Q2_avg'])
Rc_Q4, t_Rc_Q4 = get_sig(pulse, signals['IC_Rc_Q2_avg'])

#%%
fig, ax = plt.subplots()
ax.fill_between(t_P_Q2, np.squeeze(P_Q2 + P_Q4)/1e3, alpha=0.2, label='Total')
ax.plot(t_P_Q2, P_Q2/1e3, lw=2, label='Q2')
ax.plot(t_P_Q4, P_Q4/1e3, lw=2, label='Q4')
ax.set_xlabel('Time [s]', fontsize=14)
ax.set_ylabel('Transmitted Power [MW]', fontsize=14)
ax.set_xlim(3.9, 5.2)
ax.legend(fontsize=14, loc='upper left')
ax.set_title(f'WEST #{pulse}')
ax.tick_params(labelsize=12)
#%%
fig.savefig(f'WEST_{pulse}_P_IC.png', dpi=150)


#%%
file_54453 = '../reflectometry/profiles/WEST_54453_prof.mat'
data_54453 = loadmat(file_54453)

#%%
def time_averaged_profile(data, t_start, t_end):
    idx_t_start = argmin(abs(data['tX'] - t_start))
    idx_t_stop = argmin(abs(data['tX'] - t_end))
    
    m = mean(data['NEX'][idx_t_start:idx_t_stop,:], axis=0)
    s = std(data['NEX'][idx_t_start:idx_t_stop,:], axis=0)
    r = mean(data['RX'][idx_t_start:idx_t_stop,:], axis=0)
    return m, s, r
    
    
#%%
m1, s1, r1 = time_averaged_profile(data_54453, 3.0, 4.0) # no IC
m2, s2, r2 = time_averaged_profile(data_54453, 4.07, 4.5) # IC ramp-up
m3, s3, r3 = time_averaged_profile(data_54453, 4.6, 4.8) # IC plateau

fig, ax = plt.subplots()
ax.fill_between(r1, m1-s1, m1+s1, alpha=.4)
ax.plot(r1, m1, lw=2, label='3.0-4.0 s (no IC)')
ax.fill_between(r2, m2-s2, m2+s2, alpha=.4)
ax.plot(r2, m2, lw=2, label='4.07-4.5 (IC ramp-up)')
ax.fill_between(r3, m3-s3, m3+s3, alpha=.4)
ax.plot(r3, m3, lw=2, label='4.6-4.8 (IC 1.3 MW)')

ax.set_yscale('log')
ax.legend(fontsize=14)
ax.set_xlim((2.96, 3.02))
ax.grid(True)
ax.grid(True, which='minor', alpha=0.5)
ax.axvline(3.011, color='k')
ax.set_ylabel('Density $n_e$ [$m^{-3}$]', fontsize=14)
ax.set_xlabel('Radius [m]', fontsize=14)
ax.tick_params(labelsize=12)
ax.set_title(f'WEST #{pulse}')

#%%
fig.savefig(f'WEST_{pulse}_reflectometry.png', dpi=150)