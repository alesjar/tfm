# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 23:43:44 2021

@author: alexb
"""

import math
import numpy as np
from itertools import chain, combinations
import networkx as nx
import matplotlib.pyplot as plt



'generamos una nube aleatoria en la corona circular (1/2,1) que pone una red de puntos equidistantes en ambas fronteras'
 
def crearnubecorona(longitud):
    nube = []; #numero de puntos en cada frontera
    theta = (2*math.pi)/longitud; #angulo que vamos a girar
    theta2 = theta;
    thetamedios = theta/2;
    for m in range(longitud):
        nube.append([1,theta2]);
        nube.append([0.5,theta2]);
        nube.append([0.75,theta2+thetamedios]); #empezamos el giro en lugares distintos
        theta2 = theta2+theta
    return nube

def crearnubecircunferencia(epsilon,radio,centro):
    nube = [];
    theta = 0;
    dospi = 2*math.pi;
    while theta<dospi:
        nube.append([radio*math.cos(theta)+centro[0],radio*math.sin(theta)+centro[1]]);
        theta += epsilon;
    return nube

def crearnubeocho(epsilon):
    nube = []
    nube.extend(crearnubecircunferencia(epsilon,1,(0,0)))
    nube.extend(crearnubecircunferencia(epsilon,1,(1,0)))
    return nube

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

def crearnubecircunferencia3d(epsilon,altura):
    nube = [];
    theta = 0;
    dospi = 2*math.pi;
    radio = 1-altura**2;
    incremento = epsilon/radio;
    while theta<dospi:
        nube += [[radio*math.cos(theta),radio*math.sin(theta),altura]];
        theta += incremento;
    return nube

def crearnubeesfera(epsilon):
    nube = [];
    nube.append([0,0,-1]);
    nube.append([0,0,1]);
    #epsilonajustado = np.arccos(math.sqrt(math.cos(epsilon)));
    epsilonajustado = epsilon;
    incrementoaltura = epsilonajustado;
    z = -1+incrementoaltura;
    while z<1:
        nube += crearnubecircunferencia3d(epsilonajustado,z);
        z+= incrementoaltura;
    #print(nube);
    return nube

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

def disttres(z,w):
    return math.sqrt((z[0]-w[0])**2+(z[1]-w[1])**2+(z[2]-w[2])**2)

def distpolar(z,w):
    return dist(trans(z),trans(w))

'calculamos la matriz de distancias primero, para solo calcularla una vez'
def matdisttres(nube):
    distancias = np.zeros((n,n));
    for i in range(n):
        for j in range(n):
            if i < j:
                d = disttres(nube[i],nube[j]);
                distancias[i][j] = d;
                distancias[j][i] = d;
    print(distancias)
    return distancias

def matdistdos(nube):
    distancias = np.zeros((n,n));
    for i in range(n):
        for j in range(n):
            if i < j:
                d = dist(nube[i],nube[j]);
                distancias[i][j] = d;
                distancias[j][i] = d;
    print(distancias)
    return distancias

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

def udosepsilon(nube,epsilon):
    U = [];
    n = len(nube);
    nubeteorica = [i for i in range(n)];
    doseps = 2*epsilon;
    listasub = powerset(nubeteorica);
    for C in listasub: 
        if  diam(C)<doseps:
            U.append(C);
    return U

'''subc = intersection(powerset(C),listasubmod);
            for a in subc:
                U.append(a);
                listasubmod.remove(a);'''

def indicesapuntos(U):
    elemento = [];
    solucion = [];
    for u in U:
        for v in u:
            elemento.append(nube[v]);
        solucion.append(elemento);
        elemento = [];
    return solucion


'solucion = indicesacomplejos(U);'
'print(solucion);'

'para anadir los nodos usamos G.add_nodes_from(U), un iterable'
'''idea de algoritmo para dibujar sin necesariamente pasar por U:
datos: los puntos, epsilon, distancias entre puntos (por ejemplo en forma de matriz)
objetivo: nodos y relaciones entre ellos, por ejemplo poner numero a cada nodo y saber con cuales estan relacionados
cada punto z_i se identifica con el número i
probamos a empezar por abajo: 
para cada i en len(X)
    añadir i como nodo
para cada dos nodos a,b en G,
    si diam aub<eps
        añadir aub a G
        añadir edges (a,aub),(b,aub)
cuantas operaciones estamos haciendo?
primero añadimos n a G.
luego tomamos dos de esos n y medimos diametro, o sea (n sobre 2). 
pero luego solo lo hacemos con los que ya estén en G, porque todo grande de G se puede poner como union de sus subconjuntos. podria funcionar.

ahora bien, lo de la lista funciona?
primero estan los n primeros. cuando metemos los de dos, y termine con los de uno, comprueba los de dos. tenemos que hacer que al unir (1,2) con (2,3) salga el (1,2,3), o sea usar conjuntos. ademas, hay que hacer que pare cuando lleguen a longitud n, porque van a ser los mismos.

'''

def construirgrafo(nube):
    listanodos = [];
    listalados = [];
    doseps = 2*epsilon;
    n = len(nube);
    for i in range(n):
        listanodos.append((i,));
    listanodos1 = listanodos;
    for i in range(n-1):
        l = len(listanodos1);
        if l == 0:
            break;
        listanodos2 = []; #almacena los que voy metiendo en cada iteracion
        for k in range(l):
            a = listanodos1[k];
            for j in range(k+1,l):
                b = listanodos1[j];
                aubsinorden = list(set(a).union(set(b)));#esto puede dar problemas porque no guarda orden
                aub = tuple(sorted(aubsinorden));
                if len(aub)>len(a)+1:
                    continue;
                if a == aub or b == aub:
                    continue;
                if diam(aub)<doseps:
                    if aub not in listanodos2:
                        listanodos2.append(aub);
                        listanodos.append(aub);
                    if (a,aub) not in listalados:
                        listalados.append((a,aub));
                    if (b,aub) not in listalados:
                        listalados.append((b,aub));
        listanodos1  = listanodos2; #guarda los que he metido en la iteracion para poder usarlos en la siguiente para construir los siguientes
    #print(listanodos);
    #print(listalados);
    G = nx.DiGraph();
    G.add_nodes_from(listanodos);
    G.add_edges_from(listalados);
    return G

'''def construirgrafo(nube):
    lista_nodos = [];
    lista_lados = set();
    dos_eps = 2*epsilon;
    numero_de_puntos = len(nube);
    # Introducimos los conjuntos unitarios como nodos
    for i in range(numero_de_puntos):
        lista_nodos.append((i,));

    # Recuento de nodos que introducimos en la iteración anterior
    conjunto_nodos_iteracion_anterior = set(lista_nodos); 

    # Iteramos en el número de puntos de la aproximación
    for i in range(numero_de_puntos-1):
        # Si en la iteración anterior no introdujimos ninguno, paramos:
        if len(conjunto_nodos_iteracion_anterior) == 0:
            break;
        # Almacenamos los que introducimos en esta iteración
        conjunto_nodos_iteracion_actual = set(); 
        for nodo1 in conjunto_nodos_iteracion_anterior:
            #resto = {nodo1}
            #nodos_que_no_han_salido = conjunto_nodos_iteracion_anterior - resto
            for nodo2 in conjunto_nodos_iteracion_anterior:
                union_nodos = tuple(sorted(nodo1+nodo2))
                # Comprobamos que la longitud sea solo una por encima
                if len(union_nodos)>len(nodo1)+1:
                    continue;
                # Introducimos el conjunto 
                if union_nodos == nodo1 or union_nodos == nodo2:
                    continue
                if diam(union_nodos)<dos_eps:
                    if union_nodos not in conjunto_nodos_iteracion_actual: 
                        conjunto_nodos_iteracion_actual.add(union_nodos);
                        lista_nodos.append(union_nodos);
                    if (nodo1,union_nodos) not in lista_lados:
                        lista_lados.add((nodo1,union_nodos));
                    if (nodo2,union_nodos) not in lista_lados:
                        lista_lados.add((nodo2,union_nodos));
                        
        # Actualizamos la lista de reserva
        conjunto_nodos_iteracion_anterior  = conjunto_nodos_iteracion_actual; 
    # Creamos el grafo
    lista_lados = list(lista_lados)
    G = nx.DiGraph();
    G.add_nodes_from(lista_nodos);
    G.add_edges_from(lista_lados);
    return G'''
    



'''def construirgrafobasico(nube):
    listanodos = udosepsilon(nube);
    numnodos = len(listanodos);
    listalados = [];
    for i in range(numnodos):
        for j in range(i,numnodos):
            nodogrande = listanodos[i]; #estan en orden por como se contruye udosepsilon
            nodopeque = listanodos[j];
            if len(nodogrande)>len(nodopeque):
                if set(nodogrande).issubset(nodopeque):
                    listalados.append(nodogrande,nodopeque);
    
    G = nx.DiGraph();
    G.add_nodes_from(listanodos);
    G.add_edges_from(listalados);
    return G'''






def hacerminimal(G):
    i=0;
    numnodos = len(list(G.nodes));
    while i<numnodos and numnodos>1:
        #print(list(G.nodes));
        nodo = list(G.nodes)[i];
        sucesores = list(G.successors(nodo));
        #print(sucesores);
        predecesores = list(G.predecessors(nodo));
        if len(sucesores) == 1:
            sucesor = sucesores[0];
            lista1 = [];
            G.remove_node(nodo)
            for n in predecesores:
                lista1.append((n,sucesor));
            G.add_edges_from(lista1);
            return hacerminimal(G)
        elif len(predecesores) == 1:
            predecesor = predecesores[0];
            lista1 = [];
            G.remove_node(nodo);
            for n in sucesores:
                lista1.append((predecesor,n));
            G.add_edges_from(lista1);
            return hacerminimal(G)
        else:
            i = i+1;
    return G


def dibujargrafo(G):
    for nodo in list(G.nodes):
        G.nodes[nodo]["layer"] = len(nodo);
    pos = nx.multipartite_layout(G,'layer', 'horizontal', 1, None);
    plt.figure();
    nx.draw(G, pos, with_labels = True);




'''for i in range(10,12):
    epsilon = (2*math.pi)/i;
    pi  = math.pi; 
    nube = crearnubecirculo(epsilon);
    n = len(nube);
    print(nube);
    matrizdistancias = matdistdos(nube);
    G = construirgrafo(nube);
    #dibujargrafo(G);
    H = hacerminimal(G);
    dibujargrafo(H);
plt.show()'''


for i in range(7,10):
    epsilon = (2*math.pi)/i;
    pi  = math.pi; 
    nube = crearnubeocho(epsilon);
    n = len(nube);
    print(nube);
    matrizdistancias = matdistdos(nube);
    G = construirgrafo(nube);
    #dibujargrafo(G);
    H = hacerminimal(G);
    dibujargrafo(H);
plt.show()






'''la idea es
itero el proceso n veces
en cada una tengo que
creo combinacion posible de aub con listanodos
si tiene diam<2eps lo meto y meto el lado
y en la proxima iteracion parto solo con los de longitud la anterior. o sea creo una nueva lista en cada iteracion
'''


'''# Sample list of data
data_list = list(G.edges)

# Name of the text file you want to create
file_name = "data.txt"

# Open the file in write mode
with open(file_name, "w") as file:
    # Loop through the list and write each item to a new line in the file
    for item in data_list:
        file.write(str(item))

print(f"Data has been written to {file_name}")


'''