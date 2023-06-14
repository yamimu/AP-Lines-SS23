import numpy as np
from numpy.linalg import norm
import math
from .graph import Graph, Node
from vectors import *
from mathutils.geometry import intersect_point_line

def shortest_distance(p1, p2, p3):
    intersect = intersect_point_line(p3, p2, p1)
    return (intersect[0],norm(np.cross(p2-p1, p1-p3))/norm(p2-p1))

def check_point_on_node(point,nodes):
    for i in nodes:
        if i.coord[0] == point.coord[0]:
            if i.coord[1] == point.coord[1]:    
                return [i]
    return None

def check_point_on_line(point, i):
    if i[0] == "vertical":
        if i[1](0) == point.coord[0]: 
            return True           
    else:
        if i[1](point.coord[0]) == point.coord[1]:   
            return True
    return False

def check_point_between_nodes(point,edge_points, i):
    if i == "vertical":
        if edge_points[0].coord[1] < edge_points[1].coord[1]:
           if edge_points[0].coord[1] <= point.coord[1] and point.coord[1] <= edge_points[1].coord[1]:
               return [edge_points[0],edge_points[1]]
        if edge_points[0].coord[1] < edge_points[1].coord[1]:
            if edge_points[1].coord[1] <= point.coord[1] and point.coord[1] <= edge_points[0].coord[1]:
               return [edge_points[0],edge_points[1]]
           
    else:
        if edge_points[0].coord[0] < edge_points[1].coord[0]:
            if edge_points[0].coord[0] <= point.coord[0] and point.coord[0] <= edge_points[1].coord[0]:
                return [edge_points[0],edge_points[1]]
        if edge_points[0].coord[0] < edge_points[1].coord[0]:
            if edge_points[1].coord[0] <= point.coord[0] and point.coord[0] <= edge_points[0].coord[0]:
               return [edge_points[0],edge_points[1]]
        if edge_points[0].coord[0] == edge_points[1].coord[0]:
            if edge_points[0].coord[0] == point.coord[0]:
               return [edge_points[0],edge_points[1]]

def check_point_on_graph(g : Graph, point : Node) -> list:
    """
        checks if a given point is on the graph. First genarates an edge list 
        of Nodes with an edge. 
        Next it generates a straight-line function based on both connected nodes.
        It differentiats between vertical lines and lines with a gradient. 
        Afterwards the point ist tested if it is on a line by putting the x of 
        the point into the functions and checking if the y is the same as the 
        result. Then it is checked if the Point ist between the 2 Nodes that defined 
        the function. Returns the 2 Nodes the point is between of, one Node if point has same x and y or None.  

        :param g: the Graph class containing the graph to check.
        :param point: Node checked to be on graph.

        :return: List of Nodes 
        :raises: Node
    """    
    on_node = check_point_on_node(point,g.nodes)
    if on_node != None:
        return on_node
            
    edges = []
    for i in g.edge_list:
        edges.append([g.nodes[i[0]],g.nodes[i[1]]])
    
    func_list=[]
    for i in edges:
        deltax = (i[0].coord[0] - i[1].coord[0])
        deltay = (i[0].coord[1] - i[1].coord[1])
        if deltay == 0:
            func = lambda m,y=i[0].coord[1] : y
            kind= "horizontal"
        if deltax == 0:
            func = lambda m,x=i[0].coord[0] : x 
            kind = "vertical"
        if deltax != 0 and deltay != 0:
            steige = deltax / deltay
            start = i[0].coord[1] - (i[0].coord[0]*steige)
            func = lambda x,m=steige,b=start : m*x+b
            kind= "neigung"
        func_list.append((kind,func))
    
    distance = []
    for i in  func_list:
        edge_points = edges[func_list.index(i)]
        on_line = check_point_on_line(point,i)
        on_graph = None
        if on_line==True:
            on_graph = check_point_between_nodes(point,edge_points,i[0])
            if on_graph!= None:
                return on_graph  
        if i[0] == "vertical":
            if on_line:
                max_y = max([edge_points[0].coord[1],edge_points[1].coord[1]])
                min_y = min([edge_points[0].coord[1],edge_points[1].coord[1]])
                if point.coord[1] > max_y:
                    dis = point.coord[1] - max_y
                if point.coord[1] < min_y:
                    dis = min_y - point.coord[1] 
            else:
                dis = point.coord[0]-edge_points[0].coord[0]
                
        elif i[0] == "horizontal":
            if on_line:
                max_x = max([edge_points[0].coord[0],edge_points[1].coord[0]])
                min_x = min([edge_points[0].coord[0],edge_points[1].coord[0]])
                if point.coord[0] > max_x:
                    dis = point.coord[0] - max_x
                if point.coord[0] < min_x:
                    dis = min_x - point.coord[0]
            else:
                dis = point.coord[1]-edge_points[0].coord[1]
                
        elif i[0] == "neigung":
            if on_line:
                max_x = max([edge_points[0].coord[0],edge_points[1].coord[0]])
                nod_max = filter( lambda x : x.coord[0]==max_x, edge_points)
                min_x = min([edge_points[0].coord[0],edge_points[1].coord[0]])
                nod_min = filter( lambda x : x.coord[0]==min_x, edge_points)
                if point.coord[0] > max_x:
                    dis = math.dist(point.coord,nod_max.coord)
                if point.coord[0] < min_x:
                    dis = math.dist(point.coord,nod_min.coord)
            else:
                dis = (shortest_distance(edge_points[0].coord,edge_points[1].coord,point.coord))
        
        if isinstance(dis,tuple):
            c = dis[1]
        else:
            c = abs(dis)
            
        max_dis = 0.5
        if abs(c) < max_dis:
            new_point = None
            if i[0] == "vertical":
                new_point = Node((edge_points[0].coord[0],point.coord[1]))
            elif i[0] == "horizontal": 
                new_point = Node((point.coord[0],edge_points[0].coord[0]))
            elif i[0] == "neigung":
                new_point = Node(tuple(dis[0]))
            
            new_on_graph = check_point_on_node(new_point,g.nodes)
            if new_on_graph != None:
                new_on_graph.append(new_point)
                distance.append((new_on_graph,c))
            new_on_graph = check_point_between_nodes(new_point,edge_points,i[0])
            if new_on_graph != None:
                new_on_graph.append(new_point)
                distance.append((new_on_graph,c))
            if new_on_graph == None:
                if math.dist(new_point.coord,edge_points[0].coord) <= math.dist(new_point.coord,edge_points[1].coord):
                    c = math.hypot(math.dist(new_point.coord,edge_points[0].coord),c)
                    if c < max_dis:
                        distance.append((edge_points[0],c))
                else:
                    c = math.hypot(math.dist(new_point.coord,edge_points[1].coord),c)
                    if c < max_dis:
                        distance.append((edge_points[1],c))
                
    if len(distance) > 0:
        smallest = distance[0]
        for i in distance:
           if i[1] < smallest[1]:
                smallest=i 
        return smallest[0]
    
    return None               

node0 = Node(coord = [0,0])
node1 = Node(coord = [0,4])
node2 = Node(coord = [4,4])
node3 = Node(coord = [4,0])
node4 = Node(coord = [4.01,4.1])
edges = [(0,1),(0,3),(0,2),(1,2),(2,3)]
g = Graph([node0,node1,node2,node3], edges)
nod= check_point_on_graph(g,node4)

