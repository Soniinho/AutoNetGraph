from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QBrush, QFont
from PyQt6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsLineItem, QGraphicsTextItem, QMenu, QDialog, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox

from nodes import NetworkShape, MovableEllipse, MovableRect, ConnectionLine

import sys
import os
# Caminho relativo para a pasta do VirtualBox SDK
sdk_path = os.path.join(os.path.dirname(__file__), 'sdk/bindings/xpcom/python')
sys.path.append(sdk_path)
import vboxapi

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

        # Conectando o botão a uma função
        self.button_clone_machines.clicked.connect(self.generate_files)
        
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

    def generate_files(self):
        # Itera sobre todos os itens da cena
        for item in self.scene.items():
            if isinstance(item, NetworkShape):  # Verifica se o item é uma forma com parâmetros de rede
                # Nome do arquivo baseado no IP da interface enp0s3 ou enp0s8, se disponível
                # file_name = f"{item.interfaces[0].get('ip', 'sem_ip')}_network_config.txt"
                file_name = "interfaces"
               
                # Abre o arquivo em modo de escrita
                with open(file_name, "w") as file:
                    # Escreve o cabeçalho do arquivo de configuração
                    file.write("source /etc/network/interfaces.d/*\n\n")
                    
                    # Configuração da interface de loopback
                    file.write("auto lo\n")
                    file.write("iface lo inet loopback\n\n")
                    
                    # Itera sobre cada interface
                    for iface in item.interfaces:
                        # Especifica a interface como `auto` para habilitação
                        file.write(f"auto {iface['name']}\n")
                        
                        # Configura a interface com `dhcp` ou `static`
                        if iface.get("automatic", True):  # Se for automático, utiliza DHCP
                            file.write(f"iface {iface['name']} inet dhcp\n\n")
                        else:  # Se for manual, configura como estático
                            file.write(f"iface {iface['name']} inet static\n")
                            
                            # Adiciona os campos conforme a interface
                            if iface['name'] == "enp0s8":  # enp0s8 com campos padrão e gateway opcional
                                file.write(f"    address {iface.get('ip', '')}\n")
                                file.write(f"    netmask {iface.get('netmask', '')}\n")
                                file.write(f"    network {iface.get('network', '')}\n")
                                if 'gateway' in iface:
                                    file.write(f"    gateway {iface.get('gateway', '')}\n")
                            elif iface['name'] == "enp0s3":  # enp0s3 com broadcast adicional
                                file.write(f"    address {iface.get('ip', '')}\n")
                                file.write(f"    netmask {iface.get('netmask', '')}\n")
                                file.write(f"    network {iface.get('network', '')}\n")
                                file.write(f"    broadcast {iface.get('broadcast', '')}\n")
                            
                            file.write("\n")  # Separador entre as interfaces

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DrawWindow = QtWidgets.QMainWindow()
    ui = Ui_DrawInterface("Debian 12 https")
    ui.setupUi(DrawWindow)
    DrawWindow.show()
    sys.exit(app.exec())
