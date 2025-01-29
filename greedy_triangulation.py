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

def greedyTriangulationAlgorithm(points):
    triangulation = []
    edgeList = []
    num_vertices = len(points)
    for i in range(num_vertices):        #this adds all possible unique edges to edgeList, and then it sorts them by their length
        for j in range(i + 1, num_vertices):
            if [points[i],points[j]] not in edgeList and [points[j],points[i]] not in edgeList:
                edgeList.append([points[i],points[j]])
    edgeList = sorted(edgeList, key=edgeLength)

    for i in range(len(edgeList)):
        for j in triangulation:
            if i==0:
                triangulation.append(edgeList(0))
            elif not intersectQuerie(edgeList[i][0],edgeList[i][1],triangulation[j][0],triangulation[j][1]):
                triangulation.append(edgeList(i))
    return triangulation

def edgeLength(edge):
    return math.dist(edge[0], edge[1])

def intersectQuerie(a,b,s,t):
    a_left_of_st = left_of([s[0],s[1]],[t[0],t[1]],[a[0],a[1]])
    b_left_of_st = left_of([s[0],s[1]],[t[0],t[1]],[b[0],b[1]])
    s_left_of_ab = left_of([a[0],a[1]],[b[0],b[1]],[s[0],s[1]])
    t_left_of_ab = left_of([a[0],a[1]],[b[0],b[1]],[t[0],t[1]])
    #st and ab only intersect if this is a and b are on opposite sides of st and s and t are on opposite sides of ab
    if a_left_of_st != b_left_of_st and s_left_of_ab != t_left_of_ab: 
        return True
    
    return False    #returns false if the lines don't intersect



print(greedyTriangulationAlgorithm([[0,0],[1,1],[1,0],[0,1]]))