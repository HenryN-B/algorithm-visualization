import random
import math
import plotly.graph_objects as go

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

def intersectQuerie([[a1,b1],[b1,b2]][[s1,s2],[t1,t2]]):
    a_left_of_st = left_of([s1,s2],[t1,t2],[a1,a2])
    b_left_of_st = left_of([s1,s2],[t1,t2],[b1,b2])
    s_left_of_ab = left_of([a1,a2],[b1,b2],[s1,s2])
    t_left_of_ab = left_of([a1,a2],[b1,b2],[t1,t2])
    if a_left_of_st == b_left_of_st:
        return False    #a and b are on the same side of st: ab does not intersect st
    elif a_left_of_st != b_left_of_st and s_left_of_st != t_left_of_ab:
        return True
    else:
        return False
    