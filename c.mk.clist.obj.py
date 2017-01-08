from numpy import *
from detect_fsub import *
from datetime import datetime, timedelta
import util
import config_func
import IO_Master
import Cyclone
import calendar
import detect_func
import collections
#-----------------------------------------
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

#iDTime = datetime(2006,1,1,6)
#eDTime = datetime(2006,1,31,18)
#iDTime = datetime(2004,1,4,0)
#eDTime = datetime(2004,1,18,18)
iDTime = datetime(2001,1,1,0)
eDTime = datetime(2015,8,31,18)

dDTime = timedelta(hours=6)

ret_lDTime = {False: util.ret_lDTime
             ,True : util.ret_lDTime_noleap
             }[noleap]

lDTime   = ret_lDTime(iDTime, eDTime, dDTime)

miss   = -9999.0
miss_int = -9999

cfg    = config_func.config_func(prj, model, run)
iom    = IO_Master.IO_Master(prj, model, run, res)
cy     = Cyclone.Cyclone(cfg)

#*********** functions *********
def ret_a1iedist(a1ipos, a1epos):
  miss     = -9999.
  a1nx   = ones(len(a1ipos))*nx
  a1miss = ones(len(a1ipos))*miss_int
  lixy   = array(map(detect_func.fortpos2pyxy, a1ipos, a1nx, a1miss))
  lexy   = array(map(detect_func.fortpos2pyxy, a1epos, a1nx, a1miss))

  a1ix     = array(lixy[:,0], int32)
  a1iy     = array(lixy[:,1], int32)
  a1ex     = array(lexy[:,0], int32)
  a1ey     = array(lexy[:,1], int32)

  a1ilon   = a1lon.take(ma.masked_equal(a1ix, miss_int).filled(0))
  a1elon   = a1lon.take(ma.masked_equal(a1ex, miss_int).filled(0))
  a1ilat   = a1lat.take(ma.masked_equal(a1iy, miss_int).filled(0))
  a1elat   = a1lat.take(ma.masked_equal(a1ey, miss_int).filled(0))

  a1ilon   = ma.masked_where(a1ix==miss_int, a1ilon).filled(miss)
  a1elon   = ma.masked_where(a1ex==miss_int, a1elon).filled(miss)
  a1ilat   = ma.masked_where(a1iy==miss_int, a1ilat).filled(miss)
  a1elat   = ma.masked_where(a1ey==miss_int, a1elat).filled(miss)

  liedist  = map(detect_fsub.hubeny_real, a1ilat, a1ilon, a1elat, a1elon)# m
  a1iedist = array(liedist, float32)/1000.0
  a1iedist = ma.masked_invalid(a1iedist).filled(miss)
  return a1iedist

#********************************
a1lat    = iom.Lat
a1lon    = iom.Lon
a2lon, a2lat = meshgrid(a1lon, a1lat)
ny       = iom.ny
nx       = iom.nx
#---------
plev_low = 850*100.0 # (Pa)
plev_mid = 500*100.0 # (Pa)
plev_up  = 250*100.0 # (Pa)
#--- a2pos ---------------------
# pos = 1,2,3,4,....
a2nowpos  = array(arange( ny*nx).reshape(ny,nx), int32) + 1

#-----------------------------------------
for idt, DTime in enumerate(lDTime):
  #******* init **********
  year = DTime.year
  mon  = DTime.month
  day  = DTime.day
  hour = DTime.hour
  if ((idt==0)or(DTime.month != lDTime[idt-1].month)):
    print DTime.year, DTime.month
    a2num  = zeros([ny,nx],float32).reshape(ny,nx)
    #--------------
    #lstype  = ["rvort","dtlow","dtmid","dtup","wmeanlow","wmeanup","wmaxlow","dura","pgrad","sst","lat","lon","ipos","idate","nowpos","time","prepos","nextpos"]
    lstype_ex  = ["dura","pgrad","vortlw","lat","lon","ipos","epos","idate","nowpos","time","prepos","nextpos"]
    #lstype_tc  = ["rvort","dtlow","dtmid","dtup","wmeanlow","wmeanup","wmaxlow","sst"]
    da1     = {}

    #for stype in lstype_ex + lstype_tc:
    for stype in lstype_ex:
      #if stype in ["dura","ipos","idate","nowpos","time","prepos","nextpos"]:
      #  da1[stype] = array([],int32  )
      #else:
      #  da1[stype] = array([],float32)
      da1[stype] = collections.deque([])
  #-------------
  a2pgrad         =cy.load_a2dat("pgrad"  ,DTime) 
  a2vortlw        =cy.load_a2dat("vortlw" ,DTime) 
  a2dura          =cy.load_a2dat("dura"   ,DTime) 
  a2ipos          =cy.load_a2dat("ipos"   ,DTime) 
  a2epos          =cy.load_a2dat("epos"   ,DTime) 
  a2idate         =cy.load_a2dat("idate"  ,DTime) 
  a2prepos        =cy.load_a2dat("prepos",DTime) 
  a2nextpos       =cy.load_a2dat("nextpos",DTime) 

  #a2dura          = detect_fsub.solvelife_dura(a2life.T, miss_int).T 
  #---- shrink ---------------------
  a1dura_tmp      = ma.masked_where( a2pgrad==miss, a2dura     ).compressed()
  a1dura_tmp      = array(a1dura_tmp, int32)

  a1pgrad_tmp     = ma.masked_where( a2pgrad==miss, a2pgrad    ).compressed()
  a1vortlw_tmp    = ma.masked_where( a2pgrad==miss, a2vortlw   ).compressed()
  a1lat_tmp       = ma.masked_where( a2pgrad==miss, a2lat      ).compressed()
  a1lon_tmp       = ma.masked_where( a2pgrad==miss, a2lon      ).compressed()
  a1ipos_tmp      = ma.masked_where( a2pgrad==miss, a2ipos     ).compressed()
  a1epos_tmp      = ma.masked_where( a2pgrad==miss, a2epos     ).compressed()
  a1idate_tmp     = ma.masked_where( a2pgrad==miss, a2idate    ).compressed()
  a1nowpos_tmp    = ma.masked_where( a2pgrad==miss, a2nowpos   ).compressed()
  a1prepos_tmp   = ma.masked_where( a2pgrad==miss, a2prepos  ).compressed()
  a1nextpos_tmp   = ma.masked_where( a2pgrad==miss, a2nextpos  ).compressed()
  #--- a1time ------
  time            = year*10**6 + mon*10**4 + day*10**2 + hour
  a1time_tmp      = ones( len(a1pgrad_tmp) ,int32) *time

  #-----------------
  da1["dura"    ].extend( a1dura_tmp     )
  da1["pgrad"   ].extend( a1pgrad_tmp    )
  da1["vortlw"  ].extend( a1vortlw_tmp   )
  da1["lat"     ].extend( a1lat_tmp      )
  da1["lon"     ].extend( a1lon_tmp      )
  da1["ipos"    ].extend( a1ipos_tmp     )
  da1["epos"    ].extend( a1epos_tmp     )
  da1["idate"   ].extend( a1idate_tmp    )
  da1["nowpos"  ].extend( a1nowpos_tmp   )
  da1["time"    ].extend( a1time_tmp     )
  da1["prepos" ].extend( a1prepos_tmp    )
  da1["nextpos" ].extend( a1nextpos_tmp  )


  if ((DTime==lDTime[-1])or(DTime.month != lDTime[idt+1].month)):
    ##---- iedist ------------------------
    da1["iedist"] = ret_a1iedist(da1["ipos"], da1["epos"])
  
    #----- make dir ----
    sodir  = cy.path_clist("ipos", year, mon)[0]
    detect_func.mk_dir(sodir)
  
    #---- save --
    _lstype = lstype_ex + ["iedist"]
    #_lstype = lstype_ex
    
    for stype in _lstype:
      soname = cy.path_clist(stype, year, mon)[1]
      
      if stype in ["dura","ipos","epos","idate","nowpos","time","prepos","nextpos"]:
        a1out = array( da1[stype] ,int32   )
      else:
        a1out = array( da1[stype] ,float32 )
  
      a1out.tofile(soname)
      print soname
  
