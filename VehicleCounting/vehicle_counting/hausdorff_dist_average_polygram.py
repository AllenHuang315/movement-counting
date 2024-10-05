import numpy as np
import numba
import random
#import distances
from inspect import getmembers
from math import sqrt

#@numba.jit(nopython=True, fastmath=True)
def euclidean(array_x, array_y):
    ret = 0
    ret += ((array_x[0]-array_y[0])**2 + (array_x[1]-array_y[1])**2)
    return sqrt(ret)

#@numba.jit(nopython=True, fastmath=True)
def _hausdorff(XA, XB):
    sum = 0
    for i in range(len(XA)): 
        cmin = float("inf")
        for j in range(len(XB)):
            # compare one tracklet point and one typical trajectory point at a time
            d = euclidean(XA[i], XB[j]) 
            if d < cmin:
                cmin = d
        sum += cmin
    return float(sum/len(XA)) # return the average minumum distance through the whole set

def hausdorff_distance(XA, XB): # compare one typical trajectory at one time
    return _hausdorff(XA, XB)