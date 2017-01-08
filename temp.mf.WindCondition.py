from numpy import *
from datetime import datetime, timedelta
import ctrack_func
import ctrack_para
import Front
import JRA55
import fig.Fig as Fig
import calendar
import ctrack_para

ra   = JRA55.jra55()
a1lat= ra.Lat
a1lon= ra.Lon
ny   = ra.ny
nx   = ra.nx

lseason = [7]
#lseason = ["DJF","JJA",6,7,8,1,2,12]
Y       = 2004
#BBox  = [[0,100],[60,180]]
BBox  = [[-90,0],[90,360]]

thup  = 10
thlow = 1.5

for season in lseason:
  lM  = ctrack_para.ret_lmon(season)
  iM  = lM[0]
  eM  = lM[-1]
  iD  = 1
  eD  = calendar.monthrange(Y,eM)[1]
  iDTime = datetime(Y,iM,iD,0)
  eDTime = datetime(Y,eM,eD,0)
  dDTime = timedelta(seconds=60*60*24)

  v850  = ra.time_ave("vgrd", iDTime, eDTime, dDTime, 850)
  u250  = ra.time_ave("ugrd", iDTime, eDTime, dDTime, 250)

  v850_org = v850.copy()
  v850[0:int(ny*0.5)] = -v850_org[0:int(ny*0.5)] 

  v850 = ma.masked_less(v850, thlow)
  u250 = ma.masked_less(u250, thup)
  mf   = ma.masked_where(u250.mask, v850)
  mf   = mf*0.0
 
  oDir   = "/home/utsumi/temp/MoistFront"
  ctrack_func.mk_dir(oDir)
  vname  = oDir + "/v.%s.png"%(season)
  uname  = oDir + "/u.%s.png"%(season)
  condname = oDir + "/cond.%s.png"%(season)
  Fig.DrawMap(v850, a1lat, a1lon, BBox, vname)
  Fig.DrawMap(u250, a1lat, a1lon, BBox, uname)
  Fig.DrawMap(mf  , a1lat, a1lon, BBox, condname)

