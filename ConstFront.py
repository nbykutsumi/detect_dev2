import sys

myname = "ConstFront.py"

class Const(object):
  def __init__(self, prj="JRA55", model="__",run="__", res="145x288"):
    if (prj,res) == ("JRA55","145x288"):
      self.thM1t = 0.30  # K/100km/100km
#      self.thM2t = 1.4   # K/100km
      self.thM2t = 0.6   # K/100km

      self.thM1q = 2.3*1.0e-4   # temporary 
      self.thM2q = 0.9*1.0e-3   # temporary 
      self.thgrids= 5/1.25

    elif (prj,res) == ("JRA25","sa.one"):
      self.thM1t = 0.30  # K/100km/100km
      self.thM2t = 1.0   # K/100km
      self.thM1q = 2.0*1.0e-4   # temporary 
      self.thM2q = 1.5*1.0e-3   # temporary 
      self.thgrids= 5

    elif (prj,res) == ("JRA25","bn"):
      self.thM1t = 0.26  # K/100km/100km
      self.thM2t = 1.0   # K/100km
      self.thM1q = 1.7*1.0e-4   # temporary 
      self.thM2q = 1.2*1.0e-3   # temporary 
      self.thgrids= 5/1.25

    elif (prj,model,res) == ("HAPPI","MIROC5","128x256"):
      self.thM1t = 0.30  # K/100km/100km
#      self.thM2t = 1.4   # K/100km
      self.thM2t = 0.6   # K/100km

      self.thM1q = 2.3*1.0e-4   # temporary 
      self.thM2q = 0.9*1.0e-3   # temporary 
      self.thgrids= 5/1.25

    else:
      print myname,":check model,res",model,res
      sys.exit()

    #-- orog --
    self.thorog = 1000.0  # m
    self.thgradorog = 1.0e+8 # m/m
    #-- fill --
    self.trace_coef = 0.8


  def thfmask(self,model,res):
    thM1t = self.thM1t
    thM2t = self.thM2t
    thM1q = self.thM1q
    thM2q = self.thM2q
    return thM1t, thM2t, thM1q, thM2q
