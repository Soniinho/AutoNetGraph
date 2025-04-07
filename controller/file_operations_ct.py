import json
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush
from PyQt6.QtWidgets import QGraphicsItem

from model import MovableEllipse, MovableRect, ConnectionLine


class FileOperationsController:
    def __init__(self, scene, language):
        self.scene = scene
        self.language = language

    def save_diagram(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save Diagram", "", "Text Files (*.txt)")
        if filename:
            data = {
                'nodes': [],
                'connections': []
            }
        
            for item in self.scene.items():
                if isinstance(item, (MovableEllipse, MovableRect)):
                    node_data = {
                        'type': 'ellipse' if isinstance(item, MovableEllipse) else 'rect',
                        'pos': {'x': item.pos().x(), 'y': item.pos().y()},
                        'interfaces': item.interfaces,
                        'ip_forward': item.ip_forward
                    }
                    
                    # Salvar o dicionário connections_by_interface para MovableRect
                    if isinstance(item, MovableRect) and hasattr(item, 'connections_by_interface'):
                        # Salvando índices
                        # Salvando separadamente no nó
                        node_data['has_connections_by_interface'] = True
                    
                    data['nodes'].append(node_data)
            
                elif isinstance(item, ConnectionLine):
                    nodes = [i for i in self.scene.items() if isinstance(i, (MovableEllipse, MovableRect))]
                    start_idx = -1
                    end_idx = -1
                
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
        
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)

    def load_diagram(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Load Diagram", "", "Text Files (*.txt)")
        if filename:
            self.scene.clear()
        
            with open(filename, 'r') as f:
                data = json.load(f)
        
            nodes = []
            for node_data in data['nodes']:
                if node_data['type'] == 'ellipse':
                    node = MovableEllipse(0, 0, 50, 50, self.language)
                    node.setBrush(QBrush(Qt.GlobalColor.cyan))
                else:
                    node = MovableRect(0, 0, 70, 50, self.language)
                    node.setBrush(QBrush(Qt.GlobalColor.lightGray))
                    
                    # Inicializar o dicionário connections_by_interface se necessário
                    if 'has_connections_by_interface' in node_data and node_data['has_connections_by_interface']:
                        node.connections_by_interface = {interface['name']: [] for interface in node_data['interfaces']}
            
                node.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
                            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
                node.setPos(node_data['pos']['x'], node_data['pos']['y'])
                node.interfaces = node_data['interfaces']
                node.ip_forward = node_data['ip_forward']
                node.text_item.setPlainText(node.info_text())
            
                self.scene.addItem(node)
                nodes.append(node)
        
            for conn_data in data['connections']:
                start_item = nodes[conn_data['start_idx']]
                end_item = nodes[conn_data['end_idx']]
                connect = ConnectionLine(start_item, end_item, conn_data['interface_name'], self.language)
                self.scene.addItem(connect)
                
                # Se for uma conexão entre MovableRect, adicionar às listas específicas
                if conn_data['interface_name'] and '<->' in conn_data['interface_name']:
                    interfaces = conn_data['interface_name'].split(' <-> ')
                    
                    if isinstance(start_item, MovableRect) and hasattr(start_item, 'connections_by_interface'):
                        if interfaces[0] in start_item.connections_by_interface:
                            start_item.connections_by_interface[interfaces[0]].append(connect)
                            
                    if isinstance(end_item, MovableRect) and hasattr(end_item, 'connections_by_interface'):
                        if interfaces[1] in end_item.connections_by_interface:
                            end_item.connections_by_interface[interfaces[1]].append(connect)
                # Caso seja uma conexão simples com interface única
                elif conn_data['interface_name']:
                    if isinstance(start_item, MovableRect) and hasattr(start_item, 'connections_by_interface'):
                        if conn_data['interface_name'] in start_item.connections_by_interface:
                            start_item.connections_by_interface[conn_data['interface_name']].append(connect)
                    
                    if isinstance(end_item, MovableRect) and hasattr(end_item, 'connections_by_interface'):
                        if conn_data['interface_name'] in end_item.connections_by_interface:
                            end_item.connections_by_interface[conn_data['interface_name']].append(connect)
