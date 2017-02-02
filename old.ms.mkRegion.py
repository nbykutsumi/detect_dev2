from numpy import *
import myfunc.util as util
import Reanalysis
import Monsoon
import myfunc.fig.Fig as Fig

var   = "APCP"
#var   = "PWAT"
dstype= {"APCP":"fcst_phy2m125"
        ,"PWAT":"anl_column125"}
iYear = 1980
eYear = 1999
model = "JRA55"
res   = "bn"
miss  = -9999.
ra    = Reanalysis.Reanalysis(model=model, res=res)
ny    = ra.ny
nx    = ra.nx
a1lat = ra.Lat
a1lon = ra.Lon
ms    = Monsoon.MonsoonMoist(model=model, res=res)


def Region5Mon(var, iYear,eYear):
  lYear  = range(iYear,eYear+1)
  a2var0 = zeros([ny,nx],float32)
  a2var1 = zeros([ny,nx],float32)
  a2var2 = zeros([ny,nx],float32)

  for Year in lYear:
    for Mon in range(1,12+1):
      a2var0 = a2var0 + ra.load_mon(var, Year,Mon).Data
      if Mon in [5,6,7,8,9]:
        a2var1 = a2var1 + ra.load_mon(var, Year,Mon).Data
      if Mon in [11,12,1,2,3]:
        a2var2 = a2var2 + ra.load_mon(var, Year,Mon).Data

  a2var0 = a2var0/ len(lYear) /12 
  a2var1 = a2var1/ len(lYear) /5
  a2var2 = a2var2/ len(lYear) /5
  a2summer = r_[ a2var2[:ny/2,:], a2var1[ny/2:,:]]
  a2winter = r_[ a2var1[:ny/2,:], a2var2[ny/2:,:]]

  a2dif  = (a2summer - a2winter)
  return ma.masked_where(a2summer<= a2var0*0.55, a2dif)

def RegionZL04(iYear,eYear):
  var    = "PWAT"
  lYear  = range(iYear,eYear+1)

  a3var1 = zeros([3,ny,nx],float32)
  for i,Mon in enumerate([6,7,8]):
    for Year in lYear:
      a3var1[i] = a3var1[i] + ra.load_mon(var, Year,Mon).Data
    a3var1[i] = a3var1[i]/len(lYear)

  a3var2 = zeros([3,ny,nx],float32)
  for i,Mon in enumerate([12,1,2]):
    for Year in lYear:
      a3var2[i] = a3var2[i] + ra.load_mon(var, Year,Mon).Data
    a3var2[i] = a3var2[i]/len(lYear)

  a2max = r_[ a3var2[:,:ny/2,:].max(axis=0), a3var1[:,ny/2:,:].max(axis=0)]
  a2min = r_[ a3var1[:,:ny/2,:].min(axis=0), a3var2[:,ny/2:,:].min(axis=0)]

  return a2max - a2min


a2rg  = Region5Mon("APCP", iYear,eYear)
a2rg2 = RegionZL04(iYear,eYear)
a2rg  = ma.masked_where(a2rg2<=12, a2rg)
#a2out = ma.masked_less(a2rg,1.854)
a2out = ma.masked_where(a2rg<2.0, ones([ny,nx],float32))
a2out = a2out.filled(miss)

rootDir, srcDir, srcPath = ms.pathRegionW14(iYear,eYear)
util.mk_dir(srcDir)
a2out.tofile(srcPath)
print srcPath

#----- Figure ----------------
#a2fig   = r_[a2out[:,nx/2:], a2out[:,:nx/2]]
a2fig   = a2out
a2fig   = ma.masked_equal(a2fig, miss)
figname = srcPath + ".png"
BBox    = [[-90,0],[90,360]]
Fig.DrawMap(a2in=a2fig, a1lat=a1lat, a1lon=a1lon, figname=figname, BBox=BBox, vmax=3.)



