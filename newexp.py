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

username = 'pim'

eurocs = True
gabls = False

exptitle = 'PVD_WINDFARM'
expnr = '001'

if eurocs:
    exptitle = 'Single_turbine_EUROCS'
if gabls:
    exptitle = 'Single_turbine_GABLS'

newcase = True # create new case or use existing one

#casetitle = 'StableBL_turbine' # title of new case or existing case
#casetitle = 'ConvectiveBL_turbine' # title of new case or existing case
#casetitle = 'NeutralBL_turbine' # title of new case or existing case
if eurocs:
    casetitle = 'EUROCS_turbine' # title of new case or existing case
    casesubtitle = 'EUROCS_ref'
    sourcecasetitle = 'Cases_Stephan' # if newcase=True: use prof.inp and ls_flux.inp from existing case
    sourcecasesubtitle = 'H046_Eurocs'
if gabls:
    casetitle = 'GABLS_turbine' # title of new case or existing case
    casesubtitle = 'GABLS_ref'
    sourcecasetitle = 'Gabls1' # if newcase=True: use prof.inp and ls_flux.inp from existing case
    sourcecasesubtitle = 'Ref_Dales4'

lesversion = 'PVD_WINDFARM'

#-----------------------------------------------------------------
#                     1.1 General input            
#-----------------------------------------------------------------

dtav = 60 # time interval for sampling statistics [s]
timeav = 3600 # time interval for writing statistics [s]

dtavgenstat = 60 # time interval for sampling general statistics [s]
timeavgenstat = 3600 # time inverval for averaging/writing general statistics [s]

fielddump = 'true' # enable dump of full 3D fields of several variables
dtavfielddump = 60 # time interval of writing fielddump

n_scalar = 0 # number of additional scalars 

if gabls:
    isurf = 2
    ncpu = 8 # total number of cpu's
    nprocx = 0 # number of cpu's in x-direction (= 0 lets DALES decide)
    nprocy = 0 # number of cpu's in y-direction (= 0 lets DALES decide)

    itot = 256 # number of grid points in x-direction
    jtot = 128 # number of grid points in y-direction
    kmax = 64 # number of grid points in z-direction

    xsize = 1600 # size of domain in x-direction [m]
    ysize = 800 # size of domain in y-direction [m]

    dz = 0 # grid spacing in z-direction [m] (set 0 if zmax is defined)
    zmax = 400 # size of domain in z-direction [m] (set 0 if dz is defined)

    u = 8. # geostrophic wind velocity / inital wind velocity in x-direction
    v = 0. # geostrophic wind velocity / inital wind velocity in y-direction

    cu = cv = 0

    ladaptive = 'true' 
    dtmax = 3.0 # maximum time step [s]
    runtime = 32400  # simulation runtime [s]

    ltimedep = 'false'
    xlat = 73
    xlon = 0
    xday = 0
    xtime = 0
    ps = 101500.00
    thls = 265.
    lmoist = 'false'
    iradiation = 0
    irad = 0
    timerad = 1e6
    dlwbot = 0.
    sw0 = 1100.
    ltimedep = 'true'
    reff = 1e-5
    ustin = 0.18
    z0 = 2e-4
    wtsurf = -0.04
    wqsurf = 0
    albedoav = 0.05
    lsmoothflux = 'false'
    isurf = 2
    dtav = 60
    timeav = 600
    iadv_mom = 2
    iadv_etc = 2
    ldelta = 'false'
    cn = 1.2
    tcheck = 6

if eurocs:
    itot = 200 # number of grid points in x-direction
    jtot = 200 # number of grid points in y-direction
    kmax = 120 # number of grid points in z-direction

    xsize = 2500 # size of domain in x-direction [m]
    ysize = 2500 # size of domain in y-direction [m]

    dz = 0 # grid spacing in z-direction [m] (set 0 if zmax is defined)
    zmax = 1200 # size of domain in z-direction [m] (set 0 if dz is defined)

    ladaptive = 'true' 
    dtmax = 3.0 # maximum time step [s]
    runtime = 86400  # simulation runtime [s]

    ltimedep = 'false'
    xlat = 33.3
    xlon = 240.5
    xday = 195.
    xtime = 8.
    ps = 101250.00
    thls = 288.
    lmoist = 'true'
    iradiation = 2
    irad = 4
    timerad = 10
    dlwbot = 0.
    sw0 = 1100.
    ltimedep = 'false'
    reff = 1e-5
    ustin = 0.18
    z0 = 2e-4
    wtsurf = 0
    wqsurf = 0
    albedoav = 0.05
    lsmoothflux = 'true'
    isurf = 2
    dtav = 60
    timeav = 600
    iadv_mom = 5
    iadv_etc = 55
    ldelta = 'false'
    cn = 1.2
    tcheck = 6

#-----------------------------------------------------------------
#                      1.2 Wind turbine input            
#-----------------------------------------------------------------

turbine = True # enable wind turbine
wakeanalysis = 'true'
uniformadm = 'false'
nonuniformadm = 'true'
diagn = 'true'
N_an = 5 # number of annuli
tipspeedr = 9 # tip speed ratio
tura = 0.25 # axial induction factor [-]
TVdavg = 600 # time constant of exponential wind velocity smoothing [s]
Tyaw = 600 # time scale of yaw orientation system [s]
Twake = 600 # time scale of wake model fit [s]
Tsettur = 0. # time until wind turbine is turned on [s]
Tturdata = 1 # time scale of writing wind turbine data [s]
Twakedevelop = 3600
Tchktur = 30 # time scale of wind turbine monitoring [s]
nwakeV = 15 # number of datapoints in wake for fit of analytical model [-]

intA = 3 # integration area factor [-]
m_int = 20 # number of integration intervals in y-direction [-]
n_int = 20 # number of integration intervals in z-direction [-]
smthcoefax = 2.3 
smthcoefrad = 2 
smthcoefannu = 2

R_nac = 2 # nacelle radius [m]
R_towertop = 1.5 # tower radius at top [m]
R_towerbase = 3 # tower radius at base [m]
Cp = 0.34 # power coefficient [-]
Ct = 0.75 # thrust coefficient [-]
Cdnac = 0.3 # nacelle drag coefficient [-]
Cdtower = 0.4 # tower drag coefficient [-]

ntur = 1

windfarmdata = zeros((ntur,12))
turhx = [0.5*xsize,200,700,1200,1200]
turhy = [0.5*ysize,600,400,200,600]
turhz = 100
turr = 50
for i in range(0,ntur):
    turid = i+1
    windfarmdata[i,0] = turid
    windfarmdata[i,1] = turhx[i]
    windfarmdata[i,2] = turhy[i]
    windfarmdata[i,3] = turhz
    windfarmdata[i,4] = turr
    windfarmdata[i,5] = R_nac
    windfarmdata[i,6] = R_towertop
    windfarmdata[i,7] = R_towerbase
    windfarmdata[i,8] = Cp
    windfarmdata[i,9] = Ct
    windfarmdata[i,10] = Cdnac
    windfarmdata[i,11] = Cdtower

if turbine:
    cu = cv = 0

#-----------------------------------------------------------------
#                   2 Define and make folders         
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


headerfarm = ['turid', 'turhx', 'turhy', 'turhz', 'turr','R_nac', 'R_towertop', 'R_towerbase', 'Cp', 'Ct', 'Cdnac', 'Cdtower'] 
with open('%s/windfarmdata.inp.%s' % (expdir,expnr),'w') as x:
    for item in headerfarm:
        x.write('{0:>15}'.format(item))
    x.write('\n')
    for i in range(0,ntur):
        for item in windfarmdata[i,:]:
            x.write('{:>15.3f}'.format(item))
        x.write('\n')

#-----------------------------------------------------------------
#                     3 Generate case files
#-----------------------------------------------------------------

if newcase==True:
    h = dlsin.height(kmax, zmax, dz) # make height vector

    #-----------------------------------------------------------------
    #                          3.1 prof.inp
    #-----------------------------------------------------------------
    def readinpfiles(case,subcase,username='pim'):
        path = '/home/%s/%s/%s/' % (username, case, subcase)
        profinp = loadtxt(path + 'prof.inp.046',skiprows=2)
        lscaleinp = loadtxt(path + 'lscale.inp.046',skiprows=2)
        return {'prof.inp': profinp, 'lscale.inp': lscaleinp}

    headerprof = ['height', 'thl', 'qt', 'u', 'v', 'tke']

    profinp = zeros((kmax,6))

    if gabls:
        profinpin = dlsin.readprofinp(case=sourcecasetitle,subcase=sourcecasesubtitle)['prof.inp'] # read prof.inp from given case
    if eurocs:
        profinpin = readinpfiles(case=sourcecasetitle,subcase=sourcecasesubtitle)['prof.inp'] # read prof.inp from given case

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

    dlsin.writeprof(profinp,'prof.inp',headerprof,casedir,exptitle,casetitle,casesubtitle,kmax) # write to case folder

#-----------------------------------------------------------------
#                          3.2 lscale.inp
#-----------------------------------------------------------------

    headerlscale = ['height', 'ug', 'vg', 'wfls', 'dqdtx', 'dqtdy', 'dqtdtls', 'dthlrad']

    lscaleinp = zeros((kmax,8))

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

    dlsin.writelscale(lscaleinp,'lscale.inp',headerlscale,casedir,exptitle,casetitle,casesubtitle,kmax) # write to case folder

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

        dlsin.writescalar(scalarinp,'scalar.inp',headerscalar,casedir,exptitle,casetitle,casesubtitle,kmax) # write to case folder

#-----------------------------------------------------------------
#                         3.4 ls_flux.inp
#-----------------------------------------------------------------
    if ltimedep == 'true':

        lsflux = 'ls_flux.inp'
        headerlsflux1 = ['time', 'wtsurf', 'wqsurf', 'thls', 'qts', 'psurf']
        headerlsflux2 = ['[s]', '[Km/s]', '[kgm/s]', '[K]', '[kg/kg]', '[Pa]']
        headerlsflux3 = ['height', 'ug', 'vg', 'wfls', 'dqdtx', 'dqtdy', 'dqtdtls', 'dthlrad']

#-----------------------------------------------------------------
#                3.4.1 First block of ls_flux.inp
#-----------------------------------------------------------------
        nt1 = 10 # number of timesteps
        dt1 = runtime/float(nt1-1) # timestep  

        lsfluxtopin = dlsin.readlsfluxinptop(case=sourcecasetitle,subcase=sourcecasesubtitle,timesteps=nt1)['ls_flux.inp'] # read first block of ls_flux.inp from given case

        lsflux1 = zeros((nt1,6))

# column 0 (time)
        for i in range(0,nt1):
            lsflux1[i,0] = dt1*i
# column 3 (liquid water potential temperature at surface)
        #    lsflux1[i,3] = 265.+0.5*i
# column 1 (liquid water potential temperature flux at surface)
        #lsflux1[:,1] = 0.2
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
            x.write('%s %s %s %s\n' % (exptitle,casetitle,casesubtitle,lsflux))
            for item in headerlsflux1:
                x.write('{0:>12}'.format(item))
            x.write('\n')
            for item in headerlsflux2:
                x.write('{0:>12}'.format(item))
            x.write('\n')
            for i in range(0,nt1):
                for item in lsflux1[i,:]:
                    x.write('{0:>12.3f}'.format(item))
                x.write('\n')
            x.write('\n')

#-----------------------------------------------------------------
#                3.4.2 Second block of ls_flux.inp
#-----------------------------------------------------------------

        nt2 = 2 # number of timesteps
        dt2 = runtime/float(nt2-1) # timestep  

        for i in range(0,nt2):
            t = i*dt2
            if i==0:
                tcu = 1#1/float(2**0.5)
                tcv = 1#1/float(2**0.5)
            if i==1:
                tcu = 1#0
                tcv = 1#.41
            if i==2:
                tcu = -1#1/float(2**0.5)
                tcv = 1#-1/float(2**0.5)
            if i==3:
                tcu = 1
                tcv = -1
            if i==4:
                tcu = 0
                tcv = -1.41
            lsflux2 = zeros((kmax,8))
            # column 0 (height)
            lsflux2[:,0] = h[:]
            # column 1 (geostrophic wind in x-direction):
            lsflux2[:,1] = tcu*u
            # column 2 (geostrophic wind in y-direction):
            lsflux2[:,2] = tcv*v
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
                    x.write('{0:>12}'.format(item))
                x.write('\n# %s\n' % t)
                for k in range(0,kmax):
                    for item in lsflux2[k,:]:
                        x.write('{0:>12.3f}'.format(item))
                    x.write('\n')
                x.write('\n' '\n')
     
#-----------------------------------------------------------------
#                       3.5 ls_fluxsv.inp
#-----------------------------------------------------------------       
    if n_scalar > 0:

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
            x.write('%s %s %s %s\n' % (exptitle,casetitle,casesubtitle,lsfluxsv))
            for item in headerlsfluxsv1:
                x.write('{0:>12}'.format(item))
            x.write('\n')
            for item in headerlsfluxsv2:
                x.write('{0:>12}'.format(item))
            x.write('\n')
            for i in range(0,nt3):
                for item in lsfluxsv1[i,:]:
                    x.write('{0:>12.3f}'.format(item))
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
                    x.write('{0:>12}'.format(item))
                x.write('\n# %s\n' % t)
                for k in range(0,kmax):
                    for item in lsfluxsv2[k,:]:
                        x.write('{0:>12.3f}'.format(item))
                    x.write('\n')
                x.write('\n' '\n')

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
    nam.write('{0:<12}'.format('ladaptive')+'=  '+'.%s.\n' % ladaptive)
    nam.write('{0:<12}'.format('irandom')+'=  '+'43\n')
    nam.write('{0:<12}'.format('randthl')+'=  '+'0.1\n')
    nam.write('{0:<12}'.format('randqt')+'=  '+'2.5e-5\n')
    nam.write('{0:<12}'.format('nsv')+'=  '+'%s\n' % n_scalar)
    nam.write('{0:<12}'.format('nprocx')+'=  '+'%s\n' % nprocx)
    nam.write('{0:<12}'.format('nprocy')+'=  '+'%s\n/\n\n' % nprocy)
    
    if turbine == True:
        nam.write('&WINDTURBINE\n')
        nam.write('{0:<12}'.format('lwindturbine')+'=  '+'.true.\n')
        nam.write('{0:<12}'.format('lwakeanalysis')+'=  '+'.%s.\n' % wakeanalysis)
        nam.write('{0:<12}'.format('luniformadm')+'=  '+'.%s.\n' % uniformadm)
        nam.write('{0:<12}'.format('lnonuniformadm')+'=  '+'.%s.\n' % nonuniformadm)
        nam.write('{0:<12}'.format('ldiagn')+'=  '+'.%s.\n' % diagn)
        nam.write('{0:<12}'.format('ntur')+'=  '+'%s\n' % ntur)
        nam.write('{0:<12}'.format('tipspeedr')+'=  '+'%s\n' % tipspeedr)
        nam.write('{0:<12}'.format('N_an')+'=  '+'%s\n' % N_an)
        nam.write('{0:<12}'.format('tura')+'=  '+'%s\n' % tura)
        nam.write('{0:<12}'.format('TVdavg')+'=  '+'%s\n' % TVdavg)
        nam.write('{0:<12}'.format('Tyaw')+'=  '+'%s\n' % Tyaw)
        nam.write('{0:<12}'.format('Twake')+'=  '+'%s\n' % Twake)
        nam.write('{0:<12}'.format('Tsettur')+'=  '+'%s\n' % Tsettur)
        nam.write('{0:<12}'.format('Twakedevelop')+'=  '+'%s\n' % Twakedevelop)
        nam.write('{0:<12}'.format('Tturdata')+'=  '+'%s\n' % Tturdata)
        nam.write('{0:<12}'.format('Tchktur')+'=  '+'%s\n' % Tchktur)
        nam.write('{0:<12}'.format('nwakeV')+'=  '+'%s\n' % nwakeV)
        nam.write('{0:<12}'.format('intA')+'=  '+'%s\n' % intA)
        nam.write('{0:<12}'.format('m_int')+'=  '+'%s\n' % m_int)
        nam.write('{0:<12}'.format('n_int')+'=  '+'%s\n' % n_int)
        nam.write('{0:<12}'.format('smthcoefax')+'=  '+'%s\n' % smthcoefax)
        nam.write('{0:<12}'.format('smthcoefrad')+'=  '+'%s\n' % smthcoefrad)
        nam.write('{0:<12}'.format('smthcoefannu')+'=  '+'%s\n/\n\n' % smthcoefannu)

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
    nam.write('{0:<12}'.format('ps')+'=  '+'%s\n' % ps)
    nam.write('{0:<12}'.format('thls')+'=  '+'%s\n' % thls)
    nam.write('{0:<12}'.format('lmoist')+'=  '+'.%s.\n' % lmoist)
    nam.write('{0:<12}'.format('lcoriol')+'=  '+'.true.\n')
    nam.write('{0:<12}'.format('iradiation')+'=  '+'%s\n' % iradiation)
    nam.write('{0:<12}'.format('irad')+'=  '+'%s\n' % irad)
    nam.write('{0:<12}'.format('useMcICA')+'=  '+'.true.\n')
    nam.write('{0:<12}'.format('timerad')+'=  '+'%s\n' % timerad)
    nam.write('{0:<12}'.format('rad_longw')+'=  '+'.true.\n')
    nam.write('{0:<12}'.format('rad_shortw')+'=  '+'.true.\n')
    nam.write('{0:<12}'.format('rka')+'=  '+'130.\n')
    nam.write('{0:<12}'.format('dlwtop')+'=  '+'70.\n')
    nam.write('{0:<12}'.format('dlwbot')+'=  '+'%s\n' % dlwbot)
    nam.write('{0:<12}'.format('sw0')+'=  '+'%s\n' % sw0)
    nam.write('{0:<12}'.format('reff')+'=  '+'%s\n' % reff)
    nam.write('{0:<12}'.format('ltimedep')+'=  '+'.%s.\n' % ltimedep)
    nam.write('{0:<12}'.format('z0')+'=  '+'%s\n' % z0)
    nam.write('{0:<12}'.format('ustin')+'=  '+'%s\n' % ustin)
    nam.write('{0:<12}'.format('wtsurf')+'=  '+'%s\n' % wtsurf)
    nam.write('{0:<12}'.format('wqsurf')+'=  '+'%s\n/\n\n' % wqsurf)

    nam.write('&NAMSURFACE\n') 
    nam.write('{0:<12}'.format('albedoav')+'=  '+'%s\n' % albedoav)
    nam.write('{0:<12}'.format('isurf')+'=  '+'%s\n' % isurf)
    nam.write('{0:<12}'.format('lsmoothflux')+'=  '+'.%s.\n' % lsmoothflux)
    nam.write('{0:<12}'.format('z0')+'=  '+'%s\n' %  z0)
    nam.write('{0:<12}'.format('lneutral')+'=  '+'false\n')
    nam.write('{0:<12}'.format('ustin')+'=  '+'%s\n/\n\n' % ustin)

    nam.write('&NAMSUBGRID\n') 
    nam.write('{0:<12}'.format('ldelta')+'=  '+'.%s.\n' % ldelta)
    nam.write('{0:<12}'.format('cn')+'=  '+'%s\n/\n\n' % cn)

    nam.write('&NAMRADSTAT\n') 
    nam.write('{0:<12}'.format('dtav')+'=  '+'%s\n' % dtav)
    nam.write('{0:<12}'.format('timeav')+'=  '+'%s\n' % timeav)
    nam.write('{0:<12}'.format('lstat')+'=  '+'.true.\n/\n\n')

    nam.write('&DYNAMICS\n') 
    nam.write('{0:<12}'.format('llsadv')+'=  '+'.false.\n')
    nam.write('{0:<12}'.format('lqlnr')+'=  '+'.false.\n')
    nam.write('{0:<12}'.format('cu')+'=  '+'%s\n' %cu)
    nam.write('{0:<12}'.format('cv')+'=  '+'%s\n\n' %cv)
    nam.write('{0:<12}'.format('iadv_mom')+'=  '+'%s\n' % iadv_mom)
    nam.write('{0:<12}'.format('iadv_tke')+'=  '+'%s\n' % iadv_etc)
    nam.write('{0:<12}'.format('iadv_thl')+'=  '+'%s\n' % iadv_etc)
    nam.write('{0:<12}'.format('iadv_qt')+'=  '+'%s\n' % iadv_etc)
    nam.write('{0:<12}'.format('iadv_sv')+'=  '+'%s\n/\n\n' % iadv_etc)

    nam.write('&NAMBUDGET\n') 
    nam.write('{0:<12}'.format('lbudget')+'=  '+'.true.\n')
    nam.write('{0:<12}'.format('dtav')+'=  ''%s\n' % dtav)
    nam.write('{0:<12}'.format('timeav')+'=  '+'%s\n/\n\n' % timeav)

    nam.write('&NAMCHECKSIM\n') 
    nam.write('{0:<12}'.format('tcheck')+'=  '+'%s\n\n' % tcheck)

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
    nam.write('{0:<12}'.format('dtav')+'=  ''%s\n' % dtavgenstat)
    nam.write('{0:<12}'.format('timeav')+'=  '+'%s\n/\n\n' % timeavgenstat)

    nam.write('&NAMFIELDDUMP\n')
    nam.write('{0:<12}'.format('lfielddump')+'=  '+'.%s.\n' % fielddump)
    nam.write('{0:<12}'.format('dtav')+'=  ''%s\n' % dtavfielddump)
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



 

