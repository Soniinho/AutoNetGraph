from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen
from PyQt6.QtWidgets import QGraphicsTextItem, QMenu, QGraphicsLineItem, QGraphicsTextItem, QMenu

from model.translations import TRANSLATIONS


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
