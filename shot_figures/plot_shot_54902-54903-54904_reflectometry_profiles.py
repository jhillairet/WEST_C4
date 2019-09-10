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

pulses = [54902, 54903, 54904]
#%%
sigs = [
        signals['Ip'],
        signals['nl'],
        signals['Rext_median'],
        signals['IC_P_tot'],
        ]
fig, axes = scope(pulses, sigs, do_smooth=True, lw=2, alpha=0.8)
axes[0].set_xlim(0, 13)
axes[2].set_ylim(2910, 2950)
axes[0].set_title(f'WEST #54902-54903', fontsize=12)
axes[0].legend()
fig.tight_layout()
