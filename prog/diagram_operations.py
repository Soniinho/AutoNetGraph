from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem, QDialog

from prog.nodes import MovableEllipse, MovableRect, ConnectionLine
from prog.iface_select_dialog import InterfaceSelectionDialog


def add_computer(scene, language):
    computer = MovableEllipse(0, 0, 50, 50, language)
    computer.setBrush(QBrush(Qt.GlobalColor.cyan))
    computer.setFlags(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsMovable | QGraphicsEllipseItem.GraphicsItemFlag.ItemIsSelectable)
    scene.addItem(computer)

def add_gateway(scene, language):
    gateway = MovableRect(0, 0, 70, 50, language)
    gateway.setBrush(QBrush(Qt.GlobalColor.lightGray))
    gateway.setFlags(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable | QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable)
    scene.addItem(gateway)

# TODO: erro fora da tradução
# TODO: conexão entre 2 gateways na msm iface
def add_connect(scene, language):
    selected_items = scene.selectedItems()
    if len(selected_items) == 2:
        item1, item2 = selected_items
        
        # Check existing connection
        for conn in item1.connections:
            if conn.start_item == item2 or conn.end_item == item2:
                return
        
        # Check invalid host-to-host connection
        if isinstance(item1, MovableEllipse) and isinstance(item2, MovableEllipse):
            QtWidgets.QMessageBox.warning(None, "Erro", "Não é possível conectar dois hosts diretamente!")
            return
        
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
            for conn in gateway_item.connections:
                if isinstance(conn.start_item, MovableEllipse) or isinstance(conn.end_item, MovableEllipse):
                    has_connected_host = True
                    connected_interface = conn.interface_name
                    break
            
            if has_connected_host:
                interface_name = connected_interface
            else:
                dialog = InterfaceSelectionDialog(gateway_item, language)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    interface_name = dialog.combo.currentText()
                else:
                    return
        elif isinstance(item1, MovableRect) or isinstance(item2, MovableRect):
            gateway = item1 if isinstance(item1, MovableRect) else item2
            dialog = InterfaceSelectionDialog(gateway, language)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                interface_name = dialog.combo.currentText()
            else:
                return
        
        is_valid_connection = (
            (isinstance(item1, MovableEllipse) and isinstance(item2, MovableRect)) or
            (isinstance(item1, MovableRect) and isinstance(item2, MovableEllipse)) or
            (isinstance(item1, MovableRect) and isinstance(item2, MovableRect))
        )

        if is_valid_connection:
            connect = ConnectionLine(item1, item2, interface_name, language)
            scene.addItem(connect)
