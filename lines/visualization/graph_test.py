import sys
import networkx as nx
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation
from ..base.graph import Node, Graph
from ..base.game_functions import *



class MainWindow(QMainWindow):
    def __init__(self,og, start_index, step_length):
        super().__init__()

        self.setWindowTitle("Animated Graph")

        # Create a QVBoxLayout to hold the Matplotlib figure canvas
        layout = QVBoxLayout()

        # Create a widget to hold the figure canvas
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Create an empty network graph
        self.og = og
        self.step_length = step_length
        self.g ,self.runner_info = inital_step(og,start_index)

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
            self.g , self.runner_info = next_step(self.og,self.g,self.runner_info,self.step_length)
            # Clear the current plot
            self.figure.clear()

            # Draw the updated graph
            g = self.g.toNx()
            pos = nx.get_node_attributes(g, 'pos')
            ax = self.figure.add_subplot()
            labels = nx.get_node_attributes(g, 'label')
            nx.draw_networkx(g, pos, ax=ax, labels=labels,)
            ax.set_axis_on()
            ax.tick_params(left=True,
                           bottom=True,
                           labelleft=True,
                           labelbottom=True)
            self.canvas.draw()

            # Set the title for the current frame
            self.figure.suptitle("Frame {}".format(frame))

            # Refresh the canvas
            self.canvas.draw()

        # Create the animation
        self.animation = animation.FuncAnimation(self.figure, update, frames=100, interval=1)
        self.animating = True


if __name__ == "__main__":
    g1 = Graph([Node([0,0]), Node([1,1]), Node([2,0]), Node([2,1])],
               [(0,1),(0,2),(1,2),(1,3)])

    app = QApplication(sys.argv)
    window = MainWindow(g1, 0, 0.1)
    window.show()
    sys.exit(app.exec_())
