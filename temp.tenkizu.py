from numpy import *
from datetime import datetime, timedelta
import Front
import Fig
import Image
import ctrack_func

model = "JRA25"
res   = "sa.one"

#model = "JRA55"
#res   = "bn"

front = Front.front(model=model, res=res)
a1lat = front.Lat
a1lon = front.Lon
miss  = front.miss

Year = 2004
Mon  = 6
Day  = 1
Hour = 0
BBox =[[20,120],[60,170]]


figdir  = "/home/utsumi/temp/tenkizu/%04d%02d"%(Year,Mon)
Dtime = datetime(Year,Mon,Day,Hour)
a2tfront  = ma.masked_not_equal( front.load_tfront(Dtime), miss).filled(2.0)
a2qfront  = ma.masked_not_equal( front.load_qfront(Dtime), miss).filled(1.0)
print a2qfront.mean(),a2tfront.mean()
a2front   = ma.masked_where(a2tfront==2.0, a2qfront).filled(2.0)
a2front   = ma.masked_equal(a2front, miss)

#---
a2orog  = front

#ctrack_func.mk_dir(figdir)
figname = figdir + "/%s.%02d.%02d.png"%(model,Mon,Day)
stitle  = "%02d-%02d %s"%(Mon,Day,model)
Fig.DrawMap(a2front, a1lat, a1lon, BBox, figname=figname,stitle=stitle) 
print figname

