from PyQt6.QtGui import QBrush, QPen
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsEllipseItem

class NodeItem(QGraphicsEllipseItem):
    def __init__(self, x, y, diameter, name, ip_address):
        super().__init__(x, y, diameter, diameter)
        self.setBrush(QBrush(Qt.GlobalColor.red))  # Cor do círculo
        self.setPen(QPen(Qt.GlobalColor.black))    # Cor da borda
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsMovable)  # Permite mover o círculo
        
        # Atributos personalizados para o nó
        self.name = name
        self.ip_address = ip_address

    def get_info(self):
        return f"Nome: {self.name}, IP: {self.ip_address}"