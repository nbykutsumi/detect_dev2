from numpy import *
from datetime import datetime
from detect_fsub import *
import JRA55
import fig.Fig as Fig

Y = 2004
M = 6
D = 25
H = 0
DTime = datetime(Y,M,D,H)
jra = JRA55.jra55()
a1lat = jra.Lat
a1lon = jra.Lon
q     = jra.load_bn("spfh",DTime, 850)
u     = jra.load_bn("ugrd",DTime, 850)
v     = jra.load_bn("vgrd",DTime, 850)
BBox  = [[0,100],[60,180]]


dqdx  = detect_fsub.calc_dodx(q.T, a1lon, a1lat).T
dqdy  = detect_fsub.calc_dody(q.T, a1lat).T

dudx  = detect_fsub.calc_dodx(u.T, a1lon, a1lat).T
dudy  = detect_fsub.calc_dody(u.T, a1lat).T

dvdx  = detect_fsub.calc_dodx(v.T, a1lon, a1lat).T
dvdy  = detect_fsub.calc_dody(v.T, a1lat).T

A     = dudx - dvdy
B     = dvdx + dudy
C     = ma.masked_equal( abs(dqdx+dqdy), 0.0)

FG3   = -0.5*(1.0/C)\
       *( \
         (square(dqdx) - square(dqdy)) * A\
         + 2.0*dqdx*dqdy *B\
        )

FG3   = FG3*1000.*60*60*24.  # (kg/kg)/km/sec --> (kg/kg)/1000km/day
FG3   = ma.masked_greater(FG3, 100).filled(100)
FG3   = ma.masked_less(FG3, 0)
fgname= "./temp.fg.png"
Fig.DrawMap(FG3, a1lat, a1lon, BBox, fgname)
