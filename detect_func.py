from numpy import *
import os
####################################################
def mk_dir(sdir):
  try:
    os.makedirs(sdir)
  except:
    pass
#---------------------------------------------------
def solve_time(stime):
  year = int( stime/10**6 )
  mon  = int( (stime - year*10**6)/10**4 )
  day  = int( (stime - year*10**6 - mon*10**4)/10**2)
  hour = int( (stime - year*10**6 - mon*10**4 - day*10**2) )
  return year, mon, day, hour
#---------------------------------------------------
def fortpos2pyxy(number, nx, miss_int):
  if (number == miss_int):
    iy_py = miss_int
    ix_py = miss_int
  else:
    iy_py = int((number-1.0)/nx)      # iy_py = 0,1,2,..
    ix_py = number - nx*iy_py-1   # ix_py = 0,1,2,..
  #----
  return ix_py, iy_py
#---------------------------------------------------


