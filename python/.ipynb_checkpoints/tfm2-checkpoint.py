#!/usr/bin/python

import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
from itertools import chain, combinations
import math

'''epsilon = 0.5;

pi  = math.pi 

'generamos una nube aleatoria en la corona circular (1/2,1) que pone una red de puntos equidistantes en ambas fronteras'
 
def crearnube(longitud):
    nube = []; #numero de puntos en cada frontera
    theta = (2*math.pi)/longitud; #angulo que vamos a girar
    theta2 = theta;
    thetamedios = theta/2;
    for m in range(longitud):
        nube.append([1,theta2]);
        nube.append([0.5,theta2+thetamedios]);#empezamos el giro en lugares distintos
        theta2 = theta2+theta
    return nube
nube = crearnube(int(input('especifica tamaño de la nube')));
n = len(nube);
print(nube);

def trans(z):
    w = [];
    rad = z[0];
    arg = z[1];
    w.append(rad*math.cos(arg));
    w.append(rad*math.sin(arg));
    return w

def dist(z,w):
    distancia =math.sqrt((z[0]-w[0])**2+(z[1]-w[1])**2);
    return distancia

def distpolar(z,w):
    return dist(trans(z),trans(w))

'calculamos la matriz de distancias primero, para solo calcularla una vez'
def matdist(nube):
    distancias = np.zeros((n,n));
    for i in range(n):
        for j in range(n):
            if i < j:
                d = distpolar(nube[i],nube[j]);
                distancias[i][j] = d;
                distancias[j][i] = d;
    print(distancias)
    return distancias

matrizdistancias = matdist(nube);
'funciones para calcular las distancias entre complejos en forma polar'

'por fuerza bruta genero todos los posibles subconjuntos'
'el dato va a ser un conjunto de indices 0 hasta n que representen los z_0...z_n'

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(len(s),-1,-1)))

def diam(C):
    listadistancias = [];
    m = len(C);
    if m == 0 or m == 1:
        return 0
    else:
        for i in range(m):
            for j in range(i+1,m):
                listadistancias.append(matrizdistancias[C[i]][C[j]])
        return max(listadistancias)

def diamconjunto(c):
    listadistancias = [];
    lista = list(c);
    m = len(lista);
    if m == 0 or m == 1:
        return 0
    else:
        for i in range(m):
            for j in range(i+1,m):
                listadistancias.append(matrizdistancias[lista[i]][lista[j]])
        return max(listadistancias)

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

def udosepsilon(nube):
    U = [];
    n = len(nube);
    nubeteorica = [i for i in range(n)];
    doseps = 2*epsilon;
    listasub = powerset(nubeteorica);
    listasub.remove(());
    for C in listasub: 
        if  diam(C)<doseps:
            U.append(C);
    print(U)
    return U

def aconjunto(U):
    lista = [];
    for u in U:
        lista.append(set(u));
    return lista

def transformardatos(nube):
    U = aconjunto(udosepsilon(nube));
    m = len(U);
    x = list(range(1,m+1));
    orden = [];
    for i in range(m-1,-1,-1):
        for j in range(i,-1,-1):
            if U[i].issubset(U[j]):
                orden.append((x[j],x[i]));
    print(orden);
    return orden
u = transformardatos(nube);

class MyClass():
    def __init__(self):
        self.list2 = u;
        print(self.list2);
        self.list1 = []
        for a, b in self.list2:
            self.list1.append(a and b)
        for i in list(range(1,10)):
            for a in self.list1:
                while self.list1.count(a) > 1:
                    self.list1.remove(a)
        self.list1.sort()
        self.result = {}
        for first, second in self.list2:
            self.result.setdefault(first, []).append(second)
        self.reflexive_list = []
        for a, b in list(self.list2):
            if a == b:
                self.reflexive_list.append((a,b))
        self.primes = []
        for num in self.list1:
            prime = True
            for i in range(2,num):
                if (num%i==0):
                    prime = False
            if prime:
               self.primes.append(num)
            
    def check_reflexive(self):
        if len(self.reflexive_list) == len(self.list1):
            'print(self.reflexive_list)'
            print("Reflexive check ✅")
            return True
        else:
            print("Reflexive check ❌")
            return False
        
    def check_antisymmetric(self):
        antisymettric_list = []
        for b in self.list2:
            swap1 = b[0]
            swap2 = b[1]
            newtuple = (swap2, swap1)
            antisymettric_list.append(newtuple)
        for ü in self.reflexive_list:
            if ü in antisymettric_list:
                antisymettric_list.remove(ü)
            else:
                None
        print(antisymettric_list)
        for q in antisymettric_list:
            if q in self.list2:
                print("Anti-Symmetric check ❌")
                return False
        print("Anti-Symmetric check ✅")
        return True
    
    def check_transitive(self):      
        for a, b in self.list2:
            for x in self.result[b]:
                if (   x in self.result[a]  ):
                    None
                else:
                    print("Transitive check ❌")
                    print("There is no ({},{}) in the {}".format(a, x, self.result[a]))
                    return False
        print("Transitive check ✅")
        return True
    
    def draw_diagram(self):
        pos = {}
        #origin = -len(list(self.result.keys()))-5
        randlist = list(range(1,len(list(self.result.keys()))+1))
        for a in (list(self.result.keys())):
            if a == 1:
                pos.setdefault(a, ((len(list(self.result.keys()))/2), -len(list(self.result.keys()))*2-4))
            elif a in self.primes:
                pos.setdefault(a, (a, -len(list(self.result.keys()))*2))
            elif len(list(self.result[a])) == 1:
                exitr = random.choice(randlist)
                pos.setdefault(a,(exitr, 0))
                randlist.remove(exitr)
            else:
                exitr = random.choice(randlist)
                pos.setdefault(a, (exitr, (-len(list(self.result[a])))*2))
                randlist.remove(exitr)
        ###
        edges = {}
        list1_reverse = list(self.list1)
        for a in list1_reverse:
            for b in list1_reverse:
                if (a%b==0) and (a != b):
                    edges.setdefault(a, []).append(b)
        ###
        edge_list = [(x,y) for x,y in self.list2 if x!=y]
        for i in list(range(1,10)):
            for a, b in edge_list:
                if b in list(edges.keys()):
                    for z in edges[b]:
                        if (z!=a) and (z%a==0):
                            while (a,b) in edge_list:
                                edge_list.remove((a,b))
        ###
        T = nx.DiGraph()
        T.add_nodes_from(list(pos.keys()))
        T.add_edges_from(edge_list)
        plt.figure()
        if ( (self.check_reflexive() == True) and (self.check_antisymmetric() == True) and (self.check_transitive()== True) ):
            nx.draw(T, pos, node_color='black', node_size=600, font_size= 15, font_color='yellow', with_labels=True, arrowsize=18, edge_color='green')
            plt.show()
        else:
            return "There are conditions that are not provided."
    
G = MyClass();
G.draw_diagram();
print('hola');
print(list(G.nodes));
def hacerminimal(G):
    i=0;
    j=0;
    while i<len(list(G.nodes)):
        nodo = list(G.nodes)[i];
        sucesor = list(G.succesors(nodo));
        predecesor = list(G.predecessors(nodo));
        if len(sucesor) == 1:
            lista1 = [];
            predecesores = G.predecessors(nodo);
            G.remove(nodo)
            for n in predecesores:
                lista1.append((sucesor[0],n));
            G.add_edges_from(lista1);
            j = j+1;
        elif len(predecesor) == 1:
            lista1 = [];
            sucesores = G.successors(nodo);
            G.remove_node(nodo);
            for n in sucesores:
                lista1.append((n,predecesor[0]));
            G.add_edges_from(lista1);
            j = j+1;
        else:
            i = i+1;
    print(j);
    if j == 0:
        return G
    else:
        return hacerminimal(G)

H = hacerminimal(G);
print('hola');
H.draw_diagram();'''

a =((0,1),(0,1,3));
b = str(a);
print(b)
for i in range(10,1,-1):
    print(i)