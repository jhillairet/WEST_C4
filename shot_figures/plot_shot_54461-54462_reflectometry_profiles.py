# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 10:27:26 2019

@author: JH218595
"""
from numpy import *
from matplotlib.pyplot import *

from scipy.io import loadmat
#%%
figure()

idx_t54461 = argmin(abs(data_54461['tX'] - 4.0))
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