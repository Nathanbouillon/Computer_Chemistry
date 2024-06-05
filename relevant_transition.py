# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 10:33:47 2024

@author: natha
"""

import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import *
from scipy.optimize import curve_fit
from scipy.stats import linregress
import matplotlib as mpl
import matplotlib.cm as cm
from scipy.signal import find_peaks
from collections import Counter
import chardet
import os
import glob as gl

import re


plt.close('all')

mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'




mpl.rcParams['xtick.major.width'] = 3
mpl.rcParams['xtick.major.size'] = 9
mpl.rcParams['ytick.major.width'] = 3
mpl.rcParams['ytick.major.size'] = 9
mpl.rcParams['xtick.minor.width'] = 1
mpl.rcParams['xtick.minor.size'] = 2.5
mpl.rcParams['ytick.minor.width'] = 1
mpl.rcParams['ytick.minor.size'] = 2.5
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['xtick.top'] = True
mpl.rcParams['ytick.right'] = True
plt.rcParams['xtick.labelsize']=20
plt.rcParams['ytick.labelsize']=35


plt.rcParams['axes.labelsize'] = 25
plt.rcParams['axes.titlesize'] = 25
# mpl.rcParams['axes.grid'] = True
# mpl.rcParams['axes.grid.axis'] = 'both'
# mpl.rcParams['axes.grid.which'] = 'major'
# mpl.rcParams['grid.alpha'] = 1



#mpl.rcParams['font.size']=25
mpl.rcParams['axes.linewidth'] = 2
mpl.rcParams["savefig.format"]='svg'
mpl.rcParams['lines.markersize'] = 10
mpl.rcParams['lines.linewidth'] = 5
mpl.rcParams['legend.fontsize'] = 20

h=4.135*10**(-15)
c=299792458


def grep(path,pattern):
    
    L=[]

    with open(path, "r") as file:
        for line in file:
            if re.search(pattern, line):
                #print(line)
                L.append(line)
    return L


# That function exctract a tuple (wavelength,oscillator strenght) for each transition in the gaussian output
def ABS(path_file_TD):
    L=grep(path_file_TD,"Excited State")
    WL=[]
    I=[]
    N=len(L)
    for k in range(N):
        i=0
        j=0
        while L[k][i] !='V' :
            i=i+1
        while L[k][j:j+2] !='nm' :
            j=j+1
        WL.append(float(L[k][i+1:j]))
    for k in range(N):
        i=0
        j=0
        while L[k][i:i+2] !='f=' :
            i=i+1
        while L[k][j:j+2] !='<S' :
            j=j+1
        I.append(float(L[k][i+2:j]))
    return WL,I


wl,f = ABS('D:/STAGE/Rh3Per/V1/SINGLETS/tdss_fatlatRhIIIphenP-v1_1_S_pbe0.com.out')   #path of your Singlet absorption file
#e=[]
#for i in wl:
#    e.append(h*c/(i*10**(-9)))
    
#print(f[0],e[0],wl[0])
states=[]
wltrans=[]
Energy=[]
for i in range(len(f)):
    states.append([i+1,f[i],h*c/(wl[i]*10**(-9)),wl[i]])
    wltrans.append(wl[i])
    Energy.append(h*c/(wl[i]*10**(-9)))
print(states)
print(wltrans)    
    