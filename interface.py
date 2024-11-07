from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QBrush, QFont
from PyQt6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsLineItem, QGraphicsTextItem, QMenu, QDialog, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox

from nodes import NetworkShape ,MovableEllipse, MovableRect, ConnectionLine

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
        self.button_circle = QPushButton("Círculo", self.centralwidget)
        self.button_rectangle = QPushButton("Retângulo", self.centralwidget)
        self.button_line = QPushButton("Linha", self.centralwidget)
        
        for button in (self.button_circle, self.button_rectangle, self.button_line):
            button.setFixedSize(80, 30)
            button_layout.addWidget(button)
        
        self.layout.addLayout(button_layout)

        # Botão "Clonar Máquinas" no layout
        self.button_clone_machines = QPushButton("Clonar Máquinas", self.centralwidget)
        self.button_clone_machines.setFixedSize(120, 30)
        button_layout.addWidget(self.button_clone_machines)

        # Conectando o botão a uma função
        self.button_clone_machines.clicked.connect(self.clone_machines)
        
        # Graphics View
        #self.graphicsView = ZoomableGraphicsView()
        self.graphicsView = QGraphicsView()
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setStyleSheet("background-color: #F0F0F0; border: 1px solid #A9A9A9;")
        self.layout.addWidget(self.graphicsView)
        
        # Conectar botões às funções
        self.button_circle.clicked.connect(self.add_circle)
        self.button_rectangle.clicked.connect(self.add_rectangle)
        self.button_line.clicked.connect(self.add_line)

        DiagramWindow.setCentralWidget(self.centralwidget)
        DiagramWindow.setWindowTitle("Editor de Diagramas")

        # Scene setup
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 700, 500)
        self.graphicsView.setScene(self.scene)

        # Graphics view settings
        self.graphicsView.setRenderHint(self.graphicsView.renderHints().Antialiasing)
        self.graphicsView.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)


    def add_circle(self):
        circle = MovableEllipse(0, 0, 50, 50, "192.168.1.10", "enp0s3", "255.255.255.0", "192.168.1.0", "192.168.1.255", ip_forward=0)
        circle.setBrush(QBrush(Qt.GlobalColor.cyan))
        circle.setFlags(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsMovable | QGraphicsEllipseItem.GraphicsItemFlag.ItemIsSelectable)
        self.scene.addItem(circle)

    def add_rectangle(self):
        rectangle = MovableRect(0, 0, 70, 50, "192.168.1.20", "enp0s3", "255.255.255.0", "192.168.1.0", "192.168.1.255", ip_forward=1)
        rectangle.setBrush(QBrush(Qt.GlobalColor.lightGray))
        rectangle.setFlags(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable | QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable)
        self.scene.addItem(rectangle)

    def add_line(self):
        selected_items = self.scene.selectedItems()
        if len(selected_items) == 2:
            item1, item2 = selected_items
            line = ConnectionLine(item1, item2)
            self.scene.addItem(line)

    def clone_machines(self):
        # Itera sobre todos os itens da cena
        for item in self.scene.items():
            if isinstance(item, NetworkShape):  # Verifica se o item é uma forma com parâmetros de rede
                # Cria o nome do arquivo com base no IP da forma
                file_name = f"{item.ip}_properties.txt"
                
                # Abre o arquivo em modo de escrita
                with open(file_name, "w") as file:
                    # Escreve os parâmetros da forma no arquivo
                    file.write(f"IP: {item.ip}\n")
                    file.write(f"Interface: {item.interface}\n")
                    file.write(f"Netmask: {item.netmask}\n")
                    file.write(f"Network: {item.network}\n")
                    file.write(f"Broadcast: {item.broadcast}\n")
                    file.write(f"IP Forward: {item.ip_forward}\n")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DrawWindow = QtWidgets.QMainWindow()
    ui = Ui_DrawInterface()
    ui.setupUi(DrawWindow)
    DrawWindow.show()
    sys.exit(app.exec())
