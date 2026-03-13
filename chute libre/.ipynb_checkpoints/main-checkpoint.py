from kinematics import velocity
from kinematics import position
from energy import potential_energy
from energy import kinetic_energy
from energy import ke_by_pe

import argparse

import numpy as np
import matplotlib.pyplot as plt

#=====Argument Parsing===============================================
parser = argparse.ArgumentParser()
parser.add_argument(dest='t', type=float, help="Time for which the simulation is ran, in seconds.")
parser.add_argument(dest='h',type=float, help="Height of the body from the surface, in meters.")
parser.add_argument(dest='m',type=float, help="Mass of the body, in kilograms.")
parser.add_argument('-g', '--acceleration',type=float, dest='g', default="9.81", help="Acceleration due to gravity")
args = parser.parse_args()

t = args.t
y = args.h
m = args.m
g = 9.81 #m/s^2
time = np.linspace(0,t)
y = 100

v = list(map(velocity, time))
pos = list(map(position, v, time))
x = np.ones((len(pos)))

m_ene = []
for i in range((len(pos))):
    m_ene.append(m)

pe = list(map(potential_energy, m_ene, pos))
ke = list(map(kinetic_energy, m_ene,  v))
r = list(map(ke_by_pe, ke, pe))

fig, ax = plt.subplots(2,2, figsize=(8,7))

ax[0,0].scatter(x,pos,c='red',alpha=0.3)
ax[0,0].set_xlabel("X-coordinate")
ax[0,0].set_ylabel("Height (m)")
ax[0,0].grid(True)

ax[0,1].plot(time,pe,linestyle=":", color = 'black',label="Potential Energy")
ax[0,1].set_xlabel("Time (s)")
ax[0,1].set_ylabel("Potential Energy (J)")
ax[0,1].grid(True)
ax[0,1].legend(loc='lower center', frameon=False, ncol = 2)
ax2 = ax[0,1].twinx()
ax2.plot(time,ke,linestyle="-" , color = 'r', label="Kinetic Energy")
ax2.set_ylabel("Kinetic Energy (J)", color = "r")
ax2.tick_params(axis='y', labelcolor='r')
ax2.legend(loc='upper center', frameon=False, ncol = 2)

ax[1,1].plot(pos,ke,linestyle=":", color = 'b',label="Kinetic Energy")
ax[1,1].set_xlabel("Height (m)")
ax[1,1].set_ylabel("Kinetic Energy (J)")
ax[1,1].grid(True)
ax[1,1].legend(loc='lower center', frameon=False, ncol = 2)
ax3 = ax[1,1].twinx()
ax3.plot(pos,pe,linestyle="--" , color = 'g', label="Potential Energy")
ax3.set_ylabel("Potential Energy (J)", color = "g")
ax3.tick_params(axis='y', labelcolor='g')
ax3.legend(loc='upper center', frameon=False, ncol = 2)

ax[1,0].plot(time,v,linestyle="-.", color = 'b',label="Velocity")
ax[1,0].set_xlabel("Time (s)")
ax[1,0].set_ylabel("Velocity (m/s)")
ax[1,0].grid(True)
ax[1,0].legend(loc='lower center', frameon=False, ncol = 2)
ax4 = ax[1,0].twinx()
ax4.plot(time,r,linestyle="--" , color = 'r', label="KE/PE")
ax4.set_ylabel("KE/PE", color = "r")
ax4.tick_params(axis='y', labelcolor='r')
ax4.legend(loc='upper center', frameon=False, ncol = 2)
plt.tight_layout()
plt.show()