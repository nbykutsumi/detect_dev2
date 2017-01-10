from numpy import *
import myfunc.grids as grids
import numpy as np

miss = -99
x    = arange(5)
y    = arange(5)
X, Y = np.meshgrid(x,y)
print X
print Y

print "*"*50
dy, dx = -2,0
print grids.shift_map(X, dy, dx, miss)
print grids.shift_map(Y, dy, dx, miss)
