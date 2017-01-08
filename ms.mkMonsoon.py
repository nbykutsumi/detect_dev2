from numpy import *
from datetime import datetime, timedelta
import os, sys
import myfunc.util as util
import Monsoon

iDTime = datetime(1980,1,1,0)
#eDTime = datetime(2015,12,31,0)
eDTime = datetime(1980,12,31,0)
dDTime = timedelta(hours=24)
lDTime = util.ret_lDTime(iDTime, eDTime, dDTime)

model  = "JRA55"
res    = "bn"
var    = "PWAT"

ms  = Monsoon.MonsoonMoist(model=model, res=res, var=var)
ms.prepMonsoonMoist()
print lDTime
for DTime in lDTime:
  a2ms  = ms.mkMonsoonMoist(DTime)
  rootDir, sDir, sPath = ms.pathMonsoonMoist(DTime)
  util.mk_dir(sDir)
  a2ms.astype(float32).tofile(sPath)
  print sPath

