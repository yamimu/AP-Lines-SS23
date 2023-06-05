import numpy as np
from graph import Graph
from graph import Node

def check_point_on_graph(g : Graph, point : Node) -> bool:
    """
        checks if a given point is on the graph. First genarates an edge list 
        with tuple of two Nodes with an edge. 
        Next it generates a straight-line function based on both connected nodes.
        It differentiats between vertical lines and lines with a gradient. 
        Afterwards the point ist tested if it is on a line by putting the x of 
        the point into the functions and checking if the y is the same as the 
        result. Then it is checked if the Point ist between the 2 Nodes that defined 
        the function.  

        :param g: the Graph class containing the graph to check.
        :param point: Node checked to be on graph.

        :return: bool. True if point is on graph
        :raises: Node
        """
    
    edges = []
    matrix = g.adjacency_matrix
    for i in range(0,g.n_nodes):
        for j in range(0,g.n_nodes):
            if matrix[i][j] > 0:
                edges.append([g.nodes[i],g.nodes[j]])
                matrix[i][j] = 0
                matrix[j][i] = 0
    
    func_list=[]
    for i in edges:
        deltax = (i[0].coord[0] - i[1].coord[0])
        deltay = (i[0].coord[1] - i[1].coord[1])
        if deltay == 0:
            func = lambda m,x=i[0].coord[1] : x
            vertical= False
        if deltax == 0:
            func = lambda x=i[0].coord[0] : x 
            vertical = True
        if deltax != 0 and deltay != 0:
            steige = deltax / deltay
            start = i[0].coord[1] - (i[0].coord[0]*steige)
            func = lambda x,m=steige,b=start : m*x+b
            vertical= False
        func_list.append([vertical,func])
    
    for i in  func_list:
        if i[0] == True:
            if i[1]() == point.coord[0]: 
                edge_points = edges[func_list.index(i)]
                if edge_points[0].coord[1] < edge_points[1].coord[1]:
                   if edge_points[0].coord[1] <= point.coord[1] & point.coord[1] <= edge_points[1].coord[1]:
                       return True
                if edge_points[0].coord[1] < edge_points[1].coord[1]:
                   if edge_points[1].coord[1] <= point.coord[1] & point.coord[1] <= edge_points[0].coord[1]:
                       return True           
        if i[0] == False:
            if i[1](point.coord[0]) == point.coord[1]:   
                edge_points = edges[func_list.index(i)]
                if edge_points[0].coord[0] < edge_points[1].coord[0]:
                    if edge_points[0].coord[0] <= point.coord[0] & point.coord[0] <= edge_points[1].coord[0]:
                       return True
                if edge_points[0].coord[0] < edge_points[1].coord[0]:
                    if edge_points[1].coord[0] <= point.coord[0] & point.coord[0] <= edge_points[0].coord[0]:
                       return True
                if edge_points[0].coord[0] == edge_points[1].coord[0]:
                    if edge_points[0].coord[0] == point.coord[0]:
                       return True

    return False

node0 = Node(coord = [0,0])
node1 = Node(coord = [0,4])
node2 = Node(coord = [4,4])
node3 = Node(coord = [4,0])
node4 = Node(coord=[5,0])
edges = [(0,1),(0,3),(0,2),(1,2),(2,3)]
g = Graph([node0,node1,node2,node3], edges)
print(check_point_on_graph(g,node4))