from numpy import *
from datetime import datetime, timedelta
import JRA55
import fig.Fig as Fig
Y  = 2004
M  = 1
D  = 13
H  = 0
DTime = datetime(Y,M,D,H)
BBox  = [[0,100],[60,180]]

#def ret_lDTime(iDTime,eDTime,dDTime):
#  total_steps = int( (eDTime - iDTime).total_seconds() / dDTime.total_seconds() + 1 )
#  return [iDTime + dDTime*i for i in range(total_steps)]
#
iDTime = DTime - timedelta(seconds=60*60*6)*4*3
eDTime = DTime
dDTime = timedelta(seconds=60*60*6) * 2

jra  = JRA55.jra55()
a1lat= jra.Lat
a1lon= jra.Lon

v850  = jra.time_ave("vgrd", iDTime, eDTime, dDTime, 850)
u250  = jra.time_ave("ugrd", iDTime, eDTime, dDTime, 250)
#v850 = jra.load_bn("vgrd",dtime, 850)
#u250 = jra.load_bn("ugrd",DTime, 250)
#
v850 = ma.masked_less(v850, 2)
u250 = ma.masked_less(u250, 15)
mf   = ma.masked_where(v850.mask, u250)

vname = "./temp.v.png"
uname = "./temp.u.png"
mfname= "./temp.mf.png"
mfglobname= "./temp.mf.GLOB.png"
Fig.DrawMap(v850, a1lat, a1lon, BBox, vname)
Fig.DrawMap(u250, a1lat, a1lon, BBox, uname)
Fig.DrawMap(mf  , a1lat, a1lon, BBox, mfname)
Fig.DrawMap(mf  , a1lat, a1lon, [[-90,0],[90,360]], mfglobname)
