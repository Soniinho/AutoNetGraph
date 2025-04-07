from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QPushButton, QHBoxLayout, QVBoxLayout

from model.translations_md import TRANSLATIONS
from controller import NetworkItemController, NetworkOperationsController, FileOperationsController, VirtualBoxManualController


class Ui_VisualInterface(object):
    def __init__(self, selected_vm, language="en"):
        self.selected_vm = selected_vm
        self.language = language
        self.translations = TRANSLATIONS
        self.controller1 = None

    def setupUi(self, DiagramWindow):
        texts = self.translations[self.language]
        DiagramWindow.setObjectName("DiagramWindow")
        DiagramWindow.resize(900, 650)

        self.centralwidget = QtWidgets.QWidget(DiagramWindow)
        self.layout = QVBoxLayout(self.centralwidget)

        # Horizontal layout for buttons
        button_layout = QHBoxLayout()

        # Create buttons
        self.button_save = QPushButton(texts["save_button"], self.centralwidget)
        self.button_load = QPushButton(texts["load_button"], self.centralwidget)
        self.button_computer = QPushButton(texts["computer_button"], self.centralwidget)
        self.button_gateway = QPushButton(texts["gateway_button"], self.centralwidget)
        self.button_connect = QPushButton(texts["connect_button"], self.centralwidget)
        self.button_setup_network = QPushButton(texts["setup_network"], self.centralwidget)
        self.button_clone_machines = QPushButton(texts["clone_button"], self.centralwidget)

        # Set button sizes
        for button in (self.button_save, self.button_load, self.button_computer, self.button_gateway, self.button_connect):
            button.setFixedSize(80, 30)
        
        self.button_setup_network.setFixedSize(120, 30)
        self.button_clone_machines.setFixedSize(120, 30)

        # Add buttons to layout
        for button in (self.button_save, self.button_load, self.button_computer, self.button_gateway, self.button_connect,
                      self.button_setup_network, self.button_clone_machines):
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
        self.controller1 = NetworkItemController(self.scene, self.language)
        self.controller2 = FileOperationsController(self.scene, self.language)
        self.controller3 = NetworkOperationsController(self.scene, self.language)
        self.controller4 = VirtualBoxManualController(self.scene, self.selected_vm)
        self.scene.setSceneRect(0, 0, 700, 500)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setRenderHint(self.graphicsView.renderHints().Antialiasing)
        self.graphicsView.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

        # Connect button signals
        self.button_computer.clicked.connect(self.controller1.add_computer)
        self.button_gateway.clicked.connect(self.controller1.add_gateway)
        self.button_connect.clicked.connect(self.controller1.add_connection)
        self.button_clone_machines.clicked.connect(self.controller4.cloneConfigureMachines)
        self.button_setup_network.clicked.connect(self.controller3.setup_network)
        self.button_save.clicked.connect(self.controller2.save_diagram)
        self.button_load.clicked.connect(self.controller2.load_diagram)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DrawWindow = QtWidgets.QMainWindow()
    ui = Ui_VisualInterface(selected_vm="VM1")
    ui.setupUi(DrawWindow)
    DrawWindow.show()
    sys.exit(app.exec())
