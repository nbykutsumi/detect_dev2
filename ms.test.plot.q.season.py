from numpy import *
from datetime import datetime, timedelta
import util
import os, sys
import matplotlib.pyplot as plt

Year = 2006
iDTime  = datetime(Year,1,1,0)
#eDTime  = datetime(Year,2,1,0)
eDTime  = datetime(Year,12,31,0)
dDTime  = timedelta(days=1)
lDTime  = util.ret_lDTime(iDTime, eDTime, dDTime)

baseDir = "/home/utsumi/mnt/well.share/temp"
ny, nx  = 145, 288
# Function --------------
def load_var(var,DTime):
    srcDir = os.path.join(baseDir, var, "%d"%(DTime.year))
    srcPath= os.path.join(srcDir, "%s.runmean.%04d%02d%02d.%dx%d"%(var, DTime.year, DTime.month, DTime.day, ny, nx))

    return fromfile(srcPath, float32).reshape(ny,nx)


def load_mon(var, Year, Mon):
  sPath = os.path.join(baseDir,var,str(Year),"%s.mean.%04d%02d.145x288"%(var,Year,Mon))

  a2var = fromfile(sPath, float32).reshape(ny,nx)
  return a2var


#------------------------

Uref = vstack([
        array([load_mon("spfh",Year,Mon)
            for Mon in [6,7,8,9]]).mean(axis=0)[:ny/2]
       ,array([load_mon("spfh",Year,Mon)
            for Mon in [1,2,3,12]]).mean(axis=0)[ny/2:]
            ])

Vref = vstack([
        array([load_mon("spfh",Year,Mon)
            for Mon in [6,7,8,9]]).mean(axis=0)[:ny/2]
       ,array([load_mon("spfh",Year,Mon)
            for Mon in [1,2,3,12]]).mean(axis=0)[ny/2:]
            ])

a3var = empty([len(lDTime), ny, nx])

for i, DTime in enumerate(lDTime):
    q  = load_var("spfh", DTime)
    a3var[i] = q

lat = 35
lon = 140
iy  = int(floor((lat+90)/1.25))
ix  = int(floor(lon/1.25))

ts = a3var[:, iy-1:iy+2,ix-1:ix+2].mean(axis=(1,2))
plt.plot(ts,"-")
plt.show()

