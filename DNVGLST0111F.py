# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 07:32:12 2018

@author: Deki
"""

import scipy as sp
import math 

''' Claculation of Environmental Loads of DP Vessels as per DNVGL-ST-0111.
All units are in SI system; angles are in degrees.
Vessel conditions: Zero forward speed, summer load line draft and even keel;
all deck equipment is in "parked" mode'''

#wind loads
def windLoad (Lpp, Bmax, draft, Vwind, directionWind, AFwind, ALwind, XLair, AirRO):
    directionWindPi = math.radians(directionWind)
    FXwind = 0.5*AirRO*Vwind**2*AFwind*(-0.7*math.cos(directionWindPi))
    FYwind = 0.5*AirRO*Vwind**2*ALwind*(0.9*math.sin(directionWindPi))

    if directionWindPi <= math.pi:
        dirWind = directionWindPi
    else:
        dirWind = 2*math.pi-directionWindPi

#moment about Z-axis
    MZwind = FYwind*(XLair+0.3*(1-2*dirWind/math.pi)*Lpp)
    return (FXwind, FYwind, MZwind)

#current loads
def currLoad (Lpp, Bmax, draft, ALcurr, directionCurr, XLcurr, WaterRO, Vcurr):
    directionCurrPi = math.radians(directionCurr)
    FXcurr = 0.5*WaterRO*Vcurr**2*Bmax*draft*(-0.07*math.cos(directionCurrPi))
    FYcurr = 0.5*WaterRO*Vcurr**2*ALcurr*(0.6*math.sin(directionCurrPi))
    
    
    if directionCurrPi <= math.pi:
        dirCurr = directionCurrPi
    else:
        dirCurr = 2*math.pi-directionCurrPi
    
    CurrFac1 = 0.4*(1-2*dirCurr/math.pi)
    if CurrFac1 < 0.25:
        CurrFac = CurrFac1
    else: 
        CurrFac = 0.25
        
    if CurrFac > -0.2:
        CurrFacM = CurrFac
    else:
        CurrFacM = -0.2
    MZcurr = FYcurr*(XLcurr + CurrFacM*Lpp)
    return (FXcurr, FYcurr, MZcurr)

#wawe drift loads
def waveLoad (Lpp, Bmax, draft, Cwlaft, bowangle, hs, Xlos, Awlaft, waveDirection, Los, Tz, WaterRO):
    bowanglePi = math.radians(bowangle)
    h1A = 0.8*bowanglePi**0.45
    #h1B1=0.7*Cwlaft**2
    if Cwlaft >= 0.85 and Cwlaft <=1.15:
        h1B = Cwlaft
    else:
        h1B=0.7*Cwlaft**2
    directionWavePi = math.radians(waveDirection)
    
    if directionWavePi <= math.pi:
        dirWave = directionWavePi
    else:
        dirWave = 2*math.pi-directionWavePi
        
    h1 = h1A + dirWave/math.pi*(h1B*Cwlaft - h1A*bowanglePi)
    h2 = 0.05 + 0.95*math.atan(1.45*dirWave - 1.75)
    h = 0.09*h1+h2
    
    Tsurge = Tz/(0.9*Lpp**0.33)
    Tsway = Tz/(0.75*Bmax**0.5)
    
    if Tsway < 1:
        fTsway = 1
    else:
        fTsway = Tsway**-3*math.e**(1-Tsway**-3)
    if Tsurge < 1:
        fTsurge = 1
    else:
        fTsurge = Tsurge**-3*math.e**(1-Tsurge**-3)
        
    Fxwave = 0.5*WaterRO*9.81*hs**2*Bmax*h*fTsurge
    Fywave = 0.5*WaterRO*9.81*hs**2*Los*(0.09*math.sin(directionWavePi))*fTsway
    Mzwave = Fywave*(Xlos+(0.05-0.14*dirWave/math.pi)*Los)
    return (Fxwave, Fywave, Mzwave)



 
