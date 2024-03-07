import math
import numpy as np

def polar_to_r2(z):
    w = []
    rad = z[0]
    arg = z[1]
    w.append(rad*math.cos(arg))
    w.append(rad*math.sin(arg))
    return w

def euc_dist(z, w):
    return math.sqrt(sum((z_i-w_i)**2 for z_i, w_i in zip(z, w)))

def polar_dist(z,w):
    return euc_dist(polar_to_r2(z),polar_to_r2(w))

# calculates the distance matrix of a cloud
# position [i][j] gives dist. between points [i] and [j]. 
# calculates n(n-1)/2 distances
def dist_matrix(cloud):
    n = len(cloud)
    matrix = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            if i < j:
                d = euc_dist(cloud[i],cloud[j]) # only calcultates one of [i, j] = [j, i]
                matrix[i][j] = d
                matrix[j][i] = d
    return matrix

# diameter function
def diam(c, dist_matrix):
    max = 0
    lista = list(c)
    m = len(lista)
    if m == 0 or m == 1:
        return 0
    else:
        for i in range(m):
            for j in range(i+1,m):
                d = dist_matrix[lista[i]][lista[j]]
                if d>max:
                    max = d
        return max