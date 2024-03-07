from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt
import clouds as cd
import distances as dist
import math

# although it might seem easier to define a function giving the entire graph,
# we prefer to calculate first the nodes and then the edges, as this saves a lot of
# node checking and the calculation of the edges is quite simple.

def get_nodes(cloud, eps):
    two_eps = 2*eps
    dist_matrix = dist.dist_matrix(cloud)
    nodes = [(i,) for i in range(len(cloud))]
    prev_nodes = nodes.copy()
    
    # we continue if we have added more than 1 node in the last iteration
    while len(prev_nodes)>1:
        new_nodes = []
        # we call the sets of nodes "a" and "b" 
        for a, b in combinations(prev_nodes, 2):
            # if they aren't equal in every coordinate but 1, we don't need to check
            # because there must exist a combination that gives the same aub
            # with equal starting coordinates
            if not a[:-1] == b[:-1]:
                continue
            else:
                # compute union(a, b) and check if its diameter is less than 2eps
                # note that, as a and b are nodes and equal in every coord but the last one,
                # diam(a, b)<2eps iff dist(a[-1], b[-1])<2eps
                if dist_matrix[a[-1]][b[-1]] < two_eps:
                    aub = tuple(sorted(set(a+b)))
                    new_nodes.append(aub)
                    nodes.append(aub)
        prev_nodes = new_nodes
    return nodes

def get_edges(nodes):
    edges = []
    for a in nodes:
        n = len(a)
        if n == 1:
            continue

        # we add all its immediately inferior nodes
        for b in combinations(a, n-1):
            edges.append((b, a))
    return edges

def make_graph(nodes, edges):
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G

# this function is not recursive as the number of iterations can be quite large
# but the process it does is very well understood when looked recursively:
# it finds nodes with only one successor or predecessor and removes them
# as this doesn't change the homotopy type of the space. 

def minimal_graph(G):
    nodes = list(G.nodes)
    n = len(nodes)
    i = 0
    while i<n:
        if len(nodes)<2:
            return G
        node = nodes[i]
        successors = list(G.successors(node))
        predecessors = list(G.predecessors(node))
        if len(successors) == 1:
            successor = successors[0]
            G.remove_node(node)
            G.add_edges_from([(n, successor) for n in predecessors])
            i = -1
            n = n-1
            nodes = list(G.nodes)
        else:
            if len(predecessors) == 1:
                predecessor = predecessors[0]
                G.remove_node(node)
                G.add_edges_from([(predecessor, n) for n in successors])
                i = -1
                n = n-1
                nodes = list(G.nodes)
        i += 1
    return G

def draw_graph(G, ax):
    for node in list(G.nodes):
        G.nodes[node]["layer"] = len(node)
    pos = nx.multipartite_layout(G,'layer', 'horizontal', 1, None)
    nx.draw(G, pos, with_labels = True, ax = ax)

# we define the final function: given a list of points in 3d/2d and an eps it calculates
# and plots the points in space and the Hasse diagram of the minimal space
    
def plot_minimal_3d(cloud, eps):
    nodes = get_nodes(cloud, eps)
    print('nodes ready')
    edges = get_edges(nodes)
    print('edges ready')
    G = make_graph(nodes, edges)
    print('graph ready')
    G = minimal_graph(G)
    print('graph reduced to minimal')
    
    fig = plt.figure(figsize=(10,5))
    ax1 = fig.add_subplot(1,2,1, projection='3d')
    
    x_coords, y_coords, z_coords = zip(*cloud)
    ax1.scatter(x_coords, y_coords, z_coords, marker = 'o', color = 'blue')
    
    ax2 = fig.add_subplot(1,2,2)
    draw_graph(G, ax = ax2)
    
    plt.show()

def plot_minimal_2d(cloud, eps):
    nodes = get_nodes(cloud, eps)
    print('nodes ready')
    edges = get_edges(nodes)
    print('edges ready')
    G = make_graph(nodes, edges)
    print('graph ready')
    G = minimal_graph(G)
    print('graph reduced to minimal')
    
    fig = plt.figure(figsize=(10,5))
    ax1 = fig.add_subplot(1,2,1)
    
    x_coords, y_coords = zip(*cloud)
    ax1.scatter(x_coords, y_coords, marker = 'o', color = 'blue')
    
    ax2 = fig.add_subplot(1,2,2)
    draw_graph(G, ax = ax2)
    
    plt.show()  

# as an example, we plot the graph for the circumference
eps = 2*math.pi/80
cloud = cd.circumference_cloud(eps)
plot_minimal_2d(cloud, eps)