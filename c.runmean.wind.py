from numpy import *
from   datetime import datetime, timedelta
import util
import os, sys
import calendar
import config_func
import IO_Master
import Cyclone
#******************************************************
#******************************************************
prj     = "JRA55"
model   = "__"
run     = "__"
res     = "145x288"
tstp    = "6hr"
noleap  = False

#prj     = "HAPPI"
#model   = "MIROC5"
#run     = "C20-ALL-001"
#res     = "128x256"
#tstp    = "day"
#noleap  = True

lvar   = ["ua","va"]
plev   = 500

lhour  = {"6hr": [0,6,12,18]
         ,"day": [0]
         }[tstp]

#iDTime = datetime(2006,1,1,6)
#eDTime = datetime(2006,12,31,18)
#iDTime = datetime(2009,1,1,0)
#eDTime = datetime(2009,1,31,18)
iDTime = datetime(2001,1,1,0)
eDTime = datetime(2015,8,31,18)

dDTime = timedelta(days=1)

ret_lDTime = {False: util.ret_lDTime
             ,True : util.ret_lDTime_noleap
             }[noleap]

lDTime   = ret_lDTime(iDTime, eDTime, dDTime)

miss   = -9999.
#******************************************************
# set dlyrange
#******************************************************
dnx    = {}
dny    = {}
#****************************************************
cfg    = config_func.config_func(prj, model, run)
iom    = IO_Master.IO_Master(prj, model, run, res)
cy     = Cyclone.Cyclone(cfg)
nx     = iom.nx
ny     = iom.ny

#dw         = 7
dw         = 3
ldaydelta  = range(-dw, dw+1)

if   tstp=="6hr": Load_Var = iom.Load_6hrPlev
elif tstp=="day": Load_Var = iom.Load_dayPlev
#####################################################
# Function
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
#******************************************************
def date_slide(year,mon,day, daydelta, noleap):
  today       = datetime(year, mon, day)
  target      = today + timedelta(daydelta)
  targetyear  = target.year
  #***********
  if noleap == True:
    if ( calendar.isleap(targetyear) ):
      leapdate   = datetime(targetyear, 2, 29)
      #---------
      if (target <= leapdate) & (leapdate < today):
        target = target + timedelta(days=-1)
      elif (target >= leapdate ) & (leapdate > today):
        target = target + timedelta(days=1)
  #-----------
  return target
  
#******************************************************
for var in lvar:
  #------
  odir_root = os.path.join(cfg["baseDir"],"run.mean",var)
  #------------------------------
  # make heads and tails
  #------------------------------
  for DTime in lDTime:
    #*************
    year   = DTime.year
    mon    = DTime.month
    day    = DTime.day
    odir   = odir_root + "/%04d/%02d"%(year, mon)
    mk_dir(odir)
    #*************
    stime  = "%04d%02d%02d%02d"%(year,mon,day, 0)
    #***********
    oname  = odir + "/run.mean.%s.%04dhPa.%s.%s"%(var, plev, stime, res)
    #*********************
    # start running mean
    #*********************
    # dummy
    #********
    aout  = zeros([ny,nx], float32)
    ntimes = 0
    #********
    for daydelta in ldaydelta:
      target     = date_slide( year, mon, day, daydelta, noleap)
      targetyear = target.year
      targetmon  = target.month
      targetday  = target.day
      #-------------------
      for targethour in lhour:
        tDTime = datetime(targetyear, targetmon, targetday, targethour)
        ntimes = ntimes + 1
        try:
          #ain    = iom.Load_6hrPlev(var, tDTime, plev)
          ain    = Load_Var(var, tDTime, plev)
        except IOError:
          print "no file", var, tDTime, plev
          ntimes = ntimes - 1
          continue
        #--------------------
        # add 
        #--------------------
        aout  = aout + ain
    #*****************
    aout    = aout / ntimes

    if ma.isMA(aout):
      aout = aout.filled(miss)
    #*****************
    print oname
    aout.tofile(oname)
  


