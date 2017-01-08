from numpy import *
from detect_fsub import *
#from myfunc_fsub import *
from myfunc.regrid.upscale_fsub import *
from datetime import datetime, timedelta
import ctrack_func
import front_func
import calendar
import os, sys
import ConstFront
#from JRA55 import jra55
import Reanalysis
from Chart import chart
from Front import front
miss   = -9999.
tqtype = "t"
#tqtype = "q"
model  = "JRA55"
res    = "145x288"
ra     = Reanalysis.Reanalysis(model=model, res=res)
front  = front(model=model,res=res)
ny,nx  = ra.ny, ra.nx
a1lat  = ra.Lat
a1lon  = ra.Lon
rad    = 500. * 1000.  # [m]
BBox   = [[25,120],[50,160]]
lYear  = [2004]
lMon   = [1,2,3,4,5,6,7,8,9,10,11,12]
#lMon   = [3,4,5,6,7,8,9,10,11,12]
#lMon   = [1]
#lMon   = [6,7,8]
tstep   = 12  # hours

if   tqtype == "t":
  lM1    = [0.18,0.22,0.26,0.3,0.34,0.38,0.42,0.46]
  lM2    = [0.2,0.6,1.0,1.4,1.8,2.2]

elif tqtype == "q":
  lM1    = array([1.1, 1.4, 1.7, 2.0, 2.3, 2.6, 2.9])*1.0e-4
  lM2    = array([0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.4])*1.0e-3

CFront = ConstFront.const(model=model,res=res)

def ret_a2domain(BBox, a1lat, a1lon):
  ny,nx = len(a1lat), len(a1lon)
  lllat = BBox[0][0]
  lllon = BBox[0][1]
  urlat = BBox[1][0]
  urlon = BBox[1][1]
  a2lon, a2lat = meshgrid(a1lon, a1lat)
  a2domain = ones([ny,nx], float32)
  a2domain = ma.masked_where( ma.masked_outside( a2lat, lllat, urlat).mask, a2domain)
  a2domain = ma.masked_where( ma.masked_outside( a2lon, lllon, urlon).mask, a2domain).filled(miss)
  return a2domain

  


def upscale(a2in):
  a1lon_fin = ch.Lon
  a1lat_fin = ch.Lat
  a1lat_out = ra.Lat
  a1lon_out = ra.Lon
  pergrid   = 0
  missflag  = 1
  a2out = 1
  a2out     = \
     myfunc_fsub.upscale( a2in.T\
                      ,a1lon_fin\
                      ,a1lat_fin\
                      ,a1lon_out\
                      ,a1lat_out\
                      ,pergrid\
                      ,missflag\
                      ,miss).T
  return a2out


def mk_a2count(sDtime, eDtime, M1, M2, rad, thgrids, probability=True):
  Dtime = sDtime
  a2counts  = zeros([ny, nx],float32)
  a2one     = ones ([ny, nx],float32)
  dDtime    = timedelta(hours=tstep)
  while Dtime <= eDtime:

    if   tqtype == "t":
      a2dat    = front.mk_tfront(Dtime, M1=M1, M2=M2)
    elif tqtype == "q":
      a2dat    = front.mk_qfront(Dtime, M1=M1, M2=M2)

    a2terr   = detect_fsub.mk_territory(a2dat.T, a1lon, a1lat, rad, miss).T
    a2counts = a2counts + ma.masked_where(a2terr ==miss, a2one).filled(0.0)
    Dtime    = Dtime + dDtime

  if probability == True:
    steps    = (eDtime - sDtime).total_seconds() / dDtime.total_seconds() + 1
    a2counts = a2counts / steps
  return a2counts 
#-------------------------------------------
a2domain = ret_a2domain(BBox, a1lat, a1lon)
thgrids  = CFront.thgrids
#thgrids  = 3

for Year,Mon in [[Year,Mon] for Year in lYear for Mon in lMon]:

  if tqtype == "t":
    if Mon in [6,7,8,9]:
      ftype = [1,2,3]
    else:
      ftype = False

  elif tqtype == "q":
    ftype = [1,2,4]


  sout = "M1,M2,RMSE\n"
  for M1,M2 in [[M1,M2] for M1 in lM1 for M2 in lM2]:
    iDay     = 1
    eDay     = calendar.monthrange(Year,Mon)[1]
#    eDay     = 2    # test
    sDtime = datetime(Year, Mon, iDay, 0)
    eDtime = datetime(Year, Mon, eDay, 18)
    dDtime = timedelta(hours=tstep)
    ch     = chart()
    a2chart= ch.mk_a2count(sDTime=sDtime, eDTime=eDtime, dDTime=dDtime, ftype=ftype, rad=rad, probability=True)
    a2chart= upscale(a2chart)
    a2ra   = mk_a2count(sDtime, eDtime, M1, M2, rad, thgrids, probability=True)
    a2chart = ma.masked_where(a2domain==miss, a2chart)
    a2ra    = ma.masked_where(a2domain==miss, a2ra  )

    rmse    = sqrt( mean((a2ra - a2chart)**2.0) )
    sout    = sout + "%e,%e,%e\n"%(M1,M2,rmse)
    print Year,Mon,"M1=",M1,"M2=",M2
  #---------
  outDir = "/media/disk2/out/obj.valid/front.para/%s.%s"%(model, res)
  ctrack_func.mk_dir(outDir)
  outPath= os.path.join(outDir, "%s.RMSE.%04d.%02d.csv"%(tqtype,Year,Mon))
  f=open(outPath, "w"); f.write(sout); f.close()
  print "Save",outPath

