from numpy import *
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib
import os, sys
import myfunc.IO.JRA55 as JRA55
import util

Year = 2006
lMon = range(1,12+1)
#lMon = [1]
ny, nx= 145, 288
jra  = JRA55.Jra55()
a1lat  = jra.Lat
a1lon  = jra.Lon

k    = 7 # interval grids for vector 

BBox   = [[-90+1.25*0.5, 1.25*0.5], [90-1.25*0.5, 360-1.25*0.5]]

latmin = a1lat[0]  - (a1lat[1]  - a1lat[0])*0.5
latmax = a1lat[-1] + (a1lat[-1] - a1lat[-2])*0.5
lonmin = a1lon[0]  - (a1lon[1]  - a1lon[0])*0.5
lonmax = a1lon[-1] + (a1lon[-1] - a1lon[-2])*0.5

a1LAT = r_[ array([latmin]), (a1lat[1:] + a1lat[:-1])*0.5, array([latmax])]
a1LON = r_[ array([lonmin]),   (a1lon[1:] + a1lon[:-1])*0.5, array([lonmax])]

X,Y   = meshgrid(a1LON, a1LAT)
# BBox --------
[lllat,lllon],[urlat,urlon] = BBox

# Function----------------
def f_draw(U, V, scale, stitle, oPath):
    figmap = plt.figure(figsize=(6.4,3.25))
    axmap  = figmap.add_axes([0.1,0.1, 0.8, 0.8])
    M      = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
  
    im     = M.quiver(X[::k,::k], Y[::k,::k], U[::k,::k], V[::k,::k]
            ,units = "xy"
            ,scale = scale
            )
  
    M.drawcoastlines()
    parallels   = arange(-90,90+0.1, 30)
    meridians   = arange(0, 360+0.1, 30)
    M.drawparallels( parallels, labels=[1,0,0,0], fontsize=8)
    M.drawmeridians( meridians, labels=[0,0,0,1], fontsize=8)

    # title
    plt.title(stitle)

    # save
    plt.savefig(oPath)
    print oPath


def load_var(var, Year, Mon):
  sPath = os.path.join(baseDir,var,str(Year),"%s.mean.%04d%02d.145x288"%(var,Year,Mon))

  a2var = fromfile(sPath, float32).reshape(ny,nx)
  return a2var

#--------------------------
baseDir = "/home/utsumi/mnt/well.share/temp"
figdir  = os.path.join(baseDir, "pict")
util.mk_dir(figdir)

"""
# Q*Wind  
for Mon in lMon:
    U    = load_var("q.ugrd", Year,Mon)
    V    = load_var("q.vgrd", Year,Mon)
    scale = 0.004
    
    stitle = "q*wind %04d %02d"%(Year,Mon)
    oPath  = os.path.join(figdir,"qwind.%04d.%02d.png"%(Year,Mon))
    f_draw( U, V, scale, stitle, oPath)

"""

# diff Q*Wind
Uref = vstack([
        array([load_var("q.ugrd",Year,Mon)
            for Mon in [6,7,8]]).mean(axis=0)[:ny/2]
       ,array([load_var("q.ugrd",Year,Mon)
            for Mon in [1,2,12]]).mean(axis=0)[ny/2:]
            ])

Vref = vstack([
        array([load_var("q.vgrd",Year,Mon)
            for Mon in [6,7,8]]).mean(axis=0)[:ny/2]
       ,array([load_var("q.vgrd",Year,Mon)
            for Mon in [1,2,12]]).mean(axis=0)[ny/2:]
            ])


for Mon in lMon:
    U = load_var("q.ugrd", Year, Mon) - Uref
    V = load_var("q.vgrd", Year, Mon) - Vref
    scale = 0.006

    stitle = "d(q*wind) %04d %02d - DJF(JJA)"%(Year,Mon)
    oPath  = os.path.join(figdir,"d.qwind.%04d.%02d.png"%(Year,Mon))
    f_draw( U, V, scale, stitle, oPath)

"""
# Wind
for Mon in lMon:
    U    = load_var("ugrd", Year,Mon)
    V    = load_var("vgrd", Year,Mon)
    scale = 0.7
    
    stitle = "wind %04d %02d"%(Year,Mon)
    oPath  = os.path.join(figdir,"wind.%04d.%02d.png"%(Year,Mon))
    f_draw( U, V, scale, stitle, oPath)
"""

# diff Wind

Uref = vstack([
        array([load_var("ugrd",Year,Mon)
            for Mon in [6,7,8]]).mean(axis=0)[:ny/2]
       ,array([load_var("ugrd",Year,Mon)
            for Mon in [1,2,12]]).mean(axis=0)[ny/2:]
            ])

Vref = vstack([
        array([load_var("vgrd",Year,Mon)
            for Mon in [6,7,8]]).mean(axis=0)[:ny/2]
       ,array([load_var("vgrd",Year,Mon)
            for Mon in [1,2,12]]).mean(axis=0)[ny/2:]
            ])


for Mon in lMon:
    U = load_var("ugrd", Year, Mon) - Uref
    V = load_var("vgrd", Year, Mon) - Vref
    scale = 0.6

    stitle = "d(wind) %04d %02d - DJF(JJA)"%(Year,Mon)
    oPath  = os.path.join(figdir,"d.wind.%04d.%02d.png"%(Year,Mon))
    f_draw( U, V, scale, stitle, oPath)

