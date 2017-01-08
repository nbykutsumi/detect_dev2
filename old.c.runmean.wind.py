from numpy import *
import os, sys
import calendar
import datetime
import Reanalysis
import Cyclone
#******************************************************
#******************************************************
model   = "JRA55"
res     = "bn"
lvar   = ["ua","va"]
plev  = 500
#******************************************************
# set dlyrange
#******************************************************
dnx    = {}
dny    = {}
#****************************************************
#lyear  = [2010,2011,2012,2013,2014]
lyear  = range(1990,2010)
imon   = 1
emon   = 12

ra     = Reanalysis.Reanalysis(model=model, res=res)
cy     = Cyclone.Cyclone(model=model, res=res)
nx     = ra.nx
ny     = ra.ny

dw         = 7
ldaydelta  = range(-dw, dw+1)
#####################################################
# Function
#####################################################
def ret_dvarname(model):
  if   model in ["JRA25"]:
    return {"ua":"UGRD", "va":"VGRD"}
  elif model in ["JRA55"]:
    return {"ua":"ugrd", "va":"vgrd"}

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
def date_slide(year,mon,day, daydelta):
  today       = datetime.date(year, mon, day)
  target      = today + datetime.timedelta(daydelta)
  targetyear  = target.year
  #***********
  if ( calendar.isleap(targetyear) ):
    leapdate   = datetime.date(targetyear, 2, 29)
    #---------
    if (target <= leapdate) & (leapdate < today):
      target = target + datetime.timedelta(-1)
    elif (target >= leapdate ) & (leapdate > today):
      target = target + datetime.timedelta(1)
  #-----------
  return target
  
#******************************************************
dvarname = ret_dvarname(model)

for var in lvar:
  varname = dvarname[var]
  #------
#  odir_root = "/media/disk2/out/JRA55/bn/run.mean/%s"%(varname)
  odir_root = os.path.join(cy.baseDir,"run.mean",varname)
  #------------------------------
  # make heads and tails
  #------------------------------
  for year in lyear:
  #for year in range(1981, 1981+1):
    for  mon in range(imon, emon + 1):
      #*************
      odir       = odir_root + "/%04d/%02d"%(year, mon)
      mk_dir(odir)
      ##*************
      ## no leap
      ##*************
      #if (mon==2)&(calendar.isleap(year)):
      #  ed = calendar.monthrange(year,mon)[1] -1
      #else:
      #  ed = calendar.monthrange(year,mon)[1]
  
      ed = calendar.monthrange(year,mon)[1]
      #*************
      for day in range(1, ed + 1):
        stime  = "%04d%02d%02d%02d"%(year,mon,day, 0)
        #***********
        oname  = odir + "/run.mean.%s.%04dhPa.%s.%s"%(varname, plev, stime, res)
        #*********************
        # start running mean
        #*********************
        # dummy
        #********
        aout  = zeros([ny,nx], float32)
        ntimes = 0
        #********
        for daydelta in ldaydelta:
          target     = date_slide( year, mon, day, daydelta)
          targetyear = target.year
          targetmon  = target.month
          targetday  = target.day
          #-------------------
          for targethour in [0, 6, 12, 18]:
            tDTime = datetime.datetime(targetyear, targetmon, targetday, targethour)
            ntimes = ntimes + 1
            try:
              ain    = ra.load_6hr(varname, tDTime, plev).Data
            except IOError:
              print "no file", varname, tDTime, plev
              ntimes = ntimes - 1
              continue
            #--------------------
            # add 
            #--------------------
            aout  = aout + ain
        #*****************
        aout    = aout / ntimes
        #*****************
        print oname
        aout.tofile(oname)
  


