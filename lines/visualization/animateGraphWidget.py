from PyQt5 import QtCore, QtGui, QtWidgets
from ..base.graph import Graph, Node
import numpy as np

class AnimateGraph(QtWidgets.QWidget):
    pointChanged = QtCore.pyqtSignal(QtCore.QPoint)
    groupChanged = QtCore.pyqtSignal(QtCore.QSequentialAnimationGroup)

    def __init__(self,g, start_index, parent= None):
        super().__init__(parent)
        factor = 100
        start_node_coord = g.nodes[start_index].coord
        self._point = QtCore.QPoint(start_node_coord[0]*factor, start_node_coord[1]*factor)
        self._untouched_nodes = list(range(len(g.nodes)))
        self._untouched_nodes.remove(start_index)

        self._anim_next_nodes = np.array(g.nodes)[g.adjacency_matrix[start_index].nonzero()]
        self._animation = QtCore.QPropertyAnimation(
            self,
            duration=1000,
            propertyName=b"point",
            targetObject=self,
            startValue=self._point,
            endValue=self._point,
            finished=self.calculate_next_step,
        )

        points = (QtCore.QPoint(n.coord[0]*factor, n.coord[1]*factor) for n in self._anim_next_nodes)
        lines = (QtCore.QLine(self._point,p) for p in points)
        """,
            QtCore.QPoint(210, 500),
            QtCore.QPoint(500, 210),
            QtCore.QPoint(500, 200),
            QtCore.QPoint(150, 0),
            QtCore.QPoint(150, 100),
            QtCore.QPoint(50, 300),
            QtCore.QPoint(0, 500),
            QtCore.QPoint(110, 350),
            """
        self._points_iter = iter(points)
        self.calculate_next_step()

    def _update_end_point(self, p):
        s = self._animation.endValue()
        self._animation.setStartValue(s)
        self._animation.setEndValue(p)
        self._animation.start()

    def calculate_next_step(self):
        try:
            p = next(self._points_iter)
        except StopIteration:
            print("finished")
        else:
            self._update_end_point(p)

    @QtCore.pyqtProperty(QtCore.QPoint, notify=pointChanged)
    def point(self):
        return self._point

    @point.setter
    def point(self, p):
        self._point = p
        self.pointChanged.emit(p)
        self.update()

    def paintEvent(self, event):
        radius = 10

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        rect = QtCore.QRect(0, 0, 2 * radius, 2 * radius)
        rect.moveCenter(self.point)

        painter.setBrush(QtGui.QBrush(QtGui.QColor("salmon")))
        painter.drawEllipse(rect)


def main():
    import sys

    g = Graph([Node([0,0]),Node([1,1]), Node([2,0])],[(0,1),(0,2),(1,2)])

    app = QtWidgets.QApplication(sys.argv)

    print(np.array(g.nodes)[g.adjacency_matrix[0].nonzero()[0]])

    w = AnimateGraph(g,1)
    w.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()