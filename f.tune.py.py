from numpy import *
import os, csv

lYear  = [2004]
#tqtype= "t"
tqtype= "q"

if tqtype == "t":
  lMon   = [1,2,3,4,5,6,7,8,9,10,11,12]
elif tqtype == "q":
  lMon   = [6,7,8]

#model  = "JRA25"
model  = "JRA55"
res    = "bn"
srcDir = "/media/disk2/out/obj.valid/front.para/%s.%s"%(model, res)

lM1   = []
lM2   = []
dlout = {}

for Year,Mon in [[Year,Mon] for Year in lYear for Mon in lMon]:
  srcPath = os.path.join(srcDir,"%s.RMSE.%04d.%02d.csv"%(tqtype,Year,Mon))
  f = open(srcPath, "rb")
  reader = csv.reader(f, delimiter=",")
#  f.close()
  reader.next()  # skip header

  for line in reader:
    M1  = float(line[0])
    M2  = float(line[1])
    rmse= float(line[2])
    lM1.append(M1)
    lM2.append(M2)

    if dlout.has_key((M1,M2)):
      dlout[ M1, M2 ].append( rmse )
    else:
      dlout[ M1,M2 ] = [rmse]


lM1  = sort(list( set(lM1) ))
lM2  = sort(list( set(lM2) ))

for key in dlout.keys():
  dlout[key] = mean( map( float, dlout[key] ))


label = ["M1/M2"]+[M2 for M2 in lM2]
lout = [label]
for M1 in lM1:
  lout.append([M1] + [ dlout[M1,M2] for M2 in lM2])

outPath = os.path.join(srcDir, "%s.RMSE.csv"%(tqtype))
f = open(outPath, "w")
writer = csv.writer(f)
writer.writerows(lout)
f.close()
print outPath




