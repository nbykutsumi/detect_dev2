import os
import config_func
import util
import IO_Master

prj     = "JRA55"
model   = "__"
run     = "__"
res     = "145x288"

#prj     = "HAPPI"
#model   = "MIROC5"
#run     = "C20-ALL-001"
#res     = "128x256"

cfg = config_func.config_func(prj, model, run)
iom = IO_Master.IO_Master(prj, model, run, res)

baseDir = cfg["baseDir"]
Lat = iom.Lat
Lon = iom.Lon

# Make baseDir
print "*"*50
print "make baseDir"
print baseDir
util.mk_dir(baseDir)

# Make axis info
latPath = os.path.join(baseDir, "lat.txt")
lonPath = os.path.join(baseDir, "lon.txt")
sLat    = "\n".join(map(str, Lat)).strip()
sLon    = "\n".join(map(str, Lon)).strip()

f=open(latPath,"w"); f.write(sLat); f.close()
f=open(lonPath,"w"); f.write(sLon); f.close()
print "*"*50
print "make axis info"
print latPath
print lonPath
