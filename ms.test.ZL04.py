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

var    = "PWAT"
lev    = False
dstype = {"PWAT":"anl_column125"}
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

def CheckOnset3Days(a2var0, a2var1, a2var2, a2min, a2max):
  a2npwi0   = (a2var0 - a2min)/(a2max - a2min)
  a2npwi1   = (a2var1 - a2min)/(a2max - a2min)
  a2npwi2   = (a2var2 - a2min)/(a2max - a2min)

  a2count0  = ma.masked_where(a2npwi0<thrat, ones([ny,nx],float32)).filled(0.0)
  a2count1  = ma.masked_where(a2npwi1<thrat, ones([ny,nx],float32)).filled(0.0)
  a2count2  = ma.masked_where(a2npwi2<thrat, ones([ny,nx],float32)).filled(0.0)

  return    ma.masked_where((a2count0+a2count1+a2count2)<3, ones([ny,nx],float32)).filled(0.0)

def CheckOnset4Days(a2var0, a2var1, a2var2, a2var3, a2min, a2max):
  a2npwi0   = (a2var0 - a2min)/(a2max - a2min)
  a2npwi1   = (a2var1 - a2min)/(a2max - a2min)
  a2npwi2   = (a2var2 - a2min)/(a2max - a2min)
  a2npwi3   = (a2var3 - a2min)/(a2max - a2min)

  a2count0  = ma.masked_where(a2npwi0<thrat, ones([ny,nx],float32)).filled(0.0)
  a2count1  = ma.masked_where(a2npwi1<thrat, ones([ny,nx],float32)).filled(0.0)
  a2count2  = ma.masked_where(a2npwi2<thrat, ones([ny,nx],float32)).filled(0.0)
  a2count3  = ma.masked_where(a2npwi3<thrat, ones([ny,nx],float32)).filled(0.0)

  return    ma.masked_where((a2count0+a2count1+a2count2+a2count3)<3, ones([ny,nx],float32)).filled(0.0)



def CheckOnset5Days(a2var0, a2var1, a2var2, a2var3, a2var4, a2min, a2max):
  a2npwi0   = (a2var0 - a2min)/(a2max - a2min)
  a2npwi1   = (a2var1 - a2min)/(a2max - a2min)
  a2npwi2   = (a2var2 - a2min)/(a2max - a2min)
  a2npwi3   = (a2var3 - a2min)/(a2max - a2min)
  a2npwi4   = (a2var4 - a2min)/(a2max - a2min)

  a2count0  = ma.masked_where(a2npwi0<thrat, ones([ny,nx],float32)).filled(0.0)
  a2count1  = ma.masked_where(a2npwi1<thrat, ones([ny,nx],float32)).filled(0.0)
  a2count2  = ma.masked_where(a2npwi2<thrat, ones([ny,nx],float32)).filled(0.0)
  a2count3  = ma.masked_where(a2npwi3<thrat, ones([ny,nx],float32)).filled(0.0)
  a2count4  = ma.masked_where(a2npwi4<thrat, ones([ny,nx],float32)).filled(0.0)

  return    ma.masked_where((a2count0+a2count1+a2count2+a2count3+a2count4)<3, ones([ny,nx],float32)).filled(0.0)

def CheckNPWI5Days(a2var0, a2var1, a2var2, a2var3, a2var4, a2min, a2max):

  a2npwi = ((a2var0+a2var1+a2var2+a2var3+a2var4) - a2min*5)/(a2max-a2min)/5.0
  return    ma.masked_where(a2npwi<thrat, ones([ny,nx],float32)).filled(0.0)


def AveNPWI5Days(a2var0, a2var1, a2var2, a2var3, a2var4, a2min, a2max):

  return ((a2var0+a2var1+a2var2+a2var3+a2var4)/5 - a2min)/(a2max-a2min)




def CheckRetreat3Days(a2var0, a2var1, a2var2, a2min, a2max):
  a2npwi0   = (a2var0 - a2min)/(a2max - a2min)
  a2npwi1   = (a2var1 - a2min)/(a2max - a2min)
  a2npwi2   = (a2var2 - a2min)/(a2max - a2min)

  a2count0  = ma.masked_where(a2npwi0>=thrat, ones([ny,nx],float32)).filled(0.0)
  a2count1  = ma.masked_where(a2npwi1>=thrat, ones([ny,nx],float32)).filled(0.0)
  a2count2  = ma.masked_where(a2npwi2>=thrat, ones([ny,nx],float32)).filled(0.0)

  return    ma.masked_where((a2count0+a2count1+a2count2)<3, ones([ny,nx],float32)).filled(0.0)

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
  return a2var
#-----------------------------------
def ret_lDTime(iDTime,eDTime,dDTime):
  total_steps = int( (eDTime - iDTime).total_seconds() / dDTime.total_seconds() + 1 )
  return [iDTime + dDTime*i for i in range(total_steps)]
#-----------------------------------
def ret_ms_region(iYear,eYear):
  lYear  = range(iYear,eYear+1)

  a3var1 = zeros([3,ny,nx],float32)
  for i,Mon in enumerate([6,7,8]):
    for Year in lYear:
      a3var1[i] = a3var1[i] + ra.load_mon(var, Year,Mon).Data
    a3var1[i] = a3var1[i]/len(lYear)

  a3var2 = zeros([3,ny,nx],float32)
  for i,Mon in enumerate([12,1,2]):
    for Year in lYear:
      a3var2[i] = a3var2[i] + ra.load_mon(var, Year,Mon).Data
    a3var2[i] = a3var2[i]/len(lYear)
 
  a2max = r_[ a3var2[:,:ny/2,:].max(axis=0), a3var1[:,ny/2:,:].max(axis=0)]
  a2min = r_[ a3var1[:,:ny/2,:].min(axis=0), a3var2[:,ny/2:,:].min(axis=0)]

  return a2max - a2min
 
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
a2msregion = ret_ms_region(1980,1999)

a2max  = ret_maxmin_ave(1980,1999,maxmin="max")
a2min  = ret_maxmin_ave(1980,1999,maxmin="min")


a2sdayInit = empty([ny,nx],float32)
a2edayInit = empty([ny,nx],float32)

a2sdayInit[:ny/2,:] = 183
a2sdayInit[ny/2:,:] = 1

a2edayInit[:ny/2,:] = 183
a2edayInit[ny/2:,:] = 1

a2sday  = ones([ny,nx],float32)*miss
a2eday  = ones([ny,nx],float32)*miss

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
dlOnflag ={} 
dlReflag ={} 
for i,latlon in enumerate(llatlon):
  dlnpwi[i]   = []
  dlOnflag[i] = []
  dlReflag[i] = []

for DTime in lDTime:
  #-- check --
  a2var0  = ret_a2var(var, DTime, lev)
  a2var1  = ret_a2var(var, DTime-timedelta(hours=24),   lev)
  a2var2  = ret_a2var(var, DTime-timedelta(hours=24*2), lev)
  a2var3  = ret_a2var(var, DTime+timedelta(hours=24),   lev)
  a2var4  = ret_a2var(var, DTime+timedelta(hours=24*2), lev)

  #a2Onflag = CheckOnset3Days(a2var0, a2var1, a2var2, a2min, a2max)
  a2Onflag = CheckOnset4Days(a2var0, a2var1, a2var2, a2var3, a2min, a2max)
  #a2Onflag = CheckOnset5Days(a2var0, a2var1, a2var2, a2var3, a2var4, a2min, a2max)
  #a2Onflag = CheckNPWI5Days(a2var0, a2var1, a2var2, a2var3, a2var4, a2min, a2max)
  #a2Onflag = AveNPWI5Days(a2var0, a2var1, a2var2, a2var3, a2var4, a2min, a2max)

  a2Reflag = CheckRetreat3Days(a2var0, a2var1, a2var2, a2min, a2max)


  a2msOn   = Check9grids(a2Onflag)
  #a2msOn   = Ave9grids(a2Onflag)
  #a2msOn   = a2Onflag
  a2msRe   = Check9grids(a2Reflag)

  a2npwi  = (a2var0 - a2min)/(a2max - a2min)

  for i,latlon in enumerate(llatlon):
    lat,lon = latlon
    iy,ix   = latlon2yx(lat,lon)
    dlnpwi[i].append(a2npwi[iy,ix])
    dlOnflag[i].append(a2msOn[iy,ix])
    dlReflag[i].append(a2msRe[iy,ix])
  #-----------
  days   = (DTime - iDTime).days
  a2sday = ma.masked_where((a2msOn==1.)&(a2sdayInit < days)&(a2sday==miss), a2sday).filled(days)
  a2eday = ma.masked_where((a2msRe==1.)&(a2sdayInit < days)&(a2sday!=miss)&(a2eday==miss), a2eday).filled(days)


#-- load monsoon region ---
regionDir  = "."
regionPath = regionDir + "/ms.Region.bn"
a2region   = fromfile(regionPath, float32).reshape(ny,nx)

a2sday = ma.masked_where(a2region==miss, a2sday)
a2eday = ma.masked_where(a2region==miss, a2eday)

oDir   = "."
sdayPath  = oDir + "/ms.Sday.bn"
edayPath  = oDir + "/ms.Eday.bn"
a2sday.filled(miss).tofile(sdayPath)
a2eday.filled(miss).tofile(edayPath)
print sdayPath


lout = [dlnpwi[i] for i in range(len(llatlon))]
aout = array(lout).T
sout = util.array2csv(aout)
csvname = "./ms.Np.csv"
f=open(csvname,"w"); f.write(sout); f.close(); print csvname

lout = [dlOnflag[i] for i in range(len(llatlon))]
aout = array(lout).T
sout = util.array2csv(aout)
csvname = "./ms.On.csv"
f=open(csvname,"w"); f.write(sout); f.close(); print csvname

lout = [dlReflag[i] for i in range(len(llatlon))]
aout = array(lout).T
sout = util.array2csv(aout)
csvname = "./ms.Re.csv"
f=open(csvname,"w"); f.write(sout); f.close(); print csvname
