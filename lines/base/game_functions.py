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
         
            

def inital_step(g :Graph, start_index: int, step_length: float): 
    neighbour_indices = g.adjacency_matrix[start_index].nonzero()[0]

    neighbour_coord_list = np.array([n.coord for n in np.array(g.nodes)[neighbour_indices]])
    runners_coord_list = np.array([g.nodes[start_index].coord.T for i in range(len(neighbour_indices))])

    vs = (neighbour_coord_list - runners_coord_list)
    norm_vs = np.linalg.norm(vs,axis = 1)
    us = vs / norm_vs[:,None]
    #print(f"rcl: {runners_coord_list}")
    runners_coord_list = runners_coord_list + step_length * us
    #print(f"vs: {vs},\n norm_vs : {norm_vs},\n us : {us} \n")
    #print(f"rcl: {runners_coord_list}") 
    ng = Graph([g.nodes[start_index]])
    runner_info = []
    for entry, neigh_index in zip(runners_coord_list, neighbour_indices):
        ng.add_node(Node(entry),[0])
        runner_info.append((ng.n_nodes-1,neigh_index))
    
    
    return ng, runner_info
    #coord_bp = step_length / \
    #            * na.coord + best_node.coord

def next_step(og, g, runner_info, step_length: float):
    runner_info_coord_list = np.array([[g.nodes[i].coord, og.nodes[j].coord] for i,j in runner_info])
    #print(f"ricl: {runner_info_coord_list}")
    vs = runner_info_coord_list[:,1] - runner_info_coord_list[:,0]
    #print(f"vs : {vs}") 
    norm_vs = np.linalg.norm(vs,axis = 1)
    #print(f"norm_vs : {norm_vs}")
    us = vs/ norm_vs[:,None]
    #print(f"us : {us}")
    runner_new_coord = runner_info_coord_list[:,0] + step_length * us
    signs = np.sign(runner_info_coord_list[:,1] - runner_new_coord)
    print(f"signs : {signs}")
    print(f"rc : {runner_info_coord_list[:,0]}")
    print(f"rnc : {runner_new_coord}")
    #us = 


if __name__ == "__main__":
    og = Graph([Node([-1,0]),Node([0,.2]), Node([2,0])],[(0,1),(1,2)])
    ng, runner_info = inital_step(og, 1, 0.5)
    next_step(og,ng,runner_info, 1)
    g = ng.toNx()
    nx.draw_networkx(g, nx.get_node_attributes(g, 'pos'), labels=nx.get_node_attributes(g, 'label'))
    #plt.show()

    