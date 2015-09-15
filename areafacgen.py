#!/usr/bin/python
#filename: areafacgen.py
#description: generate area factor matrix gamma(j,k)

from numpy import *
import matplotlib.pyplot as plt

def areafacgen(turbr,dy,diag=False):

    turbrgr = int(turbr/dy)
    gam_q4 = zeros((turbrgr,turbrgr)) #gamma of fourth quadrant 

    for k in range(0,turbrgr):
        for j in range(0,turbrgr):
            y = linspace(j,j+1,num=100)
            z = (turbrgr**2-y**2)**0.5 - k
            for i in range(0,len(z)):
                if z[i] > 1:
                    z[i] = 1
                if z[i] < 0:
                    z[i] = 0
            gam_q4[k,j] = trapz(z,y)

    gam_q1 = rot90(gam_q4)
    gam_q2 = rot90(gam_q1)
    gam_q3 = rot90(gam_q2)

    gam_q21 = append(gam_q2,gam_q1,axis=1)
    gam_q34 = append(gam_q3,gam_q4,axis=1)
    gam = append(gam_q21,gam_q34,axis=0)

    if diag == True:
        print gam

        plt.contourf(gam)
        plt.axis([0,2*turbrgr,0,2*turbrgr])
        plt.colorbar()
        plt.show()


        fig = plt.gcf()
        ax = fig.gca()

        circle = plt.Circle((0,0),turbrgr)

        ax.add_artist(circle)
        plt.axis([0,turbrgr,0,turbrgr])
        plt.xticks(arange(0,turbrgr))
        plt.yticks(arange(0,turbrgr))
        plt.grid(which='major',alpha=1)
        ax.set_autoscale_on(False)
        plt.show()
