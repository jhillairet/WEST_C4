# -*- coding: utf-8 -*-
"""
Creating rows to fill correctly the ICRH logbook

@author: JH218595
"""

#%%
import sys; sys.path.append('..')
from control_room import *
from numpy import *
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from scipy.io import loadmat
import pywed as pw
import pandas as pd

#%%
# Getting the antenna radial position, capacitor positions for a given shot
# capacitor positions are given at the beginning of the shot
# deals with shot without ICRH, filling dataframe with '-'
def info_antenna(pulses, antenna='Q1'):
    index_ant = {'Q1':0, 'Q2':1, 'Q4':2}
    positions, cap_pos, frequencies = [], [], []
    cap1s, cap2s, cap3s, cap4s = [], [], [], []

    for pulse in pulses:
        try:
            pos, _ = get_sig(pulse, signals['IC_Positions'])
            positions.append(pos[index_ant[antenna]]*1000) # in [mm]
        except TypeError as e:
            positions.append('-')

        try:            
            cap1, _ = get_sig(pulse, signals[f'IC_Capa_{antenna}_left_upper'])
            cap2, _ = get_sig(pulse, signals[f'IC_Capa_{antenna}_left_lower'])
            cap3, _ = get_sig(pulse, signals[f'IC_Capa_{antenna}_right_upper'])
            cap4, _ = get_sig(pulse, signals[f'IC_Capa_{antenna}_right_lower'])
            cap1s.append(cap1[0])
            cap2s.append(cap2[0])
            cap3s.append(cap3[0])
            cap4s.append(cap4[0])
        except TypeError as e:
            cap1s.append('-')
            cap2s.append('-')
            cap3s.append('-')
            cap4s.append('-')

        try:            
            freq, _ = get_sig(pulse, signals['IC_Frequencies'])
            frequencies.append(freq[index_ant[antenna]])
        except TypeError as e:
            frequencies.append('-')

    df = pd.DataFrame(data={'frequency':frequencies, 'ant_pos':positions, 
                            f'{antenna}-C1':cap1s, f'{antenna}-C2':cap2s, 
                            f'{antenna}-C3':cap3s, f'{antenna}-C4':cap4s}, 
                    index=pulses)       
        
    return df
#%%
pulses = [55739, 55740, 55741, 55742, 55743, 55744, 55745]
pulses = [55724, 55725, 55728, 55731]
pulses = [55676, 55677, 55678, 55679, 55680, 55681, 55682]
pulses = [55706, 55707, 55708, 55709, 55710, 55711, 55712,
          55713, 55714, 55715, 55718, 55720, 55721, 55722,
          55723, 55724, 55725, 55728, 55729, 55730, 55731]

pulses = [55628, 55629, 55630, 55631, 55632, 55633, 55634,
          55635, 55636, 55637, 55638, 55639, 55640, 55643, 
          55644, 55646]

#%%
df_Q1 = info_antenna(pulses, antenna='Q1')
df_Q2 = info_antenna(pulses, antenna='Q2')
df_Q4 = info_antenna(pulses, antenna='Q4')
df = pd.concat([df_Q1, df_Q2, df_Q4], axis=1)
#%% export to excel for easy copy/paste
df.to_excel('__logbook.xlsx', )