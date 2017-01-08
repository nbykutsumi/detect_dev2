from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from numpy import *
from ctrack_fsub import *
import calendar
import ctrack_para
import ctrack_func
import tc_para
import tc_func
import sys, os
#--------------------------------------
model = "anl_p125"

#singleday = True
singleday = False
unitdist  = 10.0 # km / hour
#unitdist  = 150.0 # km / hour  # test
#----------------
if len(sys.argv)>1:
  year   = int(sys.argv[1])
  mon    = int(sys.argv[2])
  iday   = int(sys.argv[3])
  eday   = int(sys.argv[4])
  thdura = int(sys.argv[5])
  region = sys.argv[6]
else:
  print "cmd [year] [mon] [iday] [eday] [thdura] [region]"
  #sys.exit()
  year = 2014
  mon  = 2
  iday = 1
  eday = 28
  thdura = 48
#  thdura = 72
  region = "GLOB"
#  region = "SAM"
#  region = "NAF"
#----------------
print year,mon,iday,eday,thdura,region
#iclass_min = 2
iclass_min = 1

a1lat, a1lon = ctrack_func.ret_a1latlon("JRA55", model)
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
  clistdir  = "/media/disk2/out/JRA55/bn/6hr/clist/%04d/%02d"%(year,mon)
  da1       = {}
  #lstype  = ["rvort","dtlow","dtmid","dtup","wmeanlow","wmeanup","wmaxlow","dura","pgrad","sst","lat","lon","ipos","nowpos","time","initsst"]
  #lstype  = ["dura","pgrad","lat","lon","nowpos","time","iedist"]
  lstype  = ["dura","pgrad","lat","lon","nowpos","time","iedist"]
  for stype in lstype:
    siname        = clistdir  + "/%s.%04d.%02d.bn"%(stype,year,mon)
    if stype in ["dura","ipos","idate","nowpos","time"]:
      da1[stype]  = fromfile(siname,   int32)
    else:
      da1[stype]  = fromfile(siname, float32)

    print siname
  #**** make dictionary ***
  stepflag = 0
  dtcloc   = {}
  nlist    = len(da1["dura"])
  for i in range(nlist):
    dura        = da1["dura"     ][i]
    pgrad       = da1["pgrad"    ][i]
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

    #---- dura -------
    if dura < thdura:
      continue
    #---- thpgrad ----
    if pgrad < thpgrad:
      continue
    #---- iedist -----
    if iedist < dura*unitdist:
      continue

    #---- time ------
    yeart,mont,dayt,hourt = ctrack_func.solve_time(time)

    #---- location --
    ix, iy            = ctrack_func.fortpos2pyxy( nowpos, nx, -9999)



    #---- dictionary --
    if dtcloc.has_key((dayt,hourt)):
      dtcloc[dayt,hourt].append([ix,iy,pgrad])
    else:
      dtcloc[dayt,hourt] = [[ix,iy, pgrad]]
  #------------------
  return dtcloc

#************************************

#----------------------------
dpgradrange  = ctrack_para.ret_dpgradrange()
#lclass  = dpgradrange.keys()[2:]
lclass  = dpgradrange.keys()
nclass  = len(lclass)
thpgrad = dpgradrange[0][0]
#----------------------------
psldir_root     = "/media/disk2/data/JRA55/bn.%s/6hr/PRMSL"%(model)
pgraddir_root   = "/media/disk2/out/JRA55/bn/6hr/pgrad"
lifedir_root    = "/media/disk2/out/JRA55/bn/6hr/life"
nextposdir_root = "/media/disk2/out/JRA55/bn/6hr/nextpos"
#************************************
dtrack     = {}
for iclass in lclass:
  dtrack[iclass] = []
#------------------------------------
#************************
# load TCs
#------------------------
dTC  = tc_func.ret_ibtracs_dpyxy(year, a1lat, a1lon)

#------------------------
#eday = calendar.monthrange(year,mon)[1]
##############
dexcloc =  mk_dexcloc(year,mon)
print year,mon   
for day in range(iday, eday+1):
  print "tracklines",model,year, mon, day
  for hour in [0, 6, 12, 18]:
    #-- check exc existence ----
    if not dexcloc.has_key((day,hour)):
      continue
    #---------------------------
    stime   = "%04d%02d%02d%02d"%(year, mon, day, hour)
    #---------------------------
    nextposdir      = nextposdir_root + "/%04d/%02d"%(year, mon)
    nextposname     = nextposdir + "/nextpos.%s.bn"%(stime)
    a2nextpos       = fromfile(nextposname,  int32).reshape(ny, nx)

    #---------------------------
    ldat    = dexcloc[day,hour]
    for locdat in ldat:
      ix,iy,pgrad = locdat

      #-- nextpos ------------
      nextpos   = a2nextpos[iy, ix]
      x_next, y_next = ctrack_func.fortpos2pyxy(nextpos, nx, miss_int)

      if ( (x_next == miss_int) & (y_next == miss_int) ):
        continue            
      #-- check TC -----------
      tcflag = 0
      if (ix,iy) in dTC[year,mon,day,hour]:
        print "TC!, lat,lon=",year,mon,day,hour,iy-90.0, ix
        tcflag = tcflag +1
      else:
        ixfort = ix +1
        iyfort = iy +1
        a1surrxfort, a1surryfort = ctrack_fsub.mk_8gridsxy(ixfort, iyfort, nx, ny)
        for itemp in range(0,8):
          ixt =  a1surrxfort[itemp] -1
          iyt =  a1surryfort[itemp] -1
          if (ixt,iyt) in dTC[year,mon,day,hour]:
            print "TC!, lat,lon=",year,mon,day,hour,iy-90.0, ix
            tcflag = tcflag + 1
      #
      if tcflag > 0:
        continue
      #-----------------------
      #for iclass in range(0, nclass):
      for iclass in lclass:
        pgrad_min = dpgradrange[iclass][0]
        pgrad_max = dpgradrange[iclass][1]
        if (pgrad_min <= pgrad < pgrad_max):
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

#-- draw cyclone tracks ------
itemp = 1
#for iclass in lclass[1:]:
for iclass in lclass:
  if iclass < iclass_min: continue
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
    if iclass ==1:
      scol="gray"
      #scol="b"
    elif iclass ==2:
      scol="b"
      #scol="r"
    elif iclass ==3:
      #scol="g"
      scol="r"
    elif iclass == 4:
      #scol="gray"
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
sodir   = "/media/disk2/out/cyclone/exc.track.w.bsttc.JRA55/%s"%(region)
ctrack_func.mk_dir(sodir)
soname  = sodir + "/exc.track.w.bsttc.%s.%04d.%02d.%02d-%02d.%02dh.png"%(model, year,mon, iday, eday, thdura)
plt.savefig(soname)
plt.clf()
print soname
plt.clf()
