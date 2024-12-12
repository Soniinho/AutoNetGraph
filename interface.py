from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QBrush, QFont
from PyQt6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsLineItem, QGraphicsTextItem, QMenu, QDialog, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox

from nodes import NetworkShape, MovableEllipse, MovableRect, ConnectionLine
from virtualboxFunc import cloneConfigureMachines

class Ui_DrawInterface(object):
    def __init__(self, selected_vm):
        self.selected_vm = selected_vm

    def setupUi(self, DiagramWindow):
        DiagramWindow.setObjectName("DiagramWindow")
        DiagramWindow.resize(900, 650)
        
        # Central widget
        self.centralwidget = QtWidgets.QWidget(DiagramWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Main layout
        self.layout = QVBoxLayout(self.centralwidget)
        
        # Horizontal layout for buttons (top layout)
        button_layout = QHBoxLayout()
        
        # Buttons
        self.button_computer = QPushButton("Computador", self.centralwidget)
        self.button_gateway = QPushButton("Gateway", self.centralwidget)
        self.button_connect = QPushButton("Conectar", self.centralwidget)
        
        for button in (self.button_computer, self.button_gateway, self.button_connect):
            button.setFixedSize(80, 30)
            button_layout.addWidget(button)
        
        self.layout.addLayout(button_layout)

        # Botão "Clonar Máquinas" no layout
        self.button_clone_machines = QPushButton("Clonar Máquinas", self.centralwidget)
        self.button_clone_machines.setFixedSize(120, 30)
        button_layout.addWidget(self.button_clone_machines)

        # Conectando o botão de Clonar a uma função
        self.button_clone_machines.clicked.connect(lambda: cloneConfigureMachines(self.selected_vm, self.scene))
        
        # Graphics View
        #self.graphicsView = ZoomableGraphicsView()
        self.graphicsView = QGraphicsView()
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setStyleSheet("background-color: #F0F0F0; border: 1px solid #A9A9A9;")
        self.layout.addWidget(self.graphicsView)
        
        # Conectar botões às funções
        self.button_computer.clicked.connect(self.add_computer)
        self.button_gateway.clicked.connect(self.add_gateway)
        self.button_connect.clicked.connect(self.add_connect)

        DiagramWindow.setCentralWidget(self.centralwidget)
        DiagramWindow.setWindowTitle("Editor de Diagramas")

        # Scene setup
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 700, 500)
        self.graphicsView.setScene(self.scene)

        # Graphics view settings
        self.graphicsView.setRenderHint(self.graphicsView.renderHints().Antialiasing)
        self.graphicsView.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)


    def add_computer(self):
        computer = MovableEllipse(0, 0, 50, 50)
        computer.setBrush(QBrush(Qt.GlobalColor.cyan))
        computer.setFlags(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsMovable | QGraphicsEllipseItem.GraphicsItemFlag.ItemIsSelectable)
        self.scene.addItem(computer)

    def add_gateway(self):
        gateway = MovableRect(0, 0, 70, 50)
        gateway.setBrush(QBrush(Qt.GlobalColor.lightGray))
        gateway.setFlags(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable | QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable)
        self.scene.addItem(gateway)

    def add_connect(self):
        selected_items = self.scene.selectedItems()
        if len(selected_items) == 2:
            item1, item2 = selected_items
            connect = ConnectionLine(item1, item2)
            self.scene.addItem(connect)


""" if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DrawWindow = QtWidgets.QMainWindow()
    ui = Ui_DrawInterface("VM1")
    ui.setupUi(DrawWindow)
    DrawWindow.show()
    sys.exit(app.exec())
 """