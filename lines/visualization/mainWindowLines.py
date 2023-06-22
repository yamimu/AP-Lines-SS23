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
import networkx as nx 
from ..base.graph import Graph, Node
from ..base import game_functions as gf


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
        font = QtGui.QFont()
        font.setPointSize(10)
        self.graphView.setFont(font)
        self.graphView.setObjectName("graphView")

        #setup layout of graphView
        layout = QtWidgets.QVBoxLayout(self.graphView)
        self.figure = plt.figure()
        self.graphView.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.graphView.canvas)

        #setup buttons
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setGeometry(QtCore.QRect(900, 260, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_start.setFont(font)
        self.pushButton_start.setObjectName("pushButton_start")
        self.pushButton_start.clicked.connect(self.start)

        self.pushButton_nextLevel = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_nextLevel.setGeometry(QtCore.QRect(960, 590, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_nextLevel.setFont(font)
        self.pushButton_nextLevel.setObjectName("pushButton")
        self.pushButton_nextLevel.clicked.connect(self.nextLevel)

        self.pushButton_preLevel = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_preLevel.setGeometry(QtCore.QRect(830, 590, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_preLevel.setFont(font)
        self.pushButton_preLevel.setObjectName("pushButton")
        self.pushButton_preLevel.clicked.connect(self.preLevel)
        self.pushButton_preLevel.setEnabled(False)

        #setup labels
        self.label_lines = QtWidgets.QLabel(self.centralwidget)
        self.label_lines.setGeometry(QtCore.QRect(380, 20, 321, 31))
        self.label_lines.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_lines.setFont(font)
        self.label_lines.setScaledContents(False)
        self.label_lines.setObjectName("label_lines")

        self.label_start = QtWidgets.QLabel(self.centralwidget)
        self.label_start.setGeometry(QtCore.QRect(820, 110, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_start.setFont(font)
        self.label_start.setObjectName("label_start")

        self.label_x = QtWidgets.QLabel(self.centralwidget)
        self.label_x.setGeometry(QtCore.QRect(830, 150, 21, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_x.setFont(font)
        self.label_x.setObjectName("label_x")

        self.label_y = QtWidgets.QLabel(self.centralwidget)
        self.label_y.setGeometry(QtCore.QRect(830, 200, 21, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_y.setFont(font)
        self.label_y.setObjectName("label_y")

        self.label_winner = QtWidgets.QLabel(self.centralwidget)
        self.label_winner.setGeometry(QtCore.QRect(830, 320, 71, 21))
        self.label_winner.setObjectName("label_winner")

        self.label_winningPlayer = QtWidgets.QLabel(self.centralwidget)
        self.label_winningPlayer.setGeometry(QtCore.QRect(900, 370, 101, 21))
        self.label_winningPlayer.setText("")
        self.label_winningPlayer.setObjectName("label_winningPlayer")

        #setup edit fields
        self.lineEdit_x = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_x.setGeometry(QtCore.QRect(860, 150, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_x.setFont(font)
        self.lineEdit_x.setObjectName("lineEdit_x")
        self.lineEdit_x.setMaxLength(15)
        self.lineEdit_x.setEchoMode(0)
        self.onlyDouble = QtGui.QDoubleValidator()
        self.lineEdit_x.setValidator(self.onlyDouble)
        
        self.lineEdit_y = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_y.setGeometry(QtCore.QRect(860, 200, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
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

        #create networkx graph
        self.createGraphs()
        self.drawGraph(0)

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
        self.pushButton_nextLevel.setText(_translate("Lines", "Next Level"))
        self.pushButton_preLevel.setText(_translate("Lines", "Previous Level"))

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
        node4 = Node(coord=[5,0])
        edges1 = [(0,1),(0,3),(0,2),(1,2),(2,3)]
        g1 = Graph([node0,node1,node2,node3], edges1)
        g1.add_node(node4,[g1.nodes[0],g1.nodes[1]])
        self.graphs.append(g1)

        node5 = Node(coord = [2,2.1])
        edges2 = [(0,1),(0,3),(0,2),(2,3),]
        g2 = Graph([node5,node1,node2,node3], edges2)
        self.graphs.append(g2)
    
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
            self.g = self.graphs[level]
            g = self.g.toNx()

            pos = nx.get_node_attributes(g, 'pos')
            ax = self.figure.add_subplot()
            labels = nx.get_node_attributes(g, 'label')
            
            nx.draw_networkx(g, pos, ax=ax, labels=labels)
            ax.set_axis_on()
            ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
            self.graphView.canvas.draw_idle()
            self.label_lines.setText(f"Lines - Level {level}")


    def nextLevel(self):
        self.drawGraph(self.level+1)

        self.pushButton_preLevel.setEnabled(True)
        if self.level+1 >= len(self.graphs):
            self.pushButton_nextLevel.setEnabled(False)

    def preLevel(self):
        self.drawGraph(self.level-1)

        self.pushButton_nextLevel.setEnabled(True)
        if self.level-1 < 0:
            self.pushButton_preLevel.setEnabled(False)

    def back(self):
        self.drawGraph(self.level)

        self.pushButton_preLevel.setText("Previous level")
        self.pushButton_preLevel.clicked.connect(self.preLevel)
        if self.level < 0:
            self.pushButton_preLevel.setEnabled(False)

    def start(self):
        """
        add start node and start animation
        :param self:

        :return: None
        :raises: None
        """
        x = self.lineEdit_x.text()
        y = self.lineEdit_y.text()
        if x and y:
            x = float(self.lineEdit_x.text())
            y = float(self.lineEdit_y.text())
            try:
                newGraph = gf.set_start_point(x, y, self.g)
                if(newGraph != self.g):
                    #draw new graph with startpoint as node
                    self.figure.clear()
                    newNxGraph = newGraph.toNx()
                    pos = nx.get_node_attributes(newNxGraph, 'pos')
                    ax = self.figure.add_subplot()
                    labels = nx.get_node_attributes(newNxGraph, 'label')
                    nx.draw_networkx(newNxGraph, pos, ax=ax, labels=labels)
                    ax.set_axis_on()
                    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
                    self.graphView.canvas.draw_idle()

                    """ #setze button back
                    self.pushButton_preLevel.setText("back")
                    self.pushButton_preLevel.setEnabled(True)
                    self.pushButton_preLevel.clicked.connect(self.back) """
            except ValueError as err:
                msg = QtWidgets.QMessageBox.critical(self.centralwidget, "Error", err.args[0])
        else:
                    msg = QtWidgets.QMessageBox.critical(self.centralwidget, "Error", "Please enter a start point!")
        #
        '''
        TODO:
            - start animation
        '''
        def setOptimalPoint(self):
            #TODO: Punkt aus shortestPath.py def best_start_point()
            i = 1


if __name__ == '__main__':

    sys.path.append('..')

    app = QApplication(sys.argv)
    Lines = QMainWindow()
    mainWindow = Ui_Lines()
    mainWindow.setupUi(Lines)   
    Lines.show()
    sys.exit(app.exec_())