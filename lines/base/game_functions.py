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
    
    if graph_nodes != None:
        if len(graph_nodes) > 1:
            g.remove_edge((graph_nodes[0],graph_nodes[1]))   
            g.add_node(start,[graph_nodes[0],graph_nodes[1]])
            g.add_start_node(start)
        if len(graph_nodes) == 1:
            g.add_start_node(graph_nodes[0])
         
            

def inital_step(g :Graph, start_index: int): 
    neighbour_indices = g.adjacency_matrix[start_index].nonzero()[0]
    ng = Graph([g.nodes[start_index]])
    runner_info = []
    for neigh_index in neighbour_indices:
        node = Node(g.nodes[start_index].coord)
        ng.add_node(node,[0])
        runner_info.append((node,neigh_index))
    
    return ng, runner_info
    

def next_step(og, g, runner_info, step_length: float):
    runner_info_coord_list = np.array([[node.coord, og.nodes[j].coord] for node,j in runner_info])
    #print(f"ricl: {runner_info_coord_list}")
    vs = runner_info_coord_list[:,1] - runner_info_coord_list[:,0]
    passed = np.where(np.linalg.norm(vs,axis = 1) <= step_length)
    runner_info_coord_list[passed]
    zg , zri = inital_step(og, runner_info_coord_list[passed[0]])
    print(f"passed?: {passed}")
    #print(f"vs : {vs}") 
    norm_vs = np.linalg.norm(vs,axis = 1)
    #print(f"norm_vs : {norm_vs}")
    us = vs/ norm_vs[:,None]
    #print(f"us : {us}")
    runner_new_coord = runner_info_coord_list[:,0] + step_length * us
    print(f"rc : {runner_info_coord_list[:,0]}")
    print(f"rnc : {runner_new_coord}")
    
    return g, runner_info


if __name__ == "__main__":
    og = Graph([Node([0,0]), Node([1,1]), Node([2,0])],
               [(0,1),(0,2),(1,2)])
    ng, runner_info = inital_step(og, 0)
    next_step(og,ng,runner_info, 1.5)
    
    #nx.draw_networkx(g, nx.get_node_attributes(g, 'pos'), labels=nx.get_node_attributes(g, 'label'))
    #plt.show()

    