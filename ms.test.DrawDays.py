from numpy import *
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import Reanalysis

ra = Reanalysis.Reanalysis(model="JRA55", res="bn")
ny = ra.ny
nx = ra.nx
miss = -9999.

Lat = ra.Lat
Lon = ra.Lon

iy = 20
ey = -20

#--- data ---
#for dattype in ["Sday","Eday"]:
for dattype in ["Eday"]:
  iPath = "./ms.%s.bn"%(dattype)
  a2dat = fromfile(iPath, float32).reshape(ny,nx)
  a2dat = ma.masked_equal(a2dat, miss)
  
  #--- Domain ---
  a2dat = a2dat[iy:ey]
  Lat   = Lat[iy:ey]
  Lon   = Lon
  LONS, LATS = meshgrid(Lon, Lat)
  
  #--- prep ----
  figmap= plt.figure(figsize=(40,13))
  axmap = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
  M     = Basemap(resolution="l", llcrnrlat=Lat[0], llcrnrlon=Lon[0], urcrnrlat=Lat[-1], urcrnrlon=Lon[-1], ax=axmap)
  
  #--- imshow ---
  im    = M.imshow(a2dat)
  M.colorbar(im)
  
  #--- contour --
  im    = M.contour(LONS, LATS, a2dat, levels=range(10,560,10), colors="k")
  plt.clabel(im, fontsize=10, inline=1, fmt="%d")
  #--- coastlines --
  M.drawcoastlines(linewidth=0.5)
  
  #--- Meridians and Parallels --
  meridians  = range(0,360+1,30)
  parallels  = range(-90,90+1,30)
  M.drawmeridians(meridians, labels=[0,0,0,1], fontsize=12)
  M.drawparallels(parallels, labels=[1,0,0,0], fontsize=12)
  #--- save -----
  figPath = "./ms.%s.png"%(dattype)
  plt.savefig(figPath)
  print figPath
