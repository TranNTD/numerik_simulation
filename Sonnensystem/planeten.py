# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 17:47:50 2021

@author: trann
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation as ani


Gravitation=6.67430e-11 # m^3/kg.s^2
AU         =1.49597870700e11
#Gravitationsparameter muy m^3/s^2
GP_Sonne   = 1.32712440018e22
GP_Merkus  = 2.2032e13
GP_Jupiter = 1.26686534e17
GD_Pluto   = 8.71e11


#Masse 10^24kg
m_Sonne   = 1988500e24
m_Merkus  = 0.33011e24
m_Jupiter = 1898.19e24
m_Pluto   = 0.01303e24
m_Erde    = 5.9723e24
m_Mond    = 0.07346e24
m_Venus   = 4.87675e24

# Max und Min Abstand von CENTERPLANET

rmax_Sonne, rmin_Sonne     = 0,0
rmax_Merkus, rmin_Merkus   = 69.82e6, 46e6
rmax_Jupiter, rmin_Jupiter = 816.62e6, 740.52e6
rmax_Pluto, rmin_Pluto     = 7375.93e6, 4436.82e6
rmax_Erde, rmin_Erde       = 152.1e6 ,147.09e6
rmax_Mond, rmin_Mond       = 0.4055e6, 0.3633e6 # von ERDE
rmax_Venus, rmin_Venus     = 108.94e6,107.48e6


# Vmax und Vmin von Planeten

vmax_Sonne, vmin_Sonne = 0,0
vmax_Merkus, vmin_Merkus = 58.98, 38.86
vmax_Jupiter, vmin_Jupiter = 13.72, 12.44
vmax_Pluto, vmin_Pluto = 6.1, 3.71
vmax_Erde, vmin_Erde = 30.29, 29.29
vmax_Mond, vmin_Mond = 1.082, 1.022
vmin_Venus=34.79

#Umlaufzeit (Tag)
T_Merkus = 115.88
T_Jupiter = 398.88
T_Pluto = 266.73
T_Erde = 1
T_Mond = 27.3217
T_Venus = 583.92 

###
SONNEN_radius = 695700
MOND_radius = 1737.4
ERDE_radius = 6731
VENUS_radius =6051.8
MERKUS_radius =2439.7

### Positionsvektor, Geschwindigkeitsvektor, Beschleunigungsvektor
class vektor:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        
        
class Planet:
    def __init__(self, position, masse, v, a, t, rmin, rmax, vmin, name, centerPlanet,multi=1.0): 
        self.position = position 
        self.masse = masse
        self.v = v
        self.a = a
        self.t = t #Umlaufzeit
        self.rmin=rmin
        self.rmax=rmax
        self.vmin=vmin
        self.name = name
        #self.centerPlanet=centerPlanet 
        self.list_px=[]
        self.list_py=[]
        if centerPlanet is None: # for SUN
            self.centerPlanet = None
            self.position.x=0
            self.position.y=0
            self.all_others=[]
        else:                               #for Planets that have center as SUN or Earth...
            self.centerPlanet=centerPlanet
            self.all_others =[centerPlanet] # for the moon
            self.position.x += self.centerPlanet.position.x
            self.position.y += self.centerPlanet.position.y
            self.v.x += self.centerPlanet.v.x 
            self.v.y += self.centerPlanet.v.y
            for other in self.all_others:
                ax,ay = my_beschl(self,other)
                self.a.x +=ax
                self.a.y +=ay
            
            self.a.x += self.centerPlanet.a.x
            self.a.y += self.centerPlanet.a.y 

    def add_center(self,others):    #for the moon that rotate arround the earth and sun
        for other in others:
            self.all_others.append(other)
           
            

            
#############################################       
#----Animation----------


def my_beschl(gesuchteP,other):
    planet_location = np.asarray([gesuchteP.position.x,gesuchteP.position.y])
    center_location = np.asarray([other.position.x,other.position.y])
    dr = (planet_location-center_location)*1000
    alpha = Gravitation/np.linalg.norm(dr)**3
    a = -dr * other.masse * alpha
    return a

def beschleunigung_update(gesuchteP): # durch die gravitation der andere Planeten
    #anziehende Kraft
    acceleration=vektor(0,0)
    ax, ay = 0,0
    for other in gesuchteP.all_others:
        ax_i, ay_i = my_beschl(gesuchteP,other)
        ax += ax_i
        ay += ay_i
    acceleration.x=ax
    acceleration.y=ay
    return acceleration

def alles_update(Planet,dt):
    Planet.v.x += (dt*Planet.a.x)/1000
    Planet.v.y += (dt*Planet.a.y)/1000
    if Planet.centerPlanet is not None:
        Planet.position.x += Planet.v.x*dt 
        Planet.position.y += Planet.v.y*dt
    Planet.a=beschleunigung_update(Planet)
    
# PLANETEN DEFINIEREN    
SUN = Planet (vektor(0,0),m_Sonne, vektor(0,0), vektor(0,0), 0,0, 0, 0,name= 'Sonne',centerPlanet=None)
JUPITER = Planet(vektor(rmax_Jupiter,0), m_Jupiter, vektor(0,vmin_Jupiter), vektor(0,0), 50, rmin_Jupiter,rmax_Jupiter, vmin_Jupiter,'Jupiter', SUN   )
MERKUS = Planet(vektor(rmax_Merkus,0), m_Merkus, vektor(0,vmin_Merkus), vektor(0,0), 50, rmin_Merkus,rmax_Merkus,vmin_Merkus,'Merkus' ,SUN  )
ERDE = Planet(vektor(rmax_Erde,0), m_Erde, vektor(0,vmin_Erde), vektor(0,0), 50, rmin_Erde, rmax_Erde,vmin_Erde,'Erde',SUN)
VENUS = Planet(vektor(rmax_Venus,0), m_Venus, vektor(0,vmin_Venus), vektor(0,0), 50, rmin_Venus, rmax_Venus,vmin_Venus,'Venus',SUN)
MOND = Planet(vektor(rmax_Mond,0),m_Mond, vektor(0,vmin_Mond), vektor(0,0),0,rmin_Mond, rmax_Mond, vmin_Mond,"Mond", ERDE ,multi=10)
MOND.add_center([SUN])

Planeten=[SUN,ERDE,VENUS,MERKUS,MOND]

##########################################
simulation_days = int(12*265.25)
total_steps = int(simulation_days * 24 * 3600)
fps = 60
video_duration = 60 #sek
delta_step = int(total_steps/(fps*video_duration))
time_array = np.arange(start=0, stop = total_steps, step=delta_step)
   
fig2 = plt.figure()
plt.style.use('dark_background')
ax=plt.axes()

location_list=[] 
for planet in Planeten:
     location_list.append({"x":[], "y":[], "name":planet.name})
  
def location_update(Planeten, dt):
    for i, planet in enumerate(location_list):#
        alles_update(Planeten[i],dt)
        planet["x"].append(Planeten[i].position.x)
        planet["y"].append(Planeten[i].position.y)    
 
for i in time_array:#
    location_update(Planeten, delta_step)

###### listpx und listpy aller Planeten erstellen#####
for i, planet in enumerate(location_list):
    Planeten[i].list_px.extend(planet['x'])
    Planeten[i].list_py.extend(planet['y']) 
 
max_x=max(max(Planeten[0].list_px),max(Planeten[1].list_px),max(Planeten[2].list_px),max(Planeten[3].list_px))
max_y=max(max(Planeten[0].list_py),max(Planeten[1].list_py),max(Planeten[2].list_py),max(Planeten[3].list_py))


#### Bahnkurve Plotten 
ax=plt.axes(xlim=(-max_x*1.5,max_x*1.5),ylim=(-max_y*1.5,max_y*1.5))    
ax.plot(ERDE.list_px,ERDE.list_py, color = 'b',linewidth =0.1)
ax.plot(MERKUS.list_px,MERKUS.list_py, color = 'gray',linewidth =0.01)
ax.plot(VENUS.list_px,VENUS.list_py, color = 'g',linewidth =0.05)
ax.plot(MOND.list_px,MOND.list_py, color='r', linewidth=0.05)

Planet0, = ax.plot([SUN.list_px[0]],[SUN.list_py[0]],marker='o',markersize=25, color='orange')
Planet1, = ax.plot([ERDE.list_px[0]],[ERDE.list_py[0]],marker='o', markersize=15, color='b',label=ERDE.name)
Planet2, = ax.plot([MERKUS.list_px[0]],[MERKUS.list_px[0]],marker='o',markersize=4, color="gray",label=MERKUS.name)
Planet3, = ax.plot([VENUS.list_px[0]],[VENUS.list_px[0]],marker='o',markersize=10, color='green',label=VENUS.name)
Planet4, = ax.plot([ERDE.list_px[0]+2e7*np.cos(0)],[ERDE.list_px[0]+2e7*np.sin(0)],marker='o', color='r',markersize=4, label=MOND.name)
#Planet4, = ax.plot([MOND.list_px[0]],[MOND.list_px[0]],marker='o',markersize=10, color='r',label=MOND.name)

def animate(i):
    i = int(total_steps/delta_step * (i/(fps*video_duration)))
    Planet0.set_data([SUN.list_px[i]], [SUN.list_py[i]])
    Planet1.set_data([ERDE.list_px[i]], [ERDE.list_py[i]])
    Planet2.set_data([MERKUS.list_px[i]], [MERKUS.list_py[i]])
    Planet3.set_data([VENUS.list_px[i]], [VENUS.list_py[i]])
    Planet4.set_data([ERDE.list_px[i]+2e7*np.cos(0.1*i)], [ERDE.list_py[i]+2e7*np.sin(0.1*i)])
    #Planet4.set_data([MOND.list_px[i]], [MOND.list_py[i]])    
    return Planet0,  Planet1,Planet2, Planet3, Planet4,
plt.axis('off')
plt.legend(loc='best')
plt.title('My Solar System!')
anim = ani.FuncAnimation(fig2, animate, frames=fps*video_duration, interval=33, blit=True)

