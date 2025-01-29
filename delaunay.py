def is_convex(a, b, c, d):
    cross1 = left_of(a, b, c)
    cross2 = left_of(b, c, d)
    cross3 = left_of(c, d, a)
    cross4 = left_of(d, a, b)
    return cross1 and cross2 and cross3 and cross4


def flip_edges(triangles):
    flipped = True
    while flipped:
        flipped = False
        for i in range(len(triangles)):
            for j in range(i + 1, len(triangles)):
                t1 = triangles[i]
                t2 = triangles[j]
                
                for point in 
                
                same_edge = "temp"
                if len(same_edge) == 2:
                    a = same_edge
                    if
                    b = same_edge[1]
                    
    return triangles

def triangulate(pts):
    pts = sort_points_counterclockwise(pts)
    hull = [pts[0], pts[1]]  
    triangles = []  
    for index,_ in enumerate(pts):
        if index == (0 or 1):
            continue
        triangle = (pts[0],pts[index-1],pts[index])
        triangles.append(triangle)

    for point in pts[2:]:
        while len(hull) > 1 and not left_of(hull[-2], hull[-1], point):
            triangle = (hull[-2], hull[-1], point)
            triangles.append(triangle)
            hull.pop()  
        hull.append(point)  
    
    triangles = flip_edges(triangles)

    return triangles


points = random_points(100,100)
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