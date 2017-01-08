from numpy import *
from datetime import datetime
from Tag import Tag
#from regrid import Regrid
from myfunc.regrid import Regrid
#from cf import biIntp

class TagRegrid(Tag):
#  def __init__(self, model="JRA55", LatOut=False, LonOut=False, miss=-9999.):
  def __init__(self, cfg, LatOut=False, LonOut=False, miss=-9999.):
    """
    LatOut and LonOut can be used to extract regional domain
    """
    Tag.__init__(self, cfg, miss=miss)
    self.LatIn   = self.Front.Lat
    self.LonIn   = self.Front.Lon
    self.LatOut  = LatOut
    self.LonOut  = LonOut

  def mkMaskRegrid(self, ltag, DTime, miss=0.0):
    """
    ltag = ["tag1", "tag2", ...], without "ot"
    """
    dictMask = {}
    for tag in ltag:
      #aMaskFrac     = biIntp(\
      aMaskFrac     = Regrid.biIntp(\
                      self.LatIn, self.LonIn   \
                    , self.mkMask(tag, DTime, miss=0.0) \
                    , self.LatOut, self.LonOut \
                    )[0]

      dictMask[tag] = ma.masked_greater_equal(\
                        ma.masked_less(aMaskFrac, 0.5).filled(0.0) \
                      , 0.5 \
                     ).filled(1.0)

    return dictMask

  def mkMaskFracRegrid(self, ltag, DTime, miss=0.0):
    return self.mkMaskFracCore(\
             self.mkMaskRegrid(ltag, DTime, miss) \
            ,miss \
            )
 
