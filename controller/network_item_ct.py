from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem, QDialog

from model import MovableEllipse, MovableRect, ConnectionLine
from model.translations_md import TRANSLATIONS
from view.iface_select_dialog import Ui_InterfaceSelectionDialog


class NetworkItemController:
    def __init__(self, scene, language):
        self.scene = scene
        self.language = language
        self.texts = TRANSLATIONS[language]

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

    def add_connection(self):
        selected_items = self.scene.selectedItems()
        if len(selected_items) == 2:
            item1, item2 = selected_items

            # Ordena pelo eixo Y
            if len(selected_items) == 2:
                item1, item2 = sorted(selected_items, key=lambda item: item.pos().y())
            
            # Checa conexões existentes
            for conn in item1.connections:
                if conn.start_item == item2 or conn.end_item == item2:
                    return
            
            # Checa conexões invalidas entre computadores
            if isinstance(item1, MovableEllipse) and isinstance(item2, MovableEllipse):
                QtWidgets.QMessageBox.warning(None, self.texts["error_1"], self.texts["error_2"])
                return
            
            # Checa conexões invalidas entre gateways
            if isinstance(item1, MovableRect) and isinstance(item2, MovableRect):
                dialog = Ui_InterfaceSelectionDialog(item1, item2, self.language)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    interface1, interface2 = dialog.get_selected_interfaces()
                    
                    # Criar uma conexão com informações de ambas as interfaces
                    connect = ConnectionLine(item1, item2, f"{interface1} <-> {interface2}", self.language)
                    
                    # Adicionar às listas específicas de interfaces
                    if hasattr(item1, 'connections_by_interface') and interface1 in item1.connections_by_interface:
                        item1.connections_by_interface[interface1].append(connect)
                    
                    if hasattr(item2, 'connections_by_interface') and interface2 in item2.connections_by_interface:
                        item2.connections_by_interface[interface2].append(connect)
                    
                    self.scene.addItem(connect)
                return
            
            # Conexão entre gateway e host ou entre gateways
            interface_name = None
            gateway_item = None
            host_item = None
            
            if isinstance(item1, MovableRect):
                gateway_item = item1
                host_item = item2 if isinstance(item2, MovableEllipse) else None
            elif isinstance(item2, MovableRect):
                gateway_item = item2
                host_item = item1 if isinstance(item1, MovableEllipse) else None
            
            if gateway_item and host_item:
                has_connected_host = False
                connected_interface = None
                
                # Verifica por interface
                if hasattr(gateway_item, 'connections_by_interface'):
                    for interface, connections in gateway_item.connections_by_interface.items():
                        for conn in connections:
                            connected_item = conn.start_item if conn.start_item != gateway_item else conn.end_item
                            if isinstance(connected_item, MovableEllipse):
                                has_connected_host = True
                                connected_interface = interface
                                break
                        if has_connected_host:
                            break
                else:
                    for conn in gateway_item.connections:
                        if isinstance(conn.start_item, MovableEllipse) or isinstance(conn.end_item, MovableEllipse):
                            has_connected_host = True
                            connected_interface = conn.interface_name
                            break
                
                if has_connected_host:
                    interface_name = connected_interface
                else:
                    dialog = Ui_InterfaceSelectionDialog(gateway_item, language=self.language)
                    if dialog.exec() == QDialog.DialogCode.Accepted:
                        interface_name, _ = dialog.get_selected_interfaces()
                    else:
                        return
            elif isinstance(item1, MovableRect) or isinstance(item2, MovableRect):
                gateway = item1 if isinstance(item1, MovableRect) else item2
                dialog = Ui_InterfaceSelectionDialog(gateway, language=self.language)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    interface_name, _ = dialog.get_selected_interfaces()
                else:
                    return
            
            is_valid_connection = (
                (isinstance(item1, MovableEllipse) and isinstance(item2, MovableRect)) or
                (isinstance(item1, MovableRect) and isinstance(item2, MovableEllipse)) or
                (isinstance(item1, MovableRect) and isinstance(item2, MovableRect))
            )
            if is_valid_connection:
                connect = ConnectionLine(item1, item2, interface_name, self.language)
                self.scene.addItem(connect)
