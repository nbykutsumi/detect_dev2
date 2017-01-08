from numpy import *
import Image
import util
import os, sys

Year    = 2006
lMon    = range(1,12+1)
baseDir = "/home/utsumi/mnt/well.share/temp"
figdir  = os.path.join(baseDir, "pict")
util.mk_dir(figdir)

#lvar = ["qwind","d.qwind","wind","d.wind"]
lvar = ["qwind","d.qwind","wind","d.wind"]
for var in lvar:
    da2dat  = {}
    for Mon in lMon:
        srcPath = os.path.join(baseDir, "pict","%s.%04d.%02d.png"%(var, Year, Mon))
        iimg    = Image.open(srcPath)
        a2array = asarray(iimg)
        print shape(a2array)
        da2dat[Mon] = a2array
    
    a2line1 = hstack([ da2dat[1], da2dat[2], da2dat[3]]) 
    a2line2 = hstack([ da2dat[4], da2dat[5], da2dat[6]]) 
    a2line3 = hstack([ da2dat[7], da2dat[8], da2dat[9]]) 
    a2line4 = hstack([ da2dat[10], da2dat[11], da2dat[12]]) 
    
    oa2array= vstack([a2line1, a2line2, a2line3, a2line4])
    
    oPath = os.path.join(baseDir, "pict", "join.%s.png"%(var))
    oimg  = Image.fromarray(oa2array)
    oimg.save(oPath)
    print oPath
