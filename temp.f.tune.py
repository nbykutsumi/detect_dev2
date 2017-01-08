from numpy import *
import Front
import fig.Fig as Fig
from datetime import datetime
import Image

Year = 2004
lMD = [[3,6]]
#lMD = [[6,7]]
#lMD = [[9,8]]
#lMD = [[12,6]]
Hour = 0

lM1  = [0.26, 0.3, 0.34]
lM2  = [1.0, 1.4, 1.8]

#lM1  = [0.34]
#lM2  = [1.4]

BBox    = [[20,120],[60,170]]
front = Front.front(model="JRA55",res="bn")
a1lat = front.Lat
a1lon = front.Lon
miss  = front.miss

for Mon, Day in lMD:
  Dtime = datetime(Year,Mon,Day,Hour)
  for M1,M2 in [[M1,M2] for M1 in lM1 for M2 in lM2]:
    a2front = front.load_tfront(Dtime, M1=M1, M2=M2)
    a2front = ma.masked_equal(a2front, miss)
    oPath   = "/home/utsumi/temp/tune/%02d.%02d.M1.%04.2f.M2.%03.1f.png"%(Mon,Day,M1,M2)
    Fig.DrawMap(a2front, a1lat, a1lon, BBox, figname = oPath, stitle="%02d-%02d M1=%f M2=%f"%(Mon,Day, M1,M2))

  #- join --
  i  = -1
  da2dat = {}
  for M1,M2 in [[M1,M2] for M1 in lM1 for M2 in lM2]:
    i = i+1
    pngPath   = "/home/utsumi/temp/tune/%02d.%02d.M1.%04.2f.M2.%03.1f.png"%(Mon,Day,M1,M2)
    a2png     = Image.open(pngPath)
    a2in      = asarray(a2png)
    da2dat[i] = a2in
  #-- 
  a2line1 = hstack([da2dat[0], da2dat[1], da2dat[2]])
  a2line2 = hstack([da2dat[3], da2dat[4], da2dat[5]])
  a2line3 = hstack([da2dat[6], da2dat[7], da2dat[8]])
#  a2line4 = hstack([da2dat[9], da2dat[10], da2dat[11]])

#  a2out   = vstack([a2line1, a2line2, a2line3, a2line4])
  a2out   = vstack([a2line1, a2line2, a2line3])
  oimg    = Image.fromarray(a2out)
  joinPath= "/home/utsumi/temp/tune/join.%02d.%02d.png"%(Mon,Day)
  oimg.save(joinPath)
  print joinPath
  
      
  
