# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 11:17:24 2018

@author: Deki
"""

import numpy as np
import math
import matplotlib.pyplot as plt
import DNVGLST0111F as dnv 
import os

Lpp = 80 #vessel's length between perpendiculars, m
Bmax = 18 #vessel's max breadth at water line, m
draft = 4 #vessel's summer load line draft, m

AFwind = 1000 #frontal projected wind area
ALwind = 2000 #longitudinal projected wind area
XLair = 3 #longitudinal position of the area center of AL,wind
AirRO = 1.226 #air density in kg/m3

ALcurr = 1200 #longitudinal projected submerged current area
Lcurr = 1200 #longitudinal projected submerged current area
XLcurr = 5 #long. position of the area center of ALcurr
WaterRO = 1026 #water density kg/m3

Cwlaft = 1  #water plane area coefficient of the water plane area behind midship in range (0.85, 1.15)
bowangle = 45 #Figure 3-2

Xlos = 36 #Figure 3-1
Awlaft = 1000 #water plane area for x < 0, Fig. 3-1
Los = 75 #long. distance between foremost and aftmost points under water
Tz = 10 #zero-up-crossing period of wave spectrum
dirname = "results"
filename = "results.txt"  #results filename
os.mkdir (dirname)

#import beaufort scale & playing with files
K=np.loadtxt("Beaufort_scale.csv", dtype=float, comments="#", delimiter=',', converters=None, skiprows=1, usecols=None, unpack=False, ndmin=0)
os.chdir (dirname)
fn = open(filename, 'a')
#writting headers
file.write(fn, "\nangle, windX, windY, windMz, currentX, currentY, currentMz, waveX, waveY, waveMz, totalX, totalY, totalMz")
file.write(fn,'\nUNITS: X, Y = N, Mz = Nm, angle = degrees')            
             
BFn = []  #Beaufort number
WS = []   #wind speed
HS = []   #significant wave height
PWP =[]   #Pierson Moskowitz wave spectrum with cos2 spreading
TP = []   #peak wave period
CS = []   #current speed
weather_ang = []
wind = []
current = []
wave = []

for i in range(0,12):
    BFn.append (K[i,0])
    WS.append (K[i,1])
    HS.append (K[i,2])
    TP.append (K[i,3])
    CS.append (K[i,4])
    PWP.append (K[i,3]/1.4049)  
    

for i in range (0,12):
    file.write(fn, "\nBaufort Number = " + str(BFn[i]))
    ang = []
    totalXr=[]
    totalYr=[]
    totalMzr=[]
    for angle in np.arange(0,365,5):
        
        angPi = math.radians(angle)
        ang.append(angPi)
        windLoading = dnv.windLoad (Lpp, Bmax, draft, WS[i], angle, AFwind, ALwind, XLair, AirRO)
        currentLoading = dnv.currLoad (Lpp, Bmax, draft, ALcurr, angle, XLcurr, WaterRO, CS[i])
        waveLoading = dnv.waveLoad (Lpp, Bmax, draft, Cwlaft, bowangle, HS[i], Xlos, Awlaft, angle, Los, PWP[i], WaterRO)
        #print angle, windLoading [0], windLoading[1], windLoading[2], currentLoading[0], currentLoading[1], currentLoading[2], waveLoading[0], waveLoading[1], waveLoading[2]
        #print "%0.0f %0.2f %0.2f %0.2f\n" % (angle, windLoading[0], windLoading[1], windLoading[2])#ovo
        weather_ang.append(angle)
        wind.append(windLoading)
        current.append(currentLoading)
        wave.append(waveLoading)
        totalX=round (windLoading[0]+currentLoading[0]+waveLoading[0], 2)
        totalY=round(windLoading[1]+currentLoading[1]+waveLoading[1],2)
        totalMz=round(windLoading[2]+currentLoading[2]+waveLoading[2],2)
        totalXr.append(totalX)
        totalYr.append(totalY)
        totalMzr.append(totalMz)
        fn.write('\n'+str(angle)+','+str(round(windLoading[0],2))+','+str(round(windLoading[1],2))+','+str(round(windLoading[2],2))+','+str(round(currentLoading[0],2))+','+str(round(currentLoading[1],2))+','+str(round(currentLoading[2],2))+ ','+str(round(waveLoading[0],2))+ ','+str(round(waveLoading[1],2))+ ','+str(round(waveLoading[2],2))+',' +str(totalX)+',' +str(totalY)+','+str(totalMz))
        
    file.write(fn,"\nmax(totalX) = " +str(max(totalXr))+'; for direction: '+str(np.argmax(totalXr)*5))
    file.write(fn,"\nmin(totalX) = " +str(min(totalXr)) +'; for direction: '+str(np.argmin(totalXr)*5))
    file.write(fn,"\nmax(totalY) = " +str(max(totalYr)) +'; for direction: '+str(np.argmax(totalYr)*5))
    file.write(fn,"\nmin(totalY) = " +str(min(totalYr)) +'; for direction: '+str(np.argmin(totalYr)*5))
    file.write(fn,"\nmax(totalMz) = " +str(max(totalMzr))+'; for direction: '+str(np.argmax(totalMzr)*5))
    file.write(fn, "\nmin(totalMz) = " +str(min(totalMzr))+'; for direction: '+str(np.argmin(totalMzr)*5))
    
    #plotting into the file - filename: BFn+calculated total
    
    titlex = "BFN "+str(i) +"-"+" " + "totalX"
    titley = "BFN "+str(i) +"-"+" " + "totalY"
    titlem = "BFN "+str(i) +"-"+" " + "totalMz"
    
    axx = plt.subplot(111, projection='polar')
    axx.plot(ang, totalXr)
    axx.grid(True)
    axx.set_title(titlex, va='bottom')
    namex = titlex+".png"
    plt.savefig(namex)
    plt.close()
    
    axy = plt.subplot(111, projection = 'polar')
    axy.plot(ang, totalYr)
    axy.grid(True)
    axy.set_title(titley, va='bottom')
    namey = titley+".png"
    plt.savefig(namey)
    plt.close()
    
    axM = plt.subplot(111, projection='polar')
    axM.plot(ang, totalMzr)
    axM.grid(True)
    axM.set_title(titlem, va='bottom')
    namem = titlem+".png"
    plt.savefig(namem)
    plt.close()
    print "Running BFn: ", i
    
        
fn.close() 
print "END"      


