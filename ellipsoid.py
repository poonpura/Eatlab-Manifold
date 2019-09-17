import math

# Converts the table to a manifoldList format: a nested list, with each entry a point in the manifold.
def toManifoldList(result):
    L= []
    array= np.array([result[0], result[1], result[2]])
    size= array[0].size
    for i in range(size):
        x= array[0][i]
        y= array[1][i]
        z= array[2][i]
        L.append([x, y, z])

    return np.array(L)

# MAIN ALGORITHM
def ellipsoid(manifold):
    x= centroid(manifold)
    tip= findTip(manifold, x, 0.1)
    mean_dist= dist(centroid(tip), x)
    min_tip_dist= tip[tip[:,3].argsort()][0][3]

    if min_tip_dist > mean_dist:
        kmeans= KMeans(n_clusters= 2)
        kmeans.fit(tip)
        y_kmeans= kmeans.predict(tip)
        tip_cluster= np.append(tip, np.transpose([y_kmeans]), axis= 1)
        x1= tip_cluster[tip_cluster[:,4] == 0].mean(axis= 0)
        x2= tip_cluster[tip_cluster[:,4] == 1].mean(axis= 0)
    else:
        tip= findTip(manifold, x, 0.05)
        x1= tip.mean(axis= 0)[0:3]
        filtered= filter(manifold, x1 - x, x)
        tip2= findTip(filtered, x, 0.1)
        x2= tip2.mean(axis= 0)[0:3]

    projection= []
    p_axis= x1 - x2
    for point in manifold:
        print(projPlane(point, p_axis, x))
        projection.append(projPlane(point, p_axis, x).tolist())
    projection= np.array(projection)

    tip= findTip(projection, x, 0.1)
    mean_dist= dist(centroid(tip), x)
    min_tip_dist= tip[tip[:,3].argsort()][0][3]
    print(min_tip_dist)
    print(mean_dist)

    if min_tip_dist > mean_dist:
        kmeans= KMeans(n_clusters= 2)
        kmeans.fit(tip)
        y_kmeans= kmeans.predict(tip)
        tip_cluster= np.append(tip, np.transpose([y_kmeans]), axis= 1)
        x3= tip_cluster[tip_cluster[:,4] == 0].mean(axis= 0)
        x4= tip_cluster[tip_cluster[:,4] == 1].mean(axis= 0)
    else:
        tip= findTip(projection, x, 0.05)
        x3= tip.mean(axis= 0)[0:3]
        filtered= filter(projection, x3 - x, x)
        tip2= findTip(filtered, x, 0.1)
        x4= tip2.mean(axis= 0)[0:3]

    projection2= []
    s_axis= x3 - x4
    for point in projection:
        projection2.append(projPlane(point, s_axis, x).tolist())
    projection2= np.array(projection2)

    tip= findTip(projection2, x, 0.1)
    mean_dist= dist(centroid(tip), x)
    min_tip_dist= tip[tip[:,3].argsort()][0][3]

    if min_tip_dist > mean_dist:
        kmeans= KMeans(n_clusters= 2)
        kmeans.fit(tip)
        y_kmeans= kmeans.predict(tip)
        tip_cluster= np.append(tip, np.transpose([y_kmeans]), axis= 1)
        x5= tip_cluster[tip_cluster[:,4] == 0].mean(axis= 0)
        x6= tip_cluster[tip_cluster[:,4] == 1].mean(axis= 0)
    else:
        tip= findTip(projection2, x, 0.05)
        x5= tip.mean(axis= 0)[0:3]
        filtered= filter(projection2, x5 - x, x)
        tip2= findTip(filtered, x, 0.1)
        x6= tip2.mean(axis= 0)[0:3]

    return [x[0:3].tolist(), x1[0:3].tolist(), x2[0:3].tolist(), x3[0:3].tolist(), x4[0:3].tolist(), x5[0:3].tolist(), x6[0:3].tolist()]

# Calculate the centroid of a set of points.
# Precondition: manifold is a manifoldList
def centroid(manifold):
    sum= [0, 0, 0]
    for p in manifold:
        sum[0]= sum[0] + p[0]
        sum[1]= sum[1] + p[1]
        sum[2]= sum[2] + p[2]

    return np.array(sum) / size(manifold)

# Return the number of points in the data_set
# Precondition: data_set is not empty and is a manifoldList
def size(data_set):
    return data_set.size // data_set[0].size

# Find the furtherest p points from the centroid in the data_set. Adds a distance to centroid attribute to each point.
# Precondition: p in [0, 1], data set is a manifoldList
def findTip(data_set, centroid, p):
    matrix= data_set.tolist()
    for i in range(size(data_set)):
        point= matrix[i]
        point.append(dist(point, centroid))

    dataSet= np.array(matrix)
    dataSet= dataSet[dataSet[:,3].argsort()]
    tip= dataSet[-round(p*size(data_set)):]

    return tip

# Find the distance between 2 points in co-ordinate representation
def dist(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 + (point1[2] - point2[2])**2)

# Project point onto a 2-Dimensional plane defined by a pivot and a normal vector.
# The pivot is any given point on the plane.
def projPlane(point, normal, pivot):
    return point - projLine(point, normal, pivot) + pivot

# Project point onto a 2-Dimensional plane defined by a pivot and a normal vector.
# The pivot is any given point on the plane.
def projLine(point, line, pivot):
    point= point[0:3]
    line= line[0:3]
    pivot= pivot[0:3]

    proj_v= np.dot(point - pivot, line) / (line[0]**2 + line[1]**2 + line[2]**2) * line
    return proj_v + pivot

# Filter for points which, when projected to the vector, have a negative coefficient.
# Vector is a directional vector not a positional vector.
def filter(data_set, vector, pivot):
    filtered= []
    for point in data_set:
        if ((projLine(point, vector, pivot) - pivot) / vector)[0] < 0:
            filtered.append(point.tolist())

    return np.array(filtered)
    
