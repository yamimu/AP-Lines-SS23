from .graph import Graph, Node
import copy
import numpy as np

def best_start_node_index(graph):
    """
    returns the best node to start from to color a graph within the minimum amout of time,
    decided by the shortest travel distance to the node the farthest away
    works best for fully connected graphs otherwise returns solution, possibly not optimal
    :param graph: graph to find the node on
    
    :return: index of node 
    :raises: none
    """

    floydwarshall_matrix = floydwarshall(graph)
    best_index = np.argmin(np.max(floydwarshall_matrix,axis = 0)) #
    return best_index

# doesnt work yet
def dijkstra(graph, start_node, return_paths = False):
        """
        compute the shortest distance from the start node to any node reachable using dijkstras algorithm

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
            neighbourhood_v = [i for i,n in enumerate(graph.adjacency_matrix[v_index]) if n != 0]
            valid_indices.remove(v_index)
            for u_index in neighbourhood_v: # // where neighbor u has not yet been removed from Q.
                alt = dist[v_index] + adjacency_matrix[v_index][u_index]
                if alt < dist[u_index]:               #// A shorter path to u has been found
                    dist[u_index]  = alt            #// Update distance of u 

        return dist



def floydwarshall(graph):
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
                        M[i][j] = newDistance
        return M

        
if __name__ == "__main__":

    node0 = Node(coord = [0,0])
    node1 = Node(coord = [0,2])
    node2 = Node(coord = [1,1])
    node3 = Node(coord = [7,9])

    edges = [(0,1),(1,2)]
    g = Graph([node0,node1,node2], edges)
    g.add_node(node3,[0,1])
    print(g.adjacency_matrix)
    #g.delete_node(node0)
    #print(g.adjacency_matrix)
    print(floydwarshall(g))
    print(best_start_node_index(g))
    print(dijkstra(g, g.nodes[0]))
    print(dijkstra(g, g.nodes[1]))
    print(dijkstra(g, g.nodes[2]))
    print(dijkstra(g, g.nodes[3]))