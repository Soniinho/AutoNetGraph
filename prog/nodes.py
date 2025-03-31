from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QFont
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsLineItem, QGraphicsTextItem, QMenu, QDialog, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox

from prog.iface_properties_dialog import InterfacePropertiesDialog
from prog.translations import TRANSLATIONS


class NetworkShape:
    def __init__(self, interfaces, ip_forward=0, language="en"):
        # Atributos de rede
        self.interfaces = interfaces
        self.ip_forward = ip_forward
        self.language = language
        
        self.translations = TRANSLATIONS  # Use centralized translations

        # Exibe as informações ao lado da forma
        self.text_item = QGraphicsTextItem(self.info_text(), self)
        self.text_item.setFont(QFont("Arial", 8))
        self.text_item.setPos(self.boundingRect().width() + 5, 0)

    def info_text(self):
        # Constrói a exibição de informações
        texts = self.translations[self.language]
        info = ""
        for iface in self.interfaces:
            info += f"{texts['interface']} {iface['name']}:\n"
            for key, value in iface.items():
                if key != "name":
                    info += f"  {texts.get(key, key).capitalize()}: {value}\n"
        info += f"{texts['ip_forward']}: {self.ip_forward}\n"
        return info

    def contextMenuEvent(self, event):
        texts = self.translations[self.language]
        menu = QMenu()
        properties_action = menu.addAction(texts["properties"])
        delete_action = menu.addAction(texts["delete"])
        action = menu.exec(event.screenPos())
        
        if action == properties_action:
            self.show_properties_dialog()
        elif action == delete_action:
            # Remove all connections first
            for connection in self.connections[:]:  # Create a copy of the list to iterate
                # Remove connection from connected items
                if connection in connection.start_item.connections:
                    connection.start_item.connections.remove(connection)
                if connection in connection.end_item.connections:
                    connection.end_item.connections.remove(connection)
                # Remove connection from scene
                self.scene().removeItem(connection)
            # Remove the node itself
            self.scene().removeItem(self)

    def show_properties_dialog(self):
        dialog = InterfacePropertiesDialog(self, self.language)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.update_properties(dialog)

    def update_properties(self, dialog):
        texts = self.translations[self.language]
        for i, iface in enumerate(self.interfaces):
            # Verifica o modo de configuração
            is_automatic = dialog.interface_edits[i]['config_mode'].currentText() == texts["automatic"]
            iface['automatic'] = is_automatic

            # Somente atualiza os campos se estiver no modo "Manual"
            if not is_automatic:
                iface['ip'] = dialog.interface_edits[i]['ip'].text()
                iface['netmask'] = dialog.interface_edits[i]['netmask'].text()
                iface['network'] = dialog.interface_edits[i]['network'].text()
                if iface['name'] == "enp0s8":
                    iface['gateway'] = dialog.interface_edits[i]['gateway_or_broadcast'].text()
                else:
                    iface['broadcast'] = dialog.interface_edits[i]['gateway_or_broadcast'].text()
        
        # Atualiza o texto exibido
        self.text_item.setPlainText(self.info_text())


    def update_connections(self):
        for line in self.connections:
            line.update_position()

    def has_valid_connections(self):
        """Verifica se todas as interfaces têm pelo menos uma conexão"""
        connected_interfaces = set()
        for conn in self.connections:
            if isinstance(self, MovableRect):
                if conn.interface_name:
                    connected_interfaces.add(conn.interface_name)
        
        if isinstance(self, MovableRect):
            return len(connected_interfaces) >= 1
        elif isinstance(self, MovableEllipse):
            return len(self.connections) >= 1
        return False

    def get_connected_items(self):
        """Retorna todos os itens conectados a este nó"""
        connected = []
        for conn in self.connections:
            if conn.start_item == self:
                connected.append((conn.end_item, conn.interface_name))
            else:
                connected.append((conn.start_item, conn.interface_name))
        return connected
    
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # Update connections for all selected items
        for item in self.scene().selectedItems():
            if hasattr(item, 'update_connections'):
                item.update_connections()


class MovableEllipse(NetworkShape, QGraphicsEllipseItem):
    def __init__(self, x, y, width, height, language="en"):
        interfaces = [
            {"name": "enp0s8", "ip": "automático", "netmask": "automático", "network": "automático", "gateway": "automático", "automatic": True}
        ]
        QGraphicsEllipseItem.__init__(self, x, y, width, height)
        NetworkShape.__init__(self, interfaces, ip_forward=0, language=language)
        self.connections = []
        self.setZValue(1)


class MovableRect(NetworkShape, QGraphicsRectItem):
    def __init__(self, x, y, width, height, language="en"):
        interfaces = [
            {"name": "enp0s8", "ip": "automático", "netmask": "automático", "network": "automático", "gateway": "automático", "automatic": True},
            {"name": "enp0s3", "ip": "automático", "netmask": "automático", "network": "automático", "broadcast": "automático", "automatic": True}
        ]
        QGraphicsRectItem.__init__(self, x, y, width, height)
        NetworkShape.__init__(self, interfaces, ip_forward=1, language=language)
        
        # Criando um dicionário para armazenar conexões por interface
        self.connections_by_interface = {
            "enp0s8": [],
            "enp0s3": []
        }
        # Mantendo a lista genérica para compatibilidade
        self.connections = []
        
        self.setZValue(1)


class ConnectionLine(QGraphicsLineItem):
    def __init__(self, start_item, end_item, interface_name=None, language="en"):
        super().__init__()
        self.setFlags(QGraphicsLineItem.GraphicsItemFlag.ItemIsSelectable)
        self.start_item = start_item
        self.end_item = end_item
        self.interface_name = interface_name
        self.setPen(QPen(Qt.GlobalColor.black, 2))
        
        # Adiciona à lista genérica
        self.start_item.connections.append(self)
        self.end_item.connections.append(self)
        
        # Adiciona à lista específica da interface, se existir
        if interface_name:
            if hasattr(self.start_item, 'connections_by_interface') and interface_name in self.start_item.connections_by_interface:
                self.start_item.connections_by_interface[interface_name].append(self)
            
            if hasattr(self.end_item, 'connections_by_interface') and interface_name in self.end_item.connections_by_interface:
                self.end_item.connections_by_interface[interface_name].append(self)
        
        self.setZValue(0)
        self.update_position()
        self.language = language
        self.translations = TRANSLATIONS
        
        # Adiciona texto para mostrar a interface
        if interface_name:
            self.text_item = QGraphicsTextItem(self)
            self.text_item.setPlainText(interface_name)
            self.text_item.setDefaultTextColor(Qt.GlobalColor.blue)
            self.update_text_position()
    
    def contextMenuEvent(self, event):
        texts = self.translations[self.language]
        menu = QMenu()
        delete_action = menu.addAction(texts["delete"])
        action = menu.exec(event.screenPos())
        
        if action == delete_action:
            # Remove from generic connections list
            if self in self.start_item.connections:
                self.start_item.connections.remove(self)
            if self in self.end_item.connections:
                self.end_item.connections.remove(self)
                
            # Remove from interface-specific connections list
            if self.interface_name:
                if hasattr(self.start_item, 'connections_by_interface') and self.interface_name in self.start_item.connections_by_interface:
                    if self in self.start_item.connections_by_interface[self.interface_name]:
                        self.start_item.connections_by_interface[self.interface_name].remove(self)
                
                if hasattr(self.end_item, 'connections_by_interface') and self.interface_name in self.end_item.connections_by_interface:
                    if self in self.end_item.connections_by_interface[self.interface_name]:
                        self.end_item.connections_by_interface[self.interface_name].remove(self)
                        
            # Remove connection from scene
            self.scene().removeItem(self)

    def update_position(self):
        start_point = self.start_item.sceneBoundingRect().center()
        end_point = self.end_item.sceneBoundingRect().center()
        self.setLine(start_point.x(), start_point.y(), end_point.x(), end_point.y())
        if hasattr(self, 'text_item'):
            self.update_text_position()
    
    def update_text_position(self):
        line = self.line()
        center = line.pointAt(0.5)
        self.text_item.setPos(center.x(), center.y() - 15)
