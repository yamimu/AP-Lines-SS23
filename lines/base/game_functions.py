from graph import Graph, Node
from graph_base_functions import find_point_on_graph


def set_start_point(x:int ,y:int, g: Graph):
    """
        creates a Node to start on the graph from given coordinates. Checks if point is on graph.
        :param self:
        :param edge:

        :return: None
        :raises: None
        """
    start = Node((x,y))
    try:
        graph_node = find_point_on_graph(g,start)
    except ValueError as er:
        print(er)
        return None
    
    
    if graph_node[0] in g.nodes:
        return g
    else:
        new_g = Graph(g.nodes,g.edge_list)
        new_g.remove_edge(graph_node[1])
        new_g.add_node(graph_node[0],graph_node[1])
        return new_g
    
         
         
'''node0 = Node(coord = [0,0])
node1 = Node(coord = [0,4])
node2 = Node(coord = [4,4])
node3 = Node(coord = [4,0])
node4 = Node(coord = [2,8])
edges = [(0,1),(0,3),(0,2),(1,2),(2,3)]
g = Graph([node0,node1,node2,node3], edges)
nod= set_start_point(node4.coord[0],node4.coord[1],g)'''   