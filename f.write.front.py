from numpy import *
from datetime import datetime, timedelta
import config_func
import util
import Front
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

iDTime = datetime(2004,1,1,6)
eDTime = datetime(2004,1,31,18)
dDTime = timedelta(hours=6)

ret_lDTime = {False: util.ret_lDTime
             ,True : util.ret_lDTime_noleap
             }[noleap]

lDTime   = ret_lDTime(iDTime, eDTime, dDTime)

cfg = config_func.config_func(prj, model, run)
cfg["prj"]  = prj
cfg["model"]= model
cfg["run"]  = run
cfg["res"]  = res
F           = Front.Front(cfg=cfg)

ltq = ["t"]
for tq in ltq:

    mk_front = {"t": F.mk_tfront
               ,"q": F.mk_qfront
               }[tq]

    for DTime in lDTime:
        oDir, oPath = F.path_finloc(DTime, tq=tq)
        loc  = mk_front(DTime)
        util.mk_dir(oDir)
        loc.tofile(oPath)
        print oPath



