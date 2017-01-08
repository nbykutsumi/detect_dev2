from numpy import *
from datetime import datetime, timedelta
import Front
import Fig
import Image
import ctrack_func

#model = "JRA25"
#res   = "sa.one"

#model = "JRA25"
model = "JRA55"
res   = "bn"

#model = "JRA55"
#res   = "bn"

front = Front.Front(model=model, res=res)
a1lat = front.Lat
a1lon = front.Lon
miss  = front.miss

Year = 2004
#lMon = [3,6,9,12]
#lMon = [3,6,9,12]
lMon = [3]
lDay = [1,2,3,4,5,6,7,8]
#lDay = [1]
Hour = 0
#BBox =[[20,120],[60,170]]
BBox =[[20,110],[80,170]]
##----------------
for Mon in lMon:
  figdir  = "/home/utsumi/temp/tenkizu/%04d%02d"%(Year,Mon)
  for i,Day in enumerate(lDay):
    Dtime = datetime(Year,Mon,Day,Hour)
    a2tfront  = ma.masked_not_equal( front.mk_tfront(Dtime), miss).filled(2.0)
    a2qfront  = ma.masked_not_equal( front.mk_qfront(Dtime), miss).filled(1.0)
    a2front   = ma.masked_where(a2tfront==2.0, a2qfront).filled(2.0)
#    a2front   = a2tfront   # test, TEST
    a2front   = ma.masked_equal(a2front, miss)

    #-------------------
    ctrack_func.mk_dir(figdir)
    figname = figdir + "/%s.%s.%02d.%02d.png"%(model,res,Mon,Day)
    stitle  = "%02d-%02d %s"%(Mon,Day,model)
    Fig.DrawMap(a2front, a1lat, a1lon, BBox, figname=figname,stitle=stitle) 
    print figname

 # join -----
  da2dat = {}
  for i,Day in enumerate(lDay):
    pngname = figdir + "/%s.%s.%02d.%02d.png"%(model,res,Mon,Day)
    a2png   = Image.open(pngname)
    a2array = asarray(a2png)
    da2dat[i] = a2array
  
  a2line1 = hstack([ da2dat[0], da2dat[4] ])
  a2line2 = hstack([ da2dat[1], da2dat[5] ])
  a2line3 = hstack([ da2dat[2], da2dat[6] ])
  a2line4 = hstack([ da2dat[3], da2dat[7] ])

  a2oarray= vstack( [a2line1, a2line2, a2line3, a2line4] )
  oimg    = Image.fromarray(a2oarray)
  oPath   = figdir + "/join.%s.%s.%02d.png"%(model,res,Mon)
  oimg.save(oPath)
  print oPath


