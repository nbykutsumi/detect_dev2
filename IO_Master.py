from numpy import *
import os, sys

def IO_Master(prj, model, run, res):
    if prj=="JRA55":
        import IO_JRA55
        iom  = IO_JRA55.IO_Jra55(model, run, res)
   
    elif prj=="HAPPI":
        import IO_HAPPI
        iom  = IO_HAPPI.IO_Happi(model, run, res)

    return iom
