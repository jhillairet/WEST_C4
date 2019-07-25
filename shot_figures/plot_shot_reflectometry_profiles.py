# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 10:27:26 2019

@author: JH218595
"""
#%%
import sys; sys.path.append('..')
from control_room import *
from numpy import *
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from scipy.io import loadmat

#%%
pulse = 54525

P_IC, t_P_IC= get_sig(pulse, signals['IC_P_tot'])
nl, t_nl = get_sig(pulse, signals['nl'])


#%%
(td1, tf1) = (3.5, 3.75)
(td2, tf2) = (6.4, 6.70)
(td3, tf3) = (4.6, 4.90)

#%%
fig, ax = plt.subplots(2, 1, sharex=True)
ax[0].plot(t_nl, nl, lw=2, label=f'nl - #{pulse}' - )
ax.plot(t_P_IC, P_IC, lw=2, label=f'IC - #{pulse}')
         
ax.set_xlabel('t [s]', fontsize=14)
ax.set_title(f'WEST #{pulse}')
ax.set_ylabel('Power [kW]', fontsize=14) 
ax.set_xlim(2, 7)
ax.grid(True, alpha=.4) 
ax.tick_params(labelsize=12)

ax.axvspan(td1, tf1, color='C0', alpha=.2)
ax.axvspan(td2, tf2, color='C1', alpha=.2)
ax.axvspan(td3, tf3, color='C2', alpha=.2)

fig.subplots_adjust(hspace=0)


#%%
file = f'../reflectometry/profiles/WEST_{pulse}_prof.mat'

data = loadmat(file)

#%%
def time_averaged_profile(data, t_start, t_end):
    idx_t_start = argmin(abs(data['tX'] - t_start))
    idx_t_stop = argmin(abs(data['tX'] - t_end))
    
    ne_mean = mean(data['NEX'][idx_t_start:idx_t_stop,:], axis=0)
    ne_std = std(data['NEX'][idx_t_start:idx_t_stop,:], axis=0)
    r_mean = mean(data['RX'][idx_t_start:idx_t_stop,:], axis=0)
    r_std = std(data['RX'][idx_t_start:idx_t_stop,:], axis=0)

    return r_mean, r_std, ne_mean, ne_std

#%% ne and r mean, error bar repr with std
r1, rs1, ne1, nes1 = time_averaged_profile(data, td1, tf1)
r2, rs2, ne2, nes2 = time_averaged_profile(data, td2, tf2)
r3, rs3, ne3, nes3 = time_averaged_profile(data, td3, tf3)


# %%
fig, ax = plt.subplots()

ax.fill_betweenx(ne1, r1-rs1, r1+rs1, alpha=.4)
ax.plot(r1, ne1, lw=2, label=f'#{pulse} - {td1}-{tf1} s')
ax.fill_betweenx(ne3, r3-rs3, r3+rs3, alpha=.4)
ax.plot(r3, ne3, lw=2, label=f'#{pulse} - {td2}-{tf2} s')
        
ax.fill_betweenx(ne2, r2-rs2, r2+rs2, alpha=.4)
ax.plot(r2, ne2, lw=2, label=f'#{pulse} - {td3}-{tf3} s')


ax.legend()
ax.set_yscale('log')
ax.set_xlim((2.96, 3.02))
ax.grid(True)
ax.grid(True, which='minor', alpha=0.5)
ax.axvline(3.011, color='k')
ax.axvline(3.014, color='grey')
ax.axvline(3.016, color='darkgrey')
ax.set_ylabel('Density [$m^{-3}$]', fontsize=12)
ax.set_xlabel('Radius [m]', fontsize=12)


#%% superpose all traces
fig, ax = plt.subplots()

# Without Heating
idx_t_start = argmin(abs(data_54461['tX'] - t_start_wo))
idx_t_stop = argmin(abs(data_54461['tX'] - t_stop_wo))

for id in range(idx_t_start, idx_t_stop):
    ax.plot(data_54461['RX'][id,:], 
            data_54461['NEX'][id,:], 
            label='54461 - no heating', 
            lw=2, alpha=.2, color="C0")

# IC and LH
idx_t_start = argmin(abs(data_54461['tX'] - t_start))
idx_t_stop = argmin(abs(data_54461['tX'] - t_stop))

for id in range(idx_t_start, idx_t_stop):
    ax.plot(data_54461['RX'][id,:], 
            data_54461['NEX'][id,:], 
            label='54461 - IC and LH', 
            lw=2, alpha=.2, color="C1")

# LH only
idx_t_start = argmin(abs(data_54462['tX'] - t_start))
idx_t_stop = argmin(abs(data_54462['tX'] - t_stop))

for id in range(idx_t_start, idx_t_stop):
    ax.plot(data_54462['RX'][id,:], 
            data_54462['NEX'][id,:], 
            label='54462 - LH only', 
            lw=2, alpha=.2, color="C2")
    
ax.set_yscale('log')
ax.set_xlim((2.96, 3.02))
ax.set_ylim(1e17, 4e19)
ax.grid(True)
ax.grid(True, which='minor', alpha=0.5)
ax.axvline(3.011, color='k')
ax.set_ylabel('Density [$m^{-3}$]', fontsize=12)
ax.set_xlabel('Radius [m]', fontsize=12)

µ#%%
r_min, ne_min, r_max, ne_max = time_averaged_profile2(data_54461, 4.0, 4.25)

ax.fill(np.append(r_min, r_max[::-1]), 
        np.append(ne_min, ne_max[::-1]))
#%%
ax.plot(r_min, ne_min, c='r')
ax.plot(r_max, ne_max, c='r')


#%%
fig, ax = plt.subplots()

r_min, ne_min, r_max, ne_max = time_averaged_profile2(data_54461, 2.5, 2.75)

ax.fill(np.append(r_min, r_max[::-1]), 
        np.append(ne_min, ne_max[::-1]))

r_min, ne_min, r_max, ne_max = time_averaged_profile2(data_54462, 2.5, 2.75)

ax.fill(np.append(r_min, r_max[::-1]), 
        np.append(ne_min, ne_max[::-1]))

r_min, ne_min, r_max, ne_max = time_averaged_profile2(data_54461, 3.5, 3.75)

ax.fill(np.append(r_min, r_max[::-1]), 
        np.append(ne_min, ne_max[::-1]))

r_min, ne_min, r_max, ne_max = time_averaged_profile2(data_54462, 3.5, 3.75)

ax.fill(np.append(r_min, r_max[::-1]), 
        np.append(ne_min, ne_max[::-1]))

#%%
fig, ax = plt.subplots()

ax.fill_between(r1, m1-s1, m1+s1, alpha=.2)
ax.plot(r1, m1, lw=2, ls='--', label='54461 - no power')
ax.fill_between(r2, m2-s2, m2+s2, alpha=.2)
ax.plot(r2, m2, lw=2, ls='--', label='54462 - no power')

ax.fill_between(r3, m3-s3, m3+s3, alpha=.2)
ax.plot(r3, m3, lw=2, ls='-', label='54461 - LH and IC')
ax.fill_between(r4, m4-s4, m4+s4, alpha=.2)
ax.plot(r4, m4, lw=2, ls='-', label='54462 - LH only')


xlim((2.96, 3.02))
yscale('log')
legend()
grid(True)
grid(True, which='minor', alpha=0.5)
axvline(3.011, color='k')
ylabel('Density [$m^{-3}$]', fontsize=12)
xlabel('Radius [m]', fontsize=12)

title('WEST 54461-54462', fontsize=12)

#%%
figure()

idx_t54461 = argmin(abs(data_54461['tX'] - 5.0))
idx_t54462 = argmin(abs(data_54462['tX'] - 4.0))
plot(data_54461['RX'][idx_t54461,:], data_54461['NEX'][idx_t54461,:], label='54461 (4s)- LH (300 kW) and IC  (1.5MW) ', lw=2)
plot(data_54462['RX'][idx_t54462,:], data_54462['NEX'][idx_t54462,:], label='54462 (4s)- LH only (500kW)', lw=2)
 
 
idx_t54461 = argmin(abs(data_54461['tX'] - 5))
idx_t54462 = argmin(abs(data_54462['tX'] - 5))
plot(data_54461['RX'][idx_t54461,:], data_54461['NEX'][idx_t54461,:], label='54461 (5s) - no heating ', ls='--')
plot(data_54462['RX'][idx_t54462,:], data_54462['NEX'][idx_t54462,:], label='54462 (5s) - no heating ', ls='--')

xlim((2.96, 3.02))
yscale('log')
legend()
grid(True)
grid(True, which='minor', alpha=0.5)
axvline(3.011, color='k')
ylabel('Density [$m^{-3}$]', fontsize=12)
xlabel('Radius [m]', fontsize=12)