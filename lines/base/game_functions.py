from typing import Tuple
from .graph import Graph, Node
from .graph_base_functions import find_point_on_graph

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt



def set_start_point(x : float ,y : float , g: Graph) -> Graph:
    """
        creates a Node to start on the graph from given coordinates.
        Checks if point is on graph. If point is on graph creates new 
        graph with point as node if it is between existing nodes or
        returns existing graph if point is on node.
        :param x: x-coordinate of point
        :param y: y-coordinate of point
        :param g: Graph which is checked

        :return: Graph
        :raises: Value error if no nodes in graph
        """
    start :Node = Node((x,y))
    graph_nodes = find_point_on_graph(g,start)
    #print(graph_nodes)
    if graph_nodes[1] is None:
        g.add_start_node(graph_nodes[0])
        return g
    else:
        new_g :Graph = Graph(g.nodes,g.edge_list)
        new_g.remove_edge(graph_nodes[1])
        new_g.add_node(graph_nodes[0],graph_nodes[1])
        new_g.add_start_node(graph_nodes[0])
        return new_g
         
            

def initial_step(g :Graph, start_index: int): 
    """
    setup for animation of graph, creates one node for each edge of the
    start node returns graph with n + 1 nodes n being amount of edges 
    who all have the coords of the start_node
    runner_info is to store information along what edge the node is 
    expanding
    :param g: graph to fill
    :param start_index: start_index of node in graph from which to start

    return: new_graph, runner_info

    """
    neighbour_indices :list[int] = g.adjacency_matrix[start_index]\
                                    .nonzero()[0]
    ng :Graph= Graph([g.nodes[start_index]])
    runner_info :list[tuple[Node,tuple(int,int)]]= []
    for neigh_index in neighbour_indices:
        node :Node = Node(g.nodes[start_index].coord)
        ng.add_node(node,[0])
        runner_info.append((node,(start_index,neigh_index)))
    
    return ng, runner_info
    

def next_step(og :Graph,
                g :Graph,
                runner_info :list[tuple[Node,tuple[int,int]]],
                step_length: float):
    """
    returns the next step of the expansion of g into og  returning an
    updated graph and runner_info
    !!! currently weird things happen when walking an edge from multiple
      sides
    :param og: original graph to be simulated
    :param g: current iteration of graph to be further expanded
    :param runner_info: information about expanding nodes and edge
        along which they expand
    :param step_length: how far the expanding nodes are allowed to 
    travel

    :return:  g, runner_info updated with current expansion step
    """

    if len(runner_info) == 0:
        return g, []

    runner_info = [info for info in runner_info if info[1] != -1]

    info_rev_edges = [j[::-1] for _,j in runner_info]
    for i,info in enumerate(runner_info):
        for j, edge in enumerate(info_rev_edges):
            if info[1] == edge:
                if np.linalg.norm(info[0].coord 
                                  - runner_info[j][0].coord)\
                < step_length:
                    print(edge)
                    g.delete_node(info[0])
                    #print(runner_info[j][0])
                    g.delete_node(runner_info[j][0])
                    g.add_edge((og.nodes[info[1][0]],og.nodes[info[1][1]]))
                    runner_info[i] = (0,-1)
                    runner_info[j] = (0,-1)
                    #g.add_edge((og.nodes[info[1][0]],og.nodes[info[1][1]]))
                break
        
    
    runner_info = [info for info in runner_info if info[1] != -1]
    if len(runner_info) == 0:
        return g, []

    runner_info_coord_list :list[list[np.ndarray]] = \
        np.array([[n.coord, og.nodes[e[1]].coord] for n,e in runner_info])
    vs :np.ndarray = runner_info_coord_list[:,1] \
                     - runner_info_coord_list[:,0]
    passed :list[bool] = np.linalg.norm(vs,axis = 1) <= step_length
    rest_distance :np.ndarray = step_length - np.linalg.norm(vs,axis=1)
    norm_vs: np.ndarray = np.linalg.norm(vs,axis = 1)
    us :np.ndarray = vs/ norm_vs[:,None]

    runner_new_coord :np.ndarray = runner_info_coord_list[:,0] \
                                    + step_length * us

    for i, new_coord in enumerate(runner_new_coord):
        if (runner_info[i][1] == -1):
            continue
        # if we don't reach a node we just update the coordinates
        if(not passed[i]):
            runner_info[i][0].coord = new_coord
            continue
        
        #we set the runner node to the target node 
        og_node :Node = og.nodes[runner_info[i][1][1]]
        og_node_index :int = og.nodes.index(og_node)
        
        zg, zri = initial_step(og,og_node_index)
        if not zri:
            continue

        if og_node in g.nodes:
            continue

        g.nodes[g.nodes.index(runner_info[i][0])] = og_node
        if len(zri) > 0:
            zg ,zri = next_step(og, zg, zri, rest_distance[i])
            for zinfo in zri:
                # here second runner logic
                try:
                    if (g.index_of(og.nodes[zinfo[1][1]]),
                        g.index_of(og.nodes[zinfo[1][0]]))\
                    in g.edge_list:
                        continue
                except ValueError:
                    ...
                
                g.add_node(zinfo[0],[og_node])
                runner_info.append(zinfo)
                    
        #print([n.coord for n in zg.nodes]) 
        #print(f"zg: {len(zg.nodes)},\n zri: {len(zri)}")
        #print(runner_info)
        runner_info[i] = (runner_info[i][0],-1)
    return g, runner_info


if __name__ == "__main__":
    from  ..optimization import shortestPath
    og = Graph([Node([0,0]), Node([1,1]), Node([2,0]), Node([2,1])],
               [(0,1),(0,2),(1,2),(1,3)])
    g, runner_info = initial_step(og, 0)
    step_length = .8
    sum_step = 0
    max_dist = 6
    while(sum_step < max_dist):
        sum_step += step_length
        g, runner_info = next_step(og,g,runner_info, step_length)
        
        #print([n.coord for n in g.nodes])
        #print([n.coord for n, i in runner_info])
        show_g = g.toNx()
        
        nx.draw_networkx(show_g,
                        nx.get_node_attributes(show_g, 'pos'),
                        labels=nx.get_node_attributes(show_g, 'label')
                        )
        plt.show()

    