from numpy import *
from datetime import datetime
import Cyclone

dtime = datetime(2004,3,5,0)
c= Cyclone.cyclone(model="JRA55",res="bn")
path = c.path_a2dat("pgrad",dtime)

print path.srcDir

a2dat = c.load_a2dat("pgrad",dtime)
print a2dat

a1clist = c.load_clist("idate",2004,5)
print a1clist
