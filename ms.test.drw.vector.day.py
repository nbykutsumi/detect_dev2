from numpy import *
from mpl_toolkits.basemap import Basemap
from   datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib
import os, sys
import myfunc.IO.JRA55 as JRA55
import myfunc.fig.Fig as Fig
import myfung.grids as grids
import util

Year = 2004
lMon = range(1,12+1)
#lMon = [1]
ny, nx= 145, 288
jra  = JRA55.Jra55()
a1lat  = jra.Lat
a1lon  = jra.Lon

BBox   = [[10, 100], [60, 160]]

nwinter= [1]
swinter= [7]
# Function----------------
def load_var(var, plev, Year, Mon):
  sPath = os.path.join(baseDir,var,str(Year),"%s.mean.%04dhPa.%04d%02d.145x288"%(var,plev,Year,Mon))

  a2var = fromfile(sPath, float32).reshape(ny,nx)
  return a2var


def load_runmean(var, plev, DTime):
  Year  = DTime.year
  Mon   = DTime.month
  Day   = DTime.day 
 
  sPath = os.path.join(baseDir,var,str(Year),"%s.runmean.%04dhPa.%04d%02d%02d.145x288"%(var,plev,Year,Mon,Day))

  a2var = fromfile(sPath, float32).reshape(ny,nx)
  return a2var

def surr_mean(a2in, radgrids):
  if radgrids ==0:
    a2out=a2in
  else:
    ny,nx = a2in.shape
    nz    = (2*radgrids+1)**2
    a3dat = empty([nz,ny,nx])
    iz    = -1
    for dy in range(-radgrids,radgrids+1):
      for dx in range(-radgrids, radgrids+1):
        iz = iz+1
        a3dat(iz) = grids.shift_map(a2in, dy, dx)
    a2out = a3dat.mean(axis=0)
    a2out[:dy] = miss
    a2out[-dy:]= miss

  return a2out
#--------------------------
baseDir = "/home/utsumi/mnt/well.share/temp"
figdir  = os.path.join(baseDir, "pict")
util.mk_dir(figdir)
#"""

# diff Wind
#plev = 500
plev = 850
#varx = "q.ugrd"
#vary = "q.vgrd"
varx = "ugrd"
vary = "vgrd"


Uref = vstack([
        array([load_var(varx,plev,Year,Mon)
            for Mon in swinter]).mean(axis=0)[:ny/2]
       ,array([load_var(vary,plev,Year,Mon)
            for Mon in nwinter]).mean(axis=0)[ny/2:]
            ])

Vref = vstack([
        array([load_var(varx,plev,Year,Mon)
            for Mon in swinter]).mean(axis=0)[:ny/2]
       ,array([load_var(vary,plev,Year,Mon)
            for Mon in nwinter]).mean(axis=0)[ny/2:]
            ])

#for Mon in lMon:
#    scale = 3.0
#    U = load_var(varx, plev, Year, Mon) - Uref
#    V = load_var(vary, plev, Year, Mon) - Vref
#
#    stitle = "d(wind)@%04dhPa %04d %02d - DJF(JJA)"%(plev, Year,Mon)
#    oPath  = os.path.join(figdir,"test.d.wind.%04dhPa.%04d.%02d.png"%(plev,Year,Mon))
#    Fig.DrawVectorSimple( U, V, a1lat, a1lon, BBox=BBox, figname=oPath, stitle=stitle, scale=scale)
#

for Mon in lMon:
    scale = 2
    interval  = 2
    U = load_var(varx, plev, Year, Mon)
    V = load_var(vary, plev, Year, Mon)

    stitle = "wind@%04dhPa %04d %02d"%(plev, Year,Mon)
    oPath  = os.path.join(figdir,"wind.JPN.%04dhPa.%04d.%02d.png"%(plev,Year,Mon))
    Fig.DrawVectorSimple( U, V, a1lat, a1lon, BBox=BBox, figname=oPath, stitle=stitle, scale=scale, interval=interval)




#iDTime = datetime(2004,7,16)
#eDTime = datetime(2004,7,20)
#dDTime = timedelta(days=1)
#lDTime = util.ret_lDTime(iDTime, eDTime, dDTime)
#for DTime in lDTime:
#    Year  = DTime.year
#    Mon   = DTime.month
#    Day   = DTime.day 
#    U = load_runmean(varx, plev, DTime) - Uref
#    V = load_runmean(vary, plev, DTime) - Vref
#
#    scale = 3.0
#    stitle = "d(wind)@%04dhPa %04d %02d - DJF(JJA)"%(plev, Year,Mon)
#    oPath  = os.path.join(figdir,"d.wind.day.%04dhPa.%04d.%02d.%02d.png"%(plev,Year,Mon,Day))
#    Fig.DrawVectorSimple( U, V, a1lat, a1lon, BBox=BBox, figname=oPath, stitle=stitle, scale=scale)
#
