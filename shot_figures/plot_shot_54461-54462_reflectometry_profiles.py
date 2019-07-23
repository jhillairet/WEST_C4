# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 10:27:26 2019

@author: JH218595
"""
#%%
from numpy import *
from matplotlib.pyplot import *
from scipy.io import loadmat

#%%
P_IC_54461, t_P_IC_54461 = get_sig(54461, signals['IC_P_tot'])
P_LH_54461, t_P_LH_54461 = get_sig(54461, signals['LH_P_tot'])
P_IC_54462, t_P_IC_54462 = get_sig(54462, signals['IC_P_tot'])
P_LH_54462, t_P_LH_54462 = get_sig(54462, signals['LH_P_tot'])


#%%
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
ax1.plot(t_P_LH_54461, P_LH_54461, lw=2, label='54461')
ax1.plot(t_P_LH_54462, P_LH_54462, lw=2, label='54462')

ax2.plot(t_P_IC_54461, P_IC_54461, lw=2, label='54461')
ax2.plot(t_P_IC_54462, P_IC_54462, lw=2, label='54462')

ax2.set_xlabel('t [s]', fontsize=14)
ax2.set_xlim(2.4, 4.6)
ax1.set_title(f'WEST 54461-54462')
[a.set_ylabel('Power [kW]', fontsize=14) for a in (ax1, ax2)]
[a.grid(True, alpha=.4) for a in (ax1, ax2)]
[a.tick_params(labelsize=12) for a in (ax1, ax2)]

[a.axvspan(2.5, 2.75, color='grey', alpha=.2) for a in (ax1, ax2)]
[a.axvspan(3.5, 3.75, color='grey', alpha=.2) for a in (ax1, ax2)]

fig.subplots_adjust(hspace=0)
#%%
fig.savefig('WEST_54461-54462.png', dpi=150)

#%%
file_54445 = '../reflectometry/profiles/WEST_54461_prof.mat'
file_54462 = '../reflectometry/profiles/WEST_54462_prof.mat'

data_54461 = loadmat(file_54461)
data_54462 = loadmat(file_54462)


#%%
def time_averaged_profile(data, t_start, t_end):
    idx_t_start = argmin(abs(data['tX'] - t_start))
    idx_t_stop = argmin(abs(data['tX'] - t_end))
    
    m = mean(data['NEX'][idx_t_start:idx_t_stop,:], axis=0)
    s = std(data['NEX'][idx_t_start:idx_t_stop,:], axis=0)
    r = mean(data['RX'][idx_t_start:idx_t_stop,:], axis=0)
    return m, s, r

#%%
def time_averaged_profile2(data, t_start, t_end):
    idx_t_start = argmin(abs(data['tX'] - t_start))
    idx_t_stop = argmin(abs(data['tX'] - t_end))
    
    ne_min = amin(data['NEX'][idx_t_start:idx_t_stop,:], axis=0)
    ne_max = amax(data['NEX'][idx_t_start:idx_t_stop,:], axis=0)
    r_min = amin(data['RX'][idx_t_start:idx_t_stop,:], axis=0)
    r_max = amin(data['RX'][idx_t_start:idx_t_stop,:], axis=0)

    return r_min, ne_min, r_max, ne_max

#%%
m1, s1, r1 = time_averaged_profile(data_54461, 2.5, 2.75)
m3, s3, r3 = time_averaged_profile(data_54461, 3.5, 3.75)

m2, s2, r2 = time_averaged_profile(data_54462, 2.5, 2.75)
m4, s4, r4 = time_averaged_profile(data_54462, 3.5, 3.75)

#%%
t_start = 4
t_stop = 4.25
idx_t_start = argmin(abs(data['tX'] - t_start))
idx_t_stop = argmin(abs(data['tX'] - t_end))
fig, ax = plt.subplots()

for id in range(idx_t_start, idx_t_stop):
    ax.plot(data_54461['RX'][id,:], 
            data_54461['NEX'][id,:], 
            label='54461 (4s)- LH (300 kW) and IC  (1.5MW) ', 
            lw=2, alpha=.1, color="C0")
#%%
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