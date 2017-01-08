from numpy import *
from datetime import datetime
import HAPPI
prj = "C20"
expr= "ALL"
ens = 1

hp = HAPPI.Happi()
hp(prj, expr, ens)

var   = "T500"
DTime = datetime(2006,1,2,0)
a     = hp.load_6hr(var, DTime)
print a
