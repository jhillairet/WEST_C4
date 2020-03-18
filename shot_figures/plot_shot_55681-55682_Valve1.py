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


pulse = 55681
# reflectometry timings for average
ts = [(3.6, 3.7),  # before IC
      (4.0, 4.2),  # IC low power plateau
      (5.2, 5.4),  # Gaz puff max
      ]


#%%
pulse = [55681, 55682]

#%%
sigs = [signals['IC_P_Q2'],
        signals['IC_Rc_Q2_avg'],
        signals['Valve1']
        ]
fig, axes = scope(pulses, sigs, do_smooth=False, cycling_mode='ls')
#axes[-1].set_xlim(3.5, 6.5)
axes[0].legend()

# add gas flow rate in el/s 
ax2 = axes[2].twinx()
ax2.set_ylabel('[el/s]',fontsize=12) 
ymin, ymax = axes[2].get_ylim()
ax2.set_ylim((Pam3s_to_els(ymin), Pam3s_to_els(ymax)))

# add reflectometry data shading
for idx, (t_start, t_stop) in enumerate(ts):
    for a in axes:
        a.axvspan(t_start, t_stop, alpha=0.2, color=f'C{idx}')

# increase font
[a.yaxis.label.set_size(12) for a in axes]
axes[0].set_xlim(1, 6.8)
fig.tight_layout()


#%%
fig.savefig('IC_GasPuff_55681-55682.png', dpi=150)


#%%
pulse = 55682
data = loadmat(f'../reflectometry/profiles/WEST_{pulse}_prof.mat')

# %%
fig, ax = plt.subplots()
t_ignitron = tignitron(pulse)[0]
# Antenna position
Rant = get_sig(pulse, signals['IC_Positions'])[0][0]

for (t_start, t_stop) in ts:
    # ne and r mean, error bar repr with std
    r, rs, ne, nes = time_averaged_profile(data, t_start, t_stop, t_init=t_ignitron)
    
    ax.fill_betweenx(ne, r-rs, r+rs, alpha=.4)
    ax.plot(r, ne, lw=2, label=f'{t_start}-{t_stop}')

ax.legend()
ax.set_yscale('log')
ax.set_xlim((2.84, 2.98))
ax.grid(True)
ax.grid(True, which='minor', alpha=0.5)
ax.axvline(Rant, color='k')
ax.set_ylabel('Density [$m^{-3}$]', fontsize=12)
ax.set_xlabel('Radius [m]', fontsize=12)
ax.set_title(f'WEST #{pulse} Valve#1')

fig.savefig(f'WEST_IC_{pulse}_profiles.png', dpi=150)
     
#%%
# plot R(nco) vs time
fig, ax = plt.subplots()

nco = 1e19

pulses = [55681, 55682]
for idx, pulse in enumerate(pulses):
    data = loadmat(f'../reflectometry/profiles/WEST_{pulse}_prof.mat')

    idx_nco = np.argmin(abs(data['NEX'] - 1e19), axis=0)
    
    Dext = Rant*1e3 - Rext

    Dco = (Rant - data['RX'][idx_nco][0] )* 1e3
    
    ax.plot(data['tX'].squeeze() - t_ignitron, Dco, alpha=0.2, color=f'C{idx}')
    ax.plot(data['tX'].squeeze() - t_ignitron, smooth(Dco), label=f'Dco [mm] #{pulse}', color=f'C{idx}')

# add reflectometry data shading
for idx, (t_start, t_stop) in enumerate(ts):
    # for a in axes:
    ax.axvspan(t_start, t_stop, alpha=0.2, color=f'C{idx}')

ax.set_xlabel('Time [s]', fontsize=14)
ax.legend()
#%%
savefig(f'WEST_IC_{pulses}_Dco.png', dpi=150)








