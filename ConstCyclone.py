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
      self.exrvort = 3.7*1.0e-5 # s-1  lower 5%
      #self.exrvort = 3.3*1.0e-5 # s-1  lower 3%
      self.tcrvort = 4.0*1.0e-5 # s-1  lower 5%
      #self.thwcore = 0.0        # K
      self.thwcore = 0.2        # K  lower 5% (approx.)

    elif (cfg["prj"]=="HAPPI")&(cfg["model"]=="MIROC5"):
      # "HAPPI","128x256"

      # For Tuning
      lrun = cfg["run"].split("-")
      tune = float(lrun[3])*0.01
 
      self.thpgrad = 325.0      # Pa/1000km lower 5% of ExC
      self.exrvort = 3.7*1.0e-5 *tune # s-1  lower 5%
      #self.exrvort = 3.3*1.0e-5 # s-1  lower 3%
      self.tcrvort = 4.0*1.0e-5 # s-1  lower 5%
      #self.thwcore = 0.0        # K
      self.thwcore = 0.2        # K  lower 5% (approx.)


