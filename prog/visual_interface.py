from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QPushButton, QHBoxLayout, QVBoxLayout, QWidget

from prog.translations import TRANSLATIONS
from prog.virtualboxFunc import cloneConfigureMachines
from prog.diagram_operations import add_computer, add_gateway, add_connect
from prog.network_operations import setup_network
from prog.file_operations import save_diagram, load_diagram


class Ui_DrawInterface(object):
    def __init__(self, selected_vm, language="en"):
        self.selected_vm = selected_vm
        self.language = language
        self.translations = TRANSLATIONS

    def setupUi(self, DiagramWindow):
        texts = self.translations[self.language]
        DiagramWindow.setObjectName("DiagramWindow")
        DiagramWindow.resize(900, 650)

        self.centralwidget = QtWidgets.QWidget(DiagramWindow)
        self.layout = QVBoxLayout(self.centralwidget)

        # Horizontal layout for buttons
        button_layout = QHBoxLayout()

        # Create buttons
        self.button_computer = QPushButton(texts["computer_button"], self.centralwidget)
        self.button_gateway = QPushButton(texts["gateway_button"], self.centralwidget)
        self.button_connect = QPushButton(texts["connect_button"], self.centralwidget)
        self.button_clone_machines = QPushButton(texts["clone_button"], self.centralwidget)
        self.button_setup_network = QPushButton("Setup Network", self.centralwidget)
        self.button_save = QPushButton(texts["save_button"], self.centralwidget)
        self.button_load = QPushButton(texts["load_button"], self.centralwidget)

        # Set button sizes
        for button in (self.button_computer, self.button_gateway, self.button_connect,
                      self.button_save, self.button_load):
            button.setFixedSize(80, 30)
        
        self.button_clone_machines.setFixedSize(120, 30)
        self.button_setup_network.setFixedSize(120, 30)

        # Add buttons to layout
        for button in (self.button_computer, self.button_gateway, self.button_connect,
                      self.button_clone_machines, self.button_setup_network,
                      self.button_save, self.button_load):
            button_layout.addWidget(button)

        self.layout.addLayout(button_layout)

        # Graphics View
        #self.graphicsView = ZoomableGraphicsView()
        self.graphicsView = QGraphicsView()
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setStyleSheet("background-color: #F0F0F0; border: 1px solid #A9A9A9;")
        self.layout.addWidget(self.graphicsView)
        
        DiagramWindow.setCentralWidget(self.centralwidget)
        DiagramWindow.setWindowTitle(texts["title"])

        # Setup Scene
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 700, 500)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setRenderHint(self.graphicsView.renderHints().Antialiasing)
        self.graphicsView.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

        # Connect button signals
        self.button_computer.clicked.connect(lambda: add_computer(self.scene, self.language))
        self.button_gateway.clicked.connect(lambda: add_gateway(self.scene, self.language))
        self.button_connect.clicked.connect(lambda: add_connect(self.scene, self.language))
        self.button_clone_machines.clicked.connect(lambda: cloneConfigureMachines(self.selected_vm, self.scene))
        self.button_setup_network.clicked.connect(lambda: setup_network(self.scene, self.language))
        self.button_save.clicked.connect(lambda: save_diagram(self.scene))
        self.button_load.clicked.connect(lambda: load_diagram(self.scene, self.language))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DrawWindow = QtWidgets.QMainWindow()
    ui = Ui_DrawInterface(selected_vm="VM1")
    ui.setupUi(DrawWindow)
    DrawWindow.show()
    sys.exit(app.exec())
