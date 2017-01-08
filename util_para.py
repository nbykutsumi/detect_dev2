from numpy import *

#-----------------------------------
def ret_lmon(season):
  if season == "DJF":
    lmon  = [1,2, 12]
  elif season == "MAM":
    lmon  = [3,4,5]
  elif season == "JJA":
    lmon  = [6,7,8]
  elif season == "SON":
    lmon  = [9,10,11]
  elif season == "ALL":
    lmon  = [1,2,3,4,5,6,7,8,9,10,11,12]
  elif type(season) == int:
    lmon  = [season]
  elif season == "NDJFMA":
    lmon  = [11,12,1,2,3,4]
  elif season == "MJJASO":
    lmon  = [5,6,7,8,9,10]
  elif season == "JJASON":
    lmon  = [6,7,8,9,10,11]
  elif season == "JJAS":
    lmon  = [6,7,8,9]
  elif season == "JASO":
    lmon  = [7,8,9,10]
  elif season == "JFMA":
    lmon  = [1,2,3,4]
  elif season == "DJFM":
    lmon  = [12,1,2,3]
  elif season == "NoJune":
    lmon  = [1,2,3,4,5,7,8,9,10,11,12]
  elif season == "NoJJ":
    lmon  = [1,2,3,4,5,8,9,10,11,12]
  return lmon

#----------------------------------------------------------
def ret_tcregionlatlon(region):
  if region=="SH60":
    lllat = -59.5
    lllon = 0.5
    urlat = -0.5
    urlon = 359.5

  if region=="NH60":
    lllat = 0.5
    lllon = 0.5
    urlat = 59.5
    urlon = 359.5

  if region=="GLB60":
    lllat = -59.5
    lllon = 0.5
    urlat = 59.5
    urlon = 359.5

  if region in ["GLB","GLOB"]:
    lllat = -89.5
    lllon = 0.5
    urlat = 89.5
    urlon = 359.5
  if region=="PNW":
    lllat = 0.0
    lllon = 100.0
    urlat = 50.0
    urlon = 180.0
  if region=="PNE":
    lllat = 0.0
    lllon = 180.0
    urlon = 270.0
    urlat = 40.0
  if region=="INN":
    lllat = 0.0
    lllon = 45.0
    urlat = 30.0
    urlon = 100.0
  if region=="INS":
    lllat = -45.0
    lllon = 30.0
    urlat = 0.0
    urlon = 140.0
  if region=="PSW":
    lllat = -45.0
    lllon = 140.0
    urlat = 0.0
    urlon = 240.0
  if region=="ATN":
    lllat = 0.0
    lllon = 270.0
    urlat = 50.0
    urlon = 360.0
  #------------
  return lllat, lllon, urlat, urlon

