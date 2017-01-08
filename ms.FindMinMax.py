from numpy import *
import os, sys
import detect_func
import Reanalysis
from datetime import datetime, timedelta

iYear = 1990
eYear = 1999
lYear = range(iYear,eYear+1)
#lYear = range(eYear,iYear-1,-1)
#var   = "PWAT"
#var   = "spfh850_500"
var   = "spfh850_500_250"
dstype = {"PWAT":"anl_column125"
         ,"spfh850_500":"anl_p125"
         ,"spfh850_500_250":"anl_p125"
         }
lev   = False
#-----------------------------------
def ret_lDTime(iDTime,eDTime,dDTime):
  total_steps = int( (eDTime - iDTime).total_seconds() / dDTime.total_seconds() + 1 )
  return [iDTime + dDTime*i for i in range(total_steps)]
#-----------------------------------
def ret_a2var(var, lev=False):
  if var in ["PWAT"]:
    return ra.time_ave(var, DTime, DTime+timedelta(hours=23), timedelta(hours=6),lev=lev)

  elif var == "spfh850_500":
    a2var1 = ra.time_ave("spfh", DTime, DTime+timedelta(hours=23), timedelta(hours=6),lev=850)
    a2var2 = ra.time_ave("spfh", DTime, DTime+timedelta(hours=23), timedelta(hours=6),lev=500)
    return (a2var1 + a2var2)/2.0

  elif var == "spfh850_500_250":
    a2var1 = ra.time_ave("spfh", DTime, DTime+timedelta(hours=23), timedelta(hours=6),lev=850)
    a2var2 = ra.time_ave("spfh", DTime, DTime+timedelta(hours=23), timedelta(hours=6),lev=500)
    a2var3 = ra.time_ave("spfh", DTime, DTime+timedelta(hours=23), timedelta(hours=6),lev=250)
    return (a2var1 + a2var2 + a2var3)/3.0
  else:
    print "Check var:",var
    sys.exit()
#-----------------------------------
ra  = Reanalysis.Reanalysis(model="JRA55", res="bn")
ny  = ra.ny
nx  = ra.nx

for Year in lYear:
  iDTime = datetime(Year,1,1,0)
  #eDTime = datetime(2014,1,5,0)
  eDTime = datetime(Year,12,31,0)
  dDTime = timedelta(hours=24)
  lDTime = ret_lDTime(iDTime, eDTime, dDTime)
  nDay   = len(lDTime)
  a3dat  = zeros([nDay, ny, nx], float32)
  
  for i,DTime in enumerate(lDTime):
    #a2in  = ra.time_ave(var, DTime, DTime+timedelta(hours=23), timedelta(hours=6),lev=lev)
    a2in   = ret_a2var(var, lev=lev)
    a3dat[i] = a2in
  #
  a2max = a3dat.max(axis=0)
  a2min = a3dat.min(axis=0)

  #odir_root = "/".join(ra.path_6hr(var, iDTime, lev).srcDir.split("/")[:-2])
  odir_root = "/tank/utsumi/out/JRA55/bn/6hr"
  Maxdir    = odir_root + "/ms.max/%s"%(var)
  Mindir    = odir_root + "/ms.min/%s"%(var)
  MaxPath   = Maxdir + "/max.%s.%s.%04d.bn"%(dstype[var],var,Year)
  MinPath   = Mindir + "/min.%s.%s.%04d.bn"%(dstype[var],var,Year)

  detect_func.mk_dir(Maxdir)
  detect_func.mk_dir(Mindir) 
  a2max.astype(float32).tofile(MaxPath)
  a2min.astype(float32).tofile(MinPath)
  print MaxPath
  
  
    
