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
    if q >= 0:
        return True 
    return False

def edgeLength(edge):
    return math.dist(edge[0], edge[1])

def intersectQuerie(a,b,s,t):
    if a==s or a==t or b==s or b==t:
        return False
    a_left_of_st = left_of([s[0],s[1]],[t[0],t[1]],[a[0],a[1]])
    b_left_of_st = left_of([s[0],s[1]],[t[0],t[1]],[b[0],b[1]])
    s_left_of_ab = left_of([a[0],a[1]],[b[0],b[1]],[s[0],s[1]])
    t_left_of_ab = left_of([a[0],a[1]],[b[0],b[1]],[t[0],t[1]])
    #st and ab only intersect if this is a and b are on opposite sides of st and s and t are on opposite sides of ab
    if a_left_of_st != b_left_of_st and s_left_of_ab != t_left_of_ab: 
        return True
    
    return False    #returns false if the lines don't intersect

def greedyTriangulationAlgorithm(points):
    triangulation = []
    edgeList = []
    num_vertices = len(points)
    for i in range(num_vertices):        #this adds all possible unique edges to edgeList, and then it sorts them by their length
        for j in range(i + 1, num_vertices):
            if [points[i],points[j]] not in edgeList and [points[j],points[i]] not in edgeList:
                edgeList.append([points[i],points[j]])
    edgeList = sorted(edgeList, key=edgeLength)
    #print(edgeList)
    

    for i in range(len(edgeList)):      #iterate through, checking if the edgelist edges intersect with the existing triangulation edges
        foundIntersection = False
        for j in range(len(triangulation)):
            if intersectQuerie(edgeList[i][0],edgeList[i][1],triangulation[j][0],triangulation[j][1]):
                print("intersection")
                foundIntersection = True
                break
        if not foundIntersection:
            print("noncrossing")
            triangulation.append(edgeList[i])
    return triangulation


#print(greedyTriangulationAlgorithm([[0,0],[1,1],[1,0],[0,1]]))

#print(intersectQuerie([0,0],[1,0],[0,0],[1,1]))