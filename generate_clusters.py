import pandas as pd
import numpy as np
from numpy.linalg import norm
import  matplotlib.pyplot as plt

def centroid(vectors):
    # Input: A list where the x and y coordinates of a set of vectors are listed
    # Output: Calculates the centroid of the vectors by averaging the x and y coordinates
   
    # Keeping track of running x sum and y sum
   
    if len(vectors) == 0:
        return np.array([37, -95]) # longitude and latitude of center of the US
    else:
        xsum = 0
        ysum = 0
   
    # Finding sum of x and y coordinates
        for i in range(0,len(vectors),2):
            xsum = xsum + vectors[i]
        for j in range(1,len(vectors),2):
            ysum = ysum + vectors[j]  
       
    # Finding x and y average
   
        xcenter = float(2*xsum/len(vectors))
        ycenter = float(2*ysum/len(vectors))
    return np.array([xcenter, ycenter])

def find_minimum_distance(cluster_list, vector):
    # Inputs: A list with the clusters, a vector
    # Output: Returns the index of the cluster that is the closest to the vector
   
    minimum = norm(cluster_list[0] - vector)
    minimum_index = 0
    for i in range(1,len(cluster_list)):
        if norm(cluster_list[i] - vector) < minimum:
            minimum_index = i
            minimum = norm(cluster_list[i] - vector)
    return minimum_index

def clustering(vectors):
    # Inputs: A set of vectors
    # Outputs: Returns the vectors that corresponds to the centroids of the 20 clusters
    z0 = np.array([44.500000, -73.9])
    z1 = np.array([40.78, -89.500000])
    z2 = np.array([40.79, -73.92])
    z3 = np.array([40.81, -73.94])
    z4 = np.array([ 41.500000, -74])
    z5 = np.array([40.9, -73.7])
    z6 = np.array([40.9, -73.7])
    z7 = np.array([40.9, -71.87])
    z8 = np.array([40.9, -72.87])
    z9 = np.array([40.9, 74.87])
   
    cluster_centers = np.array([z0, z1, z2, z3, z4, z5, z6, z7, z8, z9])
   
    for i in range(100):
        cluster0 = np.array([])
        cluster1 = np.array([])
        cluster2 = np.array([])
        cluster3 = np.array([])
        cluster4 = np.array([])
        cluster5 = np.array([])
        cluster6 = np.array([])
        cluster7 = np.array([])
        cluster8 = np.array([])
        cluster9 = np.array([])
       
        for vec in vectors:
            min_index = find_minimum_distance(cluster_centers, vec)
            if min_index == 0:
                cluster0 = np.append(cluster0,vec)
            if min_index == 1:
                cluster1 = np.append(cluster1, vec)
            if min_index == 2:
                cluster2 = np.append(cluster2, vec)
            if min_index == 3:
                cluster3 = np.append(cluster3, vec)
            if min_index == 4:
                cluster4 = np.append(cluster4, vec)
            if min_index == 5:
                cluster5 = np.append(cluster5, vec)
            if min_index == 6:
                cluster6 = np.append(cluster6, vec)
            if min_index == 7:
                cluster7 = np.append(cluster7, vec)
            if min_index == 8:
                cluster8 = np.append(cluster8, vec)
            if min_index == 9:
                cluster9 = np.append(cluster9, vec)
                       
        z0 = centroid(cluster0)
        z1 = centroid(cluster1)
        z2 = centroid(cluster2)
        z3 = centroid(cluster3)
        z4 = centroid(cluster4)
        z5 = centroid(cluster5)
        z6 = centroid(cluster6)
        z7 = centroid(cluster7)
        z8 = centroid(cluster8)
        z9 = centroid(cluster9)
       
        cluster_centers = np.array([z0, z1, z2, z3, z4, z5, z6, z7, z8, z9])
    print(cluster0)
    print(cluster1)
    print(cluster2)
    print(cluster3)
    print(cluster4)
    print(cluster5)
    print(cluster6)
    print(cluster7)
    print(cluster8)
    print(cluster9)
   
    return cluster_centers  

state = pd.read_csv("mammograms_per_state _Sheet1.csv")
lat_data = state["Latitude"].to_list()
lon_data = state["Longitude"].to_list()
data = np.column_stack((lat_data, lon_data))
clusters = clustering(data)

originalx = np.array([40.769])
originaly = np.array([-73.9549])

# Creating vector for x coordinates and y coordinates

for index in range(len(data)):
    originalx = np.append(originalx, data[index][0])
    originaly = np.append(originaly, data[index][1])

# Plotting original data

plt.figure()
plt.scatter(originalx, originaly)

# Using Lloyd's Algorithm to Find 6 Clusters

answers = clustering(data)

# Finding xcoords and y coords of cluster centers

xcoords = np.array([answers[0][0], answers[1][0], answers[2][0], answers[3][0], answers[4][0], answers[5][0], answers[6][0],answers[7][0],answers[8][0],answers[9][0]])
ycoords = np.array([answers[0][1], answers[1][1], answers[2][1], answers[3][1], answers[4][1], answers[5][1], answers[6][1],answers[7][1],answers[8][1],answers[9][1]])

plt.scatter(xcoords, ycoords)
plt.xlabel("Latitude")
plt.ylabel("Longitude")
plt.title("States")

print(clusters)