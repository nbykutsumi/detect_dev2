from numpy import *
from datetime import datetime, timedelta
import myfunc.util as util
import calendar
import Monsoon
import myfunc.fig.Fig as Fig

iYear = 1980
eYear = 1980
lYear = range(iYear, eYear+1)
lMon  = range(1,12+1)
#lMon  = [1]

model = "JRA55"
res   = "bn"
var   = "PWAT"
ms    = Monsoon.MonsoonMoist(model=model, res=res, var=var)
ny,nx = ms.ny, ms.nx
Lat   = ms.Lat
Lon   = ms.Lon

for Year, Mon in [[Year,Mon] for Year in lYear for Mon in lMon]:
  iDay = 1
  eDay = calendar.monthrange(Year,Mon)[1]
  lDay = range(iDay, eDay+1)

  a2count = zeros([ny,nx],float32)
  for Day in lDay:
    DTime = datetime(Year, Mon, Day, 0)
    print DTime
    a2ms  = ms.loadMonsoonMoist(DTime, maskflag=True).filled(0.0)
    a2count = a2count + a2ms

  a2count = ma.masked_equal(a2count, 0.0)
  #-- Figure --------
  sDir  = "/tank/utsumi/temp/ms"
  figPath = sDir + "/count.%04d.%02d.png"%(Year,Mon)
  util.mk_dir(sDir)
  stitle = "%04d/%02d"%(Year,Mon)
  Fig.DrawMap(a2count, a1lat=Lat, a1lon=Lon, BBox = [[-80, 0], [80,360]], figname=figPath, vmax=31, vmin=0.0, stitle=stitle, cmap="jet")
