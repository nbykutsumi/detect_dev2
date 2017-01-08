from numpy import *
from detect_fsub import *
from datetime import datetime
import Reanalysis
import Cyclone
import calendar
import os, sys, shutil
#--------------------------------------------------
tstp        = "6hr"
hinc        = 6
iyear       = 1981
eyear       = 1990
#iyear       = 2015
#eyear       = 2015
imon        = 1
emon        = 12
#imon        = 2
#emon        = 4
miss        = -9999.0
#lmodel = ["org","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
#lmodel = ["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3","org"]
lmodel = ["JRA55"]
res    = "bn"
#####################################################
def var_psl(model):
  # variable name for mean sea level pressure
  if model in ["JRA25","JRA55"]:
    return "PRMSL"

def check_file(sname):
  if not os.access(sname, os.F_OK):
    print "no file:",sname
    sys.exit()
#####################################################
def mk_dir(sdir):
  try:
    os.makedirs(sdir)
  except:
    pass
#################################################
def mk_dir_tail(var, tstp, model, expr, ens):
  odir_tail = var + "/" + tstp + "/" +model + "/" + expr +"/"\
       +ens
  return odir_tail
#####################################################
def mk_namehead(var, tstp, model, expr, ens):
  namehead = var + "_" + tstp + "_" +model + "_" + expr +"_"\
       +ens
  return namehead
#****************************************************
def read_txtlist(iname):
  f = open(iname, "r")
  lines = f.readlines()
  f.close()
  lines = map(float, lines)
  aout  = array(lines, float32)
  return aout
#****************************************************
for model in lmodel:
  ra = Reanalysis.Reanalysis(model=model, res=res)
  #-- copy lat and lon file --
  prdType  = ra.path_6hr(var_psl(model), datetime(2014,1,1,0)).prdType
  iNameLat = os.path.join(ra.baseDir, "%s.%s"%(res,prdType), "lat.txt")
  iNameLon = os.path.join(ra.baseDir, "%s.%s"%(res,prdType), "lon.txt")

  mk_dir( Cyclone.ret_baseDir(model,res))
  shutil.copy(iNameLat, Cyclone.ret_baseDir(model,res))
  shutil.copy(iNameLon, Cyclone.ret_baseDir(model,res))

  #---------------------------  
  cy = Cyclone.Cyclone(model=model, res=res)
  #-----
  varPSL  = var_psl(model)
  varTOPO = var_psl(model)

  a1lat = ra.Lat
  a1lon = ra.Lon
  ny    = ra.ny
  nx    = ra.nx


#  #****************************************************
#  # dir_root
#  #---------------
#  psldir_root     = "/media/disk2/data/JRA55/bn.%s/%s/PRMSL"%(model,tstp)
#  pslmeandir_root = "/media/disk2/data/JRA55/bn.%s/my.mean/PRMSL"%(model)
#  axisdir_root    = psldir_root
#  #-- out ---
#  if model == "anl_surf125":
#    pgraddir_root   = "/media/disk2/out/JRA55/bn/%s/pgrad"%(tstp)
#  else:
#    pgraddir_root   = "/media/disk2/out/JRA55/bn/%s/pgrad"%(tstp)
#  #****************************************************
#  # read lat, lon data
#  #----------------------
#  axisdir    = axisdir_root  + "/%04d/%02d"%(iyear, imon)
#  latname    = axisdir  + "/lat.txt"
#  lonname    = axisdir  + "/lon.txt"
#  a1lat      = read_txtlist(latname)
#  a1lon      = read_txtlist(lonname)

  ##**************************************************
  ## Mean Sea Level Pressure
  ##------------------------
  #pslmeanname = pslmeandir_root + "/anl_surf125.PRMSL.0000000000.sa.one"
  #a2pslmean = fromfile(pslmeanname, float32).reshape(ny, nx)
  ##------------------------
  for year in range(iyear, eyear+1):
    #---------
    for mon in range(imon, emon+1):
      #---------
      # dirs
      #---------
#      psldir   = psldir_root   + "/%04d/%02d"%(year, mon)
#      pgraddir = pgraddir_root + "/%04d/%02d"%(year, mon)
      pgraddir = cy.path_a2dat("pgrad",datetime(year,mon,1)).srcDir
      mk_dir(pgraddir)
  
      ed = calendar.monthrange(year,mon)[1]
      ##############
      for day in range(1, ed+1):
      #for day in range(28, ed+1):
        for hour in range(0, 23+1, hinc):
#          stimeh  = "%04d%02d%02d%02d"%(year,mon,day,hour)
          DTime   = datetime(year,mon,day,hour)
          #***************************************
          #* names
          #---------------------------------------
#          pgradname = pgraddir + "/pgrad.%s.bn"%(stimeh)
          pgradname = cy.path_a2dat("pgrad",DTime).srcPath
      
#         #***************************************
#          a2psl   = fromfile(pslname,   float32).reshape(ny, nx)
          a2psl   = ra.load_6hr(varPSL, DTime).Data
          findcyclone_out = detect_fsub.findcyclone_bn(a2psl.T, a1lat, a1lon, -9999.0, miss)
          a2pgrad = findcyclone_out.T
          a2pgrad.tofile(pgradname)

          print pgradname



 
