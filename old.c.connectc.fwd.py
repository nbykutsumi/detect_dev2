from numpy import *
from detect_fsub import *
import Reanalysis
import Cyclone
import ConstCyclone
import calendar
import datetime
import os, sys
##***************************
#--------------------------------------------------
#lmodel = ["org","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
#lmodel = ["anl_p125"]
lmodel   = ["JRA55"]
res     = "bn"
tstp    = "6hr"
hinc    = 6

#iyear       = 1980
#eyear       = 1990
#imon        = 1
#emon        = 12

iyear       = 2015
eyear       = 2015
imon        = 1
emon        = 1

#----------------
miss_dbl     = -9999.0
miss_int     = -9999
endh         = 18
thdp         = 0.0  #[Pa]
thdist_search = 500.0*1000.0   #[m]
#####################################################
# functions
#####################################################
def ret_var_ua(model):
  if model in ["JRA25"]:
    return "UGRD"
  elif model in ["JRA55"]:
    return "ugrd"

#####################################################
def ret_var_va(model):
  if model in ["JRA25"]:
    return "VGRD"
  elif model in ["JRA55"]:
    return "vgrd"
#####################################################
def ret_var_topo(model):
  if model in ["JRA25","JRA55"]:
    return "topo"
#####################################################
def fortxy2fortpos(ix, iy, nx):
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
#####################################################
def date_slide(year,mon,day, daydelta):
  today       = datetime.date(year, mon, day)
  target      = today + datetime.timedelta(daydelta)
  targetyear  = target.year
  #***********
  #if ( calendar.isleap(targetyear) ):
  #  leapdate   = datetime.date(targetyear, 2, 29)
  #  #---------
  #  if (target <= leapdate) & (leapdate < today):
  #    target = target + datetime.timedelta(-1)
  #  elif (target >= leapdate ) & (leapdate > today):
  #    target = target + datetime.timedelta(1)
  #-----------
  return target
#****************************************************
def read_txtlist(iname):
  f = open(iname, "r")
  lines = f.readlines()
  f.close()
  lines = map(float, lines)
  aout  = array(lines, float32)
  return aout
#******************************************************
for model in lmodel:
  ra       = Reanalysis.Reanalysis(model=model, res=res)
  cy       = Cyclone.Cyclone(model=model, res=res)
  var_topo = ret_var_topo(model) 
  var_ua   = ret_var_ua(model) 
  var_va   = ret_var_va(model) 

  #-- const --- 
  const    = ConstCyclone.Const(model=model, res=res)
  thtopo   = const.thtopo
 
  #****************************************************
  # read lat, lon data
  #----------------------
  a1lat, a1lon = ra.Lat, ra.Lon
  ny           = ra.ny
  nx           = ra.nx
  #**************************************************
  # read topo data
  a2topo      = ra.load_const(var_topo).Data
  a2mask_topo = ma.masked_greater(a2topo, thtopo)
  #**************************************************
  counter = 0
  for year in range(iyear, eyear+1):
  #for year in range(1990, 1990+1):
    #---------
    # dirs
    #---------
    for mon in range(imon, emon+1):
    #for mon in range(1, 1+1):
      print "connectc.fwd.py", model, "forward",year,mon
      ###############
      ed = calendar.monthrange(year,mon)[1]
      ##############
      for day in range(1, ed+1):
      #for day in range(ed, ed+1):
        print year,mon,day
        for hour in range(0, endh+1, hinc):
          #***********************
          counter = counter + 1
          #---------
          DTime1 = datetime.datetime(year,mon,day,hour)
          year1, mon1, day1, hour1 = DTime1.year, DTime1.month, DTime1.day, DTime1.hour

          DTime0 = DTime1 - datetime.timedelta(hours=hinc)
          year0, mon0, day0, hour0 = DTime0.year, DTime0.month, DTime0.day, DTime0.hour
          stimed0= "%04d%02d%02d%02d"%(year0,mon0,day0,0)
    
          #***************************************
          #* names for 0
          #---------------------------------------
          pgradname0   = cy.path_a2dat("pgrad",  DTime0).srcPath
          preposname0  = cy.path_a2dat("prepos",DTime0).srcPath
          lastposname0 = cy.path_a2dat("lastpos",DTime0).srcPath  # temp
          #pgmaxname0   = cy.path_a2dat("pgmax",  DTime0).srcPath
          iposname0    = cy.path_a2dat("ipos",   DTime0).srcPath
          idatename0   = cy.path_a2dat("idate",  DTime0).srcPath
          agename0     = cy.path_a2dat("age",   DTime0).srcPath
          timename0    = cy.path_a2dat("time",   DTime0).srcPath  # temp

          uadir0       = os.path.join(cy.baseDir,"run.mean",var_ua,"%02d"%(year0),"%02d"%(mon0))
          vadir0       = os.path.join(cy.baseDir,"run.mean",var_va,"%02d"%(year0),"%02d"%(mon0))

          uaname0     =  os.path.join(uadir0, "run.mean.%s.0500hPa.%s.bn"%(var_ua, stimed0))
          vaname0     =  os.path.join(vadir0, "run.mean.%s.0500hPa.%s.bn"%(var_va, stimed0))

          #***************************************
          #* names for 1
          #---------------------------------------
          preposdir1  = cy.path_a2dat("prepos",DTime1).srcDir
          #pgmaxdir1   = cy.path_a2dat("pgmax",  DTime1).srcDir
          iposdir1    = cy.path_a2dat("ipos",   DTime1).srcDir
          idatedir1   = cy.path_a2dat("idate",  DTime1).srcDir
          agedir1    = cy.path_a2dat("age",     DTime1).srcDir

          mk_dir(preposdir1)
          #mk_dir(pgmaxdir1)
          mk_dir(iposdir1)
          mk_dir(idatedir1)
          mk_dir(agedir1)

          pgradname1   = cy.path_a2dat("pgrad",  DTime1).srcPath
          preposname1  = cy.path_a2dat("prepos", DTime1).srcPath
          #pgmaxname1   = cy.path_a2dat("pgmax",  DTime1).srcPath
          iposname1    = cy.path_a2dat("ipos",   DTime1).srcPath
          idatename1   = cy.path_a2dat("idate",  DTime1).srcPath
          agename1    = cy.path_a2dat("age",   DTime1).srcPath

          #***************************************
          # read data
          #---------------------------------------
          #   for 0
          #************
          if ( os.access(iposname0, os.F_OK) ):
            a2pgrad0   = fromfile(pgradname0,   float32).reshape(ny, nx)
            a2ua0      = fromfile(uaname0,      float32).reshape(ny, nx)
            a2va0      = fromfile(vaname0,      float32).reshape(ny, nx)
            #--
            try:   # temp 
              a2prepos0 = fromfile(preposname0, int32).reshape(ny, nx)
            except IOError:
              a2prepos0 = fromfile(lastposname0, int32).reshape(ny, nx)

            #a2pgmax0   = fromfile(pgmaxname0,   float32).reshape(ny, nx)
            a2ipos0    = fromfile(iposname0,    int32).reshape(ny, nx)
            a2idate0   = fromfile(idatename0,   int32).reshape(ny, nx)
   
            #-- 
            try: 
              a2age0    = fromfile(agename0,    int32).reshape(ny, nx)
            except IOError:
              a2age0    = fromfile(timename0,   int32).reshape(ny, nx)
   
          elif ( counter == 1):
            a2pgrad0    = array(ones(ny*nx).reshape(ny,nx)*miss_dbl, float32)
            a2ua0      = array(zeros(ny*nx).reshape(ny,nx), float32)
            a2va0      = array(zeros(ny*nx).reshape(ny,nx), float32)
            #--
            a2prepos0 = array(ones(ny*nx).reshape(ny,nx)*miss_int, int32)
            #a2pgmax0   = array(ones(ny*nx).reshape(ny,nx)*miss_dbl, float32)
            a2ipos0    = array(ones(ny*nx).reshape(ny,nx)*miss_int, int32)
            a2idate0   = array(ones(ny*nx).reshape(ny,nx)*miss_int, int32)
            a2age0    = array(ones(ny*nx).reshape(ny,nx)*miss_int, int32)
          else:
            print "nofiles: DTime0 = ",DTime0
            print "iposname0 =", iposname0
            sys.exit()
          #------------
          #   for 1
          #************
          a2pgrad1     = fromfile(pgradname1, float32).reshape(ny, nx)


          #*********************
          # mask high altitudes
          a2pgrad0   = ma.masked_where(a2mask_topo.mask, a2pgrad0).filled(miss_dbl)
          a2pgrad1   = ma.masked_where(a2mask_topo.mask, a2pgrad1).filled(miss_dbl)

          #****************************************
          # connectc
          ##***************************************
          ctrackout = detect_fsub.connectc_bn_nopgmax(\
             a2pgrad0.T, a2pgrad1.T, a2ua0.T, a2va0.T\
             , a2ipos0.T, a2idate0.T, a2age0.T\
             , a1lon, a1lat, thdp, thdist_search, hinc, miss_dbl, miss_int\
             , year1, mon1, day1, hour1\
             )

  
          a2prepos1 = array(ctrackout[0].T, int32)
          a2ipos1    = array(ctrackout[1].T, int32)
          a2idate1   = array(ctrackout[2].T, int32)
          a2age1    = array(ctrackout[3].T, int32)

          #****************************************
          # write to file
          #----------------------------------------
          a2prepos1.tofile(preposname1)
          #a2pgmax1.tofile(pgmaxname1)
          a2ipos1.tofile(iposname1)
          a2idate1.tofile(idatename1)
          a2age1.tofile(agename1)
  

