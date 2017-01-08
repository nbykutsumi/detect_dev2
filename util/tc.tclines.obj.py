from mpl_toolkits.basemap import Basemap
from collections import deque
import matplotlib.pyplot as plt
from numpy import *
from datetime import datetime
import socket
import calendar
import sys, os
import util
import config_func
import Cyclone
import util_para
import detect_func
#--------------------------------------
iyear = 2004
eyear = 2004
lyear = range(iyear,eyear+1)
lseason = ["ALL"]
#lseason = [2]

prj     = "JRA55"
model   = "__"
run     = "__"
res     = "145x288"

#prj     = "HAPPI"
#model   = "MIROC5"
#run     = "C20-ALL-001"
#res     = "128x256"

region= "GLOB"
#singleday = True
singleday = False
#unitdist  = 20.0 # km / hour
unitdist  = 0.0 # km / hour  # test
cfg     = config_func.config_func(prj=prj, model=model, run=run)
cy      = Cyclone.Cyclone(cfg=cfg)
a1lat   = cy.Lat
a1lon   = cy.Lon
ny      = cy.ny
nx      = cy.nx


thrvort   = cy.tcrvort
thpgrad   = cy.thpgrad
thwcore   = cy.thwcore
thdura    = cy.thdura
thinitsst = cy.thsst

lonlatfontsize = 10.0
#lonrotation    = 90
lonrotation    = 0
miss_int= -9999

#*************************************
# FUNCTION
#*************************************
def mk_dtcloc(year,mon):
  da1       = {}
  lstype  = ["dura","pgrad","nowpos","nextpos","time","iedist","vortlw","dtlow","dtmid","dtup","initsst","initland"]
  for stype in lstype:
     da1[stype]  = cy.load_clist(stype, year, mon)

  #**** make dictionary ***
  stepflag = 0
  dtcloc   = {}
  nlist    = len(da1["dura"])
  for i in range(nlist):
    dura        = da1["dura"    ][i]
    pgrad       = da1["pgrad"   ][i]
    nowpos      = da1["nowpos"  ][i]
    time        = da1["time"    ][i]
    iedist      = da1["iedist"  ][i]
    #rvort       = abs(da1["rvort"   ][i])
    rvort       = da1["vortlw"  ][i]
    dtlow       = da1["dtlow"   ][i]
    dtmid       = da1["dtmid"   ][i]
    dtup        = da1["dtup"    ][i]
    initsst     = da1["initsst" ][i]
    initland    = da1["initland"][i]
    nextpos     = da1["nextpos" ][i]
    #---- check time ----
    ### This section should be prior to the condition filtering

    if (i == nlist-1):
      stepflag = 1
    else:
      timenext    = da1["time"][i+1]
      if (timenext != time):
        stepflag = 1

    #---- dura -------
    if dura < thdura:
      #print "dura",dura,"<",thdura
      continue
    ##---- thpgrad ----
    #if pgrad < thpgrad:
    #  #print "pgrad",pgrad,"<",thpgrad
    #  continue

    #---- thrvort ----
    if rvort < thrvort:
      #print "rvort",rvort,"<",thrvort
      continue

    #---- thwcore ----
    if dtup + dtmid + dtlow < thwcore:
      #print "thwcore",dtup+dtmid+dtlow,"<",thwcore
      continue

    #---- initsst ----
    if initsst < thinitsst:
      #print "initsst",initsst,"<",thinitsst
      continue 

    #---- initland ----
    if initland > 0.0:
      #print "initland",initland,">",0.0
      continue 


#    #---- iedist -----
#    if iedist < dura*unitdist:
#      #print "iedist",iedist,"<",dura*unitdist
#      continue

    #---- time ------
    yeart,mont,dayt,hourt = detect_func.solve_time(time)

    #---- location --
    ix, iy            = detect_func.fortpos2pyxy( nowpos, nx, -9999)

    #---- dictionary --
    if dtcloc.has_key((dayt,hourt)):
      dtcloc[dayt,hourt].append([ix,iy,nextpos])
    else:
      dtcloc[dayt,hourt] = [[ix,iy, nextpos]]
  #------------------
  return dtcloc

#************************************
#************************************
ltrack     = deque([])
#------------------------------------
##############
for season in lseason:
  for year in lyear:
    lmon = util.ret_lmon(season)
    for mon in lmon:
      print year,mon   
      dtcloc =  mk_dtcloc(year,mon)
      #--------
      iday = 1
      eday = calendar.monthrange(year,mon)[1]
      #--------
      for day in range(iday, eday+1):
        print "tracklines",model,year, mon, day
        for hour in [0, 6, 12, 18]:
          #---------------------------
          print year,mon,day,"eday=",eday
          DTime  = datetime(year,mon,day,hour)
  
          #-- check exc existence ----
          if not dtcloc.has_key((day,hour)):
            continue
          #---------------------------
          ldat    = dtcloc[day,hour]
          for locdat in ldat:
            ix,iy,nextpos = locdat
      
            #-- nextpos ------------
            x_next, y_next = detect_func.fortpos2pyxy(nextpos, nx, miss_int)
      
            if ( (x_next == miss_int) & (y_next == miss_int) ):
              continue            
            #-----------------------
            lat       = a1lat[iy]
            lon       = a1lon[ix]
      
            lat_next  = a1lat[y_next]
            lon_next  = a1lon[x_next]
            #
            ltrack.append([[year, mon, day, hour],[lat, lon, lat_next, lon_next]])
      
      
  ##*************\***********
  # Basemap
  #------------------------
  lllat, lllon, urlat, urlon = util_para.ret_tcregionlatlon(region)
  print "Basemap"
  figmap   = plt.figure()
  axmap    = figmap.add_axes([0.1, 0.1, 0.8, 0.8])
  M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
  
  #-- draw cyclone tracks ------
  itemp = 1
  #-----------
  for track in ltrack:
    itemp = itemp + 1
    year = track[0][0]
    mon  = track[0][1]
    day  = track[0][2]
    hour = track[0][3]
  
    lat1 = track[1][0]
    lon1 = track[1][1]
    lat2 = track[1][2]
    lon2 = track[1][3]
  
    #---- check region ----------
    if ((lat1 < lllat) or (urlat < lat1)):
      continue
    if ((lon1 < lllon) or (urlon < lon1)):
      continue
    #--------------
    scol="r"
  
    #------------------------------------
    if abs(lon1 - lon2) >= 180.0:
      #--------------
      if (lon1 > lon2):
        lon05_1  = 360.0
        lon05_2  = 0.0
        lat05    = lat1 + (lat2 - lat1)/(lon05_1 - lon1 + lon2 - lon05_2)*(lon05_1 - lon1)
      elif (lon1 < lon2):
        lon05_1  = 0.0
        lon05_2  = 360.0
        lat05    = lat1 + (lat2 - lat1)/(lon05_1 - lon1 + lon2 - lon05_2)*(lon05_1 - lon1)
      #--------------
      M.plot( (lon1, lon05_1), (lat1, lat05), linewidth=1, color=scol)
      M.plot( (lon05_2, lon2), (lat05, lat2), linewidth=1, color=scol)
      #--------------
    else:
      M.plot( (lon1, lon2), (lat1, lat2), linewidth=1, color=scol)
  
    #-- text -----------
    if hour in [0,12]:
      xtext, ytext = M(lon1,lat1)
      #plt.text(xtext,ytext-1, "%02d.%02d"%(day,hour) ,fontsize=12, rotation=-90)
  
  
  
  
  #-- coastline ---------------
  print "coastlines"
  M.drawcoastlines(color="k")
  
  #-- meridians and parallels
  parallels = arange(-90.,90,10.)
  M.drawparallels(parallels,labels=[1,0,0,0],fontsize=lonlatfontsize)
  
  meridians = arange(0.,360.,10.)
  M.drawmeridians(meridians,labels=[0,0,0,1],fontsize=lonlatfontsize,rotation=lonrotation)
  
  #-- title --------------------
  stitle  = "%04d %02d %02d-%02d"%(year,mon,iday, eday)
  axmap.set_title(stitle, fontsize=10.0)
  
  #-- save --------------------
  print "save"
  hostname = socket.gethostname()
  #if   hostname == "well":
  #  sodir   = "/media/disk2/out/cyclone/tc.obj"
  #elif hostname in ["mizu","naam"]:
  #  sodir   = "/tank/utsumi/out/cyclone/tc.obj"
  sodir  = "/home/utsumi/temp"
  #----
  detect_func.mk_dir(sodir)
  soname  = sodir + "/tclines.%s.%s.%04d.%s.%02dh.wc%3.2f.sst%d.vor%.1e.png"%(model, region, year, season, thdura, thwcore, thinitsst -273.15, thrvort)
  
  plt.savefig(soname)
  plt.clf()
  print soname
  plt.clf()
