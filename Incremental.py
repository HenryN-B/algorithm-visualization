import random
import math
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def xcoord(e):
    return e[0]

def left_of(a,b,c):
    q = (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    if q > 0:
        return True 
    elif q <= 0:
        return False

def incsub(hull, k):
    prev = left_of(hull[-1],hull[0], k)
    bottom = -1
    top = -1
    for i in range(len(hull) - 1):
        next = left_of(hull[i],hull[i+1],k)
        if prev and (not next):
            bottom = i
        if (not prev) and next:
            top = i
        prev = next
    return bottom, top

def incr(pts):
    pts.sort(key=xcoord)
    hull = []
    if left_of(pts[0], pts[1],pts[2]):
        hull = [pts[0],pts[1],pts[2]]
    else:
        hull = [pts[0],pts[2],pts[1]]
    for i in range(3, len(pts)):
        bot, top = incsub(hull, pts[i])
        if top >= bot:
            hull[bot+1:top] = [pts[i]]
        else:
            hull[bot + 1:] = [pts[i]]
            hull[:top] = []
    return hull
