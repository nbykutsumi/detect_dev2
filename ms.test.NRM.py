from numpy import *
from datetime import datetime, timedelta
import Reanalysis


iDTime = datetime(2014,1,1,0)
#eDTime = datetime(2014,1,5,0)
eDTime = datetime(2014,12,31,0)
#iDTime = datetime(2014,6,20,0)
#eDTime = datetime(2014,6,20,0)
dDTime = timedelta(hours=24)

#-----------------------------------
def ret_lDTime(iDTime,eDTime,dDTime):
  total_steps = int( (eDTime - iDTime).total_seconds() / dDTime.total_seconds() + 1 )
  return [iDTime + dDTime*i for i in range(total_steps)]
#-----------------------------------
ra  = Reanalysis.Reanalysis(model="JRA55",res="bn")

a2slp_clim = ra.load_clim8110("PRMSL",0).Data
a2ua_clim   = ra.load_clim8110("ugrd", 850, 0).Data

lDTime = ret_lDTime(iDTime, eDTime, dDTime)
lms = []
lnrm  = []
for DTime in lDTime:
  a2slp = ra.time_ave("PRMSL", DTime-timedelta(hours=24*5), DTime, timedelta(hours=6)) - a2slp_clim
  a2ua  = ra.time_ave("ugrd", DTime-timedelta(hours=24*5), DTime, timedelta(hours=6), lev=850) - a2ua_clim

  a2ms  = ma.masked_less_equal(a2ua, 0.0)
  a2ms  = ma.masked_where(a2slp >0.0, a2ms)
  a2nrm = sign(a2ua)*abs(a2slp/100000. * a2ua)
  lms.append(a2ms[100:100+3,112+3].mean()) 
  lnrm.append(a2nrm[100:100+3,112+3].mean()) 
