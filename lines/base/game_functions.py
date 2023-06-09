from graph import Graph, Node
from graph_base_functions import check_point_on_graph






def set_start_point(x:int ,y:int, g: Graph):
    """
        creates a Node to start on the graph from given coordinates. Checks if point is on graph.
        :param self:
        :param edge:

        :return: None
        :raises: None
        """
    start = Node((x,y))

    graph_nodes = check_point_on_graph(g,start)
    
    if graph_nodes != None:
        if len(graph_nodes) > 1:
            g.remove_edge((graph_nodes[0],graph_nodes[1]))   
            g.add_node(start,[graph_nodes[0],graph_nodes[1]])
            g.add_start_node(start)
        if len(graph_nodes) == 1:
            g.add_start_node(graph_nodes[0])
         
            