from scipy.signal import savgol_filter
import numpy as np
import matplotlib.pyplot as plt
import pywed as pw
import pandas as pd
import paramiko
import os
import json
from itertools import cycle
from scipy.io import loadmat
from scipy.constants import m_p, pi, e, epsilon_0, c 
    
signals = {
    ## Shot properties
    'Datetime': {'name': None, 'fun': 'pulse_datetime', 'unit':'', 'label':'pulse datetime'},
    'year': {'name':None, 'fun': 'pulse_year', 'unit':'', 'label': 'pulse year'},
    'month': {'name':None, 'fun': 'pulse_month', 'unit':'', 'label': 'pulse month'},
    'day': {'name':None, 'fun': 'pulse_day', 'unit':'', 'label': 'pulse day'},
    ## Magnetics
    'Ip': {'name': 'SMAG_IP', 'unit': 'kA', 'label': 'Plasma current'},
    'Vloop': {'name': None, 'fun':'Vloop', 'unit': 'V', 'label': 'Loop voltage'},
    'Ohmic_P': {'name': None, 'fun':'Ohmic_power', 'unit':'MW', 'label':'Ohmic Power'},
    'Separatrix_P': {'name':None, 'fun':'Separatrix_power', 'unit':'MW', 'label':'Power at separatrix', 'options':{'ylim':(0, 5)}},
    'Te': {'name':None, 'fun':'get_Te', 'unit':'eV', 'label':'Te Central',  },
    'Rext_upper': {'name': 'GMAG_TEST%1', 'unit': 'mm', 'label': 'Rext at Z=+250 mm'},  # Rext upper
    'Rext_median': {'name': 'GMAG_TEST%2', 'unit': 'mm', 'label': 'Rext median', 'options':{'ylim':(2900, 2950)}},  # Rext median
    'Rext_lower': {'name': 'GMAG_TEST%3', 'unit': 'mm', 'label': 'Rext at Z=-250 mm'},  # Rext lower
    'Rext_upper_NICE': {'name':None, 'fun':'Rext_upper_nice', 'unit':'mm', 'label':'Rext at Z=+250 mm (NICE)'},
    'Rext_median_NICE': {'name':None, 'fun':'Rext_median_nice', 'unit':'mm', 'label':'Rext median (NICE)', 'options':{'ylim':(2900, 2950)}},
    'Rext_lower_NICE': {'name':None, 'fun':'Rext_lower_nice', 'unit':'mm', 'label':'Rext at Z=-250 mm (NICE)'},
    'Dext_Q1': {'name': None, 'fun':'Dext_Q1', 'unit': 'mm', 'label': 'Radial Gap with Q1', 'options':{'ylim':(0, 60)}},
    'Dext_Q2': {'name': None, 'fun':'Dext_Q2', 'unit': 'mm', 'label': 'Radial Gap with Q2', 'options':{'ylim':(0, 60)}},
    'Dext_Q4': {'name': None, 'fun':'Dext_Q4', 'unit': 'mm', 'label': 'Radial Gap with Q4', 'options':{'ylim':(0, 60)}},
    'Dext_LH1': {'name': None, 'fun':'Dext_LH1', 'unit': 'mm', 'label': 'Radial Gap with LH1', 'options':{'ylim':(0, 60)}},
    'Dext_LH2': {'name': None, 'fun':'Dext_LH2', 'unit': 'mm', 'label': 'Radial Gap with LH2', 'options':{'ylim':(0, 60)}},
    'Zgeo': {'name': 'GMAG_BARY%2', 'unit': 'm', 'label': 'Zgeo'},  # Zgeo barycentre
    'R0': {'name': 'GMAG_BARY%1', 'unit': 'm', 'label': 'Large radius'},  # grand rayon
    'Ignitron': {'name' : None, 'fun': 'tignitron', 'unit': 's', 'label': 'Ignitron Time'},
    'Neutron1': {'name': 'GFLUNTN%1', 'unit': 'N/s', 'label':'Neutron#1', 'options':{'ymin':10}},
    'Neutron2': {'name': 'GFLUNTN%2', 'unit': 'N/s', 'label':'Neutron#2', 'options':{'ymin':10}},
    # Movable limiter position (LPA)
    'LPA': {'name': 'GMAG_POSLPA%1', 'unit': 'm', 'label': 'LPA'},
    ## Fueling
    'nl': {'name': 'GINTLIDRT%3', 'unit': '$m^{-2}$', 'label': 'Line integrated density'},
    'Valve1': {'name': 'GDEBIT%1', 'unit': '$Pa.m^3/s$', 'label': 'Valve#1 (LH1)'},
    'Valve2': {'name': 'GDEBIT%2', 'unit': '$Pa.m^3/s$', 'label': 'Valve#2 (LH2)'},
    'Valve7': {'name': 'GDEBIT%7', 'unit': '$Pa.m^3/s$', 'label': 'Valve#7 (LPA)'},
    'Valve8': {'name': 'GDEBIT%8', 'unit': '$Pa.m^3/s$', 'label': 'Valve#8 (Q4)'},
    'Valve9': {'name': 'GDEBIT%9', 'unit': '$Pa.m^3/s$', 'label': 'Valve#9 (Q1)'},
    'Valve10': {'name': 'GDEBIT%10', 'unit': '$Pa.m^3/s$', 'label': 'Valve#10 (Q2)'},
    'Valve11': {'name': 'GDEBIT%11', 'unit': '$Pa.m^3/s$', 'label': 'Valve#11 (up.divertor)'},
    'Valve21': {'name': 'GDEBIT%21', 'unit': '$Pa.m^3/s$', 'label': 'Valve#21'},
    ## RF
    'RF_P_tot': {'name':None, 'fun':'RF_P_tot', 'unit':'MW', 'label':'Total RF Power'},
    ## ICRH
    # IC coupled powers
    'IC_P_tot': {'name': 'SICHPTOT', 'unit': 'kW', 'label': 'IC total coupled power'},
    'IC_P_tot2': {'name': None, 'fun':'sum_power', 'unit': 'kW', 'label': 'IC total coupled power'},
    'IC_P_Q1': {'name': 'SICHPQ1', 'unit': 'kW', 'label': 'IC Q1 coupled power'},
    'IC_P_Q2': {'name': 'SICHPQ2', 'unit': 'kW', 'label': 'IC Q2 coupled power'},
    'IC_P_Q4': {'name': 'SICHPQ4', 'unit': 'kW', 'label': 'IC Q4 coupled power'},
    'IC_P_Gen1': {'name': 'GICHPTRAGEN%1', 'unit': 'kW', 'label': 'Generator 1 transmitted power'},
    'IC_P_Gen2': {'name': 'GICHPTRAGEN%2', 'unit': 'kW', 'label': 'Generator 2 transmitted power'},
    'IC_P_Gen3': {'name': 'GICHPTRAGEN%3', 'unit': 'kW', 'label': 'Generator 3 transmitted power'},
    'IC_P_Gen4': {'name': 'GICHPTRAGEN%4', 'unit': 'kW', 'label': 'Generator 4 transmitted power'},
    'IC_P_Gen5': {'name': 'GICHPTRAGEN%5', 'unit': 'kW', 'label': 'Generator 5 transmitted power'},
    'IC_P_Gen6': {'name': 'GICHPTRAGEN%6', 'unit': 'kW', 'label': 'Generator 6 transmitted power'},
    'IC_P_Gen1_ref' : {'name': 'GICHPREFGEN%1', 'unit': 'kW', 'label': 'Generator 1 reflected power'},
    'IC_P_Gen2_ref' : {'name': 'GICHPREFGEN%2', 'unit': 'kW', 'label': 'Generator 2 reflected power'},
    'IC_P_Gen3_ref' : {'name': 'GICHPREFGEN%3', 'unit': 'kW', 'label': 'Generator 3 reflected power'},
    'IC_P_Gen4_ref' : {'name': 'GICHPREFGEN%4', 'unit': 'kW', 'label': 'Generator 4 reflected power'},
    'IC_P_Gen5_ref' : {'name': 'GICHPREFGEN%5', 'unit': 'kW', 'label': 'Generator 5 reflected power'},
    'IC_P_Gen6_ref' : {'name': 'GICHPREFGEN%6', 'unit': 'kW', 'label': 'Generator 6 reflected power'},
    'IC_P_Gen1_fwd' : {'name': None, 'fun':'IC_Gen_fwd1', 'unit': 'kW', 'label': 'Generator 1 forward power'},
    'IC_P_Gen2_fwd' : {'name': None, 'fun':'IC_Gen_fwd2', 'unit': 'kW', 'label': 'Generator 2 forward power'},
    'IC_P_Gen3_fwd' : {'name': None, 'fun':'IC_Gen_fwd3', 'unit': 'kW', 'label': 'Generator 3 forward power'},
    'IC_P_Gen4_fwd' : {'name': None, 'fun':'IC_Gen_fwd4', 'unit': 'kW', 'label': 'Generator 4 forward power'},
    'IC_P_Gen5_fwd' : {'name': None, 'fun':'IC_Gen_fwd5', 'unit': 'kW', 'label': 'Generator 5 forward power'},
    'IC_P_Gen6_fwd' : {'name': None, 'fun':'IC_Gen_fwd6', 'unit': 'kW', 'label': 'Generator 6 forward power'},
    # IC antenna positions (use tsmat)
    'IC_Positions': {'name': None, 'fun': 'IC_Positions', 'unit': 'm', 'label': 'IC Antenna positions'},
    'LH_Positions': {'name': None, 'fun': 'LH_Positions', 'unit': 'm', 'label': 'LH Antenna positions'},
    'LPA_Position': {'name': 'GMAG_POSLPA%1', 'unit': 'm', 'label': 'LPA position'},
    # IC antenna frequencies (use tsmat)
    'IC_Frequencies': {'name': None, 'fun': 'IC_Frequencies', 'unit': 'MHz', 'label': 'IC Antenna Frequencies'},
    # FPGA temperatures
    'IC_FPGA_Temperatures': {'name': None, 'fun': 'IC_FPGA_Temperatures', 'unit': 'degC', 'label': 'IC FPGA Card Temperatures'},
    # IC antennas left and right forward and reflected powers
    'IC_P_Q1_left_fwd': {'name': 'GICHANTPOWQ1%1', 'unit': 'kW', 'label': 'left Fwd Power Q1'},
    'IC_P_Q1_left_ref': {'name': 'GICHANTPOWQ1%2', 'unit': 'kW', 'label': 'left Ref Power Q1'},
    'IC_P_Q1_right_fwd': {'name': 'GICHANTPOWQ1%3',  'unit': 'kW', 'label': 'right Fwd Power Q1'},
    'IC_P_Q1_right_ref': {'name': 'GICHANTPOWQ1%4', 'unit': 'kW', 'label': 'right Ref Power Q1'},
    'IC_P_Q2_left_fwd': {'name': 'GICHANTPOWQ2%1', 'unit': 'kW', 'label': 'left Fwd Power Q2'},
    'IC_P_Q2_left_ref': {'name': 'GICHANTPOWQ2%2', 'unit': 'kW', 'label': 'left Ref Power Q2'},
    'IC_P_Q2_right_fwd': {'name': 'GICHANTPOWQ2%3', 'unit': 'kW', 'label': 'right Fwd Power Q2'},
    'IC_P_Q2_right_ref': {'name': 'GICHANTPOWQ2%4', 'unit': 'kW', 'label': 'right Ref Power Q2'},    
    'IC_P_Q4_left_fwd': {'name': 'GICHANTPOWQ4%1', 'unit': 'kW', 'label': 'left Fwd Power Q4'},
    'IC_P_Q4_left_ref': {'name': 'GICHANTPOWQ4%2', 'unit': 'kW', 'label': 'left Ref Power Q4'},
    'IC_P_Q4_right_fwd': {'name': 'GICHANTPOWQ4%3', 'unit': 'kW', 'label': 'right Fwd Power Q4'},
    'IC_P_Q4_right_ref': {'name': 'GICHANTPOWQ4%4', 'unit': 'kW', 'label': 'right Ref Power Q4'},
    # IC Antennas coupling resistances
    'IC_Rc_Q1_left': {'name': 'GICHCOUPRES%1', 'unit': 'Ohm', 'label': 'Rc - Q1 left', 'options':{'ylim':(0,2)} },
    'IC_Rc_Q1_right': {'name': 'GICHCOUPRES%2', 'unit': 'Ohm', 'label': 'Rc - Q1 right', 'options':{'ylim':(0,2)}},
    'IC_Rc_Q2_left': {'name': 'GICHCOUPRES%3', 'unit': 'Ohm', 'label': 'Rc - Q2 left', 'options':{'ylim':(0,2)}},
    'IC_Rc_Q2_right': {'name': 'GICHCOUPRES%4', 'unit': 'Ohm', 'label': 'Rc - Q2 right','options':{'ylim':(0,2)}},
    'IC_Rc_Q4_left': {'name': 'GICHCOUPRES%5', 'unit': 'Ohm', 'label': 'Rc - Q4 left','options':{'ylim':(0,2)}},
    'IC_Rc_Q4_right': {'name': 'GICHCOUPRES%6', 'unit': 'Ohm', 'label': 'Rc - Q4 right', 'options':{'ylim':(0,2)}},
    'IC_Rc_Q1_avg': {'name': None, 'fun': 'IC_Rc_Q1_avg', 'unit': 'Ohm', 'label': 'Avg. Rc - Q1', 'options':{'ylim':(0,2)}},
    'IC_Rc_Q2_avg': {'name': None, 'fun': 'IC_Rc_Q2_avg', 'unit': 'Ohm', 'label': 'Avg. Rc - Q2', 'options':{'ylim':(0,2)}},
    'IC_Rc_Q4_avg': {'name': None, 'fun': 'IC_Rc_Q4_avg', 'unit': 'Ohm', 'label': 'Avg. Rc - Q4', 'options':{'ylim':(0,2)}},    
    'IC_Rc_avg': {'name': None, 'fun': 'IC_Rc_avg', 'unit': 'Ohm', 'label': 'Avg. IC Rc', 'options':{'ylim':(0,2)}},
    # IC Voltage reflected coefficient at bidirectional coupler
    'IC_Gamma_Q1_left' : {'name':None, 'fun': 'IC_Gamma_Q1_left', 'unit':'', 'label':'Voltage Reflection Coefficient Q1 left'},
    'IC_Gamma_Q1_right' : {'name':None, 'fun': 'IC_Gamma_Q1_right', 'unit':'', 'label':'Voltage Reflection Coefficient Q1 right'},
    'IC_Gamma_Q2_left' : {'name':None, 'fun': 'IC_Gamma_Q2_left', 'unit':'', 'label':'Voltage Reflection Coefficient Q2 left'},
    'IC_Gamma_Q2_right' : {'name':None, 'fun': 'IC_Gamma_Q2_right', 'unit':'', 'label':'Voltage Reflection Coefficient Q2 right'},
    'IC_Gamma_Q4_left' : {'name':None, 'fun': 'IC_Gamma_Q4_left', 'unit':'', 'label':'Voltage Reflection Coefficient Q4 left'},
    'IC_Gamma_Q4_right' : {'name':None, 'fun': 'IC_Gamma_Q4_right', 'unit':'', 'label':'Voltage Reflection Coefficient Q4 left'},    
    # IC VSWR
    'IC_VSWR_Q1_left': {'name':None, 'fun':'VSWR_Q1_left', 'unit': '', 'label':'VSWR Q1 left', 'options':{'ylim':(1, 3)}},
    'IC_VSWR_Q1_right': {'name':None, 'fun':'VSWR_Q1_right', 'unit': '', 'label':'VSWR Q1 right', 'options':{'ylim':(1, 3)}},
    'IC_VSWR_Q2_left': {'name':None, 'fun':'VSWR_Q2_left', 'unit': '', 'label':'VSWR Q2 left', 'options':{'ylim':(1, 3)}},
    'IC_VSWR_Q2_right': {'name':None, 'fun':'VSWR_Q2_right', 'unit': '', 'label':'VSWR Q2 right', 'options':{'ylim':(1, 3)}},
    'IC_VSWR_Q4_left': {'name':None, 'fun':'VSWR_Q4_left', 'unit': '', 'label':'VSWR Q4 left', 'options':{'ylim':(1, 3)}},
    'IC_VSWR_Q4_right': {'name':None, 'fun':'VSWR_Q4_right', 'unit': '', 'label':'VSWR Q4 right', 'options':{'ylim':(1, 3)}},    
    # IC antennas phase Q1
    'IC_Phase_Q1 (Pf_left - Pf_right)': {'name': 'GICHPHASESQ1%1', 'unit': 'deg', 'label': 'Phase (Pf left - Pf right) antenna Q1'},
    'IC_Phase_Q1 (Pr_left - Pf_right)': {'name': 'GICHPHASESQ1%2', 'unit': 'deg', 'label': 'Phase (Pr left - Pf right) antenna Q1'},
    'IC_Phase_Q1 (Pr_right - Pf_right)': {'name': 'GICHPHASESQ1%3', 'unit': 'deg', 'label': 'Phase (Pr right - Pf right) antenna Q1'},
    'IC_Phase_Q1 (V1 - Pf_left)': {'name': 'GICHPHASESQ1%4', 'unit': 'deg', 'label': 'Phase (V1 - Pf left) antenna Q1'},
    'IC_Phase_Q1 (V2 - Pf_left)': {'name': 'GICHPHASESQ1%5', 'unit': 'deg', 'label': 'Phase (V2 - Pf left) antenna Q1'},
    'IC_Phase_Q1 (V3 - Pf_right)': {'name': 'GICHPHASESQ1%6', 'unit': 'deg', 'label': 'Phase (V3 - Pf right) antenna Q1'},
    'IC_Phase_Q1 (V4 - Pf_right)': {'name': 'GICHPHASESQ1%7', 'unit': 'deg', 'label': 'Phase (V4 - Pf right) antenna Q1'},
    # IC antennas phase Q2
    'IC_Phase_Q2 (Pf_left - Pf_right)': {'name': 'GICHPHASESQ2%1', 'unit': 'deg', 'label': 'Phase (Pf left - Pf right) antenna Q2'},
    'IC_Phase_Q2 (Pr_left - Pf_right)': {'name': 'GICHPHASESQ2%2', 'unit': 'deg', 'label': 'Phase (Pr left - Pf right) antenna Q2'},
    'IC_Phase_Q2 (Pr_right - Pf_right)': {'name': 'GICHPHASESQ2%3', 'unit': 'deg', 'label': 'Phase (Pr right - Pf right) antenna Q2'},
    'IC_Phase_Q2 (V1 - Pf_left)': {'name': 'GICHPHASESQ2%4', 'unit': 'deg', 'label': 'Phase (V1 - Pf left) antenna Q2'},
    'IC_Phase_Q2 (V2 - Pf_left)': {'name': 'GICHPHASESQ2%5', 'unit': 'deg', 'label': 'Phase (V2 - Pf left) antenna Q2'},
    'IC_Phase_Q2 (V3 - Pf_right)': {'name': 'GICHPHASESQ2%6', 'unit': 'deg', 'label': 'Phase (V3 - Pf right) antenna Q2'},
    'IC_Phase_Q2 (V4 - Pf_right)': {'name': 'GICHPHASESQ2%7', 'unit': 'deg', 'label': 'Phase (V4 - Pf right) antenna Q2'},
    # IC antennas phase Q4
    'IC_Phase_Q4 (Pf_left - Pf_right)': {'name': 'GICHPHASESQ4%1', 'unit': 'deg', 'label': 'Phase (Pf left - Pf right) antenna Q4'},
    'IC_Phase_Q4 (Pr_left - Pf_right)': {'name': 'GICHPHASESQ4%2', 'unit': 'deg', 'label': 'Phase (Pr left - Pf right) antenna Q4'},
    'IC_Phase_Q4 (Pr_right - Pf_right)': {'name': 'GICHPHASESQ4%3', 'unit': 'deg', 'label': 'Phase (Pr right - Pf right) antenna Q4'},
    'IC_Phase_Q4 (V1 - Pf_left)': {'name': 'GICHPHASESQ4%4', 'unit': 'deg', 'label': 'Phase (V1 - Pf left) antenna Q4'},
    'IC_Phase_Q4 (V2 - Pf_left)': {'name': 'GICHPHASESQ4%5', 'unit': 'deg', 'label': 'Phase (V2 - Pf left) antenna Q4'},
    'IC_Phase_Q4 (V3 - Pf_right)': {'name': 'GICHPHASESQ4%6', 'unit': 'deg', 'label': 'Phase (V3 - Pf right) antenna Q4'},
    'IC_Phase_Q4 (V4 - Pf_right)': {'name': 'GICHPHASESQ4%7', 'unit': 'deg', 'label': 'Phase (V4 - Pf right) antenna Q4'},
    # IC antenna phase differences
    'IC_delta_phi_toro_Q1_Top_LmR': {'name': None, 'fun': 'delta_phi_toro_Q1_Top_LmR', 'unit': 'deg', 'label': 'DeltaPhase Q1 (L - R) Top'},
    'IC_delta_phi_toro_Q2_Top_LmR': {'name': None, 'fun': 'delta_phi_toro_Q2_Top_LmR', 'unit': 'deg', 'label': 'DeltaPhase Q2 (L - R) Top'},
    'IC_delta_phi_toro_Q4_Top_LmR': {'name': None, 'fun': 'delta_phi_toro_Q4_Top_LmR', 'unit': 'deg', 'label': 'DeltaPhase Q4 (L - R) Top'},
    'IC_delta_phi_toro_Q1_Bot_LmR': {'name': None, 'fun': 'delta_phi_toro_Q1_Bot_LmR', 'unit': 'deg', 'label': 'DeltaPhase Q1 (L - R) Bot'},
    'IC_delta_phi_toro_Q2_Bot_LmR': {'name': None, 'fun': 'delta_phi_toro_Q2_Bot_LmR', 'unit': 'deg', 'label': 'DeltaPhase Q2 (L - R) Bot'},
    'IC_delta_phi_toro_Q4_Bot_LmR': {'name': None, 'fun': 'delta_phi_toro_Q4_Bot_LmR', 'unit': 'deg', 'label': 'DeltaPhase Q4 (L - R) Bot'},  
    'IC_delta_phi_polo_Q1_left_BmT': {'name':None, 'fun': 'delta_phi_polo_Q1_left_BmT', 'unit': 'deg', 'label': 'DeltaPhase Q1 (B - T) left'},
    'IC_delta_phi_polo_Q2_left_BmT': {'name':None, 'fun': 'delta_phi_polo_Q2_left_BmT', 'unit': 'deg', 'label': 'DeltaPhase Q2 (B - T) left'},
    'IC_delta_phi_polo_Q4_left_BmT': {'name':None, 'fun': 'delta_phi_polo_Q4_left_BmT', 'unit': 'deg', 'label': 'DeltaPhase Q4 (B - T) left'},
    'IC_delta_phi_polo_Q1_right_BmT': {'name':None, 'fun': 'delta_phi_polo_Q1_right_BmT', 'unit': 'deg', 'label': 'DeltaPhase Q1 (B - T) right'},
    'IC_delta_phi_polo_Q2_right_BmT': {'name':None, 'fun': 'delta_phi_polo_Q2_right_BmT', 'unit': 'deg', 'label': 'DeltaPhase Q2 (B - T) right'},
    'IC_delta_phi_polo_Q4_right_BmT': {'name':None, 'fun': 'delta_phi_polo_Q4_right_BmT', 'unit': 'deg', 'label': 'DeltaPhase Q4 (B - T) right'},    
    # IC antenna phase differences calculated in FPGA direclty. Default is difference between top straps except Q1 -> bottom as V1 out of order
    'IC_delta_phi_toro_Q1_LmR_FPGA': {'name': 'SICHPHQ1', 'unit': 'deg', 'label':' DeltaPhase Q1 (L - R) FPGA'},
    'IC_delta_phi_toro_Q2_LmR_FPGA': {'name': 'SICHPHQ2', 'unit': 'deg', 'label':' DeltaPhase Q2 (L - R) FPGA'},
    'IC_delta_phi_toro_Q4_LmR_FPGA': {'name': 'SICHPHQ4', 'unit': 'deg', 'label':' DeltaPhase Q4 (L - R) FPGA'},
    # convenient shortcut to toroidal phase without noise (Gives NaN when no power instead of noisy values)
    'IC_Phase_Q1': {'name':None, 'fun':'phase_Q1', 'unit':'deg', 'label':'Tor.Phase Q1'},
    'IC_Phase_Q2': {'name':None, 'fun':'phase_Q2', 'unit':'deg', 'label':'Tor.Phase Q2'},
    'IC_Phase_Q4': {'name':None, 'fun':'phase_Q4', 'unit':'deg', 'label':'Tor.Phase Q4'},    
    # IC Antennas internal vacuum (y = 10**(1.5*y - 10))
    'IC_Vacuum_Q1_left': {'name': None, 'fun': 'IC_Q1_vacuum_left', 'unit': 'Pa', 'label': 'Vaccum Q1 left', 'options': {'yscale':'log', 'ylimit':4.5e-3, 'ylimit_low':2.2e-4}},
    'IC_Vacuum_Q1_right': {'name': None, 'fun': 'IC_Q1_vacuum_right', 'unit': 'Pa', 'label': 'Vaccum Q1 right', 'options': {'yscale':'log', 'ylimit':4.5e-3, 'ylimit_low':2.2e-4}},
    'IC_Vacuum_Q2_left': {'name': None, 'fun': 'IC_Q2_vacuum_right', 'unit': 'Pa', 'label': 'Vaccum Q2 left', 'options': {'yscale':'log', 'ylimit':4.5e-3, 'ylimit_low':2.2e-4}},
    'IC_Vacuum_Q2_right': {'name': None, 'fun': 'IC_Q2_vacuum_right', 'unit': 'Pa', 'label': 'Vaccum Q2 right', 'options': {'yscale':'log', 'ylimit':4.5e-3, 'ylimit_low':2.2e-4}},
    'IC_Vacuum_Q4_left': {'name': None, 'fun': 'IC_Q4_vacuum_right', 'unit': 'Pa', 'label': 'Vaccum Q4 left', 'options': {'yscale':'log', 'ylimit':4.5e-3, 'ylimit_low':2.2e-4}},
    'IC_Vacuum_Q4_right': {'name': None, 'fun': 'IC_Q4_vacuum_right', 'unit': 'Pa', 'label': 'Vaccum Q4 right', 'options': {'yscale':'log', 'ylimit':4.5e-3, 'ylimit_low':2.2e-4}},
    # Acquisition des Consignes de puissance en sortie des FPGA 
    'IC_cons_Power_Q1': {'name': 'GICHSPP%1', 'unit': 'kW', 'label': 'Acquisition consigne generee Q1'},
    'IC_cons_Power_Q2': {'name': 'GICHSPP%2', 'unit': 'kW', 'label': 'Acquisition consigne generee Q1'},
    'IC_cons_Power_Q4': {'name': 'GICHSPP%3', 'unit': 'kW', 'label': 'Acquisition consigne generee Q1'},
    # PCS: power, phase request and authorisation
    'IC_PCS_Power_Q1': {'name': 'GICHCONSPCS%1', 'unit': 'kW', 'label': 'PCS Power request Q1'},
    'IC_PCS_Power_Q2': {'name': 'GICHCONSPCS%2', 'unit': 'kW', 'label': 'PCS Power request Q2'},
    'IC_PCS_Power_Q4': {'name': 'GICHCONSPCS%3', 'unit': 'kW', 'label': 'PCS Power request Q4'},
    'IC_PCS_Phase_Q1': {'name': 'GICHCONSPCS%4', 'unit': 'deg', 'label': 'PCS Phase request Q1'},
    'IC_PCS_Phase_Q2': {'name': 'GICHCONSPCS%5', 'unit': 'deg', 'label': 'PCS Phase request Q2'},
    'IC_PCS_Phase_Q4': {'name': 'GICHCONSPCS%6', 'unit': 'deg', 'label': 'PCS Phase request Q4'},    
    'IC_PCS_interdiction_Q1': {'name': 'GICHCONSPCS%7', 'unit': '--', 'label': 'PCS interdiction Q1'},
    'IC_PCS_interdiction_Q2': {'name': 'GICHCONSPCS%8', 'unit': '--', 'label': 'PCS interdiction Q2'},
    'IC_PCS_interdiction_Q4': {'name': 'GICHCONSPCS%9', 'unit': '--', 'label': 'PCS interdiction Q4'},    
    # NB : coupling resistance is also send to PCS for real time control.
    # IC antennas Capacitor values
    'IC_Capa_Q1_left_upper': {'name': 'GICHCAPA%1', 'unit': 'pF', 'label': 'Capa.Q1 L-U'},
    'IC_Capa_Q1_left_lower': {'name': 'GICHCAPA%2', 'unit': 'pF', 'label': 'Capa.Q1 L-L'},
    'IC_Capa_Q1_right_upper': {'name': 'GICHCAPA%3', 'unit': 'pF', 'label': 'Capa.Q1 R-U'},
    'IC_Capa_Q1_right_lower': {'name': 'GICHCAPA%4', 'unit': 'pF', 'label': 'Capa.Q1 R-L'},
    'IC_Capa_Q2_left_upper': {'name': 'GICHCAPA%5', 'unit': 'pF', 'label': 'Capa.Q2 L-U'},
    'IC_Capa_Q2_left_lower': {'name': 'GICHCAPA%6', 'unit': 'pF', 'label': 'Capa.Q2 L-L'},
    'IC_Capa_Q2_right_upper': {'name': 'GICHCAPA%7', 'unit': 'pF', 'label': 'Capa.Q2 R-U'},
    'IC_Capa_Q2_right_lower': {'name': 'GICHCAPA%8', 'unit': 'pF', 'label': 'Capa.Q2 R-L'},
    'IC_Capa_Q4_left_upper': {'name': 'GICHCAPA%9', 'unit': 'pF', 'label': 'Capa.Q4 L-U'},
    'IC_Capa_Q4_left_lower': {'name': 'GICHCAPA%10', 'unit': 'pF', 'label': 'Capa.Q4 L-L'},
    'IC_Capa_Q4_right_upper': {'name': 'GICHCAPA%11', 'unit': 'pF', 'label': 'Capa.Q4 R-U'},
    'IC_Capa_Q4_right_lower': {'name': 'GICHCAPA%12', 'unit': 'pF', 'label': 'Capa.Q4 R-L'},    
    # IC antennas Capacitor error signals
    'IC_ErrSig_Q1_left_upper': {'name': 'GICHSIGERR%1', 'unit': '', 'label': 'Err.Sig.Q1 L-U'},
    'IC_ErrSig_Q1_left_lower': {'name': 'GICHSIGERR%2', 'unit': '', 'label': 'Err.Sig.Q1 L-L'},
    'IC_ErrSig_Q1_right_upper': {'name': 'GICHSIGERR%3', 'unit': '', 'label': 'Err.Sig.Q1 R-U'},
    'IC_ErrSig_Q1_right_lower': {'name': 'GICHSIGERR%4', 'unit': '', 'label': 'Err.Sig.Q1 R-L'},
    'IC_ErrSig_Q2_left_upper': {'name': 'GICHSIGERR%5', 'unit': '', 'label': 'Err.Sig.Q2 L-U'},
    'IC_ErrSig_Q2_left_lower': {'name': 'GICHSIGERR%6', 'unit': '', 'label': 'Err.Sig.Q2 L-L'},
    'IC_ErrSig_Q2_right_upper': {'name': 'GICHSIGERR%7', 'unit': '', 'label': 'Err.Sig.Q2 R-U'},
    'IC_ErrSig_Q2_right_lower': {'name': 'GICHSIGERR%8', 'unit': '', 'label': 'Err.Sig.Q2 R-L'},
    'IC_ErrSig_Q4_left_upper': {'name': 'GICHSIGERR%9', 'unit': '', 'label': 'Err.Sig.Q4 L-U'},
    'IC_ErrSig_Q4_left_lower': {'name': 'GICHSIGERR%10', 'unit': '', 'label': 'Err.Sig.Q4 L-L'},
    'IC_ErrSig_Q4_right_upper': {'name': 'GICHSIGERR%11', 'unit': '', 'label': 'Err.Sig.Q4 R-U'},
    'IC_ErrSig_Q4_right_lower': {'name': 'GICHSIGERR%12', 'unit': '', 'label': 'Err.Sig.Q4 R-L'},    
    # IC antennas Capacitor Voltages
    'IC_Voltage_left_upper_Q1': {'name': 'GICHVPROBEQ1%1', 'unit': 'kV', 'label': 'left upper capacitor voltage Q1', 'options': {'ylimit':27}},
    'IC_Voltage_left_lower_Q1': {'name': 'GICHVPROBEQ1%2', 'unit': 'kV', 'label': 'left lower capacitor voltage Q1', 'options': {'ylimit':27}},
    'IC_Voltage_right_upper_Q1': {'name': 'GICHVPROBEQ1%3', 'unit': 'kV', 'label': 'right upper capacitor voltage Q1', 'options': {'ylimit':27}},
    'IC_Voltage_right_lower_Q1': {'name': 'GICHVPROBEQ1%4', 'unit': 'kV', 'label': 'right lower capacitor voltage Q1', 'options': {'ylimit':27}}, 
    'IC_Voltage_left_upper_Q2': {'name': 'GICHVPROBEQ2%1', 'unit': 'kV', 'label': 'left upper capacitor voltage Q2', 'options': {'ylimit':27}},
    'IC_Voltage_left_lower_Q2': {'name': 'GICHVPROBEQ2%2', 'unit': 'kV', 'label': 'left lower capacitor voltage Q2', 'options': {'ylimit':27}},
    'IC_Voltage_right_upper_Q2': {'name': 'GICHVPROBEQ2%3', 'unit': 'kV', 'label': 'right upper capacitor voltage Q2', 'options': {'ylimit':27}},
    'IC_Voltage_right_lower_Q2': {'name': 'GICHVPROBEQ2%4', 'unit': 'kV', 'label': 'right lower capacitor voltage Q2', 'options': {'ylimit':27}},
    'IC_Voltage_left_upper_Q4': {'name': 'GICHVPROBEQ4%1', 'unit': 'kV', 'label': 'left upper capacitor voltage Q4', 'options': {'ylimit':27}},
    'IC_Voltage_left_lower_Q4': {'name': 'GICHVPROBEQ4%2', 'unit': 'kV', 'label': 'left lower capacitor voltage Q4', 'options': {'ylimit':27}},
    'IC_Voltage_right_upper_Q4': {'name': 'GICHVPROBEQ4%3', 'unit': 'kV', 'label': 'right upper capacitor voltage Q4', 'options': {'ylimit':27}},
    'IC_Voltage_right_lower_Q4': {'name': 'GICHVPROBEQ4%4', 'unit': 'kV', 'label': 'right lower capacitor voltage Q4', 'options': {'ylimit':27}},
    # IC Maximum Voltage values
    'IC_Voltage_left_max_Q1': {'name':None, 'fun':'IC_Voltage_left_max_Q1', 'unit':'kV', 'label': 'left Maximum voltage Q1', 'options': {'ylimit':27}},
    'IC_Voltage_right_max_Q1': {'name':None, 'fun':'IC_Voltage_right_max_Q1', 'unit':'kV', 'label': 'right Maximum voltage Q1', 'options': {'ylimit':27}},
    'IC_Voltage_left_max_Q2': {'name':None, 'fun':'IC_Voltage_left_max_Q2', 'unit':'kV', 'label': 'left Maximum voltage Q2', 'options': {'ylimit':27}},
    'IC_Voltage_right_max_Q2': {'name':None, 'fun':'IC_Voltage_right_max_Q2', 'unit':'kV', 'label': 'right Maximum voltage Q2', 'options': {'ylimit':27}},
    'IC_Voltage_left_max_Q4': {'name':None, 'fun':'IC_Voltage_left_max_Q4', 'unit':'kV', 'label': 'left Maximum voltage Q4', 'options': {'ylimit':27}},
    'IC_Voltage_right_max_Q4': {'name':None, 'fun':'IC_Voltage_right_max_Q4', 'unit':'kV', 'label': 'right Maximum voltage Q4', 'options': {'ylimit':27}},
    # IC Maximum Current values
    'IC_Current_left_max_Q1': {'name':None, 'fun':'IC_Current_left_max_Q1', 'unit':'kV', 'label': 'left Maximum Current Q1', 'options': {'ylimit':27}},
    'IC_Current_right_max_Q1': {'name':None, 'fun':'IC_Current_right_max_Q1', 'unit':'kV', 'label': 'right Maximum Current Q1', 'options': {'ylimit':27}},
    'IC_Current_left_max_Q2': {'name':None, 'fun':'IC_Current_left_max_Q2', 'unit':'kV', 'label': 'left Maximum Current Q2', 'options': {'ylimit':27}},
    'IC_Current_right_max_Q2': {'name':None, 'fun':'IC_Current_right_max_Q2', 'unit':'kV', 'label': 'right Maximum Current Q2', 'options': {'ylimit':27}},
    'IC_Current_left_max_Q4': {'name':None, 'fun':'IC_Current_left_max_Q4', 'unit':'kV', 'label': 'left Maximum Current Q4', 'options': {'ylimit':27}},
    'IC_Current_right_max_Q4': {'name':None, 'fun':'IC_Current_right_max_Q4', 'unit':'kV', 'label': 'right Maximum Current Q4', 'options': {'ylimit':27}},
    # IC antennas Capacitor Currents
    'IC_Current_left_upper_Q1': {'name': 'GICHICAPA%1', 'unit': 'A', 'label': 'left upper capacitor current Q1', 'options': {'ylimit':915}},
    'IC_Current_left_lower_Q1': {'name': 'GICHICAPA%2', 'unit': 'A', 'label': 'left lower capacitor current Q1', 'options': {'ylimit':915}},
    'IC_Current_right_upper_Q1': {'name': 'GICHICAPA%3', 'unit': 'A', 'label': 'right upper capacitor current Q1', 'options': {'ylimit':915}},
    'IC_Current_right_lower_Q1': {'name': 'GICHICAPA%4', 'unit': 'A', 'label': 'right lower capacitor current Q1', 'options': {'ylimit':915}},
    'IC_Current_left_upper_Q2': {'name': 'GICHICAPA%5', 'unit': 'A', 'label': 'left upper capacitor current Q2', 'options': {'ylimit':915}},
    'IC_Current_left_lower_Q2': {'name': 'GICHICAPA%6', 'unit': 'A', 'label': 'left lower capacitor current Q2', 'options': {'ylimit':915}},
    'IC_Current_right_upper_Q2': {'name': 'GICHICAPA%7', 'unit': 'A', 'label': 'right upper capacitor current Q2', 'options': {'ylimit':915}},
    'IC_Current_right_lower_Q2': {'name': 'GICHICAPA%8', 'unit': 'A', 'label': 'right lower capacitor current Q2', 'options': {'ylimit':915}},   
    'IC_Current_left_upper_Q4': {'name': 'GICHICAPA%9', 'unit': 'A', 'label': 'left upper capacitor current Q4', 'options': {'ylimit':915}},
    'IC_Current_left_lower_Q4': {'name': 'GICHICAPA%10', 'unit': 'A', 'label': 'left lower capacitor current Q4', 'options': {'ylimit':915}},
    'IC_Current_right_upper_Q4': {'name': 'GICHICAPA%11', 'unit': 'A', 'label': 'right upper capacitor current Q4', 'options': {'ylimit':915}},
    'IC_Current_right_lower_Q4': {'name': 'GICHICAPA%12', 'unit': 'A', 'label': 'right lower capacitor current Q4', 'options': {'ylimit':915}}, 
    # IC Errors
    
    ## LHCD
    'LH_P_tot': {'name': 'SHYBPTOT', 'unit': 'MW', 'label': 'LH total coupled power'},
    'LH_P_LH1': {'name': 'SHYBPFORW1', 'unit': 'kW', 'label': 'LH1 coupled power'},
    'LH_P_LH2': {'name': 'SHYBPFORW2', 'unit': 'kW', 'label': 'LH2 coupled power'},
    'LH_Rc_LH1': {'name': 'SHYBREF1', 'unit': '%', 'label': 'Avg. Refl. Coeff LH1'},
    'LH_Rc_LH2': {'name': 'SHYBREF2', 'unit': '%', 'label': 'Avg. Refl. Coeff LH2'},
    # Impurities (SURVIE)
    'Cu': {'name': 'scu19', 'unit': None, 'label': 'Copper'},
    'Fe': {'name': 'SFE15', 'unit': None, 'label': 'Iron'},
    'Ag18': {'name': 'SAG18', 'unit':'a.u.', 'label':'Silver-18'},
    'Ag19': {'name': 'SAG18', 'unit':'a.u.', 'label':'Silver-19'},
    ## Temperature
    'Te1': {'name': None, 'fun': 'ECE_1', 'unit': 'eV', 'label': 'Temperature (ECE)'},
    'Te2': {'name': None, 'fun': 'ECE_2', 'unit': 'eV', 'label': 'Temperature (ECE)'},
    'Te3': {'name': None, 'fun': 'ECE_3', 'unit': 'eV', 'label': 'Temperature (ECE)'},
    'Te4': {'name': None, 'fun': 'ECE_4', 'unit': 'eV', 'label': 'Temperature (ECE)'},
    ## Langmuir probes
    'Langmuir_LHCD1': {'name': 'GISLH%1', 'unit': 'mA', 'label':'Ion saturation current on the LHCD launcher probes #1'},
    'Langmuir_LHCD2': {'name': 'GISLH%2', 'unit': 'mA', 'label':'Ion saturation current on the LHCD launcher probes #2'},
    'Langmuir_LHCD3': {'name': 'GISLH%3', 'unit': 'mA', 'label':'Ion saturation current on the LHCD launcher probes #3'},
    'Langmuir_LHCD4': {'name': 'GISLH%4', 'unit': 'mA', 'label':'Ion saturation current on the LHCD launcher probes #4'},
    'Langmuir_LHCD5': {'name': 'GISLH%5', 'unit': 'mA', 'label':'Ion saturation current on the LHCD launcher probes #5'},
    'Langmuir_LHCD6': {'name': 'GISLH%6', 'unit': 'mA', 'label':'Ion saturation current on the LHCD launcher probes #6'},
    'Langmuir_LHCD7': {'name': 'GISLH%7', 'unit': 'mA', 'label':'Ion saturation current on the LHCD launcher probes #7'},
    'Langmuir_LHCD8': {'name': 'GISLH%8', 'unit': 'mA', 'label':'Ion saturation current on the LHCD launcher probes #8'},
    ## Barometry
    'baro_Q2': {'name':'GBARDB8%4', 'unit': '--', 'label':'barometry Q2 raw'},
    'baro_Q4': {'name':'GBARDB8%9', 'unit': '--', 'label':'barometry Q4 raw'},
    ## Bolometry
    'Prad': {'name': None, 'fun':'Prad_pradwest', 'unit':'MW', 'label':'Prad total'},
    'Prad_bulk': {'name': None, 'fun':'Prad_bulk_pradwest', 'unit':'MW', 'label':'Prad bulk'},    
    'Prad_imas': {'name': None, 'fun':'Prad_imas', 'unit':'MW', 'label':'Prad total (imas)'},
    'Prad_bulk_imas': {'name': None, 'fun':'Prad_bulk_imas', 'unit':'MW', 'label':'Prad bulk (imas)'},    
    # Divertor current
    'Divertor_lower_current_cons': {'name':'GPOLO_IDC2%1', 'unit':'kA', 'label':'Lower divertor current consigne'},
    'Divertor_lower_current': {'name':'GPOLO_IDC2%2', 'unit':'kA', 'label':'Lower divertor current'},    
    'Divertor_lower_voltage_cons': {'name':'GPOLO_UDC2%2', 'unit':'V', 'label':'Lower divertor current consigne'},
    'Divertor_lower_voltage': {'name':'GPOLO_UDC2%3', 'unit':'V', 'label':'Lower divertor current'},   
    # MHD
    'MHD' : {'name':'GMHD_D1%2', 'unit':'a.u.', 'label':'MHD mode envelop'},
    }

def VSWR_Q1_left(pulse):
    Pow_IncRefQ1, tPow_IncRefQ1 = pw.tsbase(pulse,'GICHANTPOWQ1', nargout=2)   
    VSWR_Q1_left  = (1 + np.sqrt(Pow_IncRefQ1[:,1]/Pow_IncRefQ1[:,0])) / \
                    (1 - np.sqrt(Pow_IncRefQ1[:,1]/Pow_IncRefQ1[:,0]))
    return VSWR_Q1_left, tPow_IncRefQ1

def VSWR_Q1_right(pulse):
    Pow_IncRefQ1, tPow_IncRefQ1 = pw.tsbase(pulse,'GICHANTPOWQ1', nargout=2)   
    VSWR_Q1_right  = (1 + np.sqrt(Pow_IncRefQ1[:,3]/Pow_IncRefQ1[:,2])) / \
                    (1 - np.sqrt(Pow_IncRefQ1[:,3]/Pow_IncRefQ1[:,2]))
    return VSWR_Q1_right, tPow_IncRefQ1

def VSWR_Q2_left(pulse):
    Pow_IncRefQ2, tPow_IncRefQ2 = pw.tsbase(pulse,'GICHANTPOWQ2', nargout=2)   
    VSWR_Q2_left  = (1 + np.sqrt(Pow_IncRefQ2[:,1]/Pow_IncRefQ2[:,0])) / \
                    (1 - np.sqrt(Pow_IncRefQ2[:,1]/Pow_IncRefQ2[:,0]))
    return VSWR_Q2_left, tPow_IncRefQ2

def VSWR_Q2_right(pulse):
    Pow_IncRefQ2, tPow_IncRefQ2 = pw.tsbase(pulse,'GICHANTPOWQ2', nargout=2)   
    VSWR_Q2_right  = (1 + np.sqrt(Pow_IncRefQ2[:,3]/Pow_IncRefQ2[:,2])) / \
                    (1 - np.sqrt(Pow_IncRefQ2[:,3]/Pow_IncRefQ2[:,2]))
    return VSWR_Q2_right, tPow_IncRefQ2

def VSWR_Q4_left(pulse):
    Pow_IncRefQ4, tPow_IncRefQ4 = pw.tsbase(pulse,'GICHANTPOWQ4', nargout=2)   
    VSWR_Q4_left  = (1 + np.sqrt(Pow_IncRefQ4[:,1]/Pow_IncRefQ4[:,0])) / \
                    (1 - np.sqrt(Pow_IncRefQ4[:,1]/Pow_IncRefQ4[:,0]))
    return VSWR_Q4_left, tPow_IncRefQ4

def VSWR_Q4_right(pulse):
    Pow_IncRefQ4, tPow_IncRefQ4 = pw.tsbase(pulse,'GICHANTPOWQ4', nargout=2)   
    VSWR_Q4_right  = (1 + np.sqrt(Pow_IncRefQ4[:,3]/Pow_IncRefQ4[:,2])) / \
                    (1 - np.sqrt(Pow_IncRefQ4[:,3]/Pow_IncRefQ4[:,2]))
    return VSWR_Q4_right, tPow_IncRefQ4


def smooth(y, window_length=51, polyorder=3):
    return savgol_filter(np.squeeze(y), window_length, polyorder)

def IC_Positions(pulse):
    y = pw.tsmat(pulse, 'EXP=T=S;Position;PosICRH')
    return y, np.array([-1, -1, -1])

def LH_Positions(pulse):
    y = pw.tsmat(pulse, 'EXP=T=S;Position;PosLHCD')
    return y, np.array([-1, -1])

def LPA_Position(pulse):
    ' Constant value - to be used only if GMAG_POSLPA%1 is not working'
    y = pw.tsmat(pulse, 'EXP=T=S;Position;PosLPA')
    return np.array([y]), np.array([-1])

def IC_Frequencies(pulse):
    y = pw.tsmat(pulse, 'DFCI;PILOTAGE;ICHFREQ')
    return y, np.array([-1, -1, -1])

def IC_FPGA_Temperatures(pulse):
    y = pw.tsmat(pulse, 'DFCI;MONITORING;Temp')
    return y, np.array([-1, -1, -1, -1, -1, -1])

def tignitron(pulse):
    t = pw.tsmat(pulse, 'IGNITRON|1')
    return t, -1

def IC_Errors(pulse):
    '''
    Renvoie un
        // Ecriture des sécurités
    TabIT[0]=NbIntTOS[0]; TabIT[6]=NbIntTOS[1]; TabIT[12]=NbIntTOS[2];
    TabIT[1]=NbIntSHAD[0]; TabIT[7]=NbIntSHAD[1]; TabIT[13]=NbIntSHAD[2];
    TabIT[2]=NbIntOPT[0]; TabIT[8]=NbIntOPT[1]; TabIT[14]=NbIntOPT[2];
    TabIT[3]=NbIntDV[0]; TabIT[9]=NbIntDV[1]; TabIT[15]=NbIntDV[2];
    TabIT[4]=NbIntTTF[0]; TabIT[10]=NbIntTTF[1]; TabIT[16]=NbIntTTF[2];    
    TabIT[5]=TotalInt[0]; TabIT[11]=TotalInt[1]; TabIT[17]=TotalInt[2];

    '''
    y = pw.tsmat(pulse, 'DFCI;PILOTAGE;ICHINT')
    return y, np.array([-1, -1, -1])

def Gamma(pulse, antenna='Q1', side='left', t1=None, t2=None):
    ' Voltage Reflection coefficient at the antenna bidirectional coupler '
    # incident and reflecter power
    Pfwd, t_Pfwd = get_sig(pulse, signals[f'IC_P_{antenna}_{side}_fwd'])
    Pref, t_Pref = get_sig(pulse, signals[f'IC_P_{antenna}_{side}_ref'])
    # reflected phase
    phase_Pref, t_phase_Pref = get_sig(pulse, signals[f'IC_Phase_{antenna} (Pr_{side} - Pf_right)'])
    
    if t1 and t2:
        Pfwd = np.mean(in_between(Pfwd, t_Pfwd, t1, t2))
        Pref = np.mean(in_between(Pref, t_Pref, t1, t2))
        phase_Pref = np.mean(in_between(phase_Pref, t_phase_Pref, t1, t2))

    return np.sqrt(Pref/Pfwd)*np.exp(1j*phase_Pref*np.pi/180), t_Pfwd

def IC_Gamma_Q1_left(pulse):
    return np.abs(Gamma(pulse, antenna='Q1', side='left'))
def IC_Gamma_Q1_right(pulse):
    return np.abs(Gamma(pulse, antenna='Q1', side='right'))
def IC_Gamma_Q2_left(pulse):
    return np.abs(Gamma(pulse, antenna='Q2', side='left'))
def IC_Gamma_Q2_right(pulse):
    return np.abs(Gamma(pulse, antenna='Q2', side='right'))
def IC_Gamma_Q4_left(pulse):
    return np.abs(Gamma(pulse, antenna='Q4', side='left'))
def IC_Gamma_Q4_right(pulse):
    return np.abs(Gamma(pulse, antenna='Q4', side='right'))

def IC_Rc_Q1_avg(pulse):
    Q1Rcleft,  t_Q1Rcleft  = pw.tsbase(pulse, 'GICHCOUPRES%1', nargout=2)
    Q1Rcright, t_Q1Rcright = pw.tsbase(pulse, 'GICHCOUPRES%2', nargout=2)
    # clean non physical values
    Q1Rcleft = np.where((Q1Rcleft < 3) & (Q1Rcleft > 0), Q1Rcleft, np.nan)
    Q1Rcright= np.where((Q1Rcright < 3) & (Q1Rcright > 0), Q1Rcright, np.nan)
    # averages
    IC_Rc_Q1 = np.nanmean([Q1Rcleft, Q1Rcright], axis=0)
    #return IC_Rc_Q1, t_Q1Rcleft
    return Q1Rcright, t_Q1Rcright

def IC_Rc_Q2_avg(pulse):
    Q2Rcleft,  t_Q2Rcleft  = pw.tsbase(pulse, 'GICHCOUPRES%3', nargout=2)
    Q2Rcright, t_Q2Rcright = pw.tsbase(pulse, 'GICHCOUPRES%4', nargout=2)
    # clean non physical values
    Q2Rcleft = np.where((Q2Rcleft < 3) & (Q2Rcleft > 0), Q2Rcleft, np.nan)
    Q2Rcright= np.where((Q2Rcright < 3) & (Q2Rcright >0), Q2Rcright, np.nan)
    # averages
    IC_Rc_Q2 = np.nanmean([Q2Rcleft, Q2Rcright], axis=0)
    return IC_Rc_Q2, t_Q2Rcleft

def IC_Rc_Q4_avg(pulse):
    Q4Rcleft,  t_Q4Rcleft  = pw.tsbase(pulse, 'GICHCOUPRES%5', nargout=2)
    Q4Rcright, t_Q4Rcright = pw.tsbase(pulse, 'GICHCOUPRES%6', nargout=2)
    # clean non physical values
    Q4Rcleft = np.where((Q4Rcleft < 3) & (Q4Rcleft > 0), Q4Rcleft, np.nan)
    Q4Rcright= np.where((Q4Rcright < 3) & (Q4Rcright >0), Q4Rcright, np.nan)
    # averages
    IC_Rc_Q4 = np.nanmean([Q4Rcleft, Q4Rcright], axis=0)
    return IC_Rc_Q4, t_Q4Rcleft

def IC_Rc_avg(pulse):
    """
    Return the average Rc of Q1 and Q2 and Q4
    """
    Rc_Q1, t = IC_Rc_Q1_avg(pulse)
    Rc_Q2, t = IC_Rc_Q2_avg(pulse)
    Rc_Q4, t = IC_Rc_Q4_avg(pulse)
    Rc_avg = np.mean([Rc_Q1, Rc_Q2, Rc_Q4], axis=0)
    return Rc_avg, t

"""
Maximum voltage anc currents on each sides
"""
def IC_VI_max_Qi(pulse, i=1, side='left', sig='Voltage'):
    y_upper, t_upper = get_sig(pulse, signals[f'IC_{sig}_{side}_upper_Q{i}'])
    y_lower, t_lower = get_sig(pulse, signals[f'IC_{sig}_{side}_lower_Q{i}'])
    if i == 1:  # probe V1 not working
        return y_lower, t_lower
    else:
        return np.amax([y_upper, y_lower], axis=0), t_lower 

def IC_Voltage_left_max_Q1(pulse):
    return IC_VI_max_Qi(pulse, i=1, side='left', sig='Voltage')
def IC_Voltage_left_max_Q2(pulse):
    return IC_VI_max_Qi(pulse, i=2, side='left', sig='Voltage')
def IC_Voltage_left_max_Q4(pulse):
    return IC_VI_max_Qi(pulse, i=4, side='left', sig='Voltage')
def IC_Voltage_right_max_Q1(pulse):
    return IC_VI_max_Qi(pulse, i=1, side='right', sig='Voltage')
def IC_Voltage_right_max_Q2(pulse):
    return IC_VI_max_Qi(pulse, i=2, side='right', sig='Voltage')
def IC_Voltage_right_max_Q4(pulse):
    return IC_VI_max_Qi(pulse, i=4, side='right', sig='Voltage')

def IC_Current_left_max_Q1(pulse):
    return IC_VI_max_Qi(pulse, i=1, side='left', sig='Current')
def IC_Current_left_max_Q2(pulse):
    return IC_VI_max_Qi(pulse, i=2, side='left', sig='Current')
def IC_Current_left_max_Q4(pulse):
    return IC_VI_max_Qi(pulse, i=4, side='left', sig='Current')
def IC_Current_right_max_Q1(pulse):
    return IC_VI_max_Qi(pulse, i=1, side='right', sig='Current')
def IC_Current_right_max_Q2(pulse):
    return IC_VI_max_Qi(pulse, i=2, side='right', sig='Current')
def IC_Current_right_max_Q4(pulse):
    return IC_VI_max_Qi(pulse, i=4, side='right', sig='Current')

"""
Forward power at generator. 
Available signals concern transmitted and reflected, so fwd is reconstructed
"""
def IC_Gen_fwd(pulse, i=1):
    p_tra, t_p_tra = pw.tsbase(pulse, f'GICHPTRAGEN%{i}', nargout=2)
    p_ref, t_p_ref = pw.tsbase(pulse, f'GICHPREFGEN%{i}', nargout=2)
    return p_tra + p_ref, t_p_tra

def IC_Gen_fwd1(pulse):
    return IC_Gen_fwd(pulse, i=1)
def IC_Gen_fwd2(pulse):
    return IC_Gen_fwd(pulse, i=2)
def IC_Gen_fwd3(pulse):
    return IC_Gen_fwd(pulse, i=3)
def IC_Gen_fwd4(pulse):
    return IC_Gen_fwd(pulse, i=4)
def IC_Gen_fwd5(pulse):
    return IC_Gen_fwd(pulse, i=5)
def IC_Gen_fwd6(pulse):
    return IC_Gen_fwd(pulse, i=6)

"""
phases ICRH
"""
# TODO : passing argument to get_sig
def delta_phi_toro_Q1_Top_LmR(pulse):
    return delta_phi_toro_Qi_Top_LmR(pulse, i=1)
def delta_phi_toro_Q2_Top_LmR(pulse):
    return delta_phi_toro_Qi_Top_LmR(pulse, i=2)
def delta_phi_toro_Q4_Top_LmR(pulse):
    return delta_phi_toro_Qi_Top_LmR(pulse, i=4)    

def delta_phi_toro_Q1_Bot_LmR(pulse):
    return delta_phi_toro_Qi_Bot_LmR(pulse, i=1)
def delta_phi_toro_Q2_Bot_LmR(pulse):
    return delta_phi_toro_Qi_Bot_LmR(pulse, i=2)
def delta_phi_toro_Q4_Bot_LmR(pulse):
    return delta_phi_toro_Qi_Bot_LmR(pulse, i=4)

def delta_phi_polo_Q1_left_BmT(pulse):
    return delta_phi_polo_Qi_left_BmT(pulse, i=1)
def delta_phi_polo_Q2_left_BmT(pulse):
    return delta_phi_polo_Qi_left_BmT(pulse, i=2)
def delta_phi_polo_Q4_left_BmT(pulse):
    return delta_phi_polo_Qi_left_BmT(pulse, i=4)

def delta_phi_polo_Q1_right_BmT(pulse):
    return delta_phi_polo_Qi_right_BmT(pulse, i=1)
def delta_phi_polo_Q2_right_BmT(pulse):
    return delta_phi_polo_Qi_right_BmT(pulse, i=2)
def delta_phi_polo_Q4_right_BmT(pulse):
    return delta_phi_polo_Qi_right_BmT(pulse, i=4)

# Q1
def delta_phi_toro_Qi_Top_LmR(pulse, i=1):
    PhasesQi, tPhasesQi = pw.tsbase(pulse, f'GICHPHASESQ{i}', nargout=2)
    dPhiToroTOP_LmR = PhasesQi[:,3] + PhasesQi[:,0] - PhasesQi[:,5]
    return  dPhiToroTOP_LmR % 360, tPhasesQi[:,0]

def delta_phi_toro_Qi_Bot_LmR(pulse, i=1):
    PhasesQi, tPhasesQi = pw.tsbase(pulse, f'GICHPHASESQ{i}', nargout=2)
    dPhiToroBOT_LmR = PhasesQi[:,4] + PhasesQi[:,0] - PhasesQi[:,6]
    return  dPhiToroBOT_LmR % 360, tPhasesQi[:,0]

def delta_phi_polo_Qi_left_BmT(pulse, i=1):
    PhasesQi, tPhasesQi = pw.tsbase(pulse, f'GICHPHASESQ{i}', nargout=2)
    dPhiPololeft_BmT  = PhasesQi[:,4] - PhasesQi[:,3]
    return dPhiPololeft_BmT, tPhasesQi[:,0]

def delta_phi_polo_Qi_right_BmT(pulse, i=1):
    PhasesQi, tPhasesQi = pw.tsbase(pulse, f'GICHPHASESQ{i}', nargout=2)
    dPhiPoloright_BmT = PhasesQi[:,6] - PhasesQi[:,5]
    return dPhiPoloright_BmT, tPhasesQi[:,0]

'''
IC Antenna Toroidal Phase filtered (gives NaN when no IC power)
'''
def phase_Q1(pulse):
    P, t_P = get_sig(pulse, signals['IC_P_Q1'])
    Phase, t_phase = get_sig(pulse, signals['IC_delta_phi_toro_Q1_Bot_LmR'])
    _filter = np.interp(t_phase, t_P, P > 0.11)
    # _filter[_filter == False] = np.nan
    return _filter*Phase, t_phase

def phase_Q2(pulse):
    P, t_P = get_sig(pulse, signals['IC_P_Q2'])
    Phase, t_phase = get_sig(pulse, signals['IC_delta_phi_toro_Q2_Top_LmR'])
    _filter = np.interp(t_phase, t_P, P > 0.11)
    # _filter[_filter == False] = np.nan
    return _filter*Phase, t_phase

def phase_Q4(pulse):
    P, t_P = get_sig(pulse, signals['IC_P_Q4'])
    Phase, t_phase = get_sig(pulse, signals['IC_delta_phi_toro_Q4_Top_LmR'])
    _filter = np.interp(t_phase, t_P, P > 0.11)
    # _filter[_filter == False] = np.nan
    return _filter*Phase, t_phase

'''
IC Antenna internal Vacuum 
'''
def IC_Q1_vacuum_left(pulse):
    y,t = pw.tsbase(pulse, 'GICHVTRANSFO%1', nargout=2)
    y = 10**(1.667*y - 9.333)
    return y,t

def IC_Q1_vacuum_right(pulse):
    y,t = pw.tsbase(pulse, 'GICHVTRANSFO%2', nargout=2)
    y = 10**(1.667*y - 9.333)
    return y,t    

def IC_Q2_vacuum_left(pulse):
    y,t = pw.tsbase(pulse, 'GICHVTRANSFO%3', nargout=2)
    y = 10**(1.667*y - 9.333)
    return y,t

def IC_Q2_vacuum_right(pulse):
    y,t = pw.tsbase(pulse, 'GICHVTRANSFO%4', nargout=2)
    y = 10**(1.667*y - 9.333)
    return y,t    

def IC_Q4_vacuum_left(pulse):
    y,t = pw.tsbase(pulse, 'GICHVTRANSFO%5', nargout=2)
    y = 10**(1.667*y - 9.333)
    return y,t

def IC_Q4_vacuum_right(pulse):
    y,t = pw.tsbase(pulse, 'GICHVTRANSFO%6', nargout=2)
    y = 10**(1.667*y - 9.333)
    return y,t    

def get_sig(pulse, sig, do_smooth=False):
    """
    Return the (y,t) numpy arrays of the signal sig for a WEST pulse
    """
    try:
        if sig['name']:
            # if a tsbase signal name
            y, t = pw.tsbase(pulse, sig['name'], nargout=2)
        else:
            # if a specific routine
            eval_str = f"{sig['fun']}({pulse}) "
            y, t = eval(eval_str)

        t = np.squeeze(t)
        y = np.squeeze(y)

        if do_smooth:
            y_smooth = smooth(y)
            y = y_smooth
    except (pw.PyWEDException, pw.tsExQueryError) as e:
        print(f"{sig['name']} #{pulse}: {e}")
        return np.nan, np.nan
    return y, t


def in_between(y, t, t_start=0, t_end=1000):
    """
    Filter the signal between t>=t_start and t<=t_end
    """
    idx = np.where((t >= t_start) & (t <= t_end))
    if np.any(idx):
        new_y = y[idx]
        new_t = t[idx]
    else:
        new_y = np.nan
        new_t = np.nan
        
    return new_y, new_t
        

def is_sig(pulse, sig, thres=0):
    """
    Return true if data from sig are available for the pulse.

    The signal data are tested against a threshold thres.
    If larger than this threshold, means there data are available.
    """
    y, t = get_sig(pulse, sig)

    if np.any(y >= thres):
        return True
    else:
        return False


def pulse_datetime(pulse):
    """
    Return the pulse datetime as a (pandas.)Timestamp and a Python datetime
    """
    date_apilote = pw.tsmat(pulse, 'APILOTE;+VME_PIL;Date_Choc')
    if not date_apilote:  # in case of : [Query Error] Invalid query, server returned 204: 'Unknown producer'
        date_apilote = -1
    pulse_dt = pd.to_datetime(date_apilote)
    # return pulse_dt, pulse_dt.to_pydatetime()
    return [pulse_dt.year, pulse_dt.month, pulse_dt.day], [-1,-1,-1]

def pulse_year(pulse):
    ' Return the pulse year '
    date_apilote = pw.tsmat(pulse, 'APILOTE;+VME_PIL;Date_Choc')
    pulse_dt = pd.to_datetime(date_apilote)
    return [pulse_dt.year,], [-1,]

def pulse_month(pulse):
    ' Return the pulse year '
    date_apilote = pw.tsmat(pulse, 'APILOTE;+VME_PIL;Date_Choc')
    pulse_dt = pd.to_datetime(date_apilote)
    return [pulse_dt.month,], [-1,]

def pulse_day(pulse):
    ' Return the pulse day '
    date_apilote = pw.tsmat(pulse, 'APILOTE;+VME_PIL;Date_Choc')
    pulse_dt = pd.to_datetime(date_apilote)
    return [pulse_dt.day,], [-1,]

def mean_min_max(y):
    """
    Return the mean, min and max of an array
    """
    return np.mean(y), np.amin(y), np.amax(y)


def mean_std(y):
    """
    Return the mean and standard deviation of an array

    Parameters
    ----------
    y : array
        signal

    Returns
    -------
    mean : array
        mean of the signal y(t)
    std : array
        std of the signal y(t)  
    
    """
    return np.mean(y), np.std(y)

def mean_std_in_between(y, t, t_start=0, t_end=1000):
    """
    Return the mean and std for a subset of signal y(t). 

    Parameters
    ----------
    y : array
        signal
    t : array
        time
    t_start : float, optional
        Start time. The default is 0.
    t_end : float, optional
        End time. The default is 1000.

    Returns
    -------
    mean : array
        mean of the signal y(t) in [t_start, t_end]
    std : array
        std of the signal y(t) in [t_start, t_end]

    """
    _y, _t = in_between(y, t, t_start, t_end)
    return mean_std(_y)


def scope(pulses, signames, 
          do_smooth=False, style_label='default', cycling_mode='ls',
          window_loc=(0,0), **kwargs):
    """
    Generate a scope for the list of pulses and the list of signal names.

    Parameters
    ----------
    pulses : list of integer
        list of pulse number
    signames : list (of list) of signals
        Description of the signals to plot
    do_smooth : boolean, optional
        Should we smooth signals? The default is False.
    style_label : str, optional
        Matplotlib style to use for the figures. The default is 'default'.
    cycling_mode : str, optional
        'ls' (linestyle) or 'color'. The default is 'ls'.
    window_loc : tuple of 2 integer, optional
        Default location of the window. The default is (0,0).

    Returns
    -------
    None.

    """
    with plt.style.context(style_label):
    
        t_fin_acq = []
        fig, axes = plt.subplots(len(signames), 1, sharex=True, figsize=(7, 9))
        # move the figure 
        fig.canvas.manager.window.move(window_loc[0], window_loc[1])
        # cycle the color for each shot number
        color_cycle = axes[0]._get_lines.prop_cycler
        
        plt.locator_params(axis='y', nbins=6)
        if type(axes) is not list:  # case of only one signal -> put axe in a list
            axes = np.array(axes)
    
        for pulse in pulses:
            _color = next(color_cycle)['color']
            # end of acquisition time - ignitron
            try:
                t_fin_acq.append(pw.tsmat(pulse, 'FINACQ|1')[0] - 32)
            except IndexError as e:
                t_fin_acq.append(100)
    
            for (sigs, ax) in zip(signames, axes):
                _legend = ''
                _lines = cycle(['-',':', '--', '-.'])
                _colors = cycle(['C0', 'C1', 'C2', 'C3', 'C4', 'C5'])
                # if a list: superpose the trace on the same axe
                if not isinstance(sigs, list):
                    sigs = [sigs]
                for sig in sigs:
                    
                    y, t = get_sig(pulse, sig, do_smooth)
                    if cycling_mode == 'ls':
#                        import pdb;pdb.set_trace()
                        ax.plot(t, y, label=f'#{pulse}', color=_color, ls=next(_lines), **kwargs)
                    elif cycling_mode == 'color':
                        ax.plot(t, y, label=f'#{pulse}', color=next(_colors), **kwargs)
                    
                    _legend += f"{sig['label']}, "
                ax.set_ylabel(f"[{sig['unit']}]")
                ax.text(0.01, 0.85, _legend, color='gray',
                        horizontalalignment='left', transform=ax.transAxes)
                ax.autoscale(enable=True, axis='y')
                if 'options' in sig:           
                    if 'yscale' in sig['options']:
                        ax.set_yscale(sig['options']['yscale'])
                    if 'ylim' in sig['options']:
                        ax.set_ylim(sig['options']['ylim'])
                    if 'ymin' in sig['options']:
                        ax.set_ylim(bottom=sig['options']['ymin'])
                    if 'ylimit' in sig['options']:
                        ax.axhline(sig['options']['ylimit'], color='r')
                    if 'ylimit_low' in sig['options']:
                        ax.axhline(sig['options']['ylimit_low'], color='g', ls='--')

        # time axis
        axes[-1].set_xlabel('t [s]')
        axes[-1].set_xlim(-0.5, np.max(t_fin_acq))
        [a.grid(True, alpha=0.2) for a in axes]
    
        fig.tight_layout()
        fig.subplots_adjust(hspace=0)
        fig.show()
        return fig, axes


def baro_Q2(pulse):
    baroQ2BP, tbaroQ2BP = pw.tsbase(pulse, 'GBARDB8%4', nargout=2)
    return baroQ2BP, tbaroQ2BP 

def baro_Q4(pulse):
    baroQ4BP, tbaroQ4BP = pw.tsbase(pulse, 'GBARDB8%9', nargout=2)
    return baroQ4BP, tbaroQ4BP 

def ECE_1(pulse): 
    Te, t_Te = pw.tsmat(pulse, 'DVECE-GVSH1%1','+')
    return Te, t_Te-32
def ECE_2(pulse): 
    Te, t_Te = pw.tsmat(pulse, 'DVECE-GVSH2%1','+')
    return Te, t_Te-32
def ECE_3(pulse): 
    Te, t_Te = pw.tsmat(pulse, 'DVECE-GVSH3%1','+')
    return Te, t_Te-32
def ECE_4(pulse): 
    Te, t_Te = pw.tsmat(pulse, 'DVECE-GVSH4%1','+')
    return Te, t_Te-32


try:
    import imas_west        
except ModuleNotFoundError as e:
    print('IMAS only available on linux machines')

def imas(func):
    """
    Decorator for IMAS data 
    Will generate NaN data is IMAS is not available
    """
    def wrapper(*args,**kwargs):
        try:
            import imas_west
            return func(*args,**kwargs)  
        except ModuleNotFoundError as e:
            print('IMAS only available on linux machines --> return NaN')
            return np.nan, np.nan
    
        except FileNotFoundError as e:
            print('IMAS file does not exist (yet?)')
            return np.nan, np.nan
    return wrapper

def Prad_pradwest(pulse):
    " total radiated power in MW"
    import pradwestc
    try:
        Prad,Pbulk,Pdivb,Pdivh,Pchan,bolofmas,tbolo,trad = pradwestc.pradwest1(pulse, fi=0)
        return Prad, trad - tignitron(pulse)[0]
    except TypeError as e:
        return np.nan, np.nan

def Prad_bulk_pradwest(pulse):
    import pradwestc
    try:
        Prad,Pbulk,Pdivb,Pdivh,Pchan,bolofmas,tbolo,trad = pradwestc.pradwest1(pulse, fi=0)
        return Pbulk, trad - tignitron(pulse)[0]
    except TypeError as e:
        return np.nan, np.nan

def frad(pulse):
    P_ohmic, t_P_ohmic = get_sig(pulse, signals['Ohmic_P'])
    P_RF, t_P_RF = get_sig(pulse, signals['RF_P_tot'])
    
    # data['Ptot'] = data['Ohmic_P'] + data['LH_P_tot'] + data['IC_P_tot']/1e3
    # data['P_conv'] = data['Ptot'] - data['Prad_bulk']
    # data['frad'] = data['Prad']/data['Ptot']
    # data['frad_bulk'] = data['Prad_bulk']/data['Ptot']
        
    
@imas
def Prad_imas(pulse):
    bolo = imas_west.get(pulse, 'bolometer')
    return bolo.power_radiated_total/1e6, bolo.time - tignitron(pulse)[0]

@imas
def Prad_bulk_imas(pulse):
    bolo = imas_west.get(pulse, 'bolometer')
    return bolo.power_radiated_inside_lcfs/1e6, bolo.time - tignitron(pulse)[0]


# @imas
# def Rext_median_nice(pulse):
#     equi = imas_west.get(pulse, 'equilibrium', 0, 1)
#     mask_eq = np.asarray(equi.code.output_flag) >= 0 # To remove not converged equilibria
#     r_ext = np.max(equi.profiles_1d.r_outboard[mask_eq], axis=1)
#     return r_ext*1e3, equi.time[mask_eq] - tignitron(pulse)[0]


def Rext_outboard_nice(pulse):
    " Return Rext median estimated by NICE reconstruction "   
    script_name='save_from_imas.py'   
    ids_name='equilibrium'
    paths=["profiles_1d.r_outboard", "time"]
    # Run the transmitted script remotely with args passed as json-like
    #https://stackoverflow.com/questions/18006161/how-to-pass-dictionary-as-command-line-argument-to-python-script
    cmd = 'module load tools_dc; python save_from_imas.py \'{"pulse":"'+str(pulse)+'", "ids_name":"'+ids_name+'", "paths":'+json.dumps(paths)+'}\''
        
    data = imas_get_remote(pulse, cmd, script_name)
    y = data['arr_0']
    t = data['arr_1'] - tignitron(pulse)[0]
    y = np.max(y, axis=1)
    return y, t

def Rext_upper_nice(pulse):
    " Return Rext upper @ Z=+250 mm estimated by NICE reconstruction "
    script_name='save_from_imas_Rext_upper.py'  
    cmd = 'module load tools_dc; python '+script_name+' \'{"pulse":"'+str(pulse)+'", "Z":"0.25"}\''

    data  = imas_get_remote(pulse, cmd, script_name)
    r_ext = data['arr_0']
    t = data['arr_1'] - tignitron(pulse)[0]
    # z_at_r_ext = data['arr_2']
    
    return r_ext, t    

def Rext_median_nice(pulse):
    " Return Rext lower @ Z=0 mm estimated by NICE reconstruction "
    script_name='save_from_imas_Rext_upper.py'  
    cmd = 'module load tools_dc; python '+script_name+' \'{"pulse":"'+str(pulse)+'", "Z":"0"}\''

    data  = imas_get_remote(pulse, cmd, script_name)
    r_ext = data['arr_0']
    t = data['arr_1'] - tignitron(pulse)[0]
    # z_at_r_ext = data['arr_2']
    
    return r_ext, t        

def Rext_lower_nice(pulse):
    " Return Rext lower @ Z=-250 mm estimated by NICE reconstruction "
    script_name='save_from_imas_Rext_upper.py'  
    cmd = 'module load tools_dc; python '+script_name+' \'{"pulse":"'+str(pulse)+'", "Z":"-0.25"}\''

    data  = imas_get_remote(pulse, cmd, script_name)
    r_ext = data['arr_0']
    t = data['arr_1'] - tignitron(pulse)[0]
    # z_at_r_ext = data['arr_2']
    
    return r_ext, t    


def z_at_r_ext_nice(pulse):
    " Return Rext lower @ Z=-250 mm estimated by NICE reconstruction "
    script_name='save_from_imas_Rext_upper.py'  
    cmd = 'module load tools_dc; python '+script_name+' \'{"pulse":"'+str(pulse)+'", "Z":"0"}\''

    data  = imas_get_remote(pulse, cmd, script_name)
    # r_ext = data['arr_0']
    t = data['arr_1'] - tignitron(pulse)[0]
    z_at_r_ext = data['arr_2']
    
    return z_at_r_ext, t  

    
def sum_power(pulse):
    P1, t1 = pw.tsmat(pulse, 'SICHPQ1', nargout=2)
    P2, t2 = pw.tsmat(pulse, 'SICHPQ2', nargout=2)
    P4, t4 = pw.tsmat(pulse, 'SICHPQ4', nargout=2)
    return P1+P2+P4, t1


def Dext(pulse, antenna='Q1'):
    """
    Gap between the LCFS (Rext_median) and an antenna
    """
    Rext, t_ext = get_sig(pulse, signals['Rext_median'])
    PosLH, t_PosLH = get_sig(pulse, signals['LH_Positions'])
    PosIC, t_PosIC = get_sig(pulse, signals['IC_Positions'])
    
    if antenna == 'Q1':
        Pos = PosIC[0]
    elif antenna == 'Q2':
        Pos = PosIC[1]
    elif antenna == 'Q4':
        Pos = PosIC[2]
    elif antenna == 'LH1':
        Pos = PosLH[0]
    elif antenna == 'LH2':
        Pos = PosLH[1]
    
    return Pos*1e3 - Rext, t_ext

def Dext_Q1(pulse):
    return Dext(pulse, antenna='Q1')
def Dext_Q2(pulse):
    return Dext(pulse, antenna='Q2')
def Dext_Q4(pulse):
    return Dext(pulse, antenna='Q4')
def Dext_LH1(pulse):
    return Dext(pulse, antenna='LH1')
def Dext_LH2(pulse):
    return Dext(pulse, antenna='LH2')

def Vloop(pulse):
    # best flux loop among the 17 available
    V, t = pw.tsbase(pulse, 'GMAG_VLOOP%4', nargout=2)
    # smoothing the result
    V_smooth = smooth(V)
    return V_smooth, t

def RF_P_tot(pulse):
    ''' Total RF Power '''
    P_LH_tot, t_LH_tot = get_sig(pulse, signals['LH_P_tot'])   
    P_IC_tot, t_tot = get_sig(pulse, signals['IC_P_tot'])   
    
    # interpolate LH data on IC data or the opposite 
    if not np.any(np.isnan(P_LH_tot)):
        P_LH_tot = np.interp(t_tot, t_LH_tot, P_LH_tot)   
    else:
        # no LH data -> 0
        P_LH_tot = np.zeros_like(P_IC_tot)
                  
    return P_LH_tot + P_IC_tot*1e-3, t_tot

def Ohmic_power(pulse):
    V, t_V = Vloop(pulse) # V
    Ip, t_Ip = get_sig(pulse, signals['Ip'])  # kA
    # interpolate signals
    _Ip = np.squeeze(np.interp(t_V, t_Ip, np.squeeze(Ip)))
    P = V * _Ip / 1e3  # MW
    return P, t_V

def Separatrix_power(pulse):
    P_rad_b, t_Prad_b = get_sig(pulse, signals['Prad_bulk'])
    if np.any(np.isnan(P_rad_b)):
        # no bolometry data -> no Prad
        return np.nan, np.nan

    P_Ohm, t_P_Ohm = get_sig(pulse, signals['Ohmic_P'])
    P_LH, t_LH = get_sig(pulse, signals['LH_P_tot'])
    P_IC, t_IC = get_sig(pulse, signals['IC_P_tot'])

    t = t_P_Ohm
    if np.any(np.isnan(P_LH)):
        t_LH, _P_LH = t, np.zeros_like(P_Ohm)
    else:
        _P_LH = np.interp(t, t_LH, P_LH.squeeze())

    if np.any(np.isnan(P_IC)):
        t_IC, _P_IC = t, np.zeros_like(P_Ohm)
    else:
        _P_IC = np.interp(t, t_IC, P_IC.squeeze()) * 1e-3 # kW -> MW


    _P_rad_b = np.interp(t, t_Prad_b, P_rad_b.squeeze())

    return P_Ohm + _P_LH + _P_IC - _P_rad_b, t


def imas_get_remote(pulse, cmd, script_name):
                    # ids_name='ece',
                    # paths=['t_e_central.data', 'time'],
                    # imas_obj_fname='tmp_imas_data.npz',
                    # ):
    """
    Get a WEST IMAS data for a given IMAS IDS and paths

    Parameters
    ----------
    pulse : int
        WEST pulse number
    ids_name : str, optional
        IMAS IDS name. The default is 'ece'.
    paths : list, optional
        list of IMAS IDS path to retrieve. Default is paths=['t_e_central.data', 'time']
    imas_obj_fname : str, optional
        Temporary name for file exchange. The default is 'tmp_imas_data.npz'.
    scipt_name: string
        filename of the python script to execute remotly

    Returns
    -------
    data : dict
        Data corresponding to the order of the path dictionnary

    """
    # temp local file
    from tempfile import TemporaryFile
    from pathlib import Path
    
    imas_obj_fname = 'tmp_imas_data.npz'
    # if this temp file already exist
    
    # First need to set up SSH keys
    privatekeyfile = os.path.expanduser('id_priv.rsa')
    mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile, password='HenS2008')

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.connect('talitha.intra.cea.fr', username='JH218595', pkey=mykey)

    # Setup sftp connection and transmit this script
    sftp = client.open_sftp()
    sftp.put('C:/Users/JH218595/Documents/WEST_C4/'+script_name, script_name)

    stdin, stdout, stderr = client.exec_command(cmd)
    print(cmd)
    # shows the output of the command
    print('Error message:', stderr.read())
    for line in stdout:
        # Process each line in the remote output
        print(line)

    # Retrieve the IMAS object
    path_local = Path(os.getcwd()+'/'+imas_obj_fname)
    print(f'Copying remote file locally to {path_local}....')
    sftp.get(remotepath=f'/Home/JH218595/{imas_obj_fname}',
             localpath=path_local.as_posix())
    sftp.close()
    
    # close the SSH session
    client.close()
    
    # test: open local file
    data = np.load(imas_obj_fname, allow_pickle=True)

    return data



# @imas
# def Te(pulse):
#     ece = imas_west.get(pulse, 'ece')
#     return ece.t_e_central.data, ece.time - tignitron(pulse)[0]

def get_Te(pulse):
    script_name='save_from_imas.py'   
    ids_name='ece'
    paths=["t_e_central.data", "time"]
    # Run the transmitted script remotely with args passed as json-like
    #https://stackoverflow.com/questions/18006161/how-to-pass-dictionary-as-command-line-argument-to-python-script
    cmd = 'module load tools_dc; python save_from_imas.py \'{"pulse":"'+str(pulse)+'", "ids_name":"'+ids_name+'", "paths":'+json.dumps(paths)+'}\''

    data = imas_get_remote(pulse, cmd, script_name) 

    y = data['arr_0']
    t = data['arr_1'] - tignitron(pulse)[0]
    return y, t
    # y = data['data'][0,:]
    # t = data['data'][1,:]
    # return y, t - tignitron(pulse)[0]



def radiated_fraction(pulse):
    """
    Return the fraction of RF power radiated in percent. 

    Also gives intermediate values used in the calculation.

    Parameters
    ----------
    pulse : int
        pulse number

    Returns
    -------
    frac : float
        Fraction of the RF Power Radiated in %
    Prad_ohmic: float
        Max Radiated Power during Ohmic Phase (prior RF) [MW]
    Prad_RF: float
        Max Radiated Power during RF Phase [MW]
    PRF_max : float
        Max RF Coupled Power [MW]

    """
    try:
        P_RF, t_P_RF = get_sig(pulse, signals['RF_P_tot'])
        Prad, t_Prad = get_sig(pulse, signals['Prad'])
        # smoothing
        P_RF = smooth(P_RF, window_length=101)
        Prad = smooth(Prad, window_length=1001)
        
        # interpolate Prad on P_RF
        Prad = np.interp(t_P_RF, t_Prad, Prad)
        
        # max radiated power during ohmic Phase
        idx_ohmic = P_RF < 0.05
        idx_RF = P_RF > 0.1
        idx_start_RF = np.argmin(P_RF < 0.1)
        Prad_ohmic = np.amax(Prad[:idx_start_RF])
        
        Prad_RF = np.amax(Prad[idx_RF])
        PRF_max = np.amax(P_RF[idx_RF])
        
        frac = (Prad_RF - Prad_ohmic)/PRF_max * 100
        print(f'{pulse}\t{Prad_ohmic}\t{Prad_RF}\t{PRF_max}\t{frac}')
        return frac, Prad_ohmic, Prad_RF, PRF_max
    except ValueError as e:
        return np.NaN, np.NaN, np.NaN, np.NaN


def filter_times(y, t, ts):
    '''
    Keep only relevant data from a time series

    Parameters
    ----------
    y : array
        y(t)
    t : array
        time
    ts : list of tuples (t1, t2)
        [(t1, t2), (t3, t4), ...]
        where t1 is tart time, t2 stop time, etc.

    Returns
    -------
    y_out : array
        y(t)
    t_out : array
        time

    '''
    y_out = np.array([])
    t_out = np.array([])
    for (t1, t2) in ts:
        _y, _t = in_between(y, t, t1, t2)
        y_out = np.concatenate((y_out, _y))
        t_out = np.concatenate((t_out, _t))
    return y_out, t_out

def time_averaged_profile(data, t_start, t_end, t_init=32):
    '''
    Return time averaged reflectometry profiles

    Parameters
    ----------
    data : dictionnary
        data['tX'] : time
        data['NEX'] : density
        data['RX'] : radius
    t_start : float
        start time
    t_end : float
        stop time
    t_init: float. Default=32
        ignitron time

    Returns
    -------
    r_mean : array
        average radius
    r_std : array
        standard deviation radius
    ne_mean : array
        average density
    ne_std : array
        standard deviation density

    '''
    idx_t_start = np.argmin(abs(data['tX'] - t_start - t_init))
    idx_t_stop = np.argmin(abs(data['tX'] - t_end - t_init))
    
    ne_mean = np.mean(data['NEX'][:,idx_t_start:idx_t_stop], axis=1)
    ne_std = np.std(data['NEX'][:,idx_t_start:idx_t_stop], axis=1)
    r_mean = np.mean(data['RX'][:,idx_t_start:idx_t_stop], axis=1)
    r_std = np.std(data['RX'][:,idx_t_start:idx_t_stop], axis=1)

    return r_mean, r_std, ne_mean, ne_std

def Pam3s_to_els(flowrate_Pam3s, gas='H'):
    '''
    Convert flow rates from Pa.m^3/s to el/s
    
    1 mole de gaz occupe 22.4L (1L=1e-3m^3) à 1 bar (=1e5 Pa) et contient 6.022x10^23 molécules 
    et donc pour H:  1.2x10^24 elec.
    Donc 22.4*1e-3 m^3 * 1e5 Pa =  1.2x10^24 elec.
    --> 1 Pa.m^3 = 0.54x10^21 elec.    
    
    Parameters
    ----------
    flowrate_Pam3s: array
        Flow rate in Pa.m^3/s

    Returns
    -------
    flowrate_els: array
        Flow rate in el/s

    '''
    return flowrate_Pam3s * 0.54e21

def cutoff_density_fw_approx(f=55.5e6, k_parallel=11, B=3.2):
    '''
    Return the Fast-Wave cut-off density. Appoximation for Deuterium only plasma

    Parameters
    ----------
    f : float, optional
        RF frequency in Hz. Default is 55.5e6 Hz
    k_parallel : float, optional
        k_parallel value to use. Default is 11 m^-1
    B : float, optional
        magnetic field. The default is 3.2 T.

    Returns
    -------
    ne_co: float
        cut-off density in m^-3

    '''
    from scipy.constants import e, m_p, epsilon_0
    omega0 = 2*pi*f
    k0 = omega0/c
    # cyclotron frequency for Hydrogen
    omega_cH = e*B/m_p
    # deuterium
    Z = 1
    A = 2
    # approximation for m_s = Z m_p
    ne_co = c**2*epsilon_0*m_p/e**2 * (k_parallel**2 - k0**2)*omega_cH/omega0*(1 + Z/(1-Z+A*omega0/omega_cH))
    
    return ne_co

def cutoff_density_fw(f=55.5e6, k_parallel=11, B=3.2):
    '''
    Return the Fast-Wave cut-off density. Calculation made with PlasmaPy for Deuterium plasma only

    Parameters
    ----------
    f : float, optional
        RF frequency in Hz. Default is 55.5e6 Hz
    k_parallel : float, optional
        k_parallel value to use. Default is 11 m^-1
    B : float, optional
        magnetic field. The default is 3.2 T.

    Returns
    -------
    ne_co: float
        cut-off density in m^-3

    '''
    from astropy import units as u
    from plasmapy.formulary import gyrofrequency
    from plasmapy.formulary.dielectric import cold_plasma_permittivity_LRP
    omega_0 = 2*pi*f
    k0 = omega_0/c
    n_parallel = k_parallel/k0
    # assume Deuterium plasma only
    plasma=('e-','D+')
    # make a density constant (for constant magnetic field)
    ne = np.linspace(1e17, 1e20, 1001)    
    L, R, P = cold_plasma_permittivity_LRP(species=plasma, n=[ne/u.m**3]*len(plasma), 
                                           B=B*u.T, omega=omega_0*u.rad/u.s)
    idx_co =  np.argmin(np.abs(R - n_parallel**2))
    ne_co = ne[idx_co]
    
    return ne_co
    

def cutoff_radius(reflecto_data, f=55.5e6, k_parallel=11):
    '''
    Return the fast-Wave cut-off radial location defined for n//^2 = R 

    Parameters
    ----------
    reflecto_data : dict
        Reflectometry data, containing 'REX', 'NEX' and 'tX' arrays
    f : float, optional
        RF Frequency. The default is 55.5e6
    k_parallel : float, optional
        k_parallel value to use. Default is 11 m^-1

    Returns
    -------
    R_co: array
        cut-off radial location in meter
    t_co: array
        associated time array
    ne_co: float
        cut-off density in m^-3

    '''
    # approximate cut-off density
    ne_co = cutoff_density_fw_approx(f=f)
    
    # determine the cutoff radius, ie the radius for which ne=ne_co
    idx_R_co = np.argmin(np.abs(reflecto_data['NEX'] - ne_co), axis=0)
    R_co = reflecto_data['RX'][idx_R_co, np.arange(reflecto_data['RX'].shape[1])]
    return R_co, np.squeeze(reflecto_data['tX']), ne_co