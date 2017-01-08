from numpy import *
from datetime import datetime, timedelta
import util_para
import Reanalysis
import myfunc.util as util

iDTime = datetime(2013,1,1,0)
#eDTime = datetime(2014,7,1,0)
eDTime = datetime(2013,12,31,0)
#eDTime = datetime(2013,1,5,0)
#eDTime = datetime(2014,12,31,0)
#iDTime = datetime(2014,6,20,0)
#eDTime = datetime(2014,6,20,0)
dDTime = timedelta(hours=24)

#var    = "PWAT"
#var    = "spfh850_500"
var    = "spfh850_500_250"
lev    = False
dstype = {"PWAT":"anl_column125"
         ,"spfh850_500":"anl_p125"
         ,"spfh850_500_250":"anl_p125"}
miss   = -9999.
ra  = Reanalysis.Reanalysis(model="JRA55",res="bn")
ny  = ra.ny
nx  = ra.nx

thrat = 0.618

#-----------------------------------
def latlon2yx(lat,lon):
  y = (lat+90+1.25*0.5)/1.25
  x = (lon+1.25*0.5)/1.25
  return y,x

def CheckNPWI5Days(a2var0, a2var1, a2var2, a2var3, a2var4, a2min, a2max):

  a2npwi = ((a2var0+a2var1+a2var2+a2var3+a2var4)/5 - a2min)/(a2max-a2min)
  return    ma.masked_where(a2npwi<thrat, ones([ny,nx],float32)).filled(0.0)


def AveNPWI5Days(a2var0, a2var1, a2var2, a2var3, a2var4, a2min, a2max):

  return ((a2var0+a2var1+a2var2+a2var3+a2var4)/5 - a2min)/(a2max-a2min)

def Check9grids(a2flag):
  a2countN = r_[a2flag[0,:].reshape(1,nx),  a2flag[:-1,:]]
  a2countS = r_[a2flag[1:,:], a2flag[-1, :].reshape(1,nx)]

  a2count  = a2flag
  a2count  = a2count + c_[a2flag[:,1:], a2flag[:,0]]
  a2count  = a2count + c_[a2flag[:,-1], a2flag[:,:-1]]
  a2count  = a2count + a2countN
  a2count  = a2count + a2countS
  a2count  = a2count + c_[a2countN[:,1:], a2countN[:,0]]
  a2count  = a2count + c_[a2countN[:,-1], a2countN[:,:-1]]
  a2count  = a2count + c_[a2countS[:,1:], a2countS[:,0]]
  a2count  = a2count + c_[a2countS[:,-1], a2countS[:,:-1]]
  return ma.masked_where(a2count <7, ones([ny,nx], float32)).filled(0.0)

def Ave9grids(a2var):
  ny,nx  = shape(a2var)
  a2varN = r_[a2var[0,:].reshape(1,nx),  a2var[:-1,:]]
  a2varS = r_[a2var[1:,:], a2var[-1, :].reshape(1,nx)]

  a2out  = a2var
  a2out  = a2out + c_[a2var[:,1:], a2var[:,0]]
  a2out  = a2out + c_[a2var[:,-1], a2var[:,:-1]]
  a2out  = a2out + a2varN
  a2out  = a2out + a2varS
  a2out  = a2out + c_[a2varN[:,1:], a2varN[:,0]]
  a2out  = a2out + c_[a2varN[:,-1], a2varN[:,:-1]]
  a2out  = a2out + c_[a2varS[:,1:], a2varS[:,0]]
  a2out  = a2out + c_[a2varS[:,-1], a2varS[:,:-1]]
  return a2out/9.0

#-----------------------------------
def ret_a2var(var, DTime, lev):
  if var in  ["PWAT"]:
    a2var = ra.time_ave(var, DTime, DTime+timedelta(hours=23), timedelta(hours=6), lev=lev)
  elif var == "spfh850_500":
    a2var1 = ra.time_ave("spfh", DTime, DTime+timedelta(hours=23), timedelta(hours=6), lev=850)
    a2var2 = ra.time_ave("spfh", DTime, DTime+timedelta(hours=23), timedelta(hours=6), lev=500)
    a2var  = (a2var1 + a2var2)/2.0
  elif var == "spfh850_500_250":
    a2var1 = ra.time_ave("spfh", DTime, DTime+timedelta(hours=23), timedelta(hours=6), lev=850)
    a2var2 = ra.time_ave("spfh", DTime, DTime+timedelta(hours=23), timedelta(hours=6), lev=500)
    a2var3 = ra.time_ave("spfh", DTime, DTime+timedelta(hours=23), timedelta(hours=6), lev=250)
    a2var  = (a2var1 + a2var2 + a2var3)/3.0


  return a2var
#-----------------------------------
def ret_lDTime(iDTime,eDTime,dDTime):
  total_steps = int( (eDTime - iDTime).total_seconds() / dDTime.total_seconds() + 1 )
  return [iDTime + dDTime*i for i in range(total_steps)]

#-----------------------------------
def ret_maxmin_ave(iYear,eYear,maxmin="max"):
  lYear  = range(iYear,eYear+1)
  a3dat  = zeros([len(lYear), ny, nx]) 
  for i,Year in enumerate(lYear):
    sdir_root = "/tank/utsumi/out/JRA55/bn/6hr"
    sdir      = sdir_root + "/ms.%s/%s"%(maxmin,var)
    sPath     = sdir + "/%s.%s.%s.%04d.bn"%(maxmin,dstype[var],var,Year)
    a2in      = ma.masked_equal(fromfile(sPath, float32).reshape(ny,nx), miss)
    a3dat[i]  = a2in

  return a3dat.mean(axis=0)

#-----------------------------------

a2max  = ret_maxmin_ave(1980,1999,maxmin="max")
a2min  = ret_maxmin_ave(1980,1999,maxmin="min")

lDTime = ret_lDTime(iDTime, eDTime, dDTime)

llatlon   = [[19.5,72.5]
            ,[23.5,114.5]
            ,[13.5,112.5]
            ,[31.5,360-111.5]
            ,[15.5,360-10.5]
            ,[-12.5,129.5]
            ,[-22.5,360-55.5]
            ,[35,139]
            ]

dlnpwi   ={} 
dlflag   ={}
for i,latlon in enumerate(llatlon):
  dlnpwi[i]   = []
  dlflag[i]   = []

for DTime in lDTime:
  #-- check --
  a2var0  = ret_a2var(var, DTime, lev)
  a2var1  = ret_a2var(var, DTime-timedelta(hours=24),   lev)
  a2var2  = ret_a2var(var, DTime-timedelta(hours=24*2), lev)
  a2var3  = ret_a2var(var, DTime+timedelta(hours=24),   lev)
  a2var4  = ret_a2var(var, DTime+timedelta(hours=24*2), lev)

  a2flag  = CheckNPWI5Days(a2var0, a2var1, a2var2, a2var3, a2var4, a2min, a2max)
  a2flag  = Check9grids(a2flag)
  a2npwi  = (a2var0 - a2min)/(a2max - a2min)

  for i,latlon in enumerate(llatlon):
    lat,lon = latlon
    iy,ix   = latlon2yx(lat,lon)
    dlnpwi[i].append(a2npwi[iy,ix])
    dlflag[i].append(a2flag[iy,ix])


lout = [dlnpwi[i] for i in range(len(llatlon))]
aout = array(lout).T
sout = util.array2csv(aout)
csvname = "./ms.Np.%s.csv"%(var)
f=open(csvname,"w"); f.write(sout); f.close(); print csvname

lout = [dlflag[i] for i in range(len(llatlon))]
aout = array(lout).T
sout = util.array2csv(aout)
csvname = "./ms.On.%s.csv"%(var)
f=open(csvname,"w"); f.write(sout); f.close(); print csvname

