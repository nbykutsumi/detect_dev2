class Const(object):
  def __init__(self, **kwargs):
    cfg = kwargs["cfg"]

    self.thtopo    = 1500 # m
    self.thdura    = 36   # hours
    #self.thsst     = 273.15  + 25.0  # K
    self.thsst     = 273.15  + 27.0  # K

    if cfg["prj"]=="JRA55":
      # "JRA55","145x288
      self.thpgrad = 325.0      # Pa/1000km lower 5% of ExC
      self.exrvort = 3.7*1.0e-5 # s-1  lower 5%  --> Default
      #self.exrvort = 3.3*1.0e-5 # s-1  lower 3%
      self.tcrvort = 4.0*1.0e-5 # s-1  lower 5%
      #self.thwcore = 0.0        # K
      self.thwcore = 0.2        # K  lower 5% (approx.)

    elif (cfg["prj"]=="HAPPI")&(cfg["model"]=="MIROC5"):
      # "HAPPI","128x256"

      ## For Tuning
      #lrun = cfg["run"].split("-")
      #if len(lrun)>3:
      #  tune = float(lrun[3][:3])*0.01
      #else:
      #  print "no tune"
      #  tune = 1.0

      self.thpgrad = 325.0      # Pa/1000km lower 5% of ExC
      self.exrvort = 3.7*1.0e-5 *1.3     # s-1  lower 5%
      self.tcrvort = 3.7*1.0e-5 *1.3 *1.3# s-1  lower 5%
      self.thwcore = 0.2        # K  lower 5% (approx.)

      #if (len(lrun)==5):
      #  if lrun[4][0]=="t":
      #    self.thwcore = float(lrun[4][1:3])*0.1 

      #print "*"*50
      #print "tcrvort",self.tcrvort
      #print "thwcore",self.thwcore 
