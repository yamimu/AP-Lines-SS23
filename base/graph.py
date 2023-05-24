import numpy as np

# shortest path

class Node:
    #ndim vector 
    def __init__(self, coord = None, adjacent_Nodes = None) -> None:
        self.adjacent_Nodes = []
        if coord != None:
            if type(coord) != np.array:
                coord = np.array(coord)
            self.coord = coord
            if adjacent_Nodes != None:
                self.adjacent_Nodes = [node for node in adjacent_Nodes if node.dim() == self.dim()]
        else:
            self.coord = [0,0]

    def calculate_distance_to(self,node):
        ''' 
        
        '''
        if self.dim() != node.dim():
            raise(ValueError("dim don't match"))
        return np.sqrt(np.sum(np.power(self.coord - node.coord,2)))

    def dim (self) -> int:
       return len(self.coord)
    

class Graph:
    def __init__(self,nodes, edges = None, undirected = True) -> None:

        self.n_nodes = len(nodes)
        self.undirected = undirected
        self.nodes = nodes
        self.adjacency_matrix = np.zeros((len(nodes),len(nodes)))
        
        if edges != None:
            for edge in edges:
                i,j = self.check_edge(edge)
                w = self.nodes[i].calculate_distance_to(self.nodes[j])
                #add weights here
                if undirected:
                    self.adjacency_matrix[i][j] = w
                self.adjacency_matrix[j][i] = w

    def to_index(self,node):
        if type(node) != Node:
            raise(ValueError("can only convert Nodes to indices"))
        if node not in self.nodes:
            raise(ValueError("node not in list"))
        return self.nodes.index(node)

    def check_edge(self,edge):

        if type(edge[0]) != type(edge[1]):
            raise(ValueError("edge type missmatch"))
        if type(edge[0]) not in [Node, int]:
            raise(ValueError("edge must contain either nodes or indices"))
        if type(edge[0]) == Node :
            i,j = self.to_index(edge[0]), self.to_index(edge[1])
        if type(edge[0]) == int :
            i,j = edge[0], edge[1]
        return i,j
    
    
    def add_edge(self,edge):

        i,j = self.check_edge(edge)
        w = self.nodes[i].calculate_distance_to(self.nodes[j])
        self.adjacency_matrix[i][j] = w
        if self.undirected:
            self.adjacency_matrix[j][i] = w

    def remove_edge(self,edge):

        i,j = self.check_edge(edge)
        self.adjacency_matrix[i][j] = 0
        if self.undirected:
            self.adjacency_matrix[j][i] = 0


    
        
        


node0 = Node(coord = [0,0])
node1 = Node(coord = [0,2])
node2 = Node(coord = [1,1])
node3 = Node(coord = [7,9])

edges = [(0,1),(1,2)]
g = Graph([node0,node1,node2], edges)
print(g.adjacency_matrix)