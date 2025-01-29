import random
import gram_scan as gs
import matplotlib.pyplot as plt


def is_convex(a, b, c, d):
    cross1 = gs.left_of(a, b, c)
    cross2 = gs.left_of(b, c, d)
    cross3 = gs.left_of(c, d, a)
    cross4 = gs.left_of(d, a, b)
    return cross1 and cross2 and cross3 and cross4


def flip_edges(triangles):
    flipped = True
    while flipped:
        flipped = False
        for i in range(len(triangles)):
            for j in range(i + 1, len(triangles)):
                t1 = triangles[i]
                t2 = triangles[j]
                if t1 == t2:
                    continue
                same = 0
                same_list = []
                for point1 in t1:
                    for point2 in t2:
                        if point1 == point2:
                            same_list.append(point1)
                            same +=1
                if same <= 2:
                    continue
                a = same_list[0]
                b = []
                c = same_list[1]
                d = []
                for point in t1:
                    if point == (a or c):
                        continue
                    left = gs.left_of(a,c,point)
                    if left == True:
                        d = point
                        for point2 in t2:
                            if point2 == (a or c):
                                continue
                            b = point2
                    else:
                        b = point 
                        for point2 in t2:
                            if point2 == (a or c):
                                continue
                            d = point2
                print(a,b,c,d)
                if is_convex(a,b,c,d):
                    print("convex")
                            
                    
                    
    return triangles

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
    
    triangles = flip_edges(triangles)

    return triangles


points = gs.random_points(100,100)
triangles = triangulate(points)

for triangle in triangles:
    x = []
    y = []
    for point in triangle:

        x.append(point[0])
        y.append(point[1])
    x.append(triangle[0][0])
    y.append(triangle[0][1])
    plt.plot(x,y)
plt.show()