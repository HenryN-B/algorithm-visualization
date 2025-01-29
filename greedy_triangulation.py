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

def intersectQuerie(a,b,s,t):
    a_left_of_st = left_of([s[0],s[1]],[t[0],t[1]],[a[0],a[1]])
    b_left_of_st = left_of([s[0],s[1]],[t[0],t[1]],[b[0],b[1]])
    s_left_of_ab = left_of([a[0],a[1]],[b[0],b[1]],[s[0],s[1]])
    t_left_of_ab = left_of([a[0],a[1]],[b[0],b[1]],[t[0],t[1]])
    #st and ab only intersect if this is a and b are on opposite sides of st and s and t are on opposite sides of ab
    if a_left_of_st != b_left_of_st and s_left_of_ab != t_left_of_ab: 
        return True
    
    return False    #returns false if the lines don't intersect

#def greedyTriangulationAlgorithm(points):
#    triangulationEdges = [[[],[]]]
#    numVertices = len(points)
#    for i in numVertices:


print(intersectQuerie([0,0],[1,1],[1,0],[0,1]))