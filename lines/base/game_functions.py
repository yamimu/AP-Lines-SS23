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
    """
    setup for animation of graph, creates one node for each edge of the start node
    returns graph with n + 1 nodes n being amount of edges who all have the coords
    of the start_node
    runner_info is to store information along what edge the node is expanding
    :param g: graph to fill
    :param start_index: start_index of node in graph from which to start

    return: new_graph, runner_info

    """
    neighbour_indices = g.adjacency_matrix[start_index].nonzero()[0]
    ng = Graph([g.nodes[start_index]])
    runner_info = []
    for neigh_index in neighbour_indices:
        node = Node(g.nodes[start_index].coord)
        ng.add_node(node,[0])
        runner_info.append((node,g.nodes[neigh_index]))
    
    return ng, runner_info
    

def next_step(og, g, runner_info, step_length: float):
    """
    returns the next step of the expansion of g into og  returning an updated graph and runner_info
    !!! currently only expands along edge from one side and only expands until next node
    :param og: original graph to be simulated
    :param g: current iteration of graph to be further expanded
    :param runner_info: information about expanding nodes
    :param step_length: how far the expanding nodes are allowed to travel

    :return:  g, runner_info updated with current expansion step
    """

    
    runner_info_coord_list = np.array([[n.coord, m.coord] for n,m in runner_info])
    vs = runner_info_coord_list[:,1] - runner_info_coord_list[:,0]
    passed = np.linalg.norm(vs,axis = 1) <= step_length
    rest_distance = step_length - np.linalg.norm(vs,axis=1)
    norm_vs = np.linalg.norm(vs,axis = 1)
    us = vs/ norm_vs[:,None]

    runner_new_coord = runner_info_coord_list[:,0] + step_length * us

    for i, new_coord in enumerate(runner_new_coord):
        if(not passed[i]):
            runner_info[i][0].coord = new_coord
            continue

        og_node = runner_info[i][1]
        og_node_index = og.nodes.index(og_node)
        
        ### Isolated Code 
        zg, zri = inital_step(og,og_node_index)
        
        zri = [info for info in zri if info[1] not in g.nodes]
        if len(zri) > 0:
            zg ,zri = next_step(og, zg, zri, rest_distance[i])

        print(f"zg: {len(zg.nodes)},\n zri: {len(zri)}")
        ### end isolated code
        
        neighbour_indices = og.adjacency_matrix[og.nodes.index(og_node)].nonzero()[0]
        new_edges = []
        for j in neighbour_indices:
            if not((j,og_node_index) in g.edge_list):# or (og_node_index,j) in g.edge_list):
                new_edges.append((og_node_index,j))
        
        print(new_edges)
        #print(neighbour_indices)
        
        for start_index,target_index in new_edges:
            print(og.nodes[start_index].coord)
            temp_node = Node(og.nodes[start_index].coord)
            g.add_node(temp_node,[start_index])
            runner_info.append((temp_node,og.nodes[target_index]))

        print(len([n for n in g.nodes]))
        g.nodes[g.nodes.index(runner_info[i][0])] = og_node
        runner_info[i] = (runner_info[i][1],-1)
        
    for info in runner_info:
        if info[1] == -1:
            runner_info.remove(info)
    

    return g, runner_info


if __name__ == "__main__":
    og = Graph([Node([0,0]), Node([1,1]), Node([2,0]), Node([2,1])],
               [(0,1),(0,2),(1,2),(1,3)])
    ng, runner_info = inital_step(og, 0)
    g, runner_info = next_step(og,ng,runner_info, 1.5)
    g, runner_info = next_step(og,g,runner_info, .8) 
    #print([n.coord for n in g.nodes])
    #print([n.coord for n, i in runner_info])
    g = g.toNx()
    
    nx.draw_networkx(g, nx.get_node_attributes(g, 'pos'), labels=nx.get_node_attributes(g, 'label'))
    plt.show()

    