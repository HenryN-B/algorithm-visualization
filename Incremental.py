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
        elif (not prev) and next:
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
        if bot == -1 and top == -1:
            continue
        if top < bot:
            hull = hull[:bot+1] + [pts[i]] + hull[top:]
        else:
            hull = hull[:bot+1] + [pts[i]] + hull[top:]
    return hull


# def random_points(n, s):
#     pts = []
#     while len(pts) < n :
#         x = random.random() * s
#         y = random.random() * s
#         new_point = (x, y)
#         pts.append(new_point)
#     return pts 

# set = [[0,0],[1,2],[2,1],[3,7],[4,3]]
# print(incr(set))
