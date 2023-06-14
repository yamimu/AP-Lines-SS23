import numpy as np

# shortest path

class Node:
    """
    Represents a single node in a Graph, does not contain any
    knowledge about other nodes
    """
    def __init__(self, coord = None) -> None:
        """
        Initalizes a Node with n Dimensional Coordinates
        :param self:
        :param coord: (default = [0,0])

        :return: None
        :raises: None
        """
        if coord is not None:
            if type(coord) != np.array:
                coord = np.array(coord)
            self.coord = coord
        else:
            self.coord = np.array([0,0])

    def euclidian_distance(self,node):
        ''' 
        calculates the euclidian distance between self and
        another node, when the dimensions match
        :param self:
        :param node:

        :return: distance as float
        :raises: ValueError('dim don't match')
        '''
        if self.dim() != node.dim():
            raise(ValueError("dim don't match"))
        return np.sqrt(np.sum(np.power(self.coord - node.coord,2)))

    def dim (self) -> int:
       return len(self.coord)
    


class Graph:
    """
    This class represents weighted graphs using adjacency matrices
    """
    def __init__(self,nodes, edges = None, undirected = True) -> None:
        """
        :param self:
        :param nodes: nodes of the graph
        :param edges: (default None) 
            can either be type(Node) or indices of nodes
        :param undirected: (default = False)
            bool specifying if graph is directed 
            --> graph directed
        :return: Graph
        :raises: check_edge errors
        """
        self.n_nodes = len(nodes)
        self.undirected = undirected
        self.nodes = nodes
        self.adjacency_matrix = np.zeros((len(nodes),len(nodes)))
        self.edge_list = []
        self.start_nodes = []
        
        if edges != None:
            self.edge_list = edges
        
        if edges != None:
            for edge in edges:
                i,j = self.check_edge(edge)
                w = self.nodes[i].euclidian_distance(self.nodes[j])
                #add weights here
                if undirected:
                    self.adjacency_matrix[i][j] = w
                self.adjacency_matrix[j][i] = w

    def index_of(self,node):
        """
        returns the index of a node in this graph to be able to use
        indices when working with edges instead of always looking up
        edges
        :param self:
        :param node: node which index to be returned
        
        :return: index of node if node is part of the graph
        :raises: 'can only convert Node to indices' and 'node not in list'
        """
        if type(node) != Node:
            raise(ValueError("can only convert Nodes to indices"))
        if node not in self.nodes:
            raise(ValueError("node not in list"))
        return self.nodes.index(node)

    def check_edge(self,edge):
        """
        performs type checks on a given edge to prevent invalid inputs
        :param self:
        :param edge:
        :return: i,j index of first and second node in edge
        :raises: edge type missmatch; index_of errors
        """
        if type(edge[0]) != type(edge[1]):
            raise(ValueError("edge type missmatch"))
        if type(edge[0]) not in [Node, int]:
            raise(ValueError("edge must contain either nodes or indices"))
        if isinstance(edge[0],Node) :
            i,j = self.index_of(edge[0]), self.index_of(edge[1])
        if isinstance(edge[0], int) :
            i,j = edge[0], edge[1]
        return i,j
    
    
    def add_edge(self,edge, w = None):
        """
        adds edge to graph automatically calculating the euclidian distance
        as the weight respects directionality

        :param self:
        :param edge: edge to be added
        :param w: (default = None) weight to be put in the adjacency_matix

        :return: None
        :raises: Node
        """
        i,j = self.check_edge(edge)
        if w == None:
            w = self.nodes[i].euclidian_distance(self.nodes[j])
        self.adjacency_matrix[i][j] = w
        if self.undirected:
            self.adjacency_matrix[j][i] = w   
        

    def remove_edge(self,edge):
        """
        removes edge from graph respects directionality
        :param self:
        :param edge:

        :return: None
        :raises: None
        """
        i,j = self.check_edge(edge)
        self.adjacency_matrix[i][j] = 0
        if self.undirected:
            self.adjacency_matrix[j][i] = 0
        self.edge_list.remove((i,j))
            
            
    def add_node(self,point,edges = None):
        """
        adds new node into graph 
        :param self:
        :param point:
        :param edges (default = None):

        :return: None
        :raises: None
        """

        self.nodes.append(point)
        self.n_nodes = len(self.nodes)
        if edges  != None:
            if isinstance(edges[0],Node):
                for i in range(0,len(edges)):
                    edges[i] = self.index_of(edges[i])
            tup_edge = []
            for i in edges:
                tup_edge.append((i,self.n_nodes-1))
            self.edge_list.extend(tup_edge)
        adma = np.zeros((len(self.nodes),len(self.nodes)))
        adma[0:len(self.nodes)-1,0:len(self.nodes)-1] = self.adjacency_matrix 
        self.adjacency_matrix = adma
        if edges != None:
            for i in tup_edge:
                self.add_edge(i)

            
            
    def delete_node(self,point):
        """
        deletes existing node in graph 
        :param self:
        :param point:

        :return: None
        :raises: None
        """
        j = self.index_of(point)
        edges= []
        for i in range(0,g.n_nodes):
            if self.adjacency_matrix[i][j] > 0:
                if i < j:
                    edges.append((i,j))
                if j < i:
                    edges.append((j,i))
        for i in edges:
            self.edge_list.remove(i)
        self.adjacency_matrix = np.delete(self.adjacency_matrix,j,axis=0)
        self.adjacency_matrix = np.delete(self.adjacency_matrix,j,axis=1)
        self.nodes.remove(point)
        self.n_nodes = len(self.nodes)

    def get_weight(self, edge):
        """
        returns the weight of the edge in this graph
        :param self:
        :param edge:

        :return: weight
        :raises: None
        """
        i,j = self.check_edge(edge)
        return self.adjacency_matrix[i][j]
    
    def add_start_node(self,point:Node):
        """
        adds an starting point to color on this graph
        :param self:
        :param point:

        :return: None
        :raises: None
        """
        self.start_nodes.append(point)
    
            


    
        
if __name__ == "__main__":

    node0 = Node(coord = [0,0])
    node1 = Node(coord = [0,2])
    node2 = Node(coord = [1,1])
    node3 = Node(coord = [7,9])

    edges = [(0,1),(1,2)]
    g = Graph([node0,node1,node2], edges)
    print(g.edge_list)
    g.add_node(node3,[g.nodes[0],g.nodes[1]])
    print(g.edge_list)