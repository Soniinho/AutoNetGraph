from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QGraphicsTextItem, QMenu, QDialog, QGraphicsTextItem, QMenu

from view.iface_properties_dialog import Ui_InterfacePropertiesDialog
from .translations_md import TRANSLATIONS


class NetworkShape:
    def __init__(self, interfaces, ip_forward=0, language="en"):
        # Atributos de rede
        self.interfaces = interfaces
        self.ip_forward = ip_forward
        self.language = language
        
        self.translations = TRANSLATIONS

        # Exibe as informações ao lado da forma
        self.text_item = QGraphicsTextItem(self.info_text(), self)
        self.text_item.setFont(QFont("Arial", 8))
        self.text_item.setPos(self.boundingRect().width() + 5, 0)

    def info_text(self):
        # Constrói a exibição de informações
        texts = self.translations[self.language]
        info = ""

        # Ordena as interfaces por nome
        sorted_interfaces = sorted(self.interfaces, key=lambda x: x['name'], reverse=True)

        for iface in sorted_interfaces:
            info += f"{texts['interface']} {iface['name']}:\n"
            for key, value in iface.items():
                if key != "name":
                    info += f"  {texts.get(key, key).capitalize()}: {value}\n"
            info += f"\n"
        # info += f"{texts['ip_forward']}: {self.ip_forward}\n"
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
        dialog = Ui_InterfacePropertiesDialog(self, self.language)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.update_properties(dialog)

    def update_properties(self, dialog):
        texts = self.translations[self.language]
        for i, iface in enumerate(self.interfaces):
            is_automatic = dialog.interface_edits[i]['config_mode'].currentText() == texts["automatic"]
            iface['automatic'] = is_automatic

            if not is_automatic:
                iface['ip'] = dialog.interface_edits[i]['ip'].text()
                iface['netmask'] = dialog.interface_edits[i]['netmask'].text()
                iface['network'] = dialog.interface_edits[i]['network'].text()
                iface['gateway'] = dialog.interface_edits[i]['gateway'].text()
                iface['broadcast'] = dialog.interface_edits[i]['broadcast'].text()

        self.text_item.setPlainText(self.info_text())

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # Update connections for all selected items
        for item in self.scene().selectedItems():
            if hasattr(item, 'update_connections'):
                item.update_connections()

    def update_connections(self):
        for line in self.connections:
            line.update_position()

    def has_valid_connections(self):
        """Verifica se todas as interfaces têm pelo menos uma conexão"""
        # Em vez de usar isinstance, verificamos o nome da classe
        if self.__class__.__name__ == 'MovableRect' and hasattr(self, 'connections_by_interface'):
            # Verifica se pelo menos uma interface tem conexão
            for interface, connections in self.connections_by_interface.items():
                if connections:
                    return True
            return False
        elif self.__class__.__name__ == 'MovableEllipse':
            return len(self.connections) >= 1
        # Fallback para o método antigo se não tiver o dicionário
        else:
            connected_interfaces = set()
            for conn in self.connections:
                if conn.interface_name:
                    connected_interfaces.add(conn.interface_name)
            
            if self.__class__.__name__ == 'MovableRect':
                return len(connected_interfaces) >= 1
            elif self.__class__.__name__ == 'MovableEllipse':
                return len(self.connections) >= 1
            return False

    def get_connected_items(self):
        """Retorna todos os itens conectados a este nó"""
        connected = []
        
        # Para MovableRect com o dicionário connections_by_interface
        if self.__class__.__name__ == 'MovableRect' and hasattr(self, 'connections_by_interface'):
            for interface, connections in self.connections_by_interface.items():
                for conn in connections:
                    connected_item = conn.end_item if conn.start_item == self else conn.start_item
                    # Para conexões entre gateways, extrai a interface correta do formato "iface1 <-> iface2"
                    interface_name = conn.interface_name
                    if ' <-> ' in interface_name:
                        parts = interface_name.split(' <-> ')
                        if conn.start_item == self:
                            interface_name = parts[0]
                        else:
                            interface_name = parts[1]
                    
                    # Evitar duplicados
                    item_entry = (connected_item, interface_name)
                    if item_entry not in connected:
                        connected.append(item_entry)
        else:
            for conn in self.connections:
                if conn.start_item == self:
                    connected.append((conn.end_item, conn.interface_name))
                else:
                    connected.append((conn.start_item, conn.interface_name))
        
        return connected
