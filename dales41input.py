#!/usr/bin/python
# description: some useful function for generating DALES input files

from numpy import *
import matplotlib.pyplot as plt

########### area factor matrix ###########
def areafacgen(turr,dy,diag=False):

    turrgr = int(round(turr/dy))
    gam_q4 = zeros((turrgr+1,turrgr+1)) 
    
    num = 100

    for k in range(0,turrgr+1):
        for j in range(0,turrgr+1):
            if j==turrgr:
                y = linspace(j-0.5,j,num=num)
            else:
                y = linspace(j-0.5,j+0.5,num=num)
            z = (turrgr**2-(y)**2)**0.5 - (k-1) - 0.5
            for i in range(0,len(z)):
                if z[i] > 1:
                    z[i] = 1
                if z[i] < 0:
                    z[i] = 0
            gam_q4[k,j] = trapz(z,y)

    gam_q1 = flipud(gam_q4[1:,:])
    gam_q2 = fliplr(gam_q1[:,1:])
    gam_q3 = fliplr(gam_q4[:,1:])
    gam_q14 = append(gam_q1,gam_q4,axis=0)
    gam_q23 = append(gam_q2,gam_q3,axis=0)
    gam = append(gam_q23,gam_q14,axis=1)
    
    #print gam

    if diag == True:

        plt.contourf(gam_q4)
        plt.axis([0,turrgr,0,turrgr])
        plt.colorbar()
        plt.show()


        fig = plt.gcf()
        ax = fig.gca()

        circle = plt.Circle((0,0),turrgr)

        ax.add_artist(circle)
        plt.axis([-turrgr,turrgr,-turrgr,turrgr])
        plt.xticks(arange(-turrgr,turrgr))
        plt.yticks(arange(-turrgr,turrgr))
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
def writeprof(data,filename,header,casedir,exptitle,casetitle,casesubtitle,kmax):
    
    with open('%s/%s' % (casedir,filename),'w') as x:
        x.write('%s %s %s %s\n' % (exptitle,casetitle,casesubtitle,filename))
        for item in header:
            x.write('{0:>12}'.format(item))
        x.write('\n')
        for i in range(0,kmax):
            for item in data[i,:2]:
                x.write('{:>12.3f}'.format(item))
            x.write('{:>12.3e}'.format(data[i,2]))
            for item in data[i,3:]:
                x.write('{:>12.3f}'.format(item))
            x.write('\n')

def writelscale(data,filename,header,casedir,exptitle,casetitle,casesubtitle,kmax):
    
    with open('%s/%s' % (casedir,filename),'w') as x:
        x.write('%s %s %s %s\n' % (exptitle,casetitle,casesubtitle,filename))
        for item in header:
            x.write('{0:>12}'.format(item))
        x.write('\n')
        for i in range(0,kmax):
            for item in data[i,:3]:
                x.write('{:>12.3f}'.format(item))
            for item in data[i,3:]:
                x.write('{:>12.3e}'.format(item))
            x.write('\n')

########### write to windturbine.inp ########### 
def w2f2(data,filename,header,casedir,casetitle,casesubtitle):
    
    with open('%s/%s' % (casedir,filename),'w') as x:
        x.write('%s %s %s\n' % (casetitle,casesubtitle,filename))
        x.write('{0:>12}'.format(header))
        x.write('\n')
        for i in range(0,m):
            for item in data[i,:]:
                x.write('{0:>12.3f}'.format(item))
            x.write('\n')


########### read prof.inp from different case ###########
def readprofinp(case,subcase,username='pim'):
    path = '/home/%s/Les/Cases/%s/%s/prof.inp' % (username, case, subcase)
    data = loadtxt(path,skiprows=2)
    return {'prof.inp': data}

########### read ls_flux.inp from different case ###########
def readlsfluxinptop(case,subcase,timesteps,username='pim'):
    path = '/home/%s/Les/Cases/%s/%s/ls_flux.inp' % (username, case, subcase)
    data = zeros((timesteps,6))
    with open(path, 'r') as lsflux:
        for i, line in enumerate(lsflux):
            if i in range(3, timesteps+3):
                floats = map(float, line.split())
                data[i-3,:] = asarray(floats)

    return {'ls_flux.inp': data} 
