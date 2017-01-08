from numpy import *
from detect_fsub import *
from datetime import datetime, timedelta
import util
import config_func
import IO_Master
import Cyclone
import ConstCyclone
import calendar
import os, sys
##***************************
prj     = "JRA55"
model   = "__"
run     = "__"
res     = "145x288"
noleap  = False

#prj     = "HAPPI"
#model   = "MIROC5"
#run     = "C20-ALL-001"
#res     = "128x256"
#noleap  = True

#iDTime = datetime(2009,1,1,0)
#eDTime = datetime(2009,1,31,18)
#iDTime = datetime(2004,1,4,0)
#eDTime = datetime(2004,1,18,18)
iDTime = datetime(2001,1,1,0)
eDTime = datetime(2015,8,31,18)



dDTime = timedelta(hours=6)

ret_lDTime = {False: util.ret_lDTime
             ,True : util.ret_lDTime_noleap
             }[noleap]

lDTime   = ret_lDTime(iDTime, eDTime, dDTime)
lDTimeRev= lDTime[::-1]


cfg    = config_func.config_func(prj, model, run)
iom    = IO_Master.IO_Master(prj, model, run, res)
cy     = Cyclone.Cyclone(cfg)

#flgresume  = True
flgresume  = False
#------------------------
#iYM   = [1990,1]
#eYM   = [2014,12]

iYM   = [2015,1]
eYM   = [2015,1]

iyear, imon = iYM
eyear, emon = eYM
#****************
miss_dbl     = -9999.0
miss_int     = -9999
endh         = 18
thdp         = 0.0  #[Pa]
thdist_search = 500.0*1000.0   #[m]
#####################################################
# functions
#####################################################
def ret_lDTime(iDTime,eDTime,dDTime):
  total_steps = int( (eDTime - iDTime).total_seconds() / dDTime.total_seconds() + 1 )
  return [iDTime + dDTime*i for i in range(total_steps)]

#####################################################
def pyxy2fortpos(ix, iy, nx):
  ix     = ix + 1  # ix = 1,2,.. nx
  iy     = iy + 1  # iy = 1,2,.. ny
  #number = iy* nx + ix +1
  number = (iy-1)* nx + ix
  return number
#####################################################
def fortpos2pyxy(number, nx, miss_int):
  if (number == miss_int):
    iy0 = miss_int
    ix0 = miss_int
  else:
    iy0 = int((number-1)/nx)  +1  # iy0 = 1, 2, ..
    ix0 = number - nx*(iy0-1)     # ix0 = 1, 2, ..

    iy0 = iy0 -1    # iy0 = 0, 1, .. ny-1
    ix0 = ix0 -1    # ix0 = 0, 1, .. nx-1
  #----
  return ix0, iy0
#####################################################
def check_file(sname):
  if not os.access(sname, os.F_OK):
    print "no file:",sname
    sys.exit()
#####################################################
def mk_dir(sdir):
  try:
    os.makedirs(sdir)
  except:
    pass
#####################################################
def date_slide(year,mon,day, daydelta, noleap):
  today       = datetime(year, mon, day)
  target      = today + timedelta(daydelta)
  targetyear  = target.year
  #***********
  if noleap==True:
    if ( calendar.isleap(targetyear) ):
      leapdate   = datetime(targetyear, 2, 29)
      #---------
      if (target <= leapdate) & (leapdate < today):
        target = target + timedelta(-1)
      elif (target >= leapdate ) & (leapdate > today):
        target = target + timedelta(1)
  #-----------
  return target
#****************************************************
def read_txtlist(iname):
  f = open(iname, "r")
  lines = f.readlines()
  f.close()
  lines = map(float, lines)
  aout  = array(lines, float32)
  return aout
#******************************************************
#-- const --- 
thtopo   = cy.thtopo

#****************************************************
# read lat, lon data
#----------------------
a1lat, a1lon = iom.Lat, iom.Lon
ny           = iom.ny
nx           = iom.nx
X,Y          = meshgrid(arange(nx), arange(ny))
#**************************************************
# read topo data
a2topo      = iom.load_const("topo")
a2mask_topo = ma.masked_greater(a2topo, thtopo)
#*************************************************
counter = 0
for idt, DTime1 in enumerate(lDTimeRev):

  if ((DTime1==lDTimeRev[0])or(DTime1.month !=lDTime[idt-1])):
    print "connectc.bwd.py, backward",DTime1.year, DTime1.month

  counter= counter + 1
  DTime0 = DTime1 - dDTime
  if ((noleap==True)&(DTime0.month==2)&(DTime0.day==29)):
    DTime0 = DTime0 - timedelta(days=1)

  #***************************************
  # "nextpos" for final timestep
  #**********
  if counter == 1:
    #------
    if flgresume == True:
      preposnextname1 = cy.path_a2dat("prepos",DTime1+timedelta(hours=hinc)).srcPath
      a2preposnext1   = fromfile(preposnextname1, int32).reshape(ny,nx)
      a2nextpos1      = ones([ny,nx],int32)*miss_int
      for iynext in range(0, ny):
        for ixnext in range(0, nx):
          if (a2preposnext1[iynext, ixnext] != miss_int):
            (ix1,iy1) = fortpos2pyxy(a2preposnext1[iynext,ixnext], nx, miss_int)
            a2nextpos1[iy1,ix1] = pyxy2fortpos(ixnext, iynext, nx)
    #------
    else:
      a2nextpos1    = array(ones(ny*nx).reshape(ny,nx)*miss_int, int32)

    nextposdir1   = cy.path_a2dat("nextpos",DTime1).srcDir
    nextposname1  = cy.path_a2dat("nextpos",DTime1).srcPath
    mk_dir(nextposdir1)
    #------
    a2nextpos1.tofile(nextposname1)
  #----------

  #***************************************
  #* names for 1
  #---------------------------------------
  nextposname1 = cy.path_a2dat("nextpos",DTime1).srcPath
  preposname1  = cy.path_a2dat("prepos",DTime1).srcPath
  agename1     = cy.path_a2dat("age",  DTime1).srcPath
  #----------
  # read data
  #**********
  try:
    a2nextpos1   = fromfile(nextposname1,int32).reshape(ny,nx)
    a2prepos1    = fromfile(preposname1, int32).reshape(ny,nx)
    a2age1       = fromfile(agename1,    int32).reshape(ny,nx)
  except IOError:
    counter = counter -1
    print "No File:"
    print preposname1
    print nextposname1
    print agename1
    sys.exit()

  #**************************************
  #   inverse trace
  #--------------------------------------
  if (counter == 1):
    if flgresume == True:
      duraname2 = cy.path_a2dat("dura",DTime1+timedelta(hours=hinc)).srcPath
      a2dura2   = fromfile(duraname2, int32).reshape(ny,nx)

      eposname2 = cy.path_a2dat("epos",DTime1+timedelta(hours=hinc)).srcPath
      a2epos2   = fromfile(eposname2, int32).reshape(ny,nx)


      a2duranext= ones([ny,nx],int32)*miss_int
      a2eposnext= ones([ny,nx],int32)*miss_int
      for iy1 in range(ny):
        for ix1 in range(nx):
          if (a2nextpos1[iy1,ix1] !=miss_int): 
            ix2,iy2 = fortpos2pyxy(a2nextpos1[iy1,ix1], nx, miss_int)
            a2duranext[iy1,ix1] = a2dura2[iy2,ix2]
            a2eposnext[iy1,ix1] = a2epos2[iy2,ix2]
    else:  
      a2duranext   = array(ones(ny*nx).reshape(ny,nx) * miss_int, int32)
      a2eposnext   = array(ones(ny*nx).reshape(ny,nx) * miss_int, int32)
  #--------------------------
  # initialize a2dura1 and a2dura2_new
  #*****************
  a2dura1        = ones([ny,nx],int32)* miss_int
  a2duranext_new = ones([ny,nx],int32)* miss_int
  a2epos1        = ones([ny,nx],int32)* miss_int
  a2eposnext_new = ones([ny,nx],int32)* miss_int

  a2nextpos0     = ones([ny,nx],int32)* miss_int
  #*****************
  ax1 = ma.masked_where(a2age1 ==miss_int, X).compressed()
  ay1 = ma.masked_where(a2age1 ==miss_int, Y).compressed()
  for iy1,ix1 in zip(ay1, ax1):
    age1    = a2age1[iy1, ix1]
    duranext = a2duranext[iy1, ix1]
    eposnext = a2eposnext[iy1, ix1]
    (ix0,iy0) = fortpos2pyxy(a2prepos1[iy1,ix1], nx, miss_int)
    #---- 
    if (duranext == miss_int):
      #dura1 = 1000000* age1 + int(pgmax1)
      dura1 = age1
      epos1 = pyxy2fortpos(ix1,iy1,nx)
    else:
      dura1 = duranext
      epos1 = eposnext
    #----
    a2dura1[iy1, ix1] = dura1
    a2epos1[iy1, ix1] = epos1
    #-----------------------
    # fill a2duranext_new, a2eposnext_new
    #***************
    if (ix0 != miss_int):
      a2duranext_new[iy0, ix0] = dura1
      a2eposnext_new[iy0, ix0] = epos1
    #-----------------------
    # make "a2nextpos0"
    #***************
    if (iy0 != miss_int):
      a2nextpos0[iy0, ix0] = pyxy2fortpos(ix1, iy1, nx)

  #-------------------
  # replace a2duranext with new data
  #*******************
  a2duranext = a2duranext_new
  a2eposnext = a2eposnext_new
  #**************************************
  # write to file
  #--------------------------------------
  # out dir
  #**********
  duradir1     = cy.path_a2dat("dura"   ,DTime1).srcDir
  eposdir1     = cy.path_a2dat("epos"   ,DTime1).srcDir
  nextposdir0  = cy.path_a2dat("nextpos",DTime0).srcDir

  mk_dir(duradir1)
  mk_dir(eposdir1)
  mk_dir(nextposdir0)
  #----------
  # out name
  #**********
  duraname1    = cy.path_a2dat("dura"   ,DTime1).srcPath
  eposname1    = cy.path_a2dat("epos"   ,DTime1).srcPath
  nextposname0 = cy.path_a2dat("nextpos",DTime0).srcPath
  
  #----------
  # write to file
  #**********
  a2dura1.tofile(duraname1)
  a2epos1.tofile(eposname1)
  a2nextpos0.tofile(nextposname0) 

  print duraname1

