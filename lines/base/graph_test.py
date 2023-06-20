import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.animation as animation


G = nx.Graph()
G.add_node(1)
G.add_node(2)
G.add_node(3)


def update(frame):
    # Add a new node to the graph
    new_node = len(G) + 1
    G.add_node(new_node)

    # Connect the new node to existing nodes
    for node in G.nodes():
        if node != new_node:
            G.add_edge(new_node, node)

    # Clear the current plot
    plt.clf()

    # Draw the updated graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)

    # Set the title for the current frame
    plt.title("Frame {}".format(frame))


ani = animation.FuncAnimation(plt.gcf(), update, frames=10, interval=1000)

plt.show()
