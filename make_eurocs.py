#!/usr/bin/python
# Filename: make_eurocs.py
# By Pim van Dorp, TU Delft, section Atmospheric Physics, 1 nov 2015
# Description: Generate input files, jobscript and namoptions for DALES 4.1 of the EUROCS case

#-----------------------------------------------------------------
#                  0 Import Python packages             
#-----------------------------------------------------------------

import numpy as np
import dales41input as dlsin
import os
import os.path

#-----------------------------------------------------------------
#                           1  General input            
#-----------------------------------------------------------------

username = 'pim'

exptitle = 'Single_turbine_EUROCS'
expnr = '400'

casetitle = 'EUROCS_turbine' 
casesubtitle = 'EUROCS_ref'

newcase = False 
sourcecasetitle = 'Cases_Stephan' 
sourcecasesubtitle = 'H046_Eurocs'

lesversion = 'PVD_WINDFARM'

ncpu = 8

#-----------------------------------------------------------------
#                          2 Namoptions
#-----------------------------------------------------------------

#----RUN----
lwarmstart = 'false'
startfile = 'initd06h00m000.017'
runtime = 133200 # 37 hour  
dtmax = 3.0 
ladaptive = 'true' 
n_scalar = 0 
nprocx = 0
nprocy = 0
dtav_glob = 60
timeav_glob = 600.

#----DOMAIN----
itot = 64
jtot = 64
kmax = 120 

xsize = 2500
ysize = 2500
zsize = 1200 

xlat = 33.3
xlon = 240.5
xday = 195.
xtime = 8.

#----PHYSICS----
ltimedep = 'false'

#----DYNAMICS----
cu = 3.4 
cv = -4.9 

#----NAMRADSTAT----
dtavrad = 60
timeavrad = 600.

#----NAMBUDGET----
dtavbudget = 60
timeavbudget = 600.

#----NAMCHECKSIM----
tcheck = 30

#----NAMSAMPLING----
dtavsampling = 60
timeavsampling = 600.

#----NAMTIMESTAT----
dtavtimestat = 60

#----NAMGENSTAT----
dtavgenstat = 60
timeavgenstat = 600.

#----NAMFIELDDUMP----
fielddump = 'true'
dtavfielddump = 60

#----NAMSTATTEND----
dtavstattend = 60
timeavstattend = 600.

#----WINDTURBINE----
turbine = False 
ntur = 1
luniformadm = 'false'
tura = 0.25 
lnonuniformadm = 'true'
N_an = 5 
tipspeedr = 9 

Tsettur = 0. 
TVdavg = 600 
Tyaw = 600 

ldiagn = 'true'
Tchktur = 30 
Tturdata = 1

intA = 3
m_int = 20
n_int = 20

smthcoefax = 2.3 
smthcoefrad = 2 
smthcoefannu = 2

if turbine:
    cu = cv = 0

#-----------------------------------------------------------------
#                        3 Windfarmdata.inp
#-----------------------------------------------------------------

turhx = 0.5*xsize
turhy = 0.5*ysize
turhz = 100

turr = 50
R_nac = 3 
R_towertop = 1.5
R_towerbase = 3

Cp = 0.34
Ct = 0.75
Cdnac = 0.3
Cdtower = 0.4

windfarmdata = np.zeros((ntur,12))

for i in range(0,ntur):
    turid = i+1
    windfarmdata[i,0] = turid
    windfarmdata[i,1] = turhx
    windfarmdata[i,2] = turhy
    windfarmdata[i,3] = turhz
    windfarmdata[i,4] = turr
    windfarmdata[i,5] = R_nac
    windfarmdata[i,6] = R_towertop
    windfarmdata[i,7] = R_towerbase
    windfarmdata[i,8] = Cp
    windfarmdata[i,9] = Ct
    windfarmdata[i,10] = Cdnac
    windfarmdata[i,11] = Cdtower

#-----------------------------------------------------------------
#                           4 Make folders         
#-----------------------------------------------------------------

expsdir = '/home/%s/Les/Experiments' % (username)
expdir = expsdir + '/%s/%s' % (exptitle,expnr)
gitdir = '/home/%s/dales/src' % (username)
builddir = '/home/%s/Les/Les_versions/Dales4.1/%s/dales.build' % (username,lesversion)
srcdir = builddir + '/src'

if not os.path.isdir(expdir):
    os.makedirs(expdir)

casesdir = '/home/%s/Les/Cases' % (username)
casedir = casesdir +'/%s/%s/%s' % (exptitle,casetitle,casesubtitle)

if newcase==True:
    if not os.path.isdir(casedir):
        os.makedirs(casedir)
else:
    if not os.path.isdir(casedir):
        print 'Case does not exist'


#-----------------------------------------------------------------
#                     5 Generate case files
#-----------------------------------------------------------------

if newcase==True:
    h = dlsin.height(kmax, zsize) 

    def readinpfiles(case,subcase,username='pim'):
        path = '/home/%s/%s/%s/' % (username, case, subcase)
        profinp = np.loadtxt(path + 'prof.inp.046',skiprows=2)
        lscaleinp = np.loadtxt(path + 'lscale.inp.046',skiprows=2)
        return {'prof.inp': profinp, 'lscale.inp': lscaleinp}

#-----------------------------------------------------------------
#                          5.1 prof.inp
#-----------------------------------------------------------------

    headerprof = ['height', 'thl', 'qt', 'u', 'v', 'tke']

    profinp = np.zeros((kmax,6))

    profinpin = readinpfiles(case=sourcecasetitle,subcase=sourcecasesubtitle)['prof.inp'] 

    # column 0 (height)
    profinp[:,0] = h[:]
    # column 1 (liquid water potential temperature)
    #profinp[:,1] = flipud(profinpin[:,1])
    profinp[:,1] = profinpin[:kmax,1]
    # colum 2 (total humidity)
    profinp[:,2] = profinpin[:kmax,2]
    # column 3 (horizontal wind velocity)
    profinp[:,3] = profinpin[:kmax,3]
    # column 4 (vertical wind velocity)
    profinp[:,4] = profinpin[:kmax,4]
    # column 5 (sgs tke)
    profinp[:,5] = profinpin[:kmax,5]

    dlsin.writeprof(profinp,'prof.inp',headerprof,casedir,exptitle,casetitle,casesubtitle,kmax)

#-----------------------------------------------------------------
#                          5.2 lscale.inp
#-----------------------------------------------------------------

    headerlscale = ['height', 'ug', 'vg', 'wfls', 'dqdtx', 'dqtdy', 'dqtdtls', 'dthlrad']

    lscaleinp = np.zeros((kmax,8))

    lscaleinpin = readinpfiles(case=sourcecasetitle,subcase=sourcecasesubtitle)['lscale.inp']

    # column 0 (height)
    lscaleinp[:,0] = h[:]
    # column 1 (geostrophic wind in x-direction)
    lscaleinp[:,1] = lscaleinpin[:kmax,1]
    # column 2 (geostrophic wind in y-direction)
    lscaleinp[:,2] = lscaleinpin[:kmax,2]
    # column 3 (ls subsidence)
    lscaleinp[:,3] = lscaleinpin[:kmax,3]
    # column 4 (ls inflow of moisture in x-direction)
    lscaleinp[:,4] = lscaleinpin[:kmax,4]
    # column 5 (ls inflow of moisture in y-direction)
    lscaleinp[:,5] = lscaleinpin[:kmax,5]
    # column 6 (add large scale moisture change in time)
    lscaleinp[:,6] = lscaleinpin[:kmax,6]
    # column 7 (prescribed temperature tendency due to radiation)
    lscaleinp[:,7] = lscaleinpin[:kmax,7]

    dlsin.writelscale(lscaleinp,'lscale.inp',headerlscale,casedir,exptitle,casetitle,casesubtitle,kmax)

#-----------------------------------------------------------------
#                      6 Write windfarmdata.inp
#-----------------------------------------------------------------

headerfarm = ['turid', 'turhx', 'turhy', 'turhz', 'turr','R_nac', 
'R_towertop', 'R_towerbase', 'Cp', 'Ct', 'Cdnac', 'Cdtower'] 

with open('%s/windfarmdata.inp.%s' % (expdir,expnr),'w') as x:
    for item in headerfarm:
        x.write('{0:>15}'.format(item))
    x.write('\n')
    for i in range(0,ntur):
        for item in windfarmdata[i,:]:
            x.write('{:>15.3f}'.format(item))
        x.write('\n')

#-----------------------------------------------------------------
#                     7 Generate jobscript
#-----------------------------------------------------------------

with open(expdir + '/job.%s' % expnr, 'w') as job:
    job.write('#!/bin/bash\n#$ -pe mpi %s\n#$ -q all.q\n#$ -l h_rt=100000\n\n' % (ncpu))
    job.write('expnr=%s\nExp_dir=$(pwd)\nGit_dir=%s\nLes_dir=%s\nCase_dir=%s\n\n' % (expnr,gitdir,srcdir,casedir))
    job.write('cp $Exp_dir/namoptions.$expnr $Exp_dir/namoptions\n')
    job.write('cp $Case_dir/prof.inp$case_ext $Exp_dir/prof.inp.$expnr\n')
    job.write('cp $Case_dir/lscale.inp$case_ext $Exp_dir/lscale.inp.$expnr\n')
    job.write('mkdir -p $Exp_dir/Code\n')
    job.write('mkdir -p $Exp_dir/INIT\n\n')
    job.write('cp $Git_dir/*f90 $Exp_dir/Code/.\n')
    job.write('cp $Les_dir/dales4 .\n\n')
    job.write('mpirun dales4\n\n')
    job.write('mv init* $Exp_dir/INIT')

#-----------------------------------------------------------------
#                   8 Generate namoptions
#-----------------------------------------------------------------  

with open(expdir + '/namoptions.%s' % expnr, 'w') as nam:
    nam.write('&RUN\n') 
    nam.write('{0:<12}'.format('iexpnr')+'=  '+'%s\n' % expnr)
    nam.write('{0:<12}'.format('lwarmstart')+'=  '+'.%s.\n' % lwarmstart)
    nam.write('{0:<12}'.format('startfile')+'=  '+'%s\n' % startfile)
    nam.write('{0:<12}'.format('runtime')+'=  '+'%s\n' % runtime)
    nam.write('{0:<12}'.format('trestart')+'=  '+'3600\n')
    nam.write('{0:<12}'.format('dtmax')+'=  '+'%s\n' %dtmax)
    nam.write('{0:<12}'.format('ladaptive')+'=  '+'.%s.\n' % ladaptive)
    nam.write('{0:<12}'.format('irandom')+'=  '+'43\n')
    nam.write('{0:<12}'.format('randthl')+'=  '+'0.1\n')
    nam.write('{0:<12}'.format('randqt')+'=  '+'2.5e-5\n')
    nam.write('{0:<12}'.format('nsv')+'=  '+'%s\n' % n_scalar)
    nam.write('{0:<12}'.format('nprocx')+'=  '+'%s\n' % nprocx)
    nam.write('{0:<12}'.format('nprocy')+'=  '+'%s\n/\n\n' % nprocy)

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
    nam.write('{0:<12}'.format('ps')+'=  '+'101250.00\n')
    nam.write('{0:<12}'.format('thls')+'=  '+'288.\n')
    nam.write('{0:<12}'.format('lmoist')+'=  '+'.true.\n')
    nam.write('{0:<12}'.format('lcoriol')+'=  '+'.true.\n')
    nam.write('{0:<12}'.format('iradiation')+'=  '+'2\n')
    nam.write('{0:<12}'.format('irad')+'=  '+'4\n')
    nam.write('{0:<12}'.format('useMcICA')+'=  '+'.true.\n')
    nam.write('{0:<12}'.format('timerad')+'=  '+'10\n')
    nam.write('{0:<12}'.format('rad_longw')+'=  '+'.true.\n')
    nam.write('{0:<12}'.format('rad_shortw')+'=  '+'.true.\n')
    nam.write('{0:<12}'.format('rka')+'=  '+'130.\n')
    nam.write('{0:<12}'.format('dlwtop')+'=  '+'70.\n')
    nam.write('{0:<12}'.format('dlwbot')+'=  '+'0.\n') 
    nam.write('{0:<12}'.format('sw0')+'=  '+'1100\n')
    nam.write('{0:<12}'.format('reff')+'=  '+'1e-5\n')
    nam.write('{0:<12}'.format('ltimedep')+'=  '+'.%s.\n/\n\n' % ltimedep)

    nam.write('&NAMSURFACE\n') 
    nam.write('{0:<12}'.format('albedoav')+'=  '+'0.05\n')
    nam.write('{0:<12}'.format('wtsurf')+'=  '+'0.0\n')
    nam.write('{0:<12}'.format('wqsurf')+'=  '+'0e-5\n')
    nam.write('{0:<12}'.format('isurf')+'=  '+'2\n')
    nam.write('{0:<12}'.format('lsmoothflux')+'=  '+'.true.\n')
    nam.write('{0:<12}'.format('ustin')+'=  '+'0.18\n')
    nam.write('{0:<12}'.format('z0')+'=  '+'2e-4\n/\n\n')

    nam.write('&NAMRADSTAT\n') 
    nam.write('{0:<12}'.format('dtav')+'=  '+'%s\n' % dtavrad)
    nam.write('{0:<12}'.format('timeav')+'=  '+'%s\n' % timeavrad)
    nam.write('{0:<12}'.format('lstat')+'=  '+'.true.\n/\n\n')

    nam.write('&DYNAMICS\n') 
    nam.write('{0:<12}'.format('llsadv')+'=  '+'.false.\n')
    nam.write('{0:<12}'.format('lqlnr')+'=  '+'.false.\n')
    nam.write('{0:<12}'.format('cu')+'=  '+'%s\n' %cu)
    nam.write('{0:<12}'.format('cv')+'=  '+'%s\n\n' %cv)
    nam.write('{0:<12}'.format('iadv_mom')+'=  '+'5\n')
    nam.write('{0:<12}'.format('iadv_tke')+'=  '+'55\n')
    nam.write('{0:<12}'.format('iadv_thl')+'=  '+'55\n')
    nam.write('{0:<12}'.format('iadv_qt')+'=  '+'55\n')
    nam.write('{0:<12}'.format('iadv_sv')+'=  '+'55\n/\n\n')

    nam.write('&NAMSUBGRID\n') 
    nam.write('{0:<12}'.format('ldelta')+'=  '+'.false.\n')
    nam.write('{0:<12}'.format('cn')+'=  '+'1.2\n/\n\n')

    nam.write('&NAMBUDGET\n') 
    nam.write('{0:<12}'.format('lbudget')+'=  '+'.true.\n')
    nam.write('{0:<12}'.format('dtav')+'=  ''%s\n' % dtavbudget)
    nam.write('{0:<12}'.format('timeav')+'=  '+'%s\n/\n\n' % timeavbudget)

    nam.write('&NAMCHECKSIM\n') 
    nam.write('{0:<12}'.format('tcheck')+'=  '+'%s\n\n' % tcheck)

    nam.write('&NAMSAMPLING\n')
    nam.write('{0:<12}'.format('dtav')+'=  ''%s\n' % dtavsampling)
    nam.write('{0:<12}'.format('timeav')+'=  '+'%s\n' % timeavsampling)
    nam.write('{0:<12}'.format('lsampcl')+'=  '+'.false.\n')
    nam.write('{0:<12}'.format('lsampco')+'=  '+'.false.\n')
    nam.write('{0:<12}'.format('lsampup')+'=  '+'.false.\n')
    nam.write('{0:<12}'.format('lsampbuup')+'=  '+'.false.\n')
    nam.write('{0:<12}'.format('lsampcldup')+'=  '+'.false.\n/\n\n')

    nam.write('&NAMTIMESTAT\n')
    nam.write('{0:<12}'.format('ltimestat')+'=  '+'.true.\n')
    nam.write('{0:<12}'.format('dtav')+'=  ''%s\n/\n\n' % dtavtimestat)

    nam.write('&NAMCROSSSECTION\n')
    nam.write('{0:<12}'.format('lcross')+'=  '+'.false.\n')
    nam.write('{0:<12}'.format('dtav')+'=  '+'60\n/\n\n')

    nam.write('&NAMGENSTAT\n')
    nam.write('{0:<12}'.format('lstat')+'=  '+'.true.\n')
    nam.write('{0:<12}'.format('dtav')+'=  ''%s\n' % dtavgenstat)
    nam.write('{0:<12}'.format('timeav')+'=  '+'%s\n/\n\n' % timeavgenstat)

    nam.write('&NAMFIELDDUMP\n')
    nam.write('{0:<12}'.format('lfielddump')+'=  '+'.%s.\n' % fielddump)
    nam.write('{0:<12}'.format('dtav')+'=  ''%s\n' % dtavfielddump)
    nam.write('{0:<12}'.format('ldiracc')+'=  '+'.true.\n/\n\n')

    nam.write('&NAMSTATTEND\n')
    nam.write('{0:<12}'.format('dtav')+'=  ''%s\n' % dtavstattend)
    nam.write('{0:<12}'.format('ltend')+'=  '+'.true.\n')
    nam.write('{0:<12}'.format('timeav')+'=  '+'%s\n/\n\n' % timeavstattend)

    if turbine == True:
        nam.write('&WINDTURBINE\n')
        nam.write('{0:<12}'.format('lwindturbine')+'=  '+'.true.\n')
        nam.write('{0:<12}'.format('ntur')+'=  '+'%s\n' % ntur)
        nam.write('{0:<12}'.format('luniformadm')+'=  '+'.%s.\n' % luniformadm)
        nam.write('{0:<12}'.format('tura')+'=  '+'%s\n' % tura)
        nam.write('{0:<12}'.format('lnonuniformadm')+'=  '+'.%s.\n' % lnonuniformadm)
        nam.write('{0:<12}'.format('tipspeedr')+'=  '+'%s\n' % tipspeedr)
        nam.write('{0:<12}'.format('N_an')+'=  '+'%s\n\n' % N_an)

        nam.write('{0:<12}'.format('Tsettur')+'=  '+'%s\n' % Tsettur)
        nam.write('{0:<12}'.format('TVdavg')+'=  '+'%s\n' % TVdavg)
        nam.write('{0:<12}'.format('Tyaw')+'=  '+'%s\n\n' % Tyaw)

        nam.write('{0:<12}'.format('ldiagn')+'=  '+'.%s.\n' % ldiagn)
        nam.write('{0:<12}'.format('Tchktur')+'=  '+'%s\n' % Tchktur)
        nam.write('{0:<12}'.format('Tturdata')+'=  '+'%s\n\n' % Tturdata)

        nam.write('{0:<12}'.format('intA')+'=  '+'%s\n' % intA)
        nam.write('{0:<12}'.format('m_int')+'=  '+'%s\n' % m_int)
        nam.write('{0:<12}'.format('n_int')+'=  '+'%s\n\n' % n_int)

        nam.write('{0:<12}'.format('smthcoefax')+'=  '+'%s\n' % smthcoefax)
        nam.write('{0:<12}'.format('smthcoefrad')+'=  '+'%s\n' % smthcoefrad)
        nam.write('{0:<12}'.format('smthcoefannu')+'=  '+'%s\n/\n\n' % smthcoefannu)


#-----------------------------------------------------------------
#            9 Check if CMakeCache.txt contains "nocuda"
#-----------------------------------------------------------------  

with open(builddir + '/CMakeCache.txt', 'r') as cmc:
    cmc = list(cmc)
    n_nocuda = 0
    for i in range(0,len(cmc)):
        if cmc[i].find('nocuda')!=-1:
            n_nocuda += 1

if n_nocuda != 5:
    print 'FATAL ERROR: add "nocuda" to netcdf paths in CMakeCache.txt'



 

