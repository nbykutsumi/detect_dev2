from numpy import *
from detect_fsub import *
from datetime import datetime
from collections import deque
import util
import config_func
import IO_Master
import Cyclone
import os
import calendar

#--------------------------------------------------
prj     = "JRA55"
model   = "__"
run     = "__"
res     = "145x288"
noleap  = False

#prj     = "HAPPI"
#model   = "MIROC5"
#run     = "C20-ALL-001"
#res     = "128x256"
#noleap  = True

iYear  = 2004
eYear  = 2004
lYear  = range(iYear,eYear+1)
lMon   = [1,3,5,7,9,11]
#lMon   = [1]
lHour  = [0,12]

cfg    = config_func.config_func(prj, model, run)
iom    = IO_Master.IO_Master(prj, model, run, res)
cy     = Cyclone.Cyclone(cfg)
#******************************
def save_csv(var, ldat):
  """
  var: rvort, dt, wmeanlow, wmeanup
  """
  ldat   = sort(ldat)
  lendat = len(ldat)

  dunit  = {"rvort":"s-1",
            "dt"   :"K",
            "wLow_Up":"m/s",
            "pgrad":"Pa/1000km"
           }

  sout = "frac/%s(%s),%s\n"%(model,var,dunit[var])
  for i,dat in enumerate(ldat):
    frac = (i+1)/float(lendat)
    sout = sout + "%f,%f\n"%(frac,dat)

  #
  #odir   = "/media/disk2/out/obj.valid/c.%s"%(var)
  odir   = os.path.join(cy.baseDir, "obj.valid","c.%s"%(var))
  util.mk_dir(odir)
  oname  = odir + "/%s.%s.%04d-%04d.%s.csv"%(var,model,iYear,eYear,"ASAS")

  f = open(oname,"w");  f.write(sout);  f.close()
  print oname
#******************************

def nearest_idx(aSrc,val):
    ''' return nearest index. by HJKIM'''
    if hasattr(val,'__iter__'): return [abs(aSrc-v).argmin() for v in val]
    else: return abs(aSrc-val).argmin()
#******************************
def mk_saone2bnxy(a1lon_bn, a1lat_bn):
  a1lon_saone = arange(0.5,359.5+0.01,1.0)
  a1lat_saone = arange(-89.5, 89.5+0.01, 1.0)

  a1corres_x  = nearest_idx(a1lon_bn, a1lon_saone)
  a1corres_y  = nearest_idx(a1lat_bn, a1lat_saone)
  a2corres_x, a2corres_y = meshgrid(a1corres_x, a1corres_y)
  return a2corres_x, a2corres_y

def load_chart(Year,Mon,Day,Hour):
  #srcDir  = "/media/disk2/out/chart/ASAS/exc/%04d%02d"%(Year,Mon)
  srcDir  = "/home/utsumi/mnt/well.share/chart/out/ASAS/exc/%04d%02d"%(Year,Mon)
  #srcPath = os.path.join(srcDir, "exc.ASAS.2004.01.04.12.sa.one")
  srcPath = os.path.join(srcDir, "exc.ASAS.%04d.%02d.%02d.%02d.sa.one"%(Year,Mon,Day,Hour))
  a2dat   = fromfile(srcPath, float32).reshape(180,360)
  return a2dat


#******************************
def mk_maxvort(a2u, a2v, a1lon, a1lat, miss):
  a2rvort   = detect_fsub.mk_a2rvort(a2u.T, a2v.T, a1lon, a1lat, miss).T

  a2rvort[:ny/2] = -a2rvort[:ny/2]

  a2large   = empty([ny+2,nx+2],float32)
  a3rvort   = empty([9,ny,nx],float32)

  a2large[0]    = miss
  a2large[-1]   = miss
  a2large[1:-1,  0]   = a2rvort[:,-1]
  a2large[1:-1, -1]   = a2rvort[:, 0]
  a2large[1:-1, 1:-1] = a2rvort

  a3rvort[0] = a2rvort
  a3rvort[1] = a2large[:-2,:-2]
  a3rvort[2] = a2large[:-2,2:]
  a3rvort[3] = a2large[:-2,1:-1]
  a3rvort[4] = a2large[2:,:-2]
  a3rvort[5] = a2large[2:,2:]
  a3rvort[6] = a2large[2:,1:-1]
  a3rvort[7] = a2large[1:-1:,:-2]
  a3rvort[8] = a2large[1:-1:,2:]

  return a3rvort.max(axis=0)

#******************************
#-- Reanalysis --
a1lat = iom.Lat
a1lon = iom.Lon
ny    = iom.ny
nx    = iom.nx
miss  = -9999.

#----------------
a2one   = ones([ny,nx],float32)
a2miss  = ones([ny,nx],float32)*miss
a2corres_x, a2corres_y = mk_saone2bnxy(a1lon, a1lat)
print a2corres_x

#-- initialize --
lpgrad  = deque([])
lrvort  = deque([])
a2tlow  = a2one
a2tmid  = a2one
a2tup   = a2one
#a2ulow  = a2one
a2uup   = a2one
#a2vlow  = a2one
a2vup   = a2one


#----------------
for Year in lYear:
  for Mon in lMon:
    print Year,Mon
    eDay  = calendar.monthrange(Year,Mon)[1]
    lDay  = range(1,eDay+1)
    for Day, Hour in [[Day,Hour] for Day in lDay for Hour in lHour]:
      #-- chart territory ----
      a2chart_one = load_chart(Year,Mon,Day,Hour)
      a1x         = ma.masked_where(a2chart_one==0.0, a2corres_x).compressed()
      a1y         = ma.masked_where(a2chart_one==0.0, a2corres_y).compressed()
      a2chart_bn  = a2miss.copy() 
      a2chart_bn[a1y,a1x] = 1.0
      #a2chart_bn  = detect_fsub.mk_territory(a2chart_bn.T, a1lon, a1lat, 200*1000.,miss).T
      a2chart_bn  = detect_fsub.mk_territory_8grids(a2chart_bn.T, miss, nx, ny).T

      #-- load cyclone from reanalysis --
      DTime   = datetime(Year,Mon,Day,Hour)
      a2pgrad = cy.load_a2dat("pgrad",DTime)
      a2pgrad = ma.masked_where(a2chart_bn==miss, a2pgrad).filled(miss)

      #-- calc rvort --------------------
      a2ulow  = iom.Load_6hrPlev("ua", DTime, 850)
      a2vlow  = iom.Load_6hrPlev("va", DTime, 850)

      a2rvort = mk_maxvort(a2ulow, a2vlow, a1lon, a1lat, miss)
      a2rvort = ma.masked_where(a2pgrad==miss, a2rvort)

      
      a2pgrad    = ma.masked_equal(a2pgrad, miss)
      a2rvort    = ma.masked_equal(a2rvort, miss)
      #-- stack ---
      lpgrad.extend( a2pgrad.compressed() )
      lrvort.extend( a2rvort.compressed() )

#-- save ----
save_csv("pgrad",lpgrad)
save_csv("rvort",lrvort)


