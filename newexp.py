#!/usr/bin/python
# Filename: newexp.py
# By Pim van Dorp, TU Delft, section Atmospheric Physics, 14 sept 2015
# Description: Generate input files, jobscript and namoptions for DALES 4.1

#-----------------------------------------------------------------
#                  0 Import Python packages             
#-----------------------------------------------------------------

from numpy import *
import dales41input as dlsin
import os
import os.path

#-----------------------------------------------------------------
#                         1  Input            
#-----------------------------------------------------------------

exptitle = 'XY_JHU-LES'
expnr = '200'

casetitle = 'Gabls1'
casesubtitle = 'Ref_Dales4'

lesversion = 'XY_JHU-LES'

#-----------------------------------------------------------------
#                     1.1 General input            
#-----------------------------------------------------------------

ncpu = 8 # total number of cpu's
nprocx = 8 # number of cpu's in x-direction
nprocy = 1 # number of cpu's in y-direction


itot = 512 # number of grid points in x-direction
jtot = 32 # number of grid points in y-direction
kmax = 64 # number of grid points in z-direction

xsize = 3200 # size of domain in x-direction [m]
ysize = 200  # size of domain in y-direction [m]

dz = 0 # grid spacing in z-direction [m] (set 0 if zmax is defined)
zmax = 400 # size of domain in z-direction [m] (set 0 if dz is defined)

dtmax = 1.0 # maximum time step [s]
runtime = 18000  # simulation runtime [s]

dtav = 60 # time interval for sampling statistics [s]
timeav = 3600 # time interval for writing statistics [s]

fielddump = 'true' # enable dump of full 3D fields of several variables

cu = 7 # transformation velocity of the Galilei transformation in x-direction
cv = 0 # transformation velocity of the Galilei transformation in y-direction

n_scalar = 1 # number of additional scalars 

xlat = 73
xlon = 0
xday = 0
xtime = 0

#-----------------------------------------------------------------
#                    1.1 Wind turbine input            
#-----------------------------------------------------------------

turbine = True # enable wind turbine
Ct = 1.33 # modified thrust coefficient Ct' for JHU-LES [-] (Betz limit = 2) 
tau = 60 # time constant of exponential wind velocity smoothing [s]
turhx = 400 # turbine hub x-position [m]
turhy = 100 # turbine hub y-position [m]
turhz = 80 # turbine hub z-position [m]
turr = 40 # turbine radius [m]

#-----------------------------------------------------------------
#                   2 Define and make folders         
#-----------------------------------------------------------------

expsdir = '/home/pim/Les/Experiments'
expdir = expsdir + '/%s/%s' %(exptitle,expnr)
casesdir = '/home/pim/Les/Cases'
casedir = casesdir +'/%s/%s' % (exptitle,casetitle)
gitdir = '/home/pim/dales/src'
builddir = '/home/pim/Les/Les_versions/Dales4.1/%s/dales.build' %lesversion
srcdir = builddir + '/src'

if not os.path.isdir(expdir):
    os.makedirs(expdir)
    
if not os.path.isdir(casedir):
    os.makedirs(casedir)

#-----------------------------------------------------------------
#                     3 Generate input files
#-----------------------------------------------------------------

h = dlsin.height(kmax, zmax, dz) # make height vector

#-----------------------------------------------------------------
#                          3.1 prof.inp
#-----------------------------------------------------------------

headerprof = ['height', 'thl', 'qt', 'u', 'v', 'tke']

profinp = zeros((kmax,6))

profinpin = dlsin.readprofinp(case=casetitle,subcase=casesubtitle)['prof.inp'] # read prof.inp from given case

# column 0 (height)
profinp[:,0] = h[:]
# column 1 (liquid water potential temperature)
profinp[:,1] = profinpin[:,1]
# colum 2 (total humidity)
profinp[:,2] = 0.
# column 3 (horizontal wind velocity)
profinp[:,3] = 8.
# column 4 (vertical wind velocity)
profinp[:,4] = 0.
# column 5 (sgs tke)
profinp[:,5] = profinpin[:,5]

dlsin.w2f1(profinp,'prof.inp',headerprof,casedir,exptitle,casetitle,kmax) # write to case folder

#-----------------------------------------------------------------
#                          3.2 lscale.inp
#-----------------------------------------------------------------

headerlscale = ['height', 'ug', 'vg', 'wfls', 'dqdtx', 'dqtdy', 'dqtdtls', 'dthlrad']

lscaleinp = zeros((kmax,8))

# column 0 (height)
lscaleinp[:,0] = h[:]
# column 1 (geostrophic wind in x-direction)
lscaleinp[:,1] = 8.
# column 2 (geostrophic wind in y-direction)
lscaleinp[:,2] = 0
# column 3 (ls subsidence)
lscaleinp[:,3] = 0
# column 4 (ls inflow of moisture in x-direction)
lscaleinp[:,4] = 0
# column 5 (ls inflow of moisture in y-direction)
lscaleinp[:,5] = 0
# column 6 (add large scale moisture change in time)
lscaleinp[:,6] = 0
# column 7 (prescribed temperature tendency due to radiation)
lscaleinp[:,7] = 0

dlsin.w2f1(lscaleinp,'lscale.inp',headerlscale,casedir,exptitle,casetitle,kmax) # write to case folder

#-----------------------------------------------------------------
#                          3.3 scalar.inp
#-----------------------------------------------------------------

if n_scalar == 1:
    headerscalar = ['height', 'scalar 1']

    scalarinp = zeros((kmax,n_scalar+1))

    # column 0 (height)
    scalarinp[:,0] = h[:]
    # column 1 (scalar 1)
    scalarinp[:,1] = 0

    dlsin.w2f1(scalarinp,'scalar.inp',headerscalar,casedir,exptitle,casetitle,kmax) # write to case folder

#-----------------------------------------------------------------
#                         3.4 ls_flux.inp
#-----------------------------------------------------------------

lsflux = 'ls_flux.inp'
headerlsflux1 = ['time', 'wtsurf', 'wqsurf', 'thls', 'qts', 'psurf']
headerlsflux2 = ['[s]', '[Km/s]', '[kgm/s]', '[K]', '[kg/kg]', '[Pa]']
headerlsflux3 = ['height', 'ug', 'vg', 'wfls', 'dqdtx', 'dqtdy', 'dqtdtls', 'dthlrad']

#-----------------------------------------------------------------
#                3.4.1 First block of ls_flux.inp
#-----------------------------------------------------------------
nt1 = 10 # number of timesteps
dt1 = 3600 # timestep

lsfluxtopin = dlsin.readlsfluxinptop(case=casetitle,subcase=casesubtitle,timesteps=nt1)['ls_flux.inp'] # read first block of ls_flux.inp from given case

lsflux1 = zeros((nt1,6))

# column 0 (time)
for i in range(0,nt1):
    lsflux1[i,0] = dt1*i
# column 1 (liquid water potential temperature flux at surface)
lsflux1[:,1] = lsfluxtopin[:,1]
# column 2 (total humidity flux at surface)
lsflux1[:,2] = lsfluxtopin[:,2]
# column 3 (liquid water potential temperature at surface)
lsflux1[:,3] = lsfluxtopin[:,3]
# column 4 (total humidity at surface)
lsflux1[:,4] = lsfluxtopin[:,4]
# column 5 (psurf)
lsflux1[:,5] = lsfluxtopin[:,5]

# write first block of ls_flux.inp to case file
with open('%s/%s' % (casedir,lsflux),'w') as x:
    x.write('%s %s %s\n' % (exptitle,casetitle,lsflux))
    for item in headerlsflux1:
        x.write('{0:>12}'.format('%s' %item))
    x.write('\n')
    for item in headerlsflux2:
        x.write('{0:>12}'.format('%s' %item))
    x.write('\n')
    for i in range(0,nt1):
        for item in lsflux1[i,:]:
            x.write('{0:>12}'.format(str(item).ljust(8,'0')))
        x.write('\n')
    x.write('\n')

#-----------------------------------------------------------------
#                3.4.2 Second block of ls_flux.inp
#-----------------------------------------------------------------

nt2 = 2 # number of timesteps
dt2 = runtime # timestep  

for i in range(0,nt2):
    t = i*dt2
    lsflux2 = zeros((kmax,8))
    # column 0 (height)
    lsflux2[:,0] = h[:]
    # column 1 (geostrophic wind in x-direction):
    lsflux2[:,1] = 8.
    # column 2 (geostrophic wind in y-direction):
    lsflux2[:,2] = 0
    # column 3 (ls subsidence):
    lsflux2[:,3] = 0
    # column 4 (ls inflow of moisture in x-direction):
    lsflux2[:,4] = 0
    # column 5 (ls inflow of moisture in y-direction):
    lsflux2[:,5] = 0
    # column 6 (add large scale moisture change in time):
    lsflux2[:,6] = 0
    # column 7 (prescribed temperature tendency due to radiation):
    lsflux2[:,7] = 0
    
    #write second block of ls_flux.inp to case file
    with open('%s/%s' % (casedir,lsflux),'a') as x:
        x.write('large scale forcing terms \n')
        for item in headerlsflux3:
            x.write('{0:>8}'.format('%s' %item))
        x.write('\n# %s\n' % t)
        for k in range(0,kmax):
            for item in lsflux2[k,:]:
                x.write('{0:>8}'.format('%s' %item))
            x.write('\n')
        x.write('\n' '\n')
 
#-----------------------------------------------------------------
#                       3.5 ls_fluxsv.inp
#-----------------------------------------------------------------       

lsfluxsv = 'ls_fluxsv.inp'
headerlsfluxsv1 = ['time', 'scalar 1']
headerlsfluxsv2 = ['[s]', '[]']
headerlsfluxsv3 = ['height', 'scalar 1']
 
#-----------------------------------------------------------------
#              3.5.1 First block of ls_fluxsv.inp
#----------------------------------------------------------------- 

nt3 = 10 # number of timesteps
dt3 = runtime # timestep

lsfluxsv1 = zeros((nt3,n_scalar+1))

# column 0 (time)
for i in range(0,nt3):
    lsfluxsv1[i,0] = dt3*i
# column 1 (scalar 1)
lsfluxsv1[:,1] = 0

# write first block of ls_fluxsv.inp to case file
with open('%s/%s' % (casedir,lsfluxsv),'w') as x:
    x.write('%s %s %s\n' % (exptitle,casetitle,lsfluxsv))
    for item in headerlsfluxsv1:
        x.write('{0:>8}'.format('%s' %item))
    x.write('\n')
    for item in headerlsfluxsv2:
        x.write('{0:>8}'.format('%s' %item))
    x.write('\n')
    for i in range(0,nt3):
        for item in lsfluxsv1[i,:]:
            x.write('{0:>8}'.format('%s' %item))
        x.write('\n')
    x.write('\n')
#-----------------------------------------------------------------
#             3.5.1 Second block of ls_fluxsv.inp
#----------------------------------------------------------------- 

nt4 = 2 # number of timesteps
dt4 = runtime # timestep  

for i in range(0,nt4):
    t = i*dt4
    lsfluxsv2 = zeros((kmax,n_scalar+1))
    lsfluxsv2[:,0] = h[:]
    # column 1 (scalar 1):
    lsfluxsv2[:,1] = 0
    
    #write second block of ls_fluxsv.inp to case file
    with open('%s/%s' % (casedir,lsfluxsv),'a') as x:
        x.write('large scale forcing terms \n')
        for item in headerlsfluxsv3:
            x.write('{0:>8}'.format('%s' %item))
        x.write('\n# %s\n' % t)
        for k in range(0,kmax):
            for item in lsfluxsv2[k,:]:
                x.write('{0:>8}'.format('%s' %item))
            x.write('\n')
        x.write('\n' '\n')

#-----------------------------------------------------------------
#      3.6  Generate gamma.inp (area factor for wind turbine)
#-----------------------------------------------------------------

if turbine == True:
    dy = ysize/float(jtot) # grid spacing (equidistant grid is assumed and required)

    gamma = dlsin.areafacgen(turr=turr,dy=dy)['gamma'] 

    headerwindturbine = 'Area factor matrix gamma(j,k)'
    dlsin.w2f2(gamma,'gamma.inp',headerwindturbine,casedir,exptitle,casetitle)

#-----------------------------------------------------------------
#                     4 Generate jobscript
#-----------------------------------------------------------------

with open(expdir + '/job.%s' % expnr, 'w') as job:
    job.write('#!/bin/bash\n#$ -pe mpi %s\n#$ -q all.q\n#$ -l h_rt=100000\n\n' % (ncpu))
    job.write('expnr=%s\nExp_dir=$(pwd)\nGit_dir=%s\nLes_dir=%s\nCase_dir=%s\n\n' % (expnr,gitdir,srcdir,casedir))
    job.write('cp $Exp_dir/namoptions.$expnr $Exp_dir/namoptions\n')
    job.write('cp $Case_dir/prof.inp$case_ext $Exp_dir/prof.inp.$expnr\n')
    job.write('cp $Case_dir/lscale.inp$case_ext $Exp_dir/lscale.inp.$expnr\n')
    job.write('cp $Case_dir/scalar.inp$case_ext $Exp_dir/scalar.inp.$expnr\n')
    job.write('cp $Case_dir/ls_flux.inp$case_ext $Exp_dir/ls_flux.inp.$expnr\n')
    job.write('cp $Case_dir/gamma.inp$case_ext $Exp_dir/gamma.inp.$expnr\n')
    job.write('cp $Case_dir/ls_fluxsv.inp$case_ext $Exp_dir/ls_fluxsv.inp.$expnr\n\n')
    job.write('mkdir -p $Exp_dir/Code\n')
    job.write('mkdir -p $Exp_dir/INIT\n\n')
    job.write('cp $Git_dir/*f90 $Exp_dir/Code/.\n')
    job.write('cp $Les_dir/dales4 .\n\n')
    job.write('mpirun dales4\n\n')
    job.write('mv init* $Exp_dir/INIT')
#-----------------------------------------------------------------
#                   5 Generate namoptions
#-----------------------------------------------------------------  

with open(expdir + '/namoptions.%s' % expnr, 'w') as nam:
    nam.write('&RUN\n') 
    nam.write('{0:<12}'.format('iexpnr')+'=  '+'%s\n' % expnr)
    nam.write('{0:<12}'.format('lwarmstart')+'=  '+'.false.\n')
    nam.write('{0:<12}'.format('startfile')+'=  '+'\'initd06h00m000.017\'\n')
    nam.write('{0:<12}'.format('runtime')+'=  '+'%s\n' % runtime)
    nam.write('{0:<12}'.format('trestart')+'=  '+'3600\n')
    nam.write('{0:<12}'.format('dtmax')+'=  '+'%s\n' %dtmax)
    nam.write('{0:<12}'.format('ladaptive')+'=  '+'.true.\n')
    nam.write('{0:<12}'.format('irandom')+'=  '+'43\n')
    nam.write('{0:<12}'.format('randthl')+'=  '+'0.1\n')
    nam.write('{0:<12}'.format('randqt')+'=  '+'2.5e-5\n')
    nam.write('{0:<12}'.format('nsv')+'=  '+'%s\n' % n_scalar)
    nam.write('{0:<12}'.format('nprocx')+'=  '+'%s\n' % nprocx)
    nam.write('{0:<12}'.format('nprocy')+'=  '+'%s\n/\n\n' % nprocy)
    
    if turbine == True:
        nam.write('&WINDTURBINE\n')
        nam.write('{0:<12}'.format('Ct')+'=  '+'%s\n' % Ct)
        nam.write('{0:<12}'.format('tau')+'=  '+'%s\n' % tau)
        nam.write('{0:<12}'.format('turhx')+'=  '+'%s\n' % turhx)
        nam.write('{0:<12}'.format('turhy')+'=  '+'%s\n' % turhy)
        nam.write('{0:<12}'.format('turhz')+'=  '+'%s\n' % turhz)
        nam.write('{0:<12}'.format('turr')+'=  '+'%s\n/\n\n' % turr)


    nam.write('&DOMAIN\n') 
    nam.write('{0:<12}'.format('itot')+'=  '+'%s\n' % itot)
    nam.write('{0:<12}'.format('jtot')+'=  '+'%s\n' % jtot)
    nam.write('{0:<12}'.format('kmax')+'=  '+'%s\n\n' % kmax)
    nam.write('{0:<12}'.format('xsize')+'=  '+'%s\n' % xsize)
    nam.write('{0:<12}'.format('ysize')+'=  '+'%s\n\n' % ysize)
    nam.write('{0:<12}'.format('xlat')+'=  '+'%s\n' % xlat)
    nam.write('{0:<12}'.format('xlon')+'=  '+'%s\n' % xlon)
    nam.write('{0:<12}'.format('xday')+'=  '+'%s\n' % xday)
    nam.write('{0:<12}'.format('xtime')+'=  '+'%s\n/\n\n' % xtime)

    nam.write('&PHYSICS\n') 
    nam.write('{0:<12}'.format('ps')+'=  '+'101500.00\n')
    nam.write('{0:<12}'.format('thls')+'=  '+'265\n')
    nam.write('{0:<12}'.format('lmoist')+'=  '+'.false.\n')
    nam.write('{0:<12}'.format('lcoriol')+'=  '+'.true.\n')
    nam.write('{0:<12}'.format('iradiation')+'=  '+'0\n')
    nam.write('{0:<12}'.format('useMcICA')+'=  '+'.true.\n')
    nam.write('{0:<12}'.format('timerad')+'=  '+'10\n')
    nam.write('{0:<12}'.format('rad_longw')+'=  '+'.true.\n')
    nam.write('{0:<12}'.format('rad_shortw')+'=  '+'.true.\n')
    nam.write('{0:<12}'.format('dlwtop')+'=  '+'70.\n')
    nam.write('{0:<12}'.format('dlwbot')+'=  '+'15.\n')
    nam.write('{0:<12}'.format('sw0')+'=  '+'600\n')
    nam.write('{0:<12}'.format('ltimedep')+'=  '+'.true.\n')
    nam.write('{0:<12}'.format('z0')+'=  '+'0.1\n')
    nam.write('{0:<12}'.format('ustin')+'=  '+'-9999.\n')
    nam.write('{0:<12}'.format('wtsurf')+'=  '+'-9999\n')
    nam.write('{0:<12}'.format('wqsurf')+'=  '+'0.\n/\n\n')

    nam.write('&NAMSURFACE\n') 
    nam.write('{0:<12}'.format('albedoav')+'=  '+'0.24\n')
    nam.write('{0:<12}'.format('isurf')+'=  '+'2\n')
    nam.write('{0:<12}'.format('lsmoothflux')+'=  '+'.false.\n')
    nam.write('{0:<12}'.format('z0')+'=  '+'0.1\n')
    nam.write('{0:<12}'.format('lneutral')+'=  '+'false\n')
    nam.write('{0:<12}'.format('ustin')+'=  '+'-9999.\n/\n\n')

    nam.write('&NAMSUBGRID\n') 
    nam.write('{0:<12}'.format('ldelta')+'=  '+'.true.\n')
    nam.write('{0:<12}'.format('cn')+'=  '+'0.76\n/\n\n')

    nam.write('&NAMRADSTAT\n') 
    nam.write('{0:<12}'.format('dtav')+'=  '+'%s\n' % dtav)
    nam.write('{0:<12}'.format('timeav')+'=  '+'%s\n' % timeav)
    nam.write('{0:<12}'.format('lstat')+'=  '+'.true.\n/\n\n')

    nam.write('&DYNAMICS\n') 
    nam.write('{0:<12}'.format('llsadv')+'=  '+'.false.\n')
    nam.write('{0:<12}'.format('lqlnr')+'=  '+'.false.\n')
    nam.write('{0:<12}'.format('cu')+'=  '+'%s\n' %cu)
    nam.write('{0:<12}'.format('cv')+'=  '+'%s\n\n' %cv)
    nam.write('{0:<12}'.format('iadv_mom')+'=  '+'2\n')
    nam.write('{0:<12}'.format('iadv_tke')+'=  '+'2\n')
    nam.write('{0:<12}'.format('iadv_thl')+'=  '+'2\n')
    nam.write('{0:<12}'.format('iadv_qt')+'=  '+'2\n')
    nam.write('{0:<12}'.format('iadv_sv')+'=  '+'2\n/\n\n')

    nam.write('&NAMBUDGET\n') 
    nam.write('{0:<12}'.format('lbudget')+'=  '+'.true.\n')
    nam.write('{0:<12}'.format('dtav')+'=  ''%s\n' % dtav)
    nam.write('{0:<12}'.format('timeav')+'=  '+'%s\n/\n\n' % timeav)

    nam.write('&NAMCHECKSIM\n') 
    nam.write('{0:<12}'.format('tcheck')+'=  '+'60\n\n')

    nam.write('&NAMSAMPLING\n')
    nam.write('{0:<12}'.format('dtav')+'=  ''%s\n' % dtav)
    nam.write('{0:<12}'.format('timeav')+'=  '+'%s\n' % timeav)
    nam.write('{0:<12}'.format('lsampcl')+'=  '+'.false.\n')
    nam.write('{0:<12}'.format('lsampco')+'=  '+'.false.\n')
    nam.write('{0:<12}'.format('lsampup')+'=  '+'.false.\n')
    nam.write('{0:<12}'.format('lsampbuup')+'=  '+'.false.\n')
    nam.write('{0:<12}'.format('lsampcldup')+'=  '+'.false.\n/\n\n')

    nam.write('&NAMTIMESTAT\n')
    nam.write('{0:<12}'.format('ltimestat')+'=  '+'.true.\n')
    nam.write('{0:<12}'.format('dtav')+'=  ''%s\n/\n\n' % dtav)

    nam.write('&NAMCROSSSECTION\n')
    nam.write('{0:<12}'.format('lcross')+'=  '+'.false.\n')
    nam.write('{0:<12}'.format('dtav')+'=  ''%s\n/\n\n' % dtav)

    nam.write('&NAMGENSTAT\n')
    nam.write('{0:<12}'.format('lstat')+'=  '+'.true.\n')
    nam.write('{0:<12}'.format('dtav')+'=  ''%s\n' % dtav)
    nam.write('{0:<12}'.format('timeav')+'=  '+'%s\n/\n\n' % timeav)

    nam.write('&NAMFIELDDUMP\n')
    nam.write('{0:<12}'.format('lfielddump')+'=  '+'.%s.\n' % fielddump)
    nam.write('{0:<12}'.format('dtav')+'=  ''%s\n' % dtav)
    nam.write('{0:<12}'.format('ldiracc')+'=  '+'.true.\n/\n\n')

    nam.write('&NAMSTATTEND\n')
    nam.write('{0:<12}'.format('dtav')+'=  ''%s\n' % dtav)
    nam.write('{0:<12}'.format('ltend')+'=  '+'.true.\n')
    nam.write('{0:<12}'.format('timeav')+'=  '+'%s\n/\n\n' % timeav)

#-----------------------------------------------------------------
#            6 Check if CMakeCache.txt contains "nocuda"
#-----------------------------------------------------------------  

with open(builddir + '/CMakeCache.txt', 'r') as cmc:
    cmc = list(cmc)
    n_nocuda = 0
    for i in range(0,len(cmc)):
        if cmc[i].find('nocuda')!=-1:
            n_nocuda += 1

if n_nocuda != 5:
    print 'FATAL ERROR: add "nocuda" to netcdf paths in CMakeCache.txt'



 

