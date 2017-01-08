from numpy    import *
from datetime import datetime, timedelta
import util
import config_func
import IO_Master
import Front
import calendar
import detect_func
import sys, os
import ConstFront
#from dtanl_fsub import *
from front_fsub import *
#-----------------------
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

#ltq    = ["t","q"]
ltq    = ["t"]
miss  = -9999.0

dvar  = {"t":"ta", "q":"q"}

iDTime = datetime(2001,1,1,0)
eDTime = datetime(2015,8,31,18)
dDTime = timedelta(hours=6)

ret_lDTime = {False: util.ret_lDTime
             ,True : util.ret_lDTime_noleap
             }[noleap]

lDTime   = ret_lDTime(iDTime, eDTime, dDTime)

cfg    = config_func.config_func(prj, model, run)
iom    = IO_Master.IO_Master(prj, model, run, res)

cfg["prj"]   = prj
cfg["model"] = model
cfg["run"]   = run
cfg["res"]   = res

front  = Front.Front(cfg, miss=miss)
ConstF = ConstFront.Const(model=model, res=res)
#------------------------
#local region ------
plev     = 850   #(hPa)
cbarflag = "True"
#-------------------


#thorog  = ctrack_para.ret_thorog()
#thgradorog=ctrack_para.ret_thgradorog()
thorog     = ConstF.thorog
thgradorog = ConstF.thgradorog

#************************
# FUNCTIONS
#************************
# lat & lon
#--------------
a1lat = iom.Lat
a1lon = iom.Lon
#*************************
# front locator :contour
#---------------
def mk_front_loc_contour(a2thermo, a1lon, a1lat, miss):
  a2fmask1 = front_fsub.mk_a2frontmask1(a2thermo.T, a1lon, a1lat, miss).T
  a2fmask2 = front_fsub.mk_a2frontmask2(a2thermo.T, a1lon, a1lat, miss).T
  a2fmask1 = a2fmask1 * (1000.0*100.0)**2.0  #[(100km)-2]
  a2fmask2 = a2fmask2 * (1000.0*100.0)       #[(100km)-1]

  a2loc    = front_fsub.mk_a2meanaxisgrad3_h98_eq6(a2thermo.T, a1lon, a1lat, miss).T

  a2loc    = front_fsub.mk_a2contour(a2loc.T, 0.0, 0.0, miss).T
  a2loc    = ma.masked_equal(a2loc, miss)  

  a2loc    = ma.masked_where(a2fmask1 < 0.0, a2loc)
  a2loc    = ma.masked_where(a2fmask2 < 0.0, a2loc)
  a2loc1   = ma.masked_where(a2loc.mask, a2fmask1).filled(miss)
  a2loc2   = ma.masked_where(a2loc.mask, a2fmask2).filled(miss)

  return a2loc1, a2loc2

#******************************************************
##-- orog & grad orog ----

a2orog  = iom.load_const(var="topo")

#******************************************************
for tq in ltq:
  var = dvar[tq]
  #-----------
  for DTime in lDTime:
    a2thermo  = iom.Load_6hrPlev(var, DTime, plev)
    a2loc1,a2loc2  = mk_front_loc_contour(a2thermo, a1lon, a1lat, miss)
    sodir, soname1, soname2   = front.path_potloc(DTime, tq)
    detect_func.mk_dir(sodir)
    #------
    a2loc1.tofile(soname1)
    a2loc2.tofile(soname2)
    print soname1
    print soname2
  
 
