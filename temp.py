import IO_Master
from numpy import *
from datetime import datetime, timedelta
from detect_fsub import *


#####################################################
def pyxy2fortpos(ix, iy, nx):
  ix     = ix + 1  # ix = 1,2,.. nx
  iy     = iy + 1  # iy = 1,2,.. ny
  #number = iy* nx + ix +1
  number = (iy-1)* nx + ix
  return number
#####################################################
def fortpos2pyxy(number, nx, miss_int):
  if (number == miss_int):
    iy0 = miss_int
    ix0 = miss_int
  else:
    iy0 = int((number-1)/nx)  +1  # iy0 = 1, 2, ..
    ix0 = number - nx*(iy0-1)     # ix0 = 1, 2, ..

    iy0 = iy0 -1    # iy0 = 0, 1, .. ny-1
    ix0 = ix0 -1    # ix0 = 0, 1, .. nx-1
  #----
  return ix0, iy0
#####################################################

nx = 288
pos  = 33584
x, y = fortpos2pyxy(pos, nx, -9999)
x  = x+1
y  = y+1
xx, yy = detect_fsub.fortpos2fortxy(pos, nx)

print "ix,iy=" ,x, y
print "pos=",pos
print "ox,oy=" ,xx,yy



#prj    = "JRA55"
#model  = ""
#run    = ""
#res    = "145x288"
#
##prj    = "HAPPI"
##model  = ""
##run    = "C20-ALL-001"
##res    = ""
#
#miss   = -9999.
#iom    = IO_Master.IO_Master(prj, model, run, res)
#a1lat  = iom.Lat
#a1lon  = iom.Lon
#ny     = iom.ny
#nx     = iom.nx
#
#DTime  = datetime(2004,1,5,0)
#a2u  = iom.Load_6hrPlev("ua", DTime, 850)
#a2v  = iom.Load_6hrPlev("va", DTime, 850)
#
#a2rvort = detect_fsub.mk_a2rvort(a2u.T, a2v.T, a1lon, a1lat, miss,).T
#a2rvort = ma.masked_equal(a2rvort, miss)
#
#a  = empty([ny,nx])
#a[:73] = -a2rvort[:73]
#a[73:] = a2rvort[73:]
#a      = ma.masked_equal(a,miss)
#a      = ma.masked_equal(a,-miss)
#print a
#print a2rvort
