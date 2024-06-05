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



wl,f = ABS('D:/STAGE/Rh3Per/V1/SINGLETS/tdss_flatbis_RhIIIphenP-v1_1_S_pbe0.com.out')   #path of your Singlet absorption file

# This function create the gaussian expansion of the dirac signals
def spectrum(wl,osc,sigma,x):
    gwl=[]
    for wli in x:
        tot=0
        for wlj,fi in zip(wl,osc):
            tot += fi*np.exp(-(((h*c/(wlj*10**(-9)))-h*c/(wli*10**(-9)))/sigma)**2)
        gwl.append(tot)
    return gwl


# Parameters to adjust for your file
x=np.linspace(160,1000, num=25000, endpoint=True) # x serve as a fictionnal wavelength that will expand the signals
sigma=0.35

fig, ax = plt.subplots(figsize=(8, 6))  # Adjust figsize as needed

# Plot vertical sticks for oscillation strengths
for wli, osc_strength in zip(wl, f):
    ax.plot((wli, wli), (0, osc_strength), c="k", linewidth=1.5, linestyle="-")  # Adjust linewidth for sharper sticks

# Plot transient absorption spectrum
gwl = spectrum(wl, f, sigma, x)
ax.plot(x, gwl, "m", linewidth=2.0, label='Absorption spectrum (PBE0/def2svp)')

# Customize plot labels, ticks, and appearance
ax.set_xlabel("Wavelength (nm)", fontsize=14)
ax.set_ylabel("Oscillation Strength", fontsize=14)
ax.tick_params(axis='both', which='major', labelsize=12)
ax.grid(True)
ax.set_xlim(250, 830)
ax.set_ylim(0,1.5)


# Customize spine appearance for aesthetics
for spine in ax.spines.values():
    spine.set_linewidth(1.5)


# Show legend for the transient absorption plot
ax.legend(fontsize=12, loc='upper right')

# Tighten layout and save the plot
plt.tight_layout()
plt.savefig('D:/STAGE/Rh3Per/V1/SINGLETS/tdss_flatbis_RhIIIphenP-v1_1_S_pbe0.png', dpi=300)

plt.show()
