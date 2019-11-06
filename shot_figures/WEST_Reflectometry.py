#!/usr/bin/env python
# coding: utf-8
from scipy.io import savemat
import imas_west

pulse = 55564
output = imas_west.get(pulse, 'reflectometer_profile')

tX = output.time
RX = output.channel[0].position.r.data
NEX = output.channel[0].n_e.data

savemat(f'../reflectometry/profiles/WEST_{pulse}_prof.mat', {'tX':tX, 'RX':RX, 'NEX':NEX})

#reflec = imas_west.get(pulse, 'reflectometer_profile')

#plot(reflec.channel[0].position.r.data, reflec.channel[0].n_e.data)
#yscale('log')


# In[ ]:




