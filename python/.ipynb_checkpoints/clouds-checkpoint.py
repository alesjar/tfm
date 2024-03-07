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

# generamos una nube aleatoria en la corona circular (1/2,1) que pone una red de puntos equidistantes en ambas fronteras
def crearnubecorona(longitud):
    nube = [] #numero de puntos en cada frontera
    theta = (2*math.pi)/longitud #angulo que vamos a girar
    theta2 = theta
    thetamedios = theta/2
    for m in range(longitud):
        nube.append([1,theta2])
        nube.append([0.5,theta2])
        nube.append([0.75,theta2+thetamedios]) #empezamos el giro en lugares distintos
        theta2 = theta2+theta
    return nube

# generamos una nube en la circunferencia
def crearnubecircunferencia(epsilon,radio,centro):
    nube = []
    theta = 0
    dospi = 2*math.pi
    while theta<dospi:
        nube.append([radio*math.cos(theta)+centro[0],radio*math.sin(theta)+centro[1]])
        theta += epsilon
    return nube

# generamos una nube en un ocho formado por dos circunferencias
def crearnubeocho(epsilon):
    nube = []
    nube.extend(crearnubecircunferencia(epsilon,1,(0,0)))
    nube.extend(crearnubecircunferencia(epsilon,1,(1,0)))
    return nube

# generamos una nube en el circulo
def crearnubecirculo(epsilon):
    nube = []
    theta = 0
    dospi = 2*math.pi
    radio = epsilon
    while theta<dospi:
        while radio<1:
            nube.extend(crearnubecircunferencia(epsilon,radio))
            radio+=epsilon
        theta+=epsilon
    return nube

# generamos una nube en una circunferencia en el plano XY de altura dada
def crearnubecircunferencia3d(epsilon,altura):
    nube = []
    theta = 0
    dospi = 2*math.pi
    radio = 1-altura**2
    incremento = epsilon/radio
    while theta<dospi:
        nube += [[radio*math.cos(theta),radio*math.sin(theta),altura]]
        theta += incremento
    return nube

# generamos nube en la esfera
def crearnubeesfera(epsilon):
    nube = []
    nube.append([0,0,-1])
    nube.append([0,0,1])
    #epsilonajustado = np.arccos(math.sqrt(math.cos(epsilon)));
    epsilonajustado = epsilon
    incrementoaltura = epsilonajustado
    z = -1+incrementoaltura
    while z<1:
        nube += crearnubecircunferencia3d(epsilonajustado,z)
        z+= incrementoaltura
    return nube

def calcular_incremento_angulo(epsilon):
    n = 1
    while 2*math.pi/n > epsilon:
        n += 1
    return n

def calcular_incremento_altura(epsilon):
    n = 1
    while 2/n > epsilon:
        n += 1
    return n

def nube_circunferencia(epsilon):
    n = calcular_incremento_angulo(epsilon)
    return [(math.cos(theta),math.sin(theta)) for theta in np.linspace(0,2*math.pi,n)]

def nube_circunferencia_3d(epsilon, altura):
    nube = []
    dos_pi = math.pi*2
    n = calcular_incremento_angulo(epsilon)
    for i in range(n):
        radio = math.sqrt(1-altura**2)
        angulo = dos_pi*i/n
        nube.append((radio*math.cos(angulo),radio*math.sin(angulo),altura))
    return nube

def nube_esfera(epsilon):
    nube = []
    nube.append((0,0,1))
    #epsilonajustado = np.arccos(math.sqrt(math.cos(epsilon)))
    epsilonajustado = epsilon
    n = calcular_incremento_altura(epsilonajustado)
    for i in range(n):
        nube.extend(nube_circunferencia_3d(epsilon, -1+2*i/n))
    return nube