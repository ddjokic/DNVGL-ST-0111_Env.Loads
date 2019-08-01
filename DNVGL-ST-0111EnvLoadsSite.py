# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 10:21:01 2018

@author: Deki
"""

''' Calculation of Environmental Loads of DP Vessels as per DNVGL-ST-0111.
All units are in SI system; angles are in degrees.
Vessel conditions: Zero forward speed, summer load line draft and even keel;
all deck equipment is in "parked" mode'''

import DNVGLST0111F as dnv 

Lpp = 80 #vessel's length between perpendiculars, m
Bmax = 18 #vessel's max breadth at water line, m
draft = 4 #vessel's summer load line draft, m

Vwind = 2 #wind speed m/s 
directionWind = 240 #wind coming direction in degrees
AFwind = 1000 #frontal projected wind area
ALwind = 2000 #longitudinal projected wind area
XLair = 3 #longitudinal position of the area center of AL,wind
AirRO = 1.226 #air density in kg/m3

ALcurr = 1200 #longitudinal projected submerged current area
directionCurr = 240 #current speed comming from direction
XLcurr = 5 #long. position of the area center of ALcurr
WaterRO = 1026 #water density kg/m3
Vcurr = 2 #current speed

Cwlaft = 1  #water plane area coefficient of the water plane area behind midship in range (0.85, 1.15)
bowangle = 45 #Figure 3-2
hs =2  #significan wave height
Xlos = 36 #Figure 3-1
Awlaft = 1000 #water plane area for x < 0, Fig. 3-1
waveDirection = 240
Los = 75 #long. distance between foremost and aftmost points under water
Tp = 10  #peak wave period
Tz=Tp/1.04049  #Pierson Moskowitz wave spectrum with cos2 spreading

windLoading = dnv.windLoad (Lpp, Bmax, draft, Vwind, directionWind, AFwind, ALwind, XLair, AirRO)
currentLoading = dnv.currLoad (Lpp, Bmax, draft, ALcurr, directionCurr, XLcurr, WaterRO, Vcurr)
waveLoading = dnv.waveLoad (Lpp, Bmax, draft, Cwlaft, bowangle, hs, Xlos, Awlaft, waveDirection, Los, Tz, WaterRO)

Fx = windLoading[0]+currentLoading[0]+waveLoading[0]
Fy = windLoading[1]+currentLoading[1]+waveLoading[1]
Mz = windLoading[2]+currentLoading[2]+waveLoading[2]

print "FXwind, FYwind, MZwind :", windLoading
print "FXcurrent, FYCurrent, MZcurrent :", currentLoading
print "FXwave, FYwave, MZwave :", waveLoading
print "Fx[N] = ", Fx
print "Fy[N] = ", Fy
print "Mz[Nm] = ", Mz