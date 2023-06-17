from .graph import Graph, Node
from .graph_base_functions import find_point_on_graph

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt



def set_start_point(x:int ,y:int, g: Graph):
    """
        creates a Node to start on the graph from given coordinates. Checks if point is on graph.
        :param self:
        :param edge:

        :return: None
        :raises: None
        """
    start = Node((x,y))

    graph_nodes = find_point_on_graph(g,start)
    
    if graph_nodes != None:
        if len(graph_nodes) > 1:
            g.remove_edge((graph_nodes[0],graph_nodes[1]))   
            g.add_node(start,[graph_nodes[0],graph_nodes[1]])
            g.add_start_node(start)
        if len(graph_nodes) == 1:
            g.add_start_node(graph_nodes[0])
         
            

def next_step(g, start_index, step_length):
    neighbour_indices = g.adjacency_matrix[start_index].nonzero()[0]

    neighbour_coord_list = np.array([n.coord for n in np.array(g.nodes)[neighbour_indices]])
    runners_coord_list = np.array([g.nodes[start_index].coord.T for i in range(len(neighbour_indices))])

    vs = (neighbour_coord_list - runners_coord_list)
    us = vs / np.linalg.norm(vs,axis = 1)
    runners_coord_list = runners_coord_list + step_length * us
    ng = Graph([g.nodes[start_index]])
    for entry in runners_coord_list:
        ng.add_node(Node(entry),[0])
    
    return ng
    #coord_bp = step_length / \
    #            * na.coord + best_node.coord




if __name__ == "__main__":
    g = Graph([Node([0,0]),Node([1,0]), Node([2,0])],[(0,1),(1,2)])
    g = next_step(g, 1, 0.2).toNx()
    nx.draw_networkx(g, nx.get_node_attributes(g, 'pos'), labels=nx.get_node_attributes(g, 'label'))
    plt.show()

    