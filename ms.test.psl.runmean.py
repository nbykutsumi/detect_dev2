from numpy import *
from datetime import datetime, timedelta
import myfunc.IO.JRA55 as JRA55
import util
import os, sys
import calendar

iYM    = [2006,1]
eYM    = [2006,12]
lYM    = util.ret_lYM(iYM, eYM)

wD = 2
jra = JRA55.Jra55()
ny  = jra.ny
nx  = jra.nx

#var  = "vgrd"
#var  = "ugrd"
#var  = "spfh"
var  = psl

baseDir = "/home/utsumi/mnt/well.share/temp"
for Year,Mon in lYM:
    eDay = calendar.monthrange(Year,Mon)[1]
    iDTime = datetime(Year,Mon,1,0)
    eDTime = datetime(Year,Mon,eDay,0) 
    dDTime = timedelta(hours=6)
    lDTimeDay = util.ret_lDTime(iDTime, eDTime, timedelta(days=1))
    lDTime = util.ret_lDTime(iDTime, eDTime, dDTime )

    oDir   = baseDir + "/%s/%d"%(var, Year)
    util.mk_dir(oDir)

    # Running mean
    for DTime in lDTimeDay:
        WNDW = util.ret_lDTime(DTime - timedelta(days=wD), DTime+timedelta(days=wD), dDTime)
    
        a2var = zeros([ny,nx],float32)
        i  = 0
        for tDTime in WNDW:
            i = i+1
            a2var = a2var + jra.load_6hr(var, tDTime)
        a2var = a2var/i
        
        oPath = os.path.join(oDir, "%s.runmean.%04d%02d%02d.%dx%d"%(var,DTime.year, DTime.month, DTime.day, ny, nx))
        a2var.tofile(oPath)
        print oPath
        
    # Climatology
    a2clim = zeros([ny,nx],float32)
    for DTime in lDTime:
        a2clim = a2clim + jra.load_6hr(var, DTime)

    a2clim = a2clim / len(lDTime)
    oPath  = os.path.join(oDir, "%s.mean.%04d%02d.%dx%d"%(var, DTime.year, DTime.month, ny, nx))
    a2clim.tofile(oPath)


