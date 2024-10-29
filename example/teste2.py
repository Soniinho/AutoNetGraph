from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QBrush
from PyQt6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QPushButton, QVBoxLayout, QWidget, QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsLineItem

class Ui_DiagramWindow(object):
    def setupUi(self, DiagramWindow):
        DiagramWindow.setObjectName("DiagramWindow")
        DiagramWindow.resize(800, 600)
        
        # Central widget
        self.centralwidget = QtWidgets.QWidget(parent=DiagramWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Layout
        self.layout = QVBoxLayout(self.centralwidget)
        self.layout.setObjectName("layout")
        
        # Graphics View
        self.graphicsView = ZoomableGraphicsView()
        self.graphicsView.setObjectName("graphicsView")
        self.layout.addWidget(self.graphicsView)
        
        # Buttons
        self.button_circle = QPushButton("Adicionar Círculo", self.centralwidget)
        self.button_rectangle = QPushButton("Adicionar Retângulo", self.centralwidget)
        self.button_line = QPushButton("Conectar Formas", self.centralwidget)
        
        self.layout.addWidget(self.button_circle)
        self.layout.addWidget(self.button_rectangle)
        self.layout.addWidget(self.button_line)

        # Connect buttons to functions
        self.button_circle.clicked.connect(self.add_circle)
        self.button_rectangle.clicked.connect(self.add_rectangle)
        self.button_line.clicked.connect(self.add_line)

        # Set central widget
        DiagramWindow.setCentralWidget(self.centralwidget)
        DiagramWindow.setWindowTitle("Editor de Diagramas")

        # Scene setup
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 600, 400)
        self.graphicsView.setScene(self.scene)
        
        # Graphics view settings
        self.graphicsView.setRenderHint(self.graphicsView.renderHints().Antialiasing)
        self.graphicsView.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

    def add_circle(self):
        # Adiciona um círculo à cena
        circle = MovableEllipse(0, 0, 50, 50)
        circle.setBrush(QBrush(Qt.GlobalColor.blue))
        circle.setFlags(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsMovable | QGraphicsEllipseItem.GraphicsItemFlag.ItemIsSelectable)
        self.scene.addItem(circle)

    def add_rectangle(self):
        # Adiciona um retângulo à cena
        rectangle = MovableRect(0, 0, 70, 50)
        rectangle.setBrush(QBrush(Qt.GlobalColor.green))
        rectangle.setFlags(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable | QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable)
        self.scene.addItem(rectangle)

    def add_line(self):
        # Conecta duas formas selecionadas com uma linha
        selected_items = self.scene.selectedItems()
        if len(selected_items) == 2:
            item1, item2 = selected_items
            line = ConnectionLine(item1, item2)
            self.scene.addItem(line)


class MovableEllipse(QGraphicsEllipseItem):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.connections = []
        self.setZValue(1)  # Formas à frente

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.update_connections()

    def update_connections(self):
        for line in self.connections:
            line.update_position()


class MovableRect(QGraphicsRectItem):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.connections = []
        self.setZValue(1)  # Formas à frente

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.update_connections()

    def update_connections(self):
        for line in self.connections:
            line.update_position()


class ConnectionLine(QGraphicsLineItem):
    def __init__(self, start_item, end_item):
        super().__init__()
        self.start_item = start_item
        self.end_item = end_item
        self.setPen(QPen(Qt.GlobalColor.black, 2))
        self.start_item.connections.append(self)
        self.end_item.connections.append(self)
        self.setZValue(0)  # Linhas atrás
        self.update_position()

    def update_position(self):
        start_point = self.start_item.sceneBoundingRect().center()
        end_point = self.end_item.sceneBoundingRect().center()
        self.setLine(start_point.x(), start_point.y(), end_point.x(), end_point.y())


class ZoomableGraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.zoom_factor = 1.2  # Define o fator de zoom

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            zoom = self.zoom_factor
        else:
            zoom = 1 / self.zoom_factor
        self.scale(zoom, zoom)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DiagramWindow = QtWidgets.QMainWindow()
    ui = Ui_DiagramWindow()
    ui.setupUi(DiagramWindow)
    DiagramWindow.show()
    sys.exit(app.exec())
