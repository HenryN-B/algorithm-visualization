import random
import math
import plotly.graph_objects as go
import matplotlib.pyplot as plt

def bottom_most(points):
    lowest = points[0]
    for point in points:
        if lowest == point:
            continue
        if point[1] < lowest[1]:
            lowest = point
        elif point[1] == lowest[1]:
            if point[0] > lowest[0]:
                lowest = point
    return lowest
    
def sort_points_counterclockwise(points):
    bottom = bottom_most(points)
    def angle_from_bottom_most(point):
        delta_x = point[0] - bottom[0]
        delta_y = point[1] - bottom[1]
        return math.atan2(delta_y, delta_x)
    sorted_points = sorted(points, key=angle_from_bottom_most)
    return sorted_points

def random_points(n, s):
    pts = []
    while len(pts) < n :
        x = random.random() * s
        y = random.random() * s
        new_point = (x, y)
        pts.append(new_point)
    return pts 

def left_of(a,b,c):
    q = (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    if q > 0:
        return True 
    elif q <= 0:
        return False

def next(hull, pts, num):
    point = pts[num]
    while len(hull) > 1 and not left_of(point, hull[-2], hull[-1]):
        hull.pop()
    hull.append(point)
    return hull,pts, num + 1

def graham_scan(pts):
    pts = sort_points_counterclockwise(pts)
    hull = [pts[0],pts[1]]
    return next(hull, pts, 2)

def gs_complete(pts):
    pts = sort_points_counterclockwise(pts)
    hull = [pts[0],pts[1]]
    for point in pts[2:]:
        while len(hull) > 1 and not left_of(point, hull[-2], hull[-1]):
            hull.pop()
        hull.append(point)
    return hull

def gift_wrap(pts):
    pts = sort_points_counterclockwise(pts)
    hull = [pts[0],pts[1]] 
    hull_incrementor = len(hull)
    for point in pts[2:]:
        if left_of(point, hull[-hull_incrementor], hull[-hull_incrementor + 1]):
            hull_incrementor = hull_incrementor + 1
            hull.append(point)

    return hull

#pts_test=[[2.1,0.3],[4,4.2],[0,5],[0.1,0.2]]

#print(gift_wrap(pts_test))
