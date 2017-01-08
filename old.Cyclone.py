from numpy import *
from detect_fsub import *
from datetime import datetime, timedelta
from collections import deque
from ConstCyclone import Const
import os
import itertools
import socket
import BestTrackTC
import calendar
#****************************************************
def read_txtlist(iname):
  f = open(iname, "r")
  lines = f.readlines()
  f.close()
  lines = map(float, lines)
  aout  = array(lines, float32)
  return aout

def ret_baseDir(model="JRA55", res="bn"):
  hostname     = socket.gethostname()
  if hostname == "well":
    return "/media/disk2/out/%s/%s"%(model,res)
  elif hostname in ["mizu","naam"]:
    return "/tank/utsumi/out/%s/%s"%(model,res)

def ret_lYM(iYM, eYM):
  iYear, iMon = iYM
  eYear, eMon = eYM
  if iYear==eYear:
    lYM = [[iYear,Mon] for Mon in range(iMon,eMon+1)]
  else:
    lYM = [[iYear,Mon] for Mon in range(iMon,12+1)]
  
    lYM = lYM + [[Year,Mon] \
                  for Year in range(iYear+1,eYear)\
                  for Mon  in range(1,12+1)]

    lYM = lYM + [[eYear,Mon] for Mon in range(1,eMon+1)]
  return lYM

#---------------------------------------------------
def solve_time(stime):
  year = int( stime/10**6 )
  mon  = int( (stime - year*10**6)/10**4 )
  day  = int( (stime - year*10**6 - mon*10**4)/10**2)
  hour = int( (stime - year*10**6 - mon*10**4 - day*10**2) )
  return year, mon, day, hour
#---------------------------------------------------
def fortpos2pyxy(number, nx, miss_int):
  if (number == miss_int):
    iy_py = miss_int
    ix_py = miss_int
  else:
    iy_py = int((number-1.0)/nx)      # iy_py = 0,1,2,..
    ix_py = number - nx*iy_py-1   # ix_py = 0,1,2,..
  #----
  return ix_py, iy_py
#---------------------------------------------------
def expand8grids(lxy, ny, nx):
  # lxy = [(x1,y1), (x2,y2), ...]
  if len(lxy) == 0:
    lXY = array([])
  else:
    lXY = deque([])
    for x,y in lxy:
      lXY.extend(list(itertools.product([x-1,x,x+1],[y-1,y,y+1])))
  
    ax, ay = zip(*lXY)
    ax = ma.masked_equal(ax,-1).filled(nx-1)
    ax = ma.masked_equal(ax,nx).filled(0)
    ay = ma.masked_equal(ay,-1).filled(0)
    ay = ma.masked_equal(ay,ny).filled(ny-1)
  
    lXY = array(zip(ax,ay))
  return  lXY
  
#---------------------------------------------------
class Cyclone(Const):
  def __init__(self, model="JRA55", res="bn"):
    Const.__init__(self, model=model, res=res)
    self.baseDir = ret_baseDir(model=model, res=res)
    #------------
    self.Lat     = read_txtlist( os.path.join(self.baseDir, "lat.txt"))
    self.Lon     = read_txtlist( os.path.join(self.baseDir, "lon.txt"))
    self.ny      = len(self.Lat)
    self.nx      = len(self.Lon)
    self.dNumType= {"life"    :int32,
                    "dura"    :int32,
                    "ipos"    :int32,
                    "epos"    :int32,
                    "idate"   :int32,
                    "time"    :int32,
                    "age"     :int32,
                    "nowpos"  :int32,
                    "lastpos" :int32,
                    "prepos"  :int32,
                    "nextpos" :int32,
                    "pgrad"   :float32,
                    "pgmax"   :float32,
                    "pmean"   :float32,
                    #"iedist"  :float32,
                    "rvort"   :float32,
                    "dtlow"   :float32,
                    "dtmid"   :float32,
                    "dtup"    :float32,
                    "wmeanlow":float32,
                    "wmeanup" :float32,
                    "sst"     :float32,
                    "land"    :float32,
                    "initsst" :float32,
                    "initland":float32
                   }

  def path_a2dat(self, var, DTime):
    Year = DTime.year
    Mon  = DTime.month
    Day  = DTime.day
    Hour = DTime.hour
    self.tstep   = "6hr"
    self.srcDir  = os.path.join(self.baseDir, self.tstep, var, "%04d"%(Year), "%02d"%(Mon))
    self.srcPath = os.path.join(self.srcDir, "%s.%04d%02d%02d%02d.bn"%(var,Year,Mon,Day,Hour))
    return self

  def load_a2dat(self, var, DTime):
    srcPath = self.path_a2dat(var, DTime)
    a2dat = fromfile(self.srcPath, self.dNumType[var]).reshape(self.ny,self.nx)
    return a2dat

  def path_clist(self, var, Year, Mon):
    self.tstep   = "6hr"
    srcDir  = os.path.join(self.baseDir, self.tstep, "clist", "%04d"%(Year), "%02d"%(Mon))
    srcPath = os.path.join(srcDir, "%s.%04d.%02d.bn"%(var,Year,Mon))
    return srcDir, srcPath

  def load_clist(self, var, Year, Mon):
    srcPath = self.path_clist(var, Year, Mon)[1]
    return fromfile(srcPath, self.dNumType[var])

  #def dictC(self, Year, Mon, varname="pgrad", tctype="obj"):
  # if tctype == "obj":
  #   return self.dictC_objTC(Year, Mon, varname=varname)
  # if tctype == "bst":
  #   return self.dictC_bstTC(Year, Mon, varname=varname)

  def mkInstDictC(self, iYM, eYM, varname="pgrad", tctype="bst"):
   if tctype == "obj":
     return self.mkInstDictC_objTC(iYM, eYM, varname=varname)
   if tctype == "bst":
     return self.mkInstDictC_bstTC(iYM, eYM, varname=varname)

  #def dictC_bstTC(self, Year, Mon, varname="pgrad"):
  #  thpgrad   = self.thpgrad
  #  thdura    = self.thdura

  #  dictExC   = {}
  #  dictTC    = {}
  #  da1       = {}

  #  #--- TC dictionary ----
  #  bst       = BestTrackTC.BestTrack("IBTrACS")
  #  dictTC    = bst.ret_dpyxy(Year, self.Lon, self.Lat)

 
  #  #---- make ExC dictionary -----
  #  lvar      = ["dura","pgrad","nowpos","time"]
  #  for var in lvar:
  #     da1[var]  = self.load_clist(var, Year, Mon)

  #  dtcloc   = {}
  #  nlist    = len(da1["dura"])

  #  for i in range(nlist):
  #    dura        = da1["dura"    ][i]
  #    pgrad       = da1["pgrad"   ][i]
  #    nowpos      = da1["nowpos"  ][i]
  #    time        = da1["time"    ][i]
  #    oVar        = da1[varname][i]
  #    #---- dura -------
  #    if dura < thdura:
  #      #print "dura",dura,"<",thdura
  #      continue
  #    #---- thpgrad ----
  #    if pgrad < thpgrad:
  #      #print "pgrad",pgrad,"<",thpgrad
  #      continue
  #
  #    #---- time -------
  #    Year,Mon,Day,Hour = solve_time(time)
  #    DTime             = datetime(Year,Mon,Day,Hour)
  #
  #    #---- nowpos  ----
  #    x,y               = fortpos2pyxy(nowpos, self.nx, -9999)


  #    #-- check TC ----
  #    lxyTC  = expand8grids(dictTC[DTime], self.ny, self.nx)
  #    if [x,y] in lxyTC:
  #      continue 
 
  #    #-- List  -------
  #    oList  = [x,y,oVar] 


  #    try:
  #      dictExC[DTime].append(oList)
  #    except KeyError:
  #      dictExC[DTime] = [oList]
  #  #--------------------------------------------
  #  self.dictTC  = dictTC
  #  self.dictExC = dictExC
  #  return self


  def mkInstDictC_bstTC(self, iYM, eYM, varname="pgrad"):
    thpgrad   = self.thpgrad
    thdura    = self.thdura

    dictExC   = {}
    dictTC    = {}
    da1       = {}

    iYear,iMon= iYM
    eYear,eMon= eYM
    lYM       = ret_lYM(iYM, eYM)

    #--- TC dictionary ----
    bst       = BestTrackTC.BestTrack("IBTrACS")
    for Year in range(iYear,eYear+1):
      dictTC.update(bst.ret_dpyxy(Year, self.Lon, self.Lat))

    #---- make ExC dictionary -----
    lvar      = ["dura","pgrad","nowpos","time"]
    for Year,Mon in lYM:
      for var in lvar:
         da1[var]  = self.load_clist(var, Year, Mon)
  
      dtcloc   = {}
      nlist    = len(da1["dura"])
  
      for i in range(nlist):
        dura        = da1["dura"    ][i]
        pgrad       = da1["pgrad"   ][i]
        nowpos      = da1["nowpos"  ][i]
        time        = da1["time"    ][i]
        oVar        = da1[varname][i]
        #---- dura -------
        if dura < thdura:
          #print "dura",dura,"<",thdura
          continue
        #---- thpgrad ----
        if pgrad < thpgrad:
          #print "pgrad",pgrad,"<",thpgrad
          continue
    
        #---- time -------
        Year,Mon,Day,Hour = solve_time(time)
        DTime             = datetime(Year,Mon,Day,Hour)
    
        #---- nowpos  ----
        x,y               = fortpos2pyxy(nowpos, self.nx, -9999)
  
  
        #-- check TC ----
        lxyTC  = expand8grids(dictTC[DTime], self.ny, self.nx)
        if [x,y] in lxyTC:
          continue 
   
        #-- List  -------
        oList  = [x,y,oVar] 
  
  
        try:
          dictExC[DTime].append(oList)
        except KeyError:
          dictExC[DTime] = [oList]
    #--------------------------------------------
    self.dictTC  = dictTC
    self.dictExC = dictExC
    return self


  def mkInstDictC_objTC(self, iYM, eYM, varname="pgrad"):
    thrvort   = self.thrvort
    thpgrad   = self.thpgrad
    thwcore   = self.thwcore
    thdura    = self.thdura
    thinitsst = self.thsst 

    dictExC   = {}
    dictTC    = {}
    da1       = {}

    #lvar      = ["dura","pgrad","nowpos","nextpos","time","iedist","rvort","dtlow","dtmid","dtup","initsst","initland"]
    lvar      = ["dura","pgrad","nowpos","time","rvort","dtlow","dtmid","dtup","initsst","initland"]


    lYM       = ret_lYM(iYM, eYM)
    for Year,Mon in lYM:
      for var in lvar:
         da1[var]  = self.load_clist(var, Year, Mon)
    
      #---- make dictionary -----
      dtcloc   = {}
      nlist    = len(da1["dura"])
      for i in range(nlist):
        dura        = da1["dura"    ][i]
        pgrad       = da1["pgrad"   ][i]
        nowpos      = da1["nowpos"  ][i]
        time        = da1["time"    ][i]
        #iedist      = da1["iedist"  ][i]
        rvort       = abs(da1["rvort"   ][i])
        dtlow       = da1["dtlow"   ][i]
        dtmid       = da1["dtmid"   ][i]
        dtup        = da1["dtup"    ][i]
        initsst     = da1["initsst" ][i]
        initland    = da1["initland"][i]
        #nextpos     = da1["nextpos" ][i]
  
        oVar        = da1[varname][i]
        #---- dura -------
        if dura < thdura:
          #print "dura",dura,"<",thdura
          continue
        #---- thpgrad ----
        if pgrad < thpgrad:
          #print "pgrad",pgrad,"<",thpgrad
          continue
    
        #---- time -------
        Year,Mon,Day,Hour = solve_time(time)
        DTime             = datetime(Year,Mon,Day,Hour)
    
        #---- nowpos  ----
        x,y               = fortpos2pyxy(nowpos, self.nx, -9999)
    
        #-- List  -------
        oList  = [x,y,oVar] 
  
        #---- thrvort ----
        if rvort < thrvort:
          #print "rvort",rvort,"<",thrvort
          try:
            dictExC[DTime].append(oList)
          except KeyError:
            dictExC[DTime] = [oList]
    
          continue
    
        #---- thwcore ----
        if dtup + dtmid + dtlow < thwcore:
          #print "thwcore",dtup+dtmid+dtlow,"<",thwcore
          try:
            dictExC[DTime].append(oList)
          except KeyError:
            dictExC[DTime] = [oList]
    
          continue
    
        #---- initsst ----
        if initsst < thinitsst:
          #print "initsst",initsst,"<",thinitsst
          try:
            dictExC[DTime].append(oList)
          except KeyError:
            dictExC[DTime] = [oList]
    
          continue
    
        #---- initland ----
        if initland > 0.0:
          #print "initland",initland,">",0.0
          try:
            dictExC[DTime].append(oList)
          except KeyError:
            dictExC[DTime] = [oList]
    
          continue
    
        #---- TC ----
        try:
          dictTC[DTime].append(oList)
        except KeyError:
          dictTC[DTime] = [oList]
  
      #---- fill blank dates ----
      iDay = 1
      eDay = calendar.monthrange(Year,Mon)[1]
      lDay = range(iDay,eDay+1)
      lHour= [0,6,12,18]
      for Day, Hour in [[Day,Hour] for Day in lDay for Hour in lHour]:
        DTime = datetime(Year,Mon,Day,Hour)
        if not dictExC.has_key(DTime):
          dictExC[DTime] = []
        if not dictTC.has_key(DTime):
          dictTC[DTime]  = []
  
    #--------------------------------------------
    self.dictTC  = dictTC
    self.dictExC = dictExC
    return self



  #def dictC_objTC(self, Year, Mon, varname="pgrad"):
  #  thrvort   = self.thrvort
  #  thpgrad   = self.thpgrad
  #  thwcore   = self.thwcore
  #  thdura    = self.thdura
  #  thinitsst = self.thsst 

  #  dictExC   = {}
  #  dictTC    = {}
  #  da1       = {}

  #  #lvar      = ["dura","pgrad","nowpos","nextpos","time","iedist","rvort","dtlow","dtmid","dtup","initsst","initland"]
  #  lvar      = ["dura","pgrad","nowpos","time","rvort","dtlow","dtmid","dtup","initsst","initland"]
  #  for var in lvar:
  #     da1[var]  = self.load_clist(var, Year, Mon)
  #
  #  #---- make dictionary -----
  #  dtcloc   = {}
  #  nlist    = len(da1["dura"])
  #  for i in range(nlist):
  #    dura        = da1["dura"    ][i]
  #    pgrad       = da1["pgrad"   ][i]
  #    nowpos      = da1["nowpos"  ][i]
  #    time        = da1["time"    ][i]
  #    #iedist      = da1["iedist"  ][i]
  #    rvort       = abs(da1["rvort"   ][i])
  #    dtlow       = da1["dtlow"   ][i]
  #    dtmid       = da1["dtmid"   ][i]
  #    dtup        = da1["dtup"    ][i]
  #    initsst     = da1["initsst" ][i]
  #    initland    = da1["initland"][i]
  #    #nextpos     = da1["nextpos" ][i]

  #    oVar        = da1[varname][i]
  #    #---- dura -------
  #    if dura < thdura:
  #      #print "dura",dura,"<",thdura
  #      continue
  #    #---- thpgrad ----
  #    if pgrad < thpgrad:
  #      #print "pgrad",pgrad,"<",thpgrad
  #      continue
  #
  #    #---- time -------
  #    Year,Mon,Day,Hour = solve_time(time)
  #    DTime             = datetime(Year,Mon,Day,Hour)
  #
  #    #---- nowpos  ----
  #    x,y               = fortpos2pyxy(nowpos, self.nx, -9999)
  #
  #    #-- List  -------
  #    oList  = [x,y,oVar] 

  #    #---- thrvort ----
  #    if rvort < thrvort:
  #      #print "rvort",rvort,"<",thrvort
  #      try:
  #        dictExC[DTime].append(oList)
  #      except KeyError:
  #        dictExC[DTime] = [oList]
  #
  #      continue
  #
  #    #---- thwcore ----
  #    if dtup + dtmid + dtlow < thwcore:
  #      #print "thwcore",dtup+dtmid+dtlow,"<",thwcore
  #      try:
  #        dictExC[DTime].append(oList)
  #      except KeyError:
  #        dictExC[DTime] = [oList]
  #
  #      continue
  #
  #    #---- initsst ----
  #    if initsst < thinitsst:
  #      #print "initsst",initsst,"<",thinitsst
  #      try:
  #        dictExC[DTime].append(oList)
  #      except KeyError:
  #        dictExC[DTime] = [oList]
  #
  #      continue
  #
  #    #---- initland ----
  #    if initland > 0.0:
  #      #print "initland",initland,">",0.0
  #      try:
  #        dictExC[DTime].append(oList)
  #      except KeyError:
  #        dictExC[DTime] = [oList]
  #
  #      continue
  #
  #    #---- TC ----
  #    try:
  #      dictTC[DTime].append(oList)
  #    except KeyError:
  #      dictTC[DTime] = [oList]

  #  #---- fill blank dates ----
  #  iDay = 1
  #  eDay = calendar.monthrange(Year,Mon)[1]
  #  lDay = range(iDay,eDay+1)
  #  lHour= [0,6,12,18]
  #  for Day, Hour in [[Day,Hour] for Day in lDay for Hour in lHour]:
  #    DTime = datetime(Year,Mon,Day,Hour)
  #    if not dictExC.has_key(DTime):
  #      dictExC[DTime] = []
  #    if not dictTC.has_key(DTime):
  #      dictTC[DTime]  = []

  #  #--------------------------------------------
  #  self.dictTC  = dictTC
  #  self.dictExC = dictExC
  #  return self


class Cyclone_2D(Cyclone):
  #def __init__(self, Year, Mon, model="JRA55", res="bn", tctype="bst",miss=-9999.):
  #  Cyclone.__init__(self, model=model, res=res)
  #  self.instDict  = self.dictC(Year, Mon, varname="pgrad",tctype=tctype)
  #  self.a2miss    = ones([self.ny, self.nx], float32)*miss
  #  self.miss      = miss
  #  self.tctype    = tctype
  #  self.res       = res

  def __init__(self, iYM, eYM, model="JRA55", res="bn", tctype="bst",miss=-9999.):
    Cyclone.__init__(self, model=model, res=res)
    self.instDict  = self.mkInstDictC(iYM, eYM, varname="pgrad",tctype=tctype)
    self.a2miss    = ones([self.ny, self.nx], float32)*miss
    self.miss      = miss
    self.tctype    = tctype
    self.res       = res

  def mk_a2tc(self, DTime):
    if len(self.instDict.dictTC[DTime]) >0:
      aList     = zip(*array(self.instDict.dictTC[DTime]))
      a2dat     = self.a2miss.copy()
      a2dat[ aList[1], aList[0]] = aList[-1]
    else:
      a2dat     = self.a2miss.copy()
    return a2dat

  def mk_a2exc(self, DTime):
    if len(self.instDict.dictExC[DTime]) >0:
      aList     = zip(*array(self.instDict.dictExC[DTime]))
      a2dat     = self.a2miss.copy()
      a2dat[ aList[1], aList[0]] = aList[-1]
    else:
      a2dat     = a2miss.copy()
    return a2dat

  def mkMask_exc(self, DTime, radkm=1000, miss=False):
    if type(miss) == bool: miss=self.miss

    a2loc     = self.mk_a2exc(DTime)
    return detect_fsub.mk_territory(a2loc.T, self.Lon, self.Lat, radkm*1000., imiss=self.miss, omiss=miss).T

  def mkMask_tc(self, DTime, radkm=1000, miss=False):
    if type(miss) == bool: miss=self.miss
    a2loc     = self.mk_a2tc(DTime)
    return detect_fsub.mk_territory(a2loc.T, self.Lon, self.Lat, radkm*1000., imiss=self.miss, omiss=miss).T

  def path_exc(self, DTime):
    Year    = DTime.year
    Mon     = DTime.month
    Day     = DTime.day
    Hour    = DTime.hour
    srcDir  = os.path.join(self.baseDir, self.tstep, "exc.%stc"%(self.tctype), "%04d"%(Year), "%02d"%(Mon))
    srcPath = os.path.join(srcDir, "%s.%04d%02d%02d%02d.%s"%("exc",Year,Mon,Day,Hour,self.res))

    return srcDir, srcPath

  def path_tc(self, DTime):
    Year    = DTime.year
    Mon     = DTime.month
    Day     = DTime.day
    Hour    = DTime.hour

    srcDir  = os.path.join(self.baseDir, self.tstep, "tc.%s"%(self.tctype), "%04d"%(Year), "%02d"%(Mon))
    srcPath = os.path.join(srcDir, "%s.%04d%02d%02d%02d.%s"%("tc",Year,Mon,Day,Hour,self.res))
    return srcDir, srcPath

  def path_Mask_exc(self, DTime, radkm=1000):
    Year    = DTime.year
    Mon     = DTime.month
    Day     = DTime.day
    Hour    = DTime.hour

    srcDir  = os.path.join(self.baseDir, self.tstep, "mask.exc.%stc"%(self.tctype), "%04d"%(Year), "%02d"%(Mon))
    srcPath = os.path.join(srcDir, "%s.%04dkm.%04d%02d%02d%02d.%s"%("exc",radkm,Year,Mon,Day,Hour,self.res))
    return srcDir, srcPath

  def path_Mask_tc(self, DTime, radkm=1000):
    Year    = DTime.year
    Mon     = DTime.month
    Day     = DTime.day
    Hour    = DTime.hour

    srcDir  = os.path.join(self.baseDir, self.tstep, "mask.tc.%s"%(self.tctype), "%04d"%(Year), "%02d"%(Mon))
    srcPath = os.path.join(srcDir, "%s.%04dkm.%04d%02d%02d%02d.%s"%("tc",radkm,Year,Mon,Day,Hour,self.res))
    return srcDir, srcPath


