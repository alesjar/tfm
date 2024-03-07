'''
ENGLISH:
This file defines functions that create a cloud of points in some surface.
The idea is to create a cloud of points where every point in the surface is at distance 
less than epsilon from a point in the cloud. This is called being an epsilon-aproximation.

SPANISH:
Este archivo define funciones que crean una nube de puntos en una superficie.
La idea es crear una nube de tal forma que todo punto en la superficie tenga uno 
de la nube a distancia menor que epsilon. Esto se conoce como ser una epsilon-aproximacion.


'''
import math
import numpy as np

def angle_increment(epsilon):
    n = 1
    while 2*math.pi/n > epsilon:
        n += 1
    return n

def height_increment(epsilon):
    n = 1
    while 2/n > epsilon:
        n += 1
    return n

def circumference_cloud(epsilon):
    n = angle_increment(epsilon)
    return [(math.cos(theta),math.sin(theta)) for theta in np.linspace(0,2*math.pi,n)]

def circumference_cloud_3d(epsilon, altura):
    nube = []
    dos_pi = math.pi*2
    n = angle_increment(epsilon)
    for i in range(n):
        radio = math.sqrt(1-altura**2)
        angulo = dos_pi*i/n
        nube.append((radio*math.cos(angulo),radio*math.sin(angulo),altura))
    return nube

def sphere_cloud(epsilon):
    nube = []
    nube.append((0,0,1))
    #epsilonajustado = np.arccos(math.sqrt(math.cos(epsilon)))
    epsilonajustado = epsilon
    n = height_increment(epsilonajustado)
    for i in range(n):
        nube.extend(circumference_cloud_3d(epsilon, -1+2*i/n))
    return nube