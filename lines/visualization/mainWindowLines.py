# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'visualization\MainWindowLines.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx 
import numpy as np
from ..base.graph import Graph, Node
from ..base import game_functions as gf
from ..optimization import shortestPath
import copy


class Ui_Lines(object):
    def setupUi(self, Lines):

        self.level = 0
        self.graphs = []
        self.g = None

        #setup main Window
        Lines.setObjectName("Lines")
        Lines.resize(1087, 757)
        font = QtGui.QFont()
        font.setPointSize(10)
        Lines.setFont(font)

        #setup widgets
        self.centralwidget = QtWidgets.QWidget(Lines)
        self.centralwidget.setObjectName("centralwidget")
        
        self.graphView = QtWidgets.QWidget(self.centralwidget)
        self.graphView.setGeometry(QtCore.QRect(20, 90, 791, 536))
        self.graphView.setFont(font)
        self.graphView.setObjectName("graphView")

        #setup layout of graphView
        layout = QtWidgets.QVBoxLayout(self.graphView)
        self.figure = plt.figure()
        self.graphView.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.graphView.canvas)

        #setup buttons
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setGeometry(QtCore.QRect(830, 260, 93, 28))
        self.pushButton_start.setFont(font)
        self.pushButton_start.setObjectName("pushButton_start")
        self.pushButton_start.clicked.connect(self.start)

        self.pushButton_reset = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_reset.setGeometry(QtCore.QRect(960, 260, 93, 28))
        self.pushButton_reset.setFont(font)
        self.pushButton_reset.setObjectName("pushButton_reset")
        self.pushButton_reset.clicked.connect(self.reset)
        self.pushButton_reset.setEnabled(False)

        self.pushButton_nextLevel = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_nextLevel.setGeometry(QtCore.QRect(960, 590, 93, 28))
        self.pushButton_nextLevel.setFont(font)
        self.pushButton_nextLevel.setObjectName("pushButton_next")
        self.pushButton_nextLevel.clicked.connect(self.nextLevel)

        self.pushButton_preLevel = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_preLevel.setGeometry(QtCore.QRect(830, 590, 93, 28))
        self.pushButton_preLevel.setFont(font)
        self.pushButton_preLevel.setObjectName("pushButton_pre")
        self.pushButton_preLevel.clicked.connect(self.preLevel)
        self.pushButton_preLevel.setEnabled(False)

        self.pushButton_optimal = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_optimal.setGeometry(QtCore.QRect(830, 320, 110, 28))
        self.pushButton_optimal.setFont(font)
        self.pushButton_optimal.setObjectName("pushButton_optimal")
        self.pushButton_optimal.clicked.connect(self.setOptimalPoint)

        #setup labels
        self.label_lines = QtWidgets.QLabel(self.centralwidget)
        self.label_lines.setGeometry(QtCore.QRect(380, 20, 321, 31))
        self.label_lines.setAlignment(QtCore.Qt.AlignCenter)
        fontB = QtGui.QFont()
        fontB.setPointSize(20)
        fontB.setBold(True)
        fontB.setWeight(75)
        self.label_lines.setFont(fontB)
        self.label_lines.setScaledContents(False)
        self.label_lines.setObjectName("label_lines")

        self.label_start = QtWidgets.QLabel(self.centralwidget)
        self.label_start.setGeometry(QtCore.QRect(820, 110, 101, 31))
        fontS = QtGui.QFont()
        fontS.setPointSize(12)
        self.label_start.setFont(fontS)
        self.label_start.setObjectName("label_start")

        self.label_x = QtWidgets.QLabel(self.centralwidget)
        self.label_x.setGeometry(QtCore.QRect(830, 150, 21, 31))
        self.label_x.setFont(font)
        self.label_x.setObjectName("label_x")

        self.label_y = QtWidgets.QLabel(self.centralwidget)
        self.label_y.setGeometry(QtCore.QRect(830, 200, 21, 31))
        self.label_y.setFont(font)
        self.label_y.setObjectName("label_y")

        #setup edit fields
        self.lineEdit_x = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_x.setGeometry(QtCore.QRect(860, 150, 191, 31))
        self.lineEdit_x.setFont(font)
        self.lineEdit_x.setObjectName("lineEdit_x")
        self.lineEdit_x.setMaxLength(15)
        self.lineEdit_x.setEchoMode(0)
        self.onlyDouble = QtGui.QDoubleValidator()
        self.lineEdit_x.setValidator(self.onlyDouble)
        
        self.lineEdit_y = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_y.setGeometry(QtCore.QRect(860, 200, 191, 31))
        self.lineEdit_y.setFont(font)
        self.lineEdit_y.setObjectName("lineEdit_y")
        self.lineEdit_y.setMaxLength(15)
        self.lineEdit_y.setValidator(self.onlyDouble)
        
        #setup menubar and statusbar
        Lines.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Lines)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1087, 29))
        self.menubar.setObjectName("menubar")
        Lines.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Lines)
        self.statusbar.setObjectName("statusbar")
        Lines.setStatusBar(self.statusbar)

        # set up progress bar
        self.pbar = QtWidgets.QProgressBar(self.centralwidget)
        self.pbar.setGeometry(830, 530, 222, 28)
        self.pbar.setVisible(False)

        #create networkx graph
        self.createGraphs()
        self.drawGraph(0)

        #set up the mathplotlib animation
        self.animating = False
        self.animation = None
        self.step_length = 0.1

        self.retranslateUi(Lines)
        QtCore.QMetaObject.connectSlotsByName(Lines)

    def retranslateUi(self, Lines):
        _translate = QtCore.QCoreApplication.translate
        Lines.setWindowTitle(_translate("Lines", "Lines"))
        self.pushButton_start.setText(_translate("Lines", "Start"))
        self.label_lines.setText(_translate("Lines", "Lines - Level 0"))
        self.label_start.setText(_translate("Lines", "Startpunkt:"))
        self.label_x.setText(_translate("Lines", "x:"))
        self.label_y.setText(_translate("Lines", "y:"))
        self.pushButton_nextLevel.setText(_translate("Lines", "Next"))
        self.pushButton_preLevel.setText(_translate("Lines", "Previous"))
        self.pushButton_optimal.setText(_translate("Lines", "Optimal Point"))
        self.pushButton_reset.setText(_translate("Lines", "Reset"))

    def createGraphs(self):
        """
        create a list of graphs
        :param self:

        :return: None
        :raises: None
        """
        node0 = Node(coord = [0,0])
        node1 = Node(coord = [0,4])
        node2 = Node(coord = [4,4])
        node3 = Node(coord = [4,0])
        node4 = Node(coord=[5,1])
        edges1 = [(0,1),(0,3),(0,2),(1,2),(2,3)]
        g1 = Graph([node0,node1,node2,node3], edges1)
        g1.add_node(node4,[g1.nodes[0],g1.nodes[1]])
        self.graphs.append(g1)

        node5 = Node(coord = [2,2.1])
        edges2 = [(0,1),(0,3),(0,2),(2,3),]
        g2 = Graph([node5,node1,node2,node3], edges2)
        self.graphs.append(g2)
        
        node0 = Node(coord = [1,1])
        node1 = Node(coord = [2,8])
        node2 = Node(coord = [4,4])
        node3 = Node(coord = [8,8])
        node4 = Node(coord=[10,1])
        edges3 = [(0,1),(0,4),(1,2),(1,3),(2,3),(3,4)]
        g3 = Graph([node0,node1,node2,node3,node4], edges3)
        self.graphs.append(g3)
        
        node0 = Node(coord = [2,4])
        node1 = Node(coord = [2,7])
        node2 = Node(coord = [5,10])
        node3 = Node(coord = [9,8])
        node4 = Node(coord=[5,7])
        node5 = Node(coord = [5,4])
        node6 = Node(coord = [5,1])
        node7 = Node(coord = [7,6])
        node8 = Node(coord = [7,5])
        node9 = Node(coord=[10,6])
        node10 = Node(coord = [10,5])
        node11 = Node(coord=[9,3])
        
        edges4 = [(0,1),(0,5),(0,6),(1,2),(1,4),(2,3),(2,4),(3,7),(3,9),(4,5),(4,7),(5,6),(5,8),(6,11),(7,9),(8,10),(8,11),(10,11)]
        g4 = Graph([node0,node1,node2,node3,node4,node5,node6,node7,node8,node9,node10,node11], edges4)
        self.graphs.append(g4)
        
        node0 = Node(coord = [2,1])
        node1 = Node(coord = [2,5])
        node2 = Node(coord = [4,3])
        node3 = Node(coord = [2,9])
        node4 = Node(coord=[4,7])
        node5 = Node(coord = [7,3])
        node6 = Node(coord = [7,7])
        node7 = Node(coord = [9,9])
        node8 = Node(coord = [9,5])
        node9 = Node(coord=[9,1])
        node10 = Node(coord = [5,5])
        edges5 = [(0,1),(0,2),(1,2),(1,3),(1,4),(1,10),(2,5),(2,9),(3,4),(4,6),(4,7),(5,8),(5,9),(5,10),(6,7),(6,8),(6,10)]
        g5 = Graph([node0,node1,node2,node3,node4,node5,node6,node7,node8,node9,node10], edges5)
        self.graphs.append(g5)
        
        node0 = Node(coord = [2,1])
        node1 = Node(coord = [1,3])
        node2 = Node(coord = [1.5,5])
        node3 = Node(coord = [3,5])
        node4 = Node(coord=[3,7])
        node5 = Node(coord = [3,10])
        node6 = Node(coord = [6,7])
        node7 = Node(coord = [5,3])
        node8 = Node(coord = [8,3])
        node9 = Node(coord=[8,5])
        node10 = Node(coord = [10,4])
        edges6 = [(0,1),(0,3),(0,7),(1,2),(1,3),(2,4),(2,5),(3,4),(3,6),(3,7),(4,5),(4,6),(5,6),(6,7),(6,9),(7,8),(7,9),(8,9),(8,10),(9,10)]
        g6 = Graph([node0,node1,node2,node3,node4,node5,node6,node7,node8,node9,node10], edges6)
        self.graphs.append(g6)
        
        
    
    def drawGraph(self, level):
        """
        draw a new graph with axes on the canvas based on the selected level
        :param self:
        :param level: position of graph in graphs[]

        :return: None
        :raises: None
        """
        if level < len(self.graphs) and level >= 0:
            self.level = level
            self.figure.clear()
            self.g = copy.deepcopy(self.graphs[level])
            g = self.g.toNx()

            pos = nx.get_node_attributes(g, 'pos')
            ax = self.figure.add_subplot()

            #draw label
            labels = nx.get_node_attributes(g, 'label')
            pos_label = {}
            y_off = 0.2
            for k, v in pos.items():
                pos_label[k] = (v[0], v[1]+y_off)
            nx.draw_networkx_labels(g, pos_label, labels)

            #draw graph
            nx.draw_networkx(g, pos, ax=ax, with_labels=False, node_size=100, node_color='black', edge_color=[0.6784,0.6784,0.6784], width=3.0)
            ax.set_axis_on()
            ax.tick_params(left=True,
                           bottom=True,
                           labelleft=True,
                           labelbottom=True)
            self.graphView.canvas.draw()
            self.label_lines.setText(f"Lines - Level {level}")
            self.pushButton_reset.setEnabled(False)
            self.pushButton_start.setEnabled(True)

    def nextLevel(self):
        """
        switch to the next level
        :param self:

        :return: None
        :raises: None
        """
        self.drawGraph(self.level+1)

        self.pushButton_preLevel.setEnabled(True)
        if self.level+1 >= len(self.graphs):
            self.pushButton_nextLevel.setEnabled(False)
        

    def preLevel(self):
        """
        switch to the previous level
        :param self:

        :return: None
        :raises: None
        """
        self.drawGraph(self.level-1)

        self.pushButton_nextLevel.setEnabled(True)
        if self.level-1 < 0:
            self.pushButton_preLevel.setEnabled(False)
        

    def reset(self):
        """
        set graph back to original state
        :param self:

        :return: None
        :raises: None
        """
        self.drawGraph(self.level)


    def setOptimalPoint(self):
        """
        calculate best starting point for current graph and show point on line edits
        :param self:

        :retun: None
        :raises: None
        """
        n = shortestPath.best_start_point(self.g)
        x = round(n.coord[0], 5)
        y = round(n.coord[1], 5)
        self.lineEdit_x.clear()
        self.lineEdit_x.insert(str(x))
        self.lineEdit_y.clear()
        self.lineEdit_y.insert(str(y))


    def start(self):
        """
        add start node and start animation
        :param self:

        :return: None
        :raises: None
        """
        x = self.lineEdit_x.text().replace(",", ".")
        y = self.lineEdit_y.text().replace(",", ".")
        if x and y:
            x = float(x)
            y = float(y)
            try:
                self.animating = True
                self.g = gf.set_start_point(x, y, self.g) 
                self.figure.clear()
                newNxGraph = self.g.toNx()
                pos = nx.get_node_attributes(newNxGraph, 'pos')
                ax = self.figure.add_subplot()

                #draw label
                labels = nx.get_node_attributes(newNxGraph, 'label')
                pos_label = {}
                y_off = 0.2
                for k, v in pos.items():
                    pos_label[k] = (v[0], v[1]+y_off)
                nx.draw_networkx_labels(newNxGraph, pos_label, labels)

                nx.draw_networkx(newNxGraph, pos, ax=ax, with_labels=False, node_size=100, node_color='black', edge_color=[0.6784,0.6784,0.6784], width=3.0)
                ax.set_axis_on()
                ax.tick_params(left=True,
                                bottom=True,
                                labelleft=True,
                                labelbottom=True)
                self.graphView.canvas.draw_idle()

                # update buttons
                self.pushButton_start.setEnabled(False)
                self.pushButton_nextLevel.setEnabled(False)
                self.pushButton_preLevel.setEnabled(False)
                self.pbar.setVisible(True)
                self.run_animation()
                

            except ValueError as err:
                msg = QtWidgets.QMessageBox.critical(self.centralwidget,
                                                     "Error",
                                                     err.args[0])
        else:
            msg = QtWidgets.QMessageBox.critical(self.centralwidget,
                                                "Error",
                                                 "Please enter a start point!")


    def run_animation(self):
        """
        run animation with fixed amount of frames
        :param self:

        :return: None
        :raises: None
        """
        self.start_index = self.g.nodes.index(self.g.start_nodes[-1])
        self.ag, self.runner_info = gf.initial_step(self.g, self.start_index)
        floyd_matrix = shortestPath.floydwarshall(self.g)
        worst_index = np.where(floyd_matrix[self.start_index] 
                               == np.max(floyd_matrix[self.start_index]))
        framecount = int((floyd_matrix[self.start_index][worst_index]\
                    + 0.7*np.max(self.g.adjacency_matrix[worst_index]))\
                        /self.step_length)+1

        

        #init progress bar
        self.pbar.setMinimum(0)
        self.pbar.setMaximum(framecount-1)
            
        def update(frame):
            """
            generate a frame for the animation
            :param self:

            :return: None
            :raises: None
            """
            self.pbar.setValue(frame)
            # Add a new node to the graph
            self.ag , self.runner_info = gf.next_step(self.g, self.ag, self.runner_info, self.step_length)
            # Clear the current plot
            self.figure.clear()

            ax = self.figure.add_subplot()
            
            # Draw the old graph
            newNxGraph = self.g.toNx()
            pos = nx.get_node_attributes(newNxGraph, 'pos')
            #draw label
            labels = nx.get_node_attributes(newNxGraph, 'label')
            pos_label = {}
            y_off = 0.2
            for k, v in pos.items():
                pos_label[k] = (v[0], v[1]+y_off)
            nx.draw_networkx_labels(newNxGraph, pos_label, labels)

            nx.draw_networkx(newNxGraph, pos, ax=ax,labels=labels, with_labels=False, node_size=100, node_color='black', edge_color=[0.6784,0.6784,0.6784], width=3.0)

            # Draw the updated graph
            g = self.ag.toNx()
            pos = nx.get_node_attributes(g, 'pos')
            labels = nx.get_node_attributes(g, 'label')
            nx.draw_networkx(g, pos, ax=ax, with_labels = False, edge_color = 'red', nodelist = [], width=3.0)
            ax.set_axis_on()
            ax.tick_params(left=True,
                        bottom=True,
                        labelleft=True,
                        labelbottom=True)


            #activate button after animation
            if frame == framecount-1:
                self.pushButton_reset.setEnabled(True)
                if self.level < len(self.graphs)-1:
                    self.pushButton_nextLevel.setEnabled(True)
                if self.level > 0:
                    self.pushButton_preLevel.setEnabled(True)

                self.pbar.setValue(0)
                self.pbar.setVisible(False)
            
        self.animation = animation.FuncAnimation(self.figure, update, frames=framecount, interval=0, repeat=False)


if __name__ == '__main__':

    sys.path.append('..')

    app = QApplication(sys.argv)
    Lines = QMainWindow()
    mainWindow = Ui_Lines()
    mainWindow.setupUi(Lines)
    Lines.setMinimumSize(Lines.size())   
    Lines.show()
    sys.exit(app.exec_())