# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 00:17:41 2021

@author: trann
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches
from matplotlib import animation


# allgemeine Konstanten
# Erdradius, Erdbeschl, Widerstandsbeiwert
rE=6366197  # Erdradius, 6356766 m wenn geopot.
g0=9.80665  # Erdbeschleunigung, alt: 9.81
cw=0.42     # Widerstandsbeiwert
R=8.31432   # allg. Gaskonstante, alt: 8.214
rho0=1.225  # Luftdichte am Erdboden
M=0.0289644 # mittlere molare Masse, alt: 0.02896
vs0=331     # Schallgeschwindigkeit bei 0°C

# Anfangswerte
h0=130000   # Starthöhe 130km zum Vergleich mit AllenMcC.
v0=15000    # Geschwindigkeit 15 mk/s
T=273.15-50 # Temperatur in 80km ca. -50°C
n = 3           # mind. 3 Teile nach der Zerlegung
alpha = -40

# Dichte, Masse, Querschnitt
d=0.012407  # Durchmesser bei V=1cm^3, alt: 0.01
rhoM=7874   # Dichte von Eisen kg/m^3, alt: 7860

class Meteor:
    def __init__(self, h0, v0, theta0, d , t0=0):
        self.h0 = h0                          #Starthöhe 
        self.v0 = v0                #Geschwindigkeit
        self.theta0 = theta0                # Eintrittswinkel
        self.d = d                     # Durchmesser bei V=1cm^3
        self.V = self.d*self.d*self.d*np.pi/6  # Volumen, V=4/3*pi*r^3 = pi/6*d^3
        self.m = rhoM*self.V                   # Masse m = rho*V
        self.A = self.d*self.d*np.pi/4         # Querschnittsfläche, A=pi*r^2=pi/4*d^2
        self.t0 = t0                         #Startzeitpunkt
    def dichte(self,h):            # barometrische Formel
        rho=rho0*np.exp(-M*g0*h/(R*T)) 
        return rho
    def beschl(self,hv, vv):                               # Veschleunigung
        rho = self.dichte(hv[1])
        v=(vv[0]**2+vv[1]**2)**(1/2)
        a=-rho*cw*self.A*v/(2*self.m)                           # Anteil Luftwiderstand
        ax,ay=a*vv[0],-g0*(rE/(rE+hv[1]))**2+a*vv[1]  # Anteil Gravitation
        return np.array((ax,ay))
    def Zerlegen(self,n, prozent=[]): #n=Anzahl der Meteoritsstücke #prozent ist list, len(prozent)=n
        zer_mlist=[]
        for i in range(n):
            zer_mlist.append(self.m*prozent[i])
        return zer_mlist #liste von masse der neue zerlegende Meteor
    def Trajectories(self):
        hv0 = np.array((0,self.h0))
        theta0rad = self.theta0 * np.pi/180
        vv0 = self.v0 * np.array((np.cos(theta0rad), np.sin(theta0rad)))
        t,h,v,a = self.t0, hv0, vv0, self.beschl(hv0,vv0)

        tl=[t]
        hl=[h]
        vl=[v]
        al=[a]
        amax,hamax,damax,vamax,tamax=0,0,0,0,0
        amin,hamin,damin,vamin,tamin=1000,0,0,0,0
        vmax,hvmax,dvmax,avmax,tvmax=0,0,0,0,0
        dt=100/self.v0     # Zeitschritt 10m-Schritte, alt: 0.1
        cnt=0
        while h[1]>0: # v ist auf die Erde zu gerichtet: vy<0
            cnt+=1
            t=t+dt

            h=h+v*dt   # Euler-Cauchy-Verfahren
            v=v+a*dt

            a=self.beschl(h,v)
    
            tl.append(t)
            hl.append(h)
            vl.append(v)
            al.append(a)
            vm=np.linalg.norm(v)
            am=np.linalg.norm(a)
            if am>amax:
                tamax,hamax,damax,vamax,amax=t,h[1],h[0],vm,am
            if am<amin:
                tamin,hamin,damin,vamin,amin=t,h[1],h[0],vm,am
            if vm>vmax:
                tvmax,hvmax,dvmax,vmax,avmax=t,h[1],h[0],vm,am
        print("#t(%5i)=%.2f (%.2f,%.2f) (%.2f,%.2f) (%.2f,%.2f)"%(cnt,t, *h, *v, *a))
        print("amax=%.2f=%.2fg, t=%.2fs, h=%.2fm, v=%.2f=%.2fM"%(amax,amax/g0,tamax,hamax,vamax,vamax/vs0))
        print("amin=%.2f=%.2fg, t=%.2fs, h=%.2fm, v=%.2f=%.2fM"%(amin,amin/g0,tamin,hamin,vamin,vamin/vs0))
        print("vmax=%.2f=%.2fM, t=%.2fs, h=%.2fm, a=%.2f=%.2fg"%(vmax,vmax/vs0,tvmax,hvmax,avmax,avmax/g0))
        
        self.vsplit = vamax
        self.hsplit = hamax
        self.tsplit = tamax
        
        self.hl = np.asarray(hl)
        self.vl = np.asarray(vl)
        self.al = np.asarray(al)
        self.tl = np.asarray(tl)
        
title='Meteorit'
fig , ax = plt.subplots()
plt.title(title)

Meteor_A=Meteor(h0,v0,alpha,d)
#print(Meteor_A.h0, Meteor_A.t0)
Meteor_A.Trajectories()
plt.plot(Meteor_A.tl[:1627],Meteor_A.hl[:1627,1],c="C00",label="Meteorit")
n=4
mneu = Meteor_A.Zerlegen(n,[0.1, 0.2, 0.3, 0.4])
Meteor_split_list = []
for i,alphaneu, k in zip(mneu,[-30,-45,-60, -65],range(1,n+1)):
    Meteor_split=Meteor(Meteor_A.hsplit,Meteor_A.vsplit,alphaneu ,i,Meteor_A.tsplit )
    Meteor_split.Trajectories()
    Meteor_split_list.append(Meteor_split)
    plt.plot(Meteor_split.tl,Meteor_split.hl[:,1],c="C0{}".format(k),label="Teil {}".format(k))
#print(Meteor_split_list[1].h0)
plt.grid(True)
plt.legend(loc="best")
plt.tight_layout()
#plt.savefig("Trajektorien.png")
#plt.show()

#Animation

width = 10
height = 6000
#print(Meteor_A.tl[0])
Ganz  = ax.add_patch(patches.Ellipse((Meteor_A.tl[0] , h0) , width ,height , fc = 'C00'))
Teil_list = []
for i in range(n):
    Teil = ax.add_patch(patches.Ellipse((Meteor_split_list[i].tl[1] , Meteor_split_list[i].h0) , width ,height , fc = "C0{}".format(i+1)))
    Teil_list.append(Teil)
#print(Meteor_A.hl[30,1])
def animate(i):
    t =  30*i
    #if Meteor_A.tl[t] <= Meteor_A.tsplit:
    if t < Meteor_A.tsplit*15:
        Ganz.center = (Meteor_A.tl[t], Meteor_A.hl[t,1] )
        
    else:
        for i in range(n):
            if t < len(Meteor_split_list[i].tl):
                Teil_list[i].center = (Meteor_split_list[i].tl[t], Meteor_split_list[i].hl[t,1])
    return  Ganz,Teil_list[0],Teil_list[1],Teil_list[2], Teil_list[3]

animation = animation.FuncAnimation(fig, animate, frames=int(len(Meteor_split_list[0].tl)), interval=15, blit=True)


#plt.show()
#animation.save('Meteorit_korrigiert.mp4', fps=100)