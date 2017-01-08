from numpy import *
from datetime import datetime, timedelta
import os, sys
import Reanalysis
import socket

def Check9grids(a2flag,miss_out=-9999.):
  ny,nx    = shape(a2flag)
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
  return ma.masked_where(a2count <7, ones([ny,nx], float32)).filled(miss_out)


class MonsoonMoist(object):
  def __init__(self, model="JRA55", res="bn", var="PWAT",miss=-9999.):
    #----------------
    hostname = socket.gethostname()
    if hostname == "well":
      self.rootDir  = "/media/disk2"
    if hostname in ["mizu","naam"]:
      self.rootDir  = "/tank/utsumi"
    #----------------
    self.ra = Reanalysis.Reanalysis(model="JRA55",res="bn")

    self.model  = model
    self.res    = res
    self.var    = var
    self.miss   = miss
    self.Lat    = self.ra.Lat
    self.Lon    = self.ra.Lon
    self.ny     = self.ra.ny
    self.nx     = self.ra.nx
    self.thrat  = 0.618
    self.dPWAT  = {"JRA55":"PWAT"}
    self.dSPFH  = {"JRA55":"spfh"}
    self.dstypePWAT = {"JRA55":"anl_column125"}
    self.dstypeSPFH = {"JRA55":"anl_p125"}


  def prepMonsoonMoist(self):
    if self.var == "PWAT":
      self.a2min    = self.mkAveMaxMinPWAT(1980,1999, maxmin="min")
      self.a2max    = self.mkAveMaxMinPWAT(1980,1999, maxmin="max")
      self.a2region = self.loadRegionW14(1980,1999)

  def pathRegionW14(self, iYear, eYear):
    rootDir = self.rootDir
    srcDir  = rootDir + "/out/%s/%s/const/ms.region/W14"%(self.model,self.res)
    srcPath = srcDir  + "/region.%04d-%04d.%s"%(iYear,eYear,self.res)
    return rootDir, srcDir, srcPath

  def loadRegionW14(self, iYear, eYear):
    srcPath = self.pathRegionW14(iYear, eYear)[-1]
    return fromfile(srcPath, float32).reshape(self.ny, self.nx)

  def pathMaxMinPWAT(self, Year,maxmin="max"):
    model  = self.model
    res    = self.res
    rootDir = self.rootDir
    srcDir  = rootDir + "/out/%s/%s/6hr/ms.%s/%s"%(model,res,maxmin,self.dPWAT[model])
    srcPath = srcDir  + "/%s.%s.%s.%04d.%s"%(maxmin,self.dstypePWAT[model],self.dPWAT[model],Year,res)
    return rootDir, srcDir, srcPath

  def mkAveMaxMinPWAT(self, iYear,eYear,maxmin="max"):
    ny,nx  = self.ny, self. nx
    miss   = self.miss
    lYear  = range(iYear,eYear+1)
    a3dat  = zeros([len(lYear), self.ny, self.nx])
    for i,Year in enumerate(lYear):
      sPath     = self.pathMaxMinPWAT(Year, maxmin)[-1]
      a2in      = ma.masked_equal(fromfile(sPath, float32).reshape(ny,nx), miss)
      a3dat[i]  = a2in
    return a3dat.mean(axis=0)

  def mkDailyVar(self, DTime):
    if self.var == "PWAT":
      var   = self.dPWAT[self.model]
      return self.ra.time_ave(var, DTime, DTime+timedelta(hours=23), timedelta(hours=6))


  def pathMonsoonMoist(self, DTime):
    model   = self.model
    res     = self.res
    rootDir = self.rootDir
    Year    = DTime.year
    Mon     = DTime.month
    Day     = DTime.day 
    var     = self.var
 
    srcDir  = rootDir + "/%s/6hr/ms.%s/%04d/%02d"%(res,var,Year,Mon) 
    srcPath = srcDir  + "/ms.%04d.%02d.%02d.%s"%(Year,Mon,Day,res)
    return rootDir, srcDir, srcPath


  def mkMonsoonMoist(self, DTime, miss_out=-9999.):
    model   = self.model
    ny, nx  = self.ny, self.nx
    DTime0  = datetime(DTime.year, DTime.month, DTime.day, 0)
    a2var0  = self.mkDailyVar(DTime0)
    a2var1  = self.mkDailyVar(DTime0-timedelta(hours=24))
    a2var2  = self.mkDailyVar(DTime0-timedelta(hours=24*2))
    a2var3  = self.mkDailyVar(DTime0+timedelta(hours=24))
    a2var4  = self.mkDailyVar(DTime0+timedelta(hours=24*2))
       
    a2npwi = ((a2var0+a2var1+a2var2+a2var3+a2var4)/5 - self.a2min)/(self.a2max-self.a2min)
    #a2out  = ma.masked_where(a2npwi<self.thrat, ones([ny,nx],float32)).filled(miss_out)
    a2out  = ma.masked_where(a2npwi<self.thrat, ones([ny,nx],float32)).filled(0.0)
    a2out  = Check9grids(a2out,miss_out=miss_out)
    return ma.masked_where(self.a2region==self.miss, a2out).filled(miss_out)

  def loadMonsoonMoist(self, DTime, maskflag=False):
    sPath  = self.pathMonsoonMoist(DTime)[-1]
    if maskflag == False:
      return fromfile(sPath, float32).reshape(self.ny, self.nx)
    elif maskflag == True:
      return ma.masked_equal(fromfile(sPath, float32).reshape(self.ny, self.nx), self.miss)
