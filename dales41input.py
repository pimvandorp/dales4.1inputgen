#!/usr/bin/python
# description: some useful function for generating DALES input files

from numpy import *
import matplotlib.pyplot as plt

########### area factor matrix ###########
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
            gam_q4[k,j] = trapz(z,y) #z-axis: rows, y=axis: columns, vice versa in DALES code

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

    return {'gamma': gam} 
########### height ###########
def height(kmax,zmax=0,dz=0):
    h = zeros((kmax))
    zmax = float(zmax)
    dz = float(dz)
    if dz == 0:
        h[0] = zmax/(2*kmax)
        dz = zmax/kmax
        for i in range(1,kmax):
            h[i] = h[0] + i*dz
    elif zmax == 0:
        h[0] = dz/2
        for i in range(1,kmax):
            h[i] = h[0] + i*dz
    else:
        print 'dz and zmax are both defined (non-zero)'
    return h

########### write to files prof.inp, lscale.inp and scalar.inp ########### 
def w2f1(data,filename,header,casedir,casetitle,casesubtitle,kmax):
    
    mn = shape(data)
    m = mn[0]
    n = mn[1]
    for i in range(0,m):
        for j in range(0,n):
            data[i,j] = '{0:.3f}'.format(data[i,j])
          
    
    with open('%s/%s' % (casedir,filename),'w') as x:
        x.write('%s %s %s\n' % (casetitle,casesubtitle,filename))
        for item in header:
            x.write('{0:>12}'.format('%s' %item))
        x.write('\n')
        for i in range(0,kmax):
            for item in data[i,:]:
                x.write('{0:>12}'.format(str(item).ljust(8,'0')))
            x.write('\n')


########### write to windturbine.inp ########### 
def w2f2(data,filename,header,casedir,casetitle,casesubtitle):
    
    mn = shape(data)
    m = mn[0]
    n = mn[1]
    for i in range(0,m):
        for j in range(0,n):
            data[i,j] = '{0:.3f}'.format(data[i,j])
          
    
    with open('%s/%s' % (casedir,filename),'w') as x:
        x.write('%s %s %s\n' % (casetitle,casesubtitle,filename))
        x.write('{0:>12}'.format('%s' %header))
        x.write('\n')
        for i in range(0,m):
            for item in data[i,:]:
                x.write('{0:>12}'.format(str(item).ljust(8,'0')))
            x.write('\n')


########### read prof.inp from different case ###########
def readprofinp(case,subcase):
    path = '/home/pim/Les/Cases/%s/%s/prof.inp' % (case, subcase)
    data = loadtxt(path,skiprows=2)
    return {'prof.inp': data}

########### read ls_flux.inp from different case ###########
def readlsfluxinptop(case,subcase,timesteps):
    path = '/home/pim/Les/Cases/%s/%s/ls_flux.inp' % (case, subcase)
    data = zeros((timesteps,6))
    with open(path, 'r') as lsflux:
        for i, line in enumerate(lsflux):
            if i in range(3, timesteps+3):
                floats = map(float, line.split())
                data[i-3,:] = asarray(floats)

    return {'ls_flux.inp': data} 
