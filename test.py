#----------------------------------
import sys, os
myPath  = os.path.abspath(__file__)
myDir   = os.path.dirname(myPath)
parDir  = "/".join(myDir.split("/")[:-1])
sys.path.append(parDir)
#----------------------------------
from   mpl_toolkits.basemap import Basemap
from   numpy import *
from   detect_fsub import *
from   datetime import datetime, timedelta
import matplotlib.pyplot as plt
import config_func
import detect_func
import IO_Master
import BestTrackTC
import util
import Cyclone
#--------------------------------------
prj     = "JRA55"
model   = "__"
run     = "__"
res     = "145x288"

#Prj     = "HAPPI"
#Model   = "MIROC5"
#Run     = "C20-ALL-001"
#Res     = "128x256"

#singleday = True
singleday = False
unitdist  = 10.0 # km / hour
#unitdist  = 150.0 # km / hour  # test
#----------------
iDTime = datetime(2004,1,8,0)
eDTime = datetime(2004,1,14,18)
dDTime = timedelta(hours=6)
lDTime = util.ret_lDTime(iDTime, eDTime, dDTime)

thdura = 48
#thdura = 72
#region = "GLOB"
region = "JPN"
#region = "NAF"

iom    = IO_Master.IO_Master(prj, model, run, res)
bst    = BestTrackTC.BestTrack("IBTrACS")
cfg = config_func.config_func(prj=prj, model=model, run=run)
iom = IO_Master.IO_Master(prj, model, run, res)
cy  = Cyclone.Cyclone(cfg=cfg)
#----------------------------------
#iclass_min = 2
#iclass_min = 1
iclass_min = 0

a1lat   = iom.Lat
a1lon   = iom.Lon
ny      = len(a1lat)
nx      = len(a1lon)

lonlatfontsize = 10.0
#lonrotation    = 90
lonrotation    = 0
miss_int= -9999

# local region ------
if region =="JPN":
  lllat   = 25.
  urlat   = 60.
  lllon   = 110.
  urlon   = 180.
elif region == "INDIA":
  lllat   = 0.
  urlat   = 30.
  lllon   = 50.
  urlon   = 100.
elif region == "AUS":
  lllat   = -50.
  urlat   = 10.
  lllon   = 110.
  urlon   = 160.
elif region == "GLOB":
  lllat   = -90.
  urlat   = 90.
  lllon   = 0.
  urlon   = 360.
elif region == "SAM":
  lllat   = -50.
  urlat   = 10.
  lllon   = 270.
  urlon   = 320.
elif region == "NAF":
  lllat   = -10.
  urlat   = 40.
  lllon   = 0.
  urlon   = 55.


#*************************************
# FUNCTION
#*************************************
def mk_dexcloc(year,mon):
  da1       = {}
  lstype  = ["dura","pgrad","vortlw","lat","lon","nowpos","time","iedist"]
  for stype in lstype:
    siname        = cy.path_clist(stype, year, mon)[1]
    if stype in ["dura","ipos","idate","nowpos","time"]:
      da1[stype]  = fromfile(siname,   int32)
    else:
      da1[stype]  = fromfile(siname, float32)

    print siname
  #*******
  stepflag = 0
  dcloc    = {}
  nlist    = len(da1["dura"])
  for i in range(nlist):
    dura        = da1["dura"     ][i]
    #pgrad       = da1["pgrad"    ][i]
    rvort       = da1["vortlw"    ][i]
    nowpos      = da1["nowpos"   ][i]
    time        = da1["time"     ][i]
    iedist      = da1["iedist"   ][i]
    #---- check time ----
    ### This section should be prior to the condition filtering

    if (i == nlist-1):
      stepflag = 1
    else:
      timenext    = da1["time"][i+1]
      if (timenext != time):
        stepflag = 1

    ##---- dura -------
    #if dura < thdura:
    #  continue
    ##---- thpgrad ----
    #if pgrad < thpgrad:
    #  continue
    #---- thrvort ----
    #if rvort < exrvort:
    #if rvort < exrvort*0.5:   # test
    #  continue

    ##---- iedist -----
    #if iedist < dura*unitdist:
    #  continue

    #---- time ------
    yeart,mont,dayt,hourt = detect_func.solve_time(time)

    #---- location --
    ix, iy            = detect_func.fortpos2pyxy( nowpos, nx, -9999)

    #---- dictionary --
    if dcloc.has_key((dayt,hourt)):
      dcloc[dayt,hourt].append([ix,iy,rvort])
    else:
      dcloc[dayt,hourt] = [[ix,iy, rvort]]
  #------------------
  return dcloc

#************************************

#----------------------------
#thpgrad = cy.thpgrad
#dpgradrange  = {0:[thpgrad, 1.e+10]}
#lclass  = dpgradrange.keys()[2:]

#exrvort = cy.exrvort
exrvort = 3.7e-5   # test
drvortrange  = {0:[exrvort, 1.e+10]
              , 1:[exrvort*0.5, exrvort]
              , 2:[exrvort, exrvort*2.0]
              , 3:[exrvort*2.0, 1.e+10]
               }
lclass  = drvortrange.keys()
nclass  = len(lclass)
#************************************
dtrack     = {}
for iclass in lclass:
  dtrack[iclass] = []
#------------------------------------
##############
for itime, DTime in enumerate(lDTime):
  print "tracklines",DTime
  year = DTime.year
  mon  = DTime.month
  day  = DTime.day
  hour = DTime.hour
  #************************
  # load TCs
  #------------------------
  if ((itime ==0)or(DTime.year > lDTime[itime-1].year)):
    dTC   = bst.ret_dpyxy(year, a1lon, a1lat)

  if ((itime ==0)or(DTime.month != lDTime[itime-1].month)):
    dexcloc =  mk_dexcloc(year,mon)


  ## Test
  #dTC[DTime.year,DTime.month,DTime.day,DTime.hour] =[]   # test

  #-- check exc existence ----
  if not dexcloc.has_key((day,hour)):
    continue
  #---------------------------
  nextposname     = cy.path_a2dat("nextpos",DTime).srcPath
  a2nextpos       = fromfile(nextposname,  int32).reshape(ny, nx)


  #---------------------------
  ldat    = dexcloc[day,hour]
  for locdat in ldat:
    ix,iy,rvort = locdat

    #-- nextpos ------------
    nextpos   = a2nextpos[iy, ix]
    x_next, y_next = detect_func.fortpos2pyxy(nextpos, nx, miss_int)

    if ( (x_next == miss_int) & (y_next == miss_int) ):
      continue            
    #-- check TC -----------
    tcflag = 0
    if (ix,iy) in dTC[datetime(year,mon,day,hour,0)]:
      print "TC!, lat,lon=",year,mon,day,hour,iy-90.0, ix
      tcflag = tcflag +1
    else:
      ixfort = ix +1
      iyfort = iy +1
      a1surrxfort, a1surryfort = detect_fsub.mk_8gridsxy(ixfort, iyfort, nx, ny)
      for itemp in range(0,8):
        ixt =  a1surrxfort[itemp] -1
        iyt =  a1surryfort[itemp] -1
        if (ixt,iyt) in dTC[datetime(year,mon,day,hour,0)]:
          print "TC!, lat,lon=",year,mon,day,hour,iy-90.0, ix
          tcflag = tcflag + 1
    #
    if tcflag > 0:
      continue
    #-----------------------
    #for iclass in range(0, nclass):
    for iclass in lclass:
      #pgrad_min = dpgradrange[iclass][0]
      #pgrad_max = dpgradrange[iclass][1]
      rvort_min = drvortrange[iclass][0]
      rvort_max = drvortrange[iclass][1]

      if (rvort_min <= rvort < rvort_max):
        #------
        if ( (x_next == miss_int) & (y_next == miss_int) ):
          continue
        #------
        lat       = a1lat[iy]
        lon       = a1lon[ix]

        lat_next  = a1lat[y_next]
        lon_next  = a1lon[x_next]
        #
        dtrack[iclass].append([[year, mon, day, hour],[lat, lon, lat_next, lon_next]])


##*************\***********
## for mapping
#nnx        = int( (urlon - lllon)/dlon)
#nny        = int( (urlat - lllat)/dlat)
#a1lon_loc  = linspace(lllon, urlon, nnx)
#a1lat_loc  = linspace(lllat, urlat, nny)
#LONS, LATS = meshgrid( a1lon_loc, a1lat_loc)
#------------------------
# Basemap
#------------------------
print "Basemap"
figmap   = plt.figure()
axmap    = figmap.add_axes([0.1, 0.1, 0.8, 0.8])
M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)


a2out = ones([ny,nx],float32)
for DTime in lDTime:
  day = DTime.day
  hour= DTime.hour
  lxyz = dexcloc[(day,hour)]
  for (x,y,z) in lxyz:
    lon = a1lon[x]
    lat = a1lat[y]
    if ((lllon<lon)&(lon<urlon)&(lllat<lat)&(lat<urlat)):
      print x,y, "***",lon, lat
      M.plot( lon, lat, "o")



#-- draw cyclone tracks ------
itemp = 1
for iclass in lclass[1:]:
#for iclass in lclass:
  #if iclass < iclass_min: continue
  if (len(dtrack[iclass]) ==  0.0):
    continue
  #-----------
  for track in dtrack[iclass]:
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
    #if iclass ==0:
    #  scol="r"

    if iclass ==1:
      scol="gray"
      #scol="b"
    elif iclass ==2:
      scol="b"
      #scol="r"
    elif iclass ==3:
      scol="r"
#    elif iclass == 4:
#      #scol="gray"
#      scol="r"
 
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
stitle  = "%04d/%02d/%02d-%04d/%02d/%02d"\
          %(iDTime.year, iDTime.month, iDTime.day, eDTime.year, eDTime.month, eDTime.day)
axmap.set_title(stitle, fontsize=10.0)

#-- save --------------------
print "save"
#sodir   = "/media/disk2/out/cyclone/exc.track.w.bsttc.JRA55/%s"%(region)
#sodir   = "/home/utsumi/temp"
sodir  = "."
util.mk_dir(sodir)
#soname  = sodir + "/exc.track.w.bsttc.%s.%04d.%02d.%02d-%02d.%02dh.png"%(model, year,mon, iday, eday, thdura)
soname  = sodir + "/test.png"
plt.savefig(soname)
plt.clf()
print soname
plt.clf()
