import random
import math
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def xcoord(e):
    return e[0]

def left_of(a,b,c):
    q = ((b[0]-a[0])*(c[1]-a[1]))-((b[1]-a[1])*(c[0]-a[0]))
    return q > 0

def incsub(hull, k):
    top = -1
    bottom = -1
    prev = left_of(hull[-1],hull[0], k)
    for i in range(len(hull) - 1):
        next = left_of(hull[i],hull[i+1],k)
        if prev and (not next):
            bottom = i
        elif (not prev) and next:
            top = i
        prev = next
    prev = left_of(hull[-2],hull[-1],k)
    next = left_of(hull[-1],hull[0],k)
    if prev and (not next):
        bottom = len(hull) - 1
    elif (not prev) and next:
        top = len(hull) - 1
    return bottom, top

def incr(pts):
    pts.sort(key=xcoord)
    hull = [pts[0],pts[1],pts[2]]
    if not left_of(pts[0], pts[1], pts[2]):
        hull = [pts[0],pts[2],pts[1]]
    for i in range(3, len(pts)):
        bot, top = incsub(hull, pts[i])
        if bot == -1 and top == -1:
            continue
        if top < bot:
            hull = hull[top:bot] + [hull[bot]] + [pts[i]]
        if top > bot:
            hull = hull[:bot+1] + [pts[i]] + hull[top:]
    return hull


def random_points(n, s):
    pts = []
    while len(pts) < n :
        x = random.random() * s
        y = random.random() * s
        new_point = (x, y)
        pts.append(new_point)
    return pts 

# set = random_points(10, 10)
# hull = incr(set)
# x = []
# y = []
# pX = []
# pY = []
# for i in hull:
#     x.append(i[0])
#     y.append(i[1])
# x.append(hull[0][0])
# y.append(hull[0][1])
# for j in set:
#     pX.append(j[0])
#     pY.append(j[1])
    
# fig = px.imshow(np.zeros(shape=(120, 120, 4)), origin='lower')
# fig.add_scatter(x=x, y=y, mode='lines+markers', marker_color='white', marker_size=8)
# fig.add_scatter(x=pX, y=pY, mode='markers', marker_color='white', marker_size=4)
# fig.show()