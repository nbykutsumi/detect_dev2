import sys
from detect_fsub import *
from front_fsub import *
from numpy import *
from CHART import chart
import datetime
import front_func
import fig.Fig as Fig
import Image

Year = 2004
lMon = [3,6,9,12]
lDay = [1,2,3,4,5,6,7,8]
#lDay = [1]
Hour = 0
miss = -9999.
M1   = 0.3
M2   = 1.0
thgrids = 3
BBox    = [[20,120],[60,170]]
#****************************************************
def read_txtlist(iname):
  f = open(iname, "r")
  lines = f.readlines()
  f.close()
  lines = map(float, lines)
  aout  = array(lines, float32)
  return aout

def mk_front_loc_contour(a2thermo, a1lon, a1lat, miss):
  a2fmask1 = front_fsub.mk_a2frontmask1(a2thermo.T, a1lon, a1lat, miss).T
  a2fmask2 = front_fsub.mk_a2frontmask2(a2thermo.T, a1lon, a1lat, miss).T
  a2fmask1 = a2fmask1 * (1000.0*100.0)**2.0  #[(100km)-2]
  a2fmask2 = a2fmask2 * (1000.0*100.0)       #[(100km)-1]

  a2loc    = front_fsub.mk_a2meanaxisgrad3_h98_eq6(a2thermo.T, a1lon, a1lat, miss).T

  a2loc    = front_fsub.mk_a2contour(a2loc.T, 0.0, 0.0, miss).T
  a2loc    = ma.masked_equal(a2loc, miss)

  a2loc    = ma.masked_where(a2fmask1 < 0.0, a2loc)
  a2loc    = ma.masked_where(a2fmask2 < 0.0, a2loc)
  a2loc1   = ma.masked_where(a2loc.mask, a2fmask1).filled(miss)
  a2loc2   = ma.masked_where(a2loc.mask, a2fmask2).filled(miss)

  return a2loc1, a2loc2

def ret_old_loc(Year,Mon,Day,Hour):
  srcPath1 = "/media/disk2/out/JRA25/sa.one.anl_p/6hr/front.t/%04d%02d/front.t.M1.%04d.%02d.%02d.%02d.sa.one"%(Year,Mon,Year,Mon,Day,Hour)
  srcPath2 = "/media/disk2/out/JRA25/sa.one.anl_p/6hr/front.t/%04d%02d/front.t.M2.%04d.%02d.%02d.%02d.sa.one"%(Year,Mon,Year,Mon,Day,Hour)
  a2loc1   = fromfile(srcPath1, float32).reshape(ny,nx)
  a2loc2   = fromfile(srcPath2, float32).reshape(ny,nx)
  return a2loc1, a2loc2

  a2fbc    = front_func.complete_front_t(a2fbc1, a2fbc2, M1, M2, thgrids, miss )
  return a2fbc


latname = "/media/disk2/data/JRA25/sa.one.anl_p/lat.txt"
lonname = "/media/disk2/data/JRA25/sa.one.anl_p/lon.txt"
a1lat   = read_txtlist(latname)
a1lon   = read_txtlist(lonname)
ny,nx   = len(a1lat), len(a1lon)

#for Mon in lMon:
#  for Day in lDay:
#    srcPath = "/media/disk2/data/JRA25/sa.one.anl_p/6hr/TMP/%04d%02d/anl_p.TMP.0850hPa.%04d%02d%02d%02d.sa.one"%(Year,Mon,Year,Mon,Day,Hour)
#    a2t     = fromfile(srcPath,float32).reshape(ny,nx)
#    a2loc1, a2loc2 = mk_front_loc_contour(a2t, a1lon, a1lat, miss)
#  
#    a2old1, a2old2 = ret_old_loc(Year,Mon,Day,Hour)
#  
#    a2front = front_func.complete_front_t(a2loc1, a2loc2, M1, M2, thgrids, miss )
#    a2old   = front_func.complete_front_t(a2old1, a2old2, M1, M2, thgrids, miss )
#  
#    a2front = ma.masked_equal(a2front, miss)
#    a2old   = ma.masked_equal(a2old  , miss)
#    #---
#    newname = "/home/utsumi/temp/comp/%02d.%02d.png"%(Mon,Day)
#    oldname = "/home/utsumi/temp/comp/%02d.%02d.old.png"%(Mon,Day)
#  
#    Fig.DrawMap(a2front, a1lat, a1lon, BBox, figname=newname, stitle="NEW %02d-%02d"%(Mon,Day))
#    Fig.DrawMap(a2old  , a1lat, a1lon, BBox, figname=oldname, stitle="OLD %02d-%02d"%(Mon,Day))
  

#-- join ---
for Mon in lMon:
  da2dat1 = {}
  da2dat2 = {}
  for i,Day in enumerate(lDay):
    newname = "/home/utsumi/temp/comp/%02d.%02d.png"%(Mon,Day)
    oldname = "/home/utsumi/temp/comp/%02d.%02d.old.png"%(Mon,Day)
    a2png1 = Image.open(newname)
    a2png2 = Image.open(oldname)
    a2in1  = asarray(a2png1)
    a2in2  = asarray(a2png2)
    da2dat1[i] = a2in1
    da2dat2[i] = a2in2

  a2line1   = hstack([da2dat1[0], da2dat2[0], da2dat1[4], da2dat2[4]])
  a2line2   = hstack([da2dat1[1], da2dat2[1], da2dat1[5], da2dat2[5]])
  a2line3   = hstack([da2dat1[2], da2dat2[2], da2dat1[6], da2dat2[6]])
  a2line4   = hstack([da2dat1[3], da2dat2[3], da2dat1[7], da2dat2[7]])

  a2out     = vstack([a2line1,a2line2,a2line3,a2line4])
  oimg      = Image.fromarray(a2out)
  joinPath  = "/home/utsumi/temp/comp/join.%02d.png"%(Mon)
  oimg.save(joinPath)
  print joinPath





