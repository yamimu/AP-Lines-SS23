from ..base.graph import Graph, Node
from ..base.graph_base_functions import find_point_on_graph
import copy
import numpy as np

def best_start_point(graph):
    """
    given a graph this function calculates the point on the graph,
    node or edge, that has the smallest possible distance to the
    point(a) the farthest away regarding shortest paths. 
    This algorithm uses the propertie that when walking towards a,
    we walk away from the second farthest node b. when a and b are
    equally far away, our result is a node on the graph calculated like
    best_start_node_index to find our optimal point we walk half the
    distance of the difference between the distances of a and b from the
    best_start_node towards the first node(na) on the path to a

    :param graph:
    :return: Node
    :raises: None
    """
    
    #we need the index and 
    res_floyd = floydwarshall(graph,True)
    floydwarshall_matrix = res_floyd[0]
    max_floyd = np.max(floydwarshall_matrix,axis= 0)
    best_index = np.argmin(max_floyd)
    
    #print(floydwarshall_matrix[best_index])
    sorted_by_dist = np.argsort(floydwarshall_matrix[best_index])
    a_index, b_index = sorted_by_dist[-1], sorted_by_dist[-2]
    if graph.adjacency_matrix[best_index][a_index] ==\
        graph.adjacency_matrix[best_index][b_index]:
        return graph.nodes[best_index]
    
    walk_towards_A = 1/2 * (floydwarshall_matrix[best_index][a_index]\
                        - floydwarshall_matrix[best_index][b_index])
    
    na_index = construct_path(best_index, a_index, *res_floyd)[1]
    best_node ,na = graph.nodes[best_index], graph.nodes[na_index]

    coord_bp = walk_towards_A / graph.adjacency_matrix[best_index][na_index]\
                * na.coord + best_node.coord
    
    return  Node(coord= coord_bp)



def best_start_node_index(graph):   
    """
    returns the best node to start from to color a graph within the 
    minimum amout of time, decided by the shortest travel distance to 
    the node the farthest away works best for fully connected graphs
    otherwise returns solution, possibly not optimal
    :param graph: graph to find the node on
    
    :return: index of node 
    :raises: none
    """

    floydwarshall_matrix = floydwarshall(graph)
    best_index = np.argmin(np.max(floydwarshall_matrix,axis = 0)) #
    return best_index

#doesn't fully work
def dijkstra(graph, start_node):
        """
        compute the shortest distance from the start node to any node 
        reachable using dijkstras algorithm

        :param graph: graph to apply algorithm on
        :param start_node: graph to calculate distances for
        :return_paths: returns the paths (edges?) taken 

        :return: distances to nodes; (paths)
        :raises: 
        """
        adjacency_matrix = copy.deepcopy(graph.adjacency_matrix)
        # to reset edges but keep node knowledge
        adjacency_matrix[adjacency_matrix ==0] = float("inf")
        dist = np.full(adjacency_matrix.shape[0],float("inf"))
        dist[graph.index_of(start_node)] = 0
        valid_indices = [*range(graph.n_nodes)]
        i = 0

        while valid_indices:
            d_index = np.argmin(dist[valid_indices])
            v_index = valid_indices[d_index]
            neighbourhood_v = [i for i,n 
                               in enumerate(graph.adjacency_matrix[v_index])
                                 if n != 0]
            valid_indices.remove(v_index)
            for u_index in neighbourhood_v: 
                # where neighbor u has not yet been removed from Q.
                alt = dist[v_index] + adjacency_matrix[v_index][u_index]
                if alt < dist[u_index]:  #// A shorter path to u has been found
                    dist[u_index]  = alt #// Update distance of u 

        return dist



def floydwarshall(graph, return_paths = False):
        
        next = np.full_like(graph.adjacency_matrix,-1,int)
        next[graph.adjacency_matrix.nonzero()] = graph.adjacency_matrix\
                                                      .nonzero()[1]
        M = np.full_like(graph.adjacency_matrix,float('inf'))
        for x in range(len(M)):
            for y in range(len(M[0])):
                if x == y:
                    M[x][y] = 0
                if graph.adjacency_matrix[x,y] != 0:
                    M[x][y] = graph.adjacency_matrix[x][y]
        for k in range(len(M)):
            for i in range(len(M)):
                for j in range(len(M)):
                    newDistance = M[i][k] + M[k][j]
                    if newDistance < M[i][j]:
                        next[i][j] = next[i][k]
                        M[i][j] = newDistance
        if return_paths:
             return (M, next)
        return M

def construct_path(u,v, graph, next):
    # If there's no path between
    # node u and v, simply return
    # an empty array
    if (next[u][v] == -1):
        return {}
 
    # Storing the path in a vector
    path = [u]
    while (u != v):
        u = next[u][v]
        path.append(u)
 
    return path
     
        
if __name__ == "__main__":

    node0 = Node(coord = [0,0])
    node1 = Node(coord = [1,15])
    node2 = Node(coord = [-4,1])
    node3 = Node(coord = [15,1])

    edges = [(0,1),(0,2),(1,2),(1,3)]
    g = Graph([node0,node1,node2,node3], edges)

    g2 = Graph([Node([-5,0]),\
               Node([0,0]),\
                Node([6,0])],\
                    [(0,1),(1,2)])
    
    res = floydwarshall(g,True)

    print(best_start_node_index(g))
    print(best_start_point(g))
    print(floydwarshall(g,True)[1])
    #print(g.adjacency_matrix)
    #g.delete_node(node0)
    #print(g.adjacency_matrix)