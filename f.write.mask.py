from numpy import *
from datetime import datetime, timedelta
import util
import config_func
import Front
import ConstMask

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

iDTime = datetime(2004,1,1,6)
eDTime = datetime(2004,1,31,18)
dDTime = timedelta(hours=6)

lDTime = {False: util.ret_lDTime
         ,True : util.ret_lDTime_noleap
         }[noleap]( iDTime, eDTime, dDTime )

cfg     = config_func.config_func(prj, model, run)
cfg["prj"  ] = prj
cfg["model"] = model
cfg["run"  ] = run
cfg["res"  ] = res

ConM    = ConstMask.Const(model=model, res=res)
radkmt  = ConM.dictRadkm["front.t"]
radkmq  = ConM.dictRadkm["front.q"]

F  = Front.Front(cfg=cfg)

for tq in ltq:
    func_mkMask = {"t": F.mkMask_tfront
                  ,"q": F.mkMask_qfront
                  }[tq]

    for DTime in lDTime:
        oDir, oPath = F.path_mask(DTime, tq=tq, radkm=radkmt)
        a2dat       = func_mkMask(DTime)
        util.mk_dir(oDir)
        a2dat.tofile(oPath)
        print oPath
  
  
  
