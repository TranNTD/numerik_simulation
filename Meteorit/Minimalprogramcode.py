#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 10:45:32 2021

@author: datnguyen
"""

import numpy as np
from matplotlib import pyplot as plt


# allgemeine Konstanten
# Erdradius, Erdbeschl, Widerstandsbeiwert
rE      # Erdradius, 6356766 m wenn geopot.
g0      # Erdbeschleunigung, alt: 9.81
cw      # Widerstandsbeiwert
R       # allg. Gaskonstante, alt: 8.214
rho0    # Luftdichte am Erdboden
M       # mittlere molare Masse, alt: 0.02896
vs0     # Schallgeschwindigkeit bei 0°C

# Anfangswerte
h0    # Starthöhe 130km zum Vergleich mit AllenMcC.
v0    # Geschwindigkeit 15 mk/s
T     # Temperatur in 80km ca. -50°C
n     # mind. 3 Teile nach der Zerlegung
alpha 

# Dichte, Masse, Querschnitt
d     # Durchmesser bei V=1cm^3, alt: 0.01
rhoM  # Dichte von Eisen kg/m^3, alt: 7860

class Meteor:
    def __init__(self, h0, v0, theta0, d , t0=0):
        #Parameter definieren
    
    def dichte(self,h): 
        #Dichte berechnen
        
    def beschl(self,h, v):   
        #Beschleunigung berechnen
        
    def Zerlegen(self,n, prozent=[]): 
        #n=Anzahl der Meteoritsstücke #prozent ist list, len(prozent)=n
        #Neue Masse berechnen
    def Trajectories(self):
        #Amax, Tmax, Hmax definieren und berechnen
    
#Main programm
Meteorganz = Meteor(....)
Meterganz.Trajactorie()


#Plot
title='Meteorit'
fig = plt.figure()
plt.title(title)
......
......
#Animation
def Animation:
    .......
    
anim = animation.FuncAnimation(fig, MeteorAni, frames = maxframes, interval = 10, blit = True)
#print("saving animation")
#anim.save("Meteorit.mp4", fps=10)
        
    
        
    
