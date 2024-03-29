import numpy as np
from numpy.linalg import norm
import math
from .graph import Graph, Node

def compute_intersection(edge_point1, edge_point2, point):
    """
        computes the intersection point between point and line defined by 2 points.  

        :param edge_point1: first graph point on line 
        :param edge_point2: second graph point on line
        :param point: node not on line

        :return: Node on line
        :raises: None
    """
    if edge_point1[0] == edge_point2[0]:
        # Line is vertical
        intersection_x = edge_point1[0]
        intersection_y = point[1]  
    else:
        # Compute the direction vector of the line
        direction_vector = edge_point2 - edge_point1
        # Compute the vector from edge_point1 to the point
        x_to_z_vector = point - edge_point1
        # Calculate the parameter along the line for the intersection point
        t = np.dot(x_to_z_vector, direction_vector) / np.dot(direction_vector, direction_vector)
        
        intersection = edge_point1 + t * direction_vector
        intersection_x, intersection_y = intersection
        
    intersection = Node((intersection_x,intersection_y))
    return intersection 

def shortest_distance(edge_point1, edge_point2, point):
    """
        gives back nearest point on line and distance between point and line defined by the edgepoints.  

        :param edge_point1: first graph point on line 
        :param edge_point2: second graph point on line
        :param point: Node checked distance to graph

        :return: Tuple of intersected node on line and distance  
        :raises: None
    """
    return (compute_intersection(edge_point2, edge_point1, point),norm(np.cross(edge_point2-edge_point1, edge_point1-point))/norm(edge_point2-edge_point1))

def check_point_on_node(point,nodes):
    """
        checks if point is on existing point on graph  

        :param point: Node checked to be on graph.
        :param nodes: List of nodes in graph.

        :return: Node or None
        :raises: None
    """
    for nod in nodes:
        if nod.coord[0] == point.coord[0]:
            if nod.coord[1] == point.coord[1]:    
                return nod
    return None

def check_point_on_line(point, f):
    """
        checks if a given point is on the line.  

        :param point: Node checked to be on graph.
        :param f: Line function.

        :return: True if on line or false if not 
        :raises: None
    """
    if f[0] == "vertical":
        if f[1](0) == point.coord[0]: 
            return True           
    else:
        if f[1](point.coord[0]) == point.coord[1]:   
            return True
    return False

def check_point_between_nodes(point,edge_points, kind):
    """
        checks if a given point is between nodes on the line. Other checking process when line is vertical.  

        :param point: Node checked to be on graph.
        :param edge_points: 2 Nodes enclosing line
        :param kind: kind of line.

        :return: True if between points. False if not.
        :raises: None
    """
    if kind == "vertical":
        if edge_points[0].coord[1] < edge_points[1].coord[1]:
            if edge_points[0].coord[1] <= point.coord[1] and point.coord[1] <= edge_points[1].coord[1]:
               return True
        if edge_points[0].coord[1] > edge_points[1].coord[1]:
            if edge_points[1].coord[1] <= point.coord[1] and point.coord[1] <= edge_points[0].coord[1]:
               return True
           
    else:
        if edge_points[0].coord[0] < edge_points[1].coord[0]:
            if edge_points[0].coord[0] <= point.coord[0] and point.coord[0] <= edge_points[1].coord[0]:
                return True
        if edge_points[0].coord[0] < edge_points[1].coord[0]:
            if edge_points[1].coord[0] <= point.coord[0] and point.coord[0] <= edge_points[0].coord[0]:
                return True
        if edge_points[0].coord[0] == edge_points[1].coord[0]:
            if edge_points[0].coord[0] == point.coord[0]:
                return True
    return False

def find_point_on_graph(g : Graph, point : Node):
    """
        checks if a given point is on the graph. First genarates an edge list 
        of Nodes with an edge. 
        Next it generates a straight-line function based on both connected nodes.
        It differentiats between vertical lines and lines with a gradient. 
        Afterwards the point ist tested if it is on a line by putting the x of 
        the point into the functions and checking if the y is the same as the 
        result. Then it is checked if the Point ist between the 2 Nodes that defined 
        the function. Returns the the point on the graph and a tuple of the 2 Nodes the point is between of. If the point is on a existing Node Tuple is None.  

        :param g: the Graph class containing the graph to check.
        :param point: Node checked to be on graph.

        :return: List with point on graph and tuple of nodes enclosing point.
        :raises: Value error if graph has no nodes or point not on or near graph
    """    
    if g.n_nodes <= 0:
        raise ValueError('Graph has no Nodes')
    
    on_node = check_point_on_node(point,g.nodes)
    if on_node != None:
        return (on_node,(None))
            
    edges = []
    for i in g.edge_list:
        edges.append([g.nodes[i[0]],g.nodes[i[1]]])
    
    #creates list with line funtion of all edges
    func_list=[]
    for i in edges:
        deltax = (i[0].coord[0] - i[1].coord[0])
        deltay = (i[0].coord[1] - i[1].coord[1])
        if deltay == 0:
            func = lambda m,y=i[0].coord[1] : y
            kind= "horizontal"
        elif deltax == 0:
            func = lambda m,x=i[0].coord[0] : x 
            kind = "vertical"
        else:
            steige = deltax / deltay
            start = i[0].coord[1] - (i[0].coord[0]*steige)
            func = lambda x,m=steige,b=start : m*x+b
            kind= "pitch"
        func_list.append((kind,func))
    
    distance_list = []
    for f in  func_list:
        # checks if point is on edge of graph
        edge_points = edges[func_list.index(f)]
        on_line = check_point_on_line(point,f)
        on_edge = None
        if on_line==True:
            on_edge = check_point_between_nodes(point,edge_points,f[0])
            if on_edge:
                return (point,edge_points)  
        #checks distance between point and graph   
        if f[0] == "vertical":
            if on_line:
                max_y = max([edge_points[0].coord[1],edge_points[1].coord[1]])
                min_y = min([edge_points[0].coord[1],edge_points[1].coord[1]])
                if point.coord[1] > max_y:
                    dis = point.coord[1] - max_y
                if point.coord[1] < min_y:
                    dis = min_y - point.coord[1] 
            else:
                dis = point.coord[0]-edge_points[0].coord[0]
            c = abs(dis)
                
        elif f[0] == "horizontal":
            if on_line:
                max_x = max([edge_points[0].coord[0],edge_points[1].coord[0]])
                min_x = min([edge_points[0].coord[0],edge_points[1].coord[0]])
                if point.coord[0] > max_x:
                    dis = point.coord[0] - max_x
                if point.coord[0] < min_x:
                    dis = min_x - point.coord[0]
            else:
                dis = point.coord[1]-edge_points[0].coord[1]
            c = abs(dis)
                
        elif f[0] == "pitch":
            if on_line:
                max_x = max([edge_points[0].coord[0],edge_points[1].coord[0]])
                nod_max = filter( lambda x : x.coord[0]==max_x, edge_points)
                min_x = min([edge_points[0].coord[0],edge_points[1].coord[0]])
                nod_min = filter( lambda x : x.coord[0]==min_x, edge_points)
                if point.coord[0] > max_x:
                    dis = math.dist(point.coord,nod_max.coord)
                if point.coord[0] < min_x:
                    dis = math.dist(point.coord,nod_min.coord)
                c = abs(dis)
            else:
                dis = shortest_distance(edge_points[0].coord,edge_points[1].coord,point.coord)
                c = dis[1]
        
        #creates new_point on graph if distance c is less than max_dis    
        max_dis = 0.5
        if c < max_dis:
            new_point = None
            if f[0] == "vertical":
                new_point = Node((edge_points[0].coord[0],point.coord[1]))
            elif f[0] == "horizontal": 
                new_point = Node((point.coord[0],edge_points[0].coord[0]))
            elif f[0] == "pitch":
                new_point = dis[0]
            
            new_on_graph = check_point_on_node(new_point,g.nodes)
            if new_on_graph != None:
                distance_list.append(((new_on_graph,None),c))
            on_edge = check_point_between_nodes(new_point,edge_points,f[0])
            if on_edge:
                distance_list.append(((new_point,edge_points),c))
            if on_edge == False:
                if math.dist(new_point.coord,edge_points[0].coord) <= math.dist(new_point.coord,edge_points[1].coord):
                    c = math.hypot(math.dist(new_point.coord,edge_points[0].coord),c)
                    if c < max_dis:
                        distance_list.append(((edge_points[0],None),c))
                else:
                    c = math.hypot(math.dist(new_point.coord,edge_points[1].coord),c)
                    if c < max_dis:
                        distance_list.append(((edge_points[1],None),c))
         
    if len(distance_list) > 0:
        smallest = distance_list[0]
        for i in distance_list:
           if i[1] < smallest[1]:
                smallest=i 
        return smallest[0]
    
    raise ValueError('The given point is to far from the graph! Please choose a closer point.')   

if __name__ == "__main__":
    node0 = Node(coord = [0,0])
    node1 = Node(coord = [0,4])
    node2 = Node(coord = [4,4])
    node3 = Node(coord = [4,0])
    node4 = Node(coord = [4,4.1])
    edges = [(0,1),(0,3),(0,2),(1,2),(2,3)]
    g = Graph([node0,node1,node2,node3], edges)
    nod= find_point_on_graph(g,node4)
    print(nod)
    node4 = Node(coord = [0,4.4])
    nod= find_point_on_graph(g,node4)
    print(nod)
    node4 = Node(coord = [4.4,0])
    nod= find_point_on_graph(g,node4)
    print(nod)
    node4 = Node(coord = [-0.3,0])
    nod= find_point_on_graph(g,node4)
    print(nod)
    node4 = Node(coord = [3,0])
    nod= find_point_on_graph(g,node4)
    print(nod)
    #print(nod[1][0].coord)
    #print(nod[1][1].coord) 
