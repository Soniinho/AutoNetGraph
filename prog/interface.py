from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QBrush, QFont
from PyQt6.QtWidgets import QGraphicsItem, QMainWindow, QGraphicsScene, QGraphicsView, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsLineItem, QGraphicsTextItem, QMenu, QDialog, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox

from ifaceSelectDialog import InterfaceSelectionDialog
from nodes import MovableEllipse, MovableRect, ConnectionLine
from virtualboxFunc import cloneConfigureMachines
from translations import TRANSLATIONS

class Ui_DrawInterface(object):
    def __init__(self, selected_vm, language="en"):
        self.selected_vm = selected_vm
        self.language = language
        self.translations = TRANSLATIONS  # Centralized translations

    def setupUi(self, DiagramWindow):
        texts = self.translations[self.language]
        DiagramWindow.setObjectName("DiagramWindow")
        DiagramWindow.resize(900, 650)

        # Central widget
        self.centralwidget = QtWidgets.QWidget(DiagramWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Main layout
        self.layout = QVBoxLayout(self.centralwidget)

        # Horizontal layout for buttons
        button_layout = QHBoxLayout()

        # Buttons
        self.button_computer = QPushButton(texts["computer_button"], self.centralwidget)
        self.button_gateway = QPushButton(texts["gateway_button"], self.centralwidget)
        self.button_connect = QPushButton(texts["connect_button"], self.centralwidget)

        for button in (self.button_computer, self.button_gateway, self.button_connect):
            button.setFixedSize(80, 30)
            button_layout.addWidget(button)

        self.layout.addLayout(button_layout)

        # Clone Machines Button
        self.button_clone_machines = QPushButton(texts["clone_button"], self.centralwidget)
        self.button_clone_machines.setFixedSize(120, 30)
        button_layout.addWidget(self.button_clone_machines)

        # Adiciona o botão de configuração de rede
        self.button_setup_network = QPushButton("Setup Network", self.centralwidget)
        self.button_setup_network.setFixedSize(120, 30)
        self.button_setup_network.clicked.connect(self.setup_network)
        button_layout.addWidget(self.button_setup_network)

        # Add save/load buttons
        self.button_save = QPushButton(texts["save_button"], self.centralwidget)
        self.button_load = QPushButton(texts["load_button"], self.centralwidget)
        self.button_save.setFixedSize(80, 30)
        self.button_load.setFixedSize(80, 30)
        button_layout.addWidget(self.button_save)
        button_layout.addWidget(self.button_load)

        # Conecting the buttons to the functions
        self.button_clone_machines.clicked.connect(lambda: cloneConfigureMachines(self.selected_vm, self.scene))
        self.button_computer.clicked.connect(self.add_computer)
        self.button_gateway.clicked.connect(self.add_gateway)
        self.button_connect.clicked.connect(self.add_connect)
        self.button_save.clicked.connect(self.save_diagram)
        self.button_load.clicked.connect(self.load_diagram)

        # Graphics View
        #self.graphicsView = ZoomableGraphicsView()
        self.graphicsView = QGraphicsView()
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setStyleSheet("background-color: #F0F0F0; border: 1px solid #A9A9A9;")
        self.layout.addWidget(self.graphicsView)
        
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
        computer = MovableEllipse(0, 0, 50, 50, self.language)
        computer.setBrush(QBrush(Qt.GlobalColor.cyan))
        computer.setFlags(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsMovable | QGraphicsEllipseItem.GraphicsItemFlag.ItemIsSelectable)
        self.scene.addItem(computer)

    def add_gateway(self):
        gateway = MovableRect(0, 0, 70, 50, self.language)
        gateway.setBrush(QBrush(Qt.GlobalColor.lightGray))
        gateway.setFlags(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable | QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable)
        self.scene.addItem(gateway)

    def add_connect(self):
        selected_items = self.scene.selectedItems()
        if len(selected_items) == 2:
            item1, item2 = selected_items
            
            # Verifica se já existe uma conexão entre os itens
            for conn in item1.connections:
                if conn.start_item == item2 or conn.end_item == item2:
                    return  # Já existe uma conexão entre estes itens
            
            # Check for invalid host-to-host connection first
            if isinstance(item1, MovableEllipse) and isinstance(item2, MovableEllipse):
                QtWidgets.QMessageBox.warning(None, "Erro", "Não é possível conectar dois hosts diretamente!")
                return
            
            interface_name = None
            # Se um dos itens é um gateway, precisamos selecionar a interface
            gateway_item = None
            host_item = None
            
            if isinstance(item1, MovableRect):
                gateway_item = item1
                host_item = item2 if isinstance(item2, MovableEllipse) else None
            elif isinstance(item2, MovableRect):
                gateway_item = item2
                host_item = item1 if isinstance(item1, MovableEllipse) else None
                
            if gateway_item and host_item:
                # Verifica se o gateway já tem um host conectado
                has_connected_host = False
                connected_interface = None
                for conn in gateway_item.connections:
                    if isinstance(conn.start_item, MovableEllipse) or isinstance(conn.end_item, MovableEllipse):
                        has_connected_host = True
                        connected_interface = conn.interface_name
                        break
                
                if has_connected_host:
                    # Se já tem host conectado, força usar a mesma interface
                    interface_name = connected_interface
                else:
                    # Se não tem host conectado, permite escolher a interface
                    dialog = InterfaceSelectionDialog(gateway_item, self.language)
                    if dialog.exec() == QDialog.DialogCode.Accepted:
                        interface_name = dialog.combo.currentText()
                    else:
                        return
            elif isinstance(item1, MovableRect) or isinstance(item2, MovableRect):
                # Caso gateway-gateway, permite escolher a interface normalmente
                gateway = item1 if isinstance(item1, MovableRect) else item2
                dialog = InterfaceSelectionDialog(gateway, self.language)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    interface_name = dialog.combo.currentText()
                else:
                    return
            
            # Verifica se os tipos de conexão são válidos
            is_valid_connection = (
                # Host para Gateway (Ellipse para Rect)
                (isinstance(item1, MovableEllipse) and isinstance(item2, MovableRect)) or
                # Gateway para Host (Rect para Ellipse)
                (isinstance(item1, MovableRect) and isinstance(item2, MovableEllipse)) or
                # Gateway para Gateway (Rect para Rect)
                (isinstance(item1, MovableRect) and isinstance(item2, MovableRect))
            )

            if is_valid_connection:
                connect = ConnectionLine(item1, item2, interface_name, self.language)
                self.scene.addItem(connect)

    def setup_network(self):
        # Encontra todos os objetos na cena
        all_items = [item for item in self.scene.items() if isinstance(item, (MovableRect, MovableEllipse))]
        
        # Encontra o gateway raiz (com apenas uma interface conectada)
        root = None
        for item in all_items:
            if isinstance(item, MovableRect):
                connected_interfaces = set()
                for conn in item.connections:
                    if conn.interface_name:
                        connected_interfaces.add(conn.interface_name)
                if len(connected_interfaces) == 1:
                    if root is None:
                        root = item
                    else:
                        QtWidgets.QMessageBox.warning(None, "Erro", "Múltiplos gateways com apenas uma interface conectada encontrados!")
                        return
        
        if not root:
            QtWidgets.QMessageBox.warning(None, "Erro", "Nenhum gateway raiz encontrado!")
            return
        
        # Verifica se todos os objetos têm conexões válidas
        for item in all_items:
            if not item.has_valid_connections():
                QtWidgets.QMessageBox.warning(None, "Erro", "Alguns objetos não têm todas as interfaces necessárias conectadas!")
                return
        
        # Configura os IPs começando do root
        used_ips = set()
        def configure_network(node, subnet_counter=1):
            if isinstance(node, MovableRect):
                # Configura gateway
                for interface in node.interfaces:
                    interface['automatic'] = False
                    if interface['name'] == 'enp0s8':
                        ip = f"192.168.{subnet_counter}.1"
                        if ip not in used_ips:
                            interface['ip'] = ip
                            interface['netmask'] = "255.255.255.0"
                            interface['network'] = f"192.168.{subnet_counter}.0"
                            interface['gateway'] = "0.0.0.0"
                            used_ips.add(ip)
                            subnet_counter += 1
            elif isinstance(node, MovableEllipse):
                # Configura host
                interface = node.interfaces[0]
                interface['automatic'] = False
                ip = f"192.168.{subnet_counter-1}.{len(used_ips) % 254 + 1}"
                if ip not in used_ips:
                    interface['ip'] = ip
                    interface['netmask'] = "255.255.255.0"
                    interface['network'] = f"192.168.{subnet_counter-1}.0"
                    interface['gateway'] = f"192.168.{subnet_counter-1}.1"
                    used_ips.add(ip)
            
            # Atualiza texto
            node.text_item.setPlainText(node.info_text())
            
            # Configura nós conectados
            for connected_node, _ in node.get_connected_items():
                if connected_node.interfaces[0]['ip'] == "automático":
                    configure_network(connected_node, subnet_counter)
        
        # Inicia a configuração a partir do root
        configure_network(root)

    def save_diagram(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save Diagram", "", "Text Files (*.txt)")
        if filename:
            data = {
                'nodes': [],
                'connections': []
            }
            
            # Save all nodes
            for item in self.scene.items():
                if isinstance(item, (MovableEllipse, MovableRect)):
                    node_data = {
                        'type': 'ellipse' if isinstance(item, MovableEllipse) else 'rect',
                        'pos': {'x': item.pos().x(), 'y': item.pos().y()},
                        'interfaces': item.interfaces,
                        'ip_forward': item.ip_forward
                    }
                    data['nodes'].append(node_data)
                
                elif isinstance(item, ConnectionLine):
                    # Get indices of connected items
                    start_idx = -1
                    end_idx = -1
                    nodes = [i for i in self.scene.items() if isinstance(i, (MovableEllipse, MovableRect))]
                    
                    for i, node in enumerate(nodes):
                        if node == item.start_item:
                            start_idx = i
                        if node == item.end_item:
                            end_idx = i
                    
                    conn_data = {
                        'start_idx': start_idx,
                        'end_idx': end_idx,
                        'interface_name': item.interface_name
                    }
                    data['connections'].append(conn_data)
            
            import json
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)

    def load_diagram(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Load Diagram", "", "Text Files (*.txt)")
        if filename:
            # Clear current scene
            self.scene.clear()
            
            import json
            with open(filename, 'r') as f:
                data = json.load(f)
            
            # Create nodes first
            nodes = []
            for node_data in data['nodes']:
                if node_data['type'] == 'ellipse':
                    node = MovableEllipse(0, 0, 50, 50, self.language)
                    node.setBrush(QBrush(Qt.GlobalColor.cyan))
                else:
                    node = MovableRect(0, 0, 70, 50, self.language)
                    node.setBrush(QBrush(Qt.GlobalColor.lightGray))
                
                node.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsMovable | 
                             QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
                node.setPos(node_data['pos']['x'], node_data['pos']['y'])
                node.interfaces = node_data['interfaces']
                node.ip_forward = node_data['ip_forward']
                node.text_item.setPlainText(node.info_text())
                
                self.scene.addItem(node)
                nodes.append(node)
            
            # Create connections
            for conn_data in data['connections']:
                start_item = nodes[conn_data['start_idx']]
                end_item = nodes[conn_data['end_idx']]
                connect = ConnectionLine(start_item, end_item, conn_data['interface_name'])
                self.scene.addItem(connect)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DrawWindow = QtWidgets.QMainWindow()
    ui = Ui_DrawInterface(selected_vm = "VM1")
    ui.setupUi(DrawWindow)
    DrawWindow.show()
    sys.exit(app.exec())
