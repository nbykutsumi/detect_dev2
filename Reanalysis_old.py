import sys
import JRA55
import JRA25

def Reanalysis(model, res):
  if   model=="JRA55":
    self = JRA55.Jra55(res)
  elif (model=="JRA25")&(res=="sa.one"):
    self = JRA25.Jra25saone()
  elif (model=="JRA25")&(res=="bn"):
    self = JRA25.Jra25(res)
  else:
    print "check 'model'"
    sys.exit()
  return self
  
