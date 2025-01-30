import random
import gram_scan as gs
import math


def is_ccw(p1, p2, p3):

    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0]) > 0

def is_convex(a, b, c, d):
    if not is_ccw(a, b, c):  
        b, c = c, b 
    if not is_ccw(c, d, a):  
        d, a = a, d  

    return gs.left_of(a, b, c) and gs.left_of(b, c, d) and gs.left_of(c, d, a) and gs.left_of(d, a, b)


def angle(p1, p2, p3):
    v1 = (p1[0] - p2[0], p1[1] - p2[1])
    v2 = (p3[0] - p2[0], p3[1] - p2[1])

    dot = v1[0] * v2[0] + v1[1] * v2[1]
    norm1 = math.sqrt(v1[0]**2 + v1[1]**2)
    norm2 = math.sqrt(v2[0]**2 + v2[1]**2)

    if norm1 == 0 or norm2 == 0:
        return 180 
    cos_theta = max(-1, min(1, dot / (norm1 * norm2)))
    return math.degrees(math.acos(cos_theta))

def max_triangle_angle(triangle):
    a, b, c = triangle
    return max(angle(a, b, c), angle(b, c, a), angle(c, a, b))

def should_flip(a, b, c, d):
    before_flip = max(max_triangle_angle((a, b, c)), max_triangle_angle((a, c, d)))
    after_flip = max(max_triangle_angle((a, b, d)), max_triangle_angle((b, c, d)))
    return after_flip < before_flip

def flip_edges(triangles):
    flipped = True
    while flipped:
        flipped = False
        for i in range(len(triangles)):
            for j in range(i + 1, len(triangles)):
                t1 = triangles[i]
                t2 = triangles[j]

                shared = list(set(t1) & set(t2))
                if len(shared) != 2:
                    continue  
                
                a, c = shared
                unique_t1 = [p for p in t1 if p not in shared]
                unique_t2 = [p for p in t2 if p not in shared]
                
                if len(unique_t1) != 1 or len(unique_t2) != 1:
                    continue 
                
                b, d = unique_t1[0], unique_t2[0]
                if is_convex(a, b, c, d) and should_flip(a, b, c, d):

                    triangles[i] = (a, b, d)

                    triangles[j] = (b, c, d) 

                    flipped = True

    return triangles
                            
def totalEdgeLength(triangles, hull):
    edgeLength = 0
    hullEdgeLength = 0
    for i in range(len(triangles)):
        edgeLength += math.dist(triangles[i][0],triangles[i][1])
        #each triangle shares an edge, because this list does not include the hull. edges are double counted
        edgeLength += math.dist(triangles[i][1],triangles[i][2])
        edgeLength += math.dist(triangles[i][2],triangles[i][0])
    edgeLength = edgeLength / 2
    for i in range(1, len(hull)):   #calculate twice the hull length
        edgeLength += math.dist(hull[i-1],hull[i])
    return edgeLength   #divide by two for the correct weight


                    
  

def triangulate(pts):
    pts = gs.sort_points_counterclockwise(pts)
    hull = [pts[0], pts[1]]  
    triangles = []  
    for index,_ in enumerate(pts):
        if index == (0 or 1):
            continue
        triangle = (pts[0],pts[index-1],pts[index])
        triangles.append(triangle)

    for point in pts[2:]:
        while len(hull) > 1 and not gs.left_of(hull[-2], hull[-1], point):
            triangle = (hull[-2], hull[-1], point)
            triangles.append(triangle)
            hull.pop()  
        hull.append(point)  
    triangles_del = [t[:] for t in triangles]
    triangles_del = flip_edges(triangles_del)
    return triangles, triangles_del, hull

# pts = [(0,0),(1,1),(1,0)]
# tri, tdel, hul = triangulate(pts)
# print(tri, hul, tdel)
# print(totalEdgeLength(tdel, hul))
