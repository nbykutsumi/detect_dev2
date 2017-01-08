from numpy import *
from detect_fsub import *
from datetime import datetime
from collections import deque
import Reanalysis
import IBTrACS
import util_para
import calendar
import detect_func
#*******************************************
#iyear     = 1980
#eyear     = 1999
iYear     = 2004
eYear     = 2004
lMon      = [1,2,3,4,5,6,7,8,9,10,11,12]
#lMon      = [1]
lHour     = [0,6,12,18]
lmodel    = ["JRA55"]
res       = "bn"
lregion = ["GLB","PNW", "PNE","INN","INS", "PSW","ATN"]
#lregion   = ["GLB"]
miss      = -9999.0
ver       = "v03r06"
odir      = "/media/disk2/out/obj.valid"
tstep     = "6hr"
#------------------
def ret_dvarname(model):
  if   model in ["JRA25"]:
    return {"ua":"UGRD", "va":"VGRD", "ta":"TMP","sst":"WTMPsfc"}
  elif model in ["JRA55"]:
    return {"ua":"ugrd", "va":"vgrd", "ta":"tmp","sst":"BRTMP"}


def save_csv(var, ldat):
  """
  var: rvort, dt, wmeanlow, wmeanup
  """
  ldat   = sort(ldat)
  lendat = len(ldat)

  dunit  = {"rvort":"s-1",
            "dt"   :"K",
            "wLow_Up":"m/s"
           }

  sout = "frac/%s(%s),%s\n"%(model,var,dunit[var])
  for i,dat in enumerate(ldat):
    frac = (i+1)/float(lendat)
    sout = sout + "%f,%f\n"%(frac,dat)

  #
  odir   = "/media/disk2/out/obj.valid/tc.%s/%s"%(var, region)
  detect_func.mk_dir(odir)
  oname  = odir + "/%s.%s.%04d-%04d.%s.csv"%(var,model,iYear,eYear,region)

  f = open(oname,"w");  f.write(sout);  f.close()
  print oname
#------------------
def positive_lon(lon):
  if lon <0.0:
    positive_lon = 360 + lon
  else:
    positive_lon = lon
  #
  return positive_lon
#------------------
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

#------------------
for model in lmodel:
  ra     = Reanalysis.Reanalysis(model=model,res=res)
  a1lon  = ra.Lon
  a1lat  = ra.Lat
  nx     = ra.nx
  ny     = ra.ny
  dvarname = ret_dvarname(model)
  var_ta   = dvarname["ta"]
  var_va   = dvarname["va"]
  var_ua   = dvarname["ua"]

  bst  = IBTrACS.ibtracs()
  #-------------------
  for region in lregion:
    #-- region mask ---
    lllat, lllon, urlat, urlon = util_para.ret_tcregionlatlon(region)
    BBox = [[lllat,lllon],[urlat,urlon]]
    a2domain  = ret_a2domain(BBox, a1lat, a1lon)

    #--- initialize ----
    lrvort    = deque([])
    ldt       = deque([])
    lwLow_Up  = []
  
    #------------------
    for Year in range(iYear, eYear+1):
      print region, Year
      #-- load Best Track Data --
      dpyxy  = bst.ret_dpyxy(Year, a1lon, a1lat, ver=ver)
      #--------------------------
      for Mon in lMon:
        eDay = calendar.monthrange(Year,Mon)[1]
        lDay = arange(1, eDay+1)
        for Day,Hour in [[Day,Hour] for Day in lDay for Hour in lHour]:
          lpyxy = dpyxy[(Year,Mon,Day,Hour)]

          if len(lpyxy) == 0:
            continue

          DTime = datetime(Year,Mon,Day,Hour)
          #*************************************
          #------  for check psl minima ---
          a2psl   = ra.load_6hr("PRMSL",DTime).Data
          findcyclone_out = detect_fsub.findcyclone_bn(a2psl.T, a1lat, a1lon, -9999.0, miss)
          a2pgrad = findcyclone_out.T
          #-------------------------------------

          a2tlow  = ra.load_6hr(var_ta ,DTime, lev=850).Data
          a2tmid  = ra.load_6hr(var_ta ,DTime, lev=500).Data
          a2tup   = ra.load_6hr(var_ta ,DTime, lev=250).Data
          a2ulow  = ra.load_6hr(var_ua ,DTime, lev=850).Data
          a2vlow  = ra.load_6hr(var_ua ,DTime, lev=850).Data
          a2uup   = ra.load_6hr(var_va ,DTime, lev=250).Data
          a2vup   = ra.load_6hr(var_va ,DTime, lev=250).Data
          #
          a2pos   = ones([ny,nx],float32)*miss
          for pyxy in lpyxy:
            ix,iy   = pyxy
            if a2pgrad[iy,ix] ==miss:
              continue
             
            a2pos[iy,ix] = 1.0

          #-- calc tc parameters ----
          tout = detect_fsub.calc_tcvar\
                (  a2pos.T, a2tlow.T, a2tmid.T, a2tup.T\
                 , a2ulow.T, a2uup.T, a2vlow.T, a2vup.T\
                 , a1lon, a1lat\
                 , miss\
                ) 

          a2rvort    = tout[0].T
          a2dtlow    = tout[1].T
          a2dtmid    = tout[2].T
          a2dtup     = tout[3].T
          a2wmeanlow = tout[4].T
          a2wmeanup  = tout[5].T

          a2dt       = a2dtlow + a2dtmid + a2dtup
          a2dt       = ma.masked_where(a2pos==miss, a2dt).filled(miss)

          a2wLow_Up  = a2wmeanlow - a2wmeanup
          a2wLow_Up  = ma.masked_where(a2wmeanlow==miss, a2wLow_Up).filled(miss)

          lrvort_    = deque(ma.masked_equal(a2rvort   ,miss).compressed())
          ldt_       = deque(ma.masked_equal(a2dt      ,miss).compressed())
          lwLow_Up_  = deque(ma.masked_equal(a2wLow_Up ,miss).compressed())

          lrvort   .extend(lrvort_  ) 
          ldt      .extend(ldt_     ) 
          lwLow_Up .extend(lwLow_Up_) 
          
    #- abs rvort ---------
    lrvort  = map(abs, lrvort)
    #- save --------------
    save_csv("rvort"  ,lrvort)
    save_csv("dt"     ,ldt)
    save_csv("wLow_Up",lwLow_Up)


