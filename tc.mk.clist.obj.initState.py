from numpy import *
from collections import deque
from   datetime import datetime, timedelta
import sys
import util
import config_func
import Cyclone

prj   = "JRA55"
model = "__"
run   = "__"
res   = "125x288"
noleap= False
#iyear_data = 1958
#imon_data  = 1
iyear_data = 2004
imon_data  = 1



#prj     = "HAPPI"
#model   = "MIROC5"
#run     = "C20-ALL-001"
#res     = "128x256"
#noleap  = True
#iyear_data = 2006
#imon_data  = 1

#iYM    = [2006,1]
#eYM    = [2006,1]
iYM    = [2004,1]
eYM    = [2004,12]
lYM    = util.ret_lYM(iYM, eYM)

cfg    = config_func.config_func(prj, model, run)
cy     = Cyclone.Cyclone(cfg)
#**********************************************
def ret_a1initState(var, year,mon,dinitState_pre):
  #----------
  dinitState              = {}
  dinitState[-9999,-9999] = -9999.0
  #----------
  a1idate     = cy.load_clist("idate",year,mon) 
  a1ipos      = cy.load_clist("ipos" ,year,mon) 
  a1time      = cy.load_clist("time" ,year,mon) 
  a1state     = cy.load_clist(var    ,year,mon) 
  a1land      = cy.load_clist("land" ,year,mon) 

  #------------------------
  n  = len(a1idate)
  ldat    = deque([])
  for i in range(n):
    idate = a1idate[i]
    ipos  = a1ipos [i]
    time  = a1time [i]
    state = a1state[i]
    #print idate, ipos, time
    #--- check initial time --
    if time == idate:
      dinitState[idate, ipos] = state

    #-----------
    try:
      ldat.append( dinitState[idate, ipos] )
    except KeyError:
      try:
        ldat.append( dinitState_pre[idate, ipos])
      except:
        ldat.append( -9999.0)
#        sys.exit() 
  #---------------------------
  a1initState = array(ldat, float32)
  return dinitState, a1initState
#**********************************************

#--- init ----
iyear, imon= lYM[0]
date_first = datetime(iyear,imon, 1)
date_pre   = date_first + timedelta(days = -2)
year_pre   = date_pre.year
mon_pre    = date_pre.month
if (iyear == iyear_data)&(imon ==imon_data):
  dinitsst   = {} 
  dinitland  = {} 
else:
  dinitsst , a1temp = ret_a1initState("sst" , year_pre, mon_pre, {} )
  dinitland, a1temp = ret_a1initstate("land", year_pre, mon_pre, {} )
#-------------
for [year, mon] in lYM:
  dinitsst_pre          = dinitsst
  dinitsst, a1initsst   = ret_a1initState( "sst", year, mon, dinitsst_pre )

  dinitland_pre         = dinitland
  dinitland, a1initland = ret_a1initState( "land",year, mon, dinitland_pre )
 
 
  #---- oname ----------------
  name_sst  = cy.path_clist("initsst" ,year,mon)[1]
  name_land = cy.path_clist("initland",year,mon)[1]
  a1initsst.tofile(name_sst)
  a1initland.tofile(name_land)
  print name_sst

  
