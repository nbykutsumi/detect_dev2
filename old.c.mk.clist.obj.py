from numpy import *
from detect_fsub import *
from datetime import datetime
import Reanalysis
import Cyclone
import calendar
import detect_func
#import ctrack_para
#import ctrack_func
#import tc_para
import collections
#-----------------------------------------
#singleday= True
singleday = False

#iyear  = 1990
#eyear  = 2014
#lmon   = [1,2,3,4,5,6,7,8,9,10,11,12]

iyear  = 2015
eyear  = 2015
lmon   = [1]
iday   = 1
lhour  = [0,6,12,18]
miss   = -9999.0
miss_int = -9999

prj    = "JRA55"
lmodel = [prj]
run    = ""
res    = "bn"


#--- a2lat, a2lon --------------
#*********** functions *********
def ret_var_ta(model):
  if model in ["JRA55"]:
    return "tmp"
  elif model in ["JRA25"]:
    return "TMP"

def ret_var_ua(model):
  if model in ["JRA55"]:
    return "UGRD"
  elif model in ["JRA25"]:
    return "ugrd"

def ret_var_va(model):
  if model in ["JRA55"]:
    return "VGRD"
  elif model in ["JRA25"]:
    return "vgrd"

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
#---------------------------
for model in lmodel:
  #---------
  ra       = Reanalysis.Reanalysis(model=model,res=res)
  cy       = Cyclone.Cyclone(model=model,res=res)

  a1lat    = ra.Lat
  a1lon    = ra.Lon
  a2lon, a2lat = meshgrid(a1lon, a1lat)
  ny       = ra.ny
  nx       = ra.nx
  #---------
  var_ta   = ret_var_ta(model)
  var_ua   = ret_var_ua(model)
  var_va   = ret_var_va(model)
  #---------
  plev_low = 850*100.0 # (Pa)
  plev_mid = 500*100.0 # (Pa)
  plev_up  = 250*100.0 # (Pa)
  #--- a2pos ---------------------
  # pos = 1,2,3,4,....
  a2nowpos  = array(arange( ny*nx).reshape(ny,nx), int32) + 1
 
  #-----------------------------------------
  for year in range(iyear,eyear+1):
    for mon in lmon:
      #----------
      if singleday == True:
        eday = iday
      else:
        eday = calendar.monthrange(year,mon)[1]
      #******* init **********
      a2num  = zeros([ny,nx],float32).reshape(ny,nx)
      #--------------
      #lstype  = ["rvort","dtlow","dtmid","dtup","wmeanlow","wmeanup","wmaxlow","dura","pgrad","sst","lat","lon","ipos","idate","nowpos","time","prepos","nextpos"]
      lstype_ex  = ["dura","pgrad","lat","lon","ipos","epos","idate","nowpos","time","prepos","nextpos"]
      lstype_tc  = ["rvort","dtlow","dtmid","dtup","wmeanlow","wmeanup","wmaxlow","sst"]
      da1     = {}
      for stype in lstype_ex + lstype_tc:
        #if stype in ["dura","ipos","idate","nowpos","time","prepos","nextpos"]:
        #  da1[stype] = array([],int32  )
        #else:
        #  da1[stype] = array([],float32)
        da1[stype] = collections.deque([])
      ###############
      ##  SST
      ##-------------
      #sstdir   = sstdir_root + "/%04d"%(year)
      #sstname  = sstdir + "/fcst_phy2m.WTMPsfc.%04d%02d.bn"%(year,mon)
      #a2sst    = fromfile( sstname, float32).reshape(ny,nx)
      #-------------
      for day in range(iday, eday+1):
        print year, mon, day
        for hour in lhour:
          DTime  = datetime(year,mon,day,hour)
          a2pgrad         =cy.load_a2dat("pgrad"  ,DTime) 
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
          da1["lat"     ].extend( a1lat_tmp      )
          da1["lon"     ].extend( a1lon_tmp      )
          da1["ipos"    ].extend( a1ipos_tmp     )
          da1["epos"    ].extend( a1epos_tmp     )
          da1["idate"   ].extend( a1idate_tmp    )
          da1["nowpos"  ].extend( a1nowpos_tmp   )
          da1["time"    ].extend( a1time_tmp     )
          da1["prepos" ].extend( a1prepos_tmp  )
          da1["nextpos" ].extend( a1nextpos_tmp  )


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
        if stype == "rvort": print soname

