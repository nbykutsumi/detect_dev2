from numpy import *
from datetime import datetime
import util
import calendar
import Cyclone
import config_func

#-- test @ 27 Oct --
iYear = 2004
eYear = 2004
lYear = range(iYear,eYear+1)
lMon  = range(1,12+1)
lHour = [0,6,12,18]

prj    = "JRA55"
model  = "__"
run    = "__"
res    = "145x288"
#tctype = "obj"
tctype = "bst"
radkm  = 1000.

cfg    = config_func.config_func(prj, model, run)
cfg["res"] = res 

for Year in lYear:
  for Mon in lMon:
    #--- init ----
    iYM  = [Year,Mon]
    eYM  = iYM
    Cy   = Cyclone.Cyclone_2D(iYM,eYM, cfg, tctype=tctype)
    #-------------
    iDay = 1
    eDay = calendar.monthrange(Year,Mon)[1]
    for Day,Hour in [[Day,Hour] for Day in range(iDay, eDay+1) for Hour in lHour]:
      DTime = datetime(Year,Mon,Day,Hour)
            
      a2exc = Cy.mkMask_exc(DTime, radkm=radkm) 
      a2tc  = Cy.mkMask_tc (DTime, radkm=radkm)

      oDir_exc, oPath_exc = Cy.path_Mask_exc(DTime)
      oDir_tc,  oPath_tc  = Cy.path_Mask_tc (DTime)

      util.mk_dir(oDir_exc)
      util.mk_dir(oDir_tc )

      a2exc.tofile(oPath_exc)
      a2tc .tofile(oPath_tc)
      print oPath_exc



