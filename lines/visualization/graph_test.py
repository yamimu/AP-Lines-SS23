import sys
import networkx as nx
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Animated Graph")

        # Create a QVBoxLayout to hold the Matplotlib figure canvas
        layout = QVBoxLayout()

        # Create a widget to hold the figure canvas
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Create an empty network graph
        self.G = nx.Graph()
        self.G.add_node(1)

        # Create a Matplotlib figure and canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Set up the Matplotlib animation
        self.animating = False
        self.animation = None

        self.create_animation()

    def create_animation(self):
        # Define the update function for the animation
        def update(frame):
            # Add a new node to the graph
            new_node = len(self.G) + 1
            self.G.add_node(new_node)

            # Connect the new node to existing nodes
            for node in self.G.nodes():
                if node != new_node:
                    self.G.add_edge(new_node, node)

            # Clear the current plot
            self.figure.clear()

            # Draw the updated graph
            pos = nx.spring_layout(self.G)
            nx.draw(self.G, pos, with_labels=True, ax=self.figure.gca())

            # Set the title for the current frame
            self.figure.suptitle("Frame {}".format(frame))

            # Refresh the canvas
            self.canvas.draw()

        # Create the animation
        self.animation = animation.FuncAnimation(self.figure, update, frames=10, interval=1000)
        self.animating = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
