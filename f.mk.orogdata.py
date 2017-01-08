from numpy import *
from detect_fsub import *
import util
import config_func
import IO_Master
import Fig

calcflag  = True
#calcflag  = False

prj     = "JRA55"
model   = "__"
run     = "__"
res     = "145x288"

#prj     = "HAPPI"
#model   = "MIROC5"
#run     = "C20-ALL-001"
#res     = "128x256"

radkm = 300.  # (km)

cfg   = config_func.config_func(prj, model, run)
iom   = IO_Master.IO_Master(prj, model, run, res)
ny    = iom.ny
nx    = iom.nx
a1lat = iom.Lat 
a1lon = iom.Lon
miss  = -9999.

orog       = iom.Load_const("topo")
oDir       = cfg["baseDir"] + "/const"
util.mk_dir(oDir)
maxorogname= oDir + "/maxtopo.%04dkm.%s"%(radkm, res)

if calcflag==True:
  a2orog     = iom.load_const("topo")
  a2maxorog  = detect_fsub.mk_a2max_rad(a2orog.T, a1lon, a1lat, radkm, miss).T
  #--- write to file -------
  a2maxorog.tofile(maxorogname)

#--- figure: max orog ----
figname = maxorogname + ".png"
Fig.DrawMap( a2maxorog, a1lat, a1lon, figname=figname)
print figname
