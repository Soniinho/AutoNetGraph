from PyQt6.QtWidgets import QGraphicsRectItem

from .network_shape import NetworkShape


class MovableRect(NetworkShape, QGraphicsRectItem):
    def __init__(self, x, y, width, height, language="en"):
        interfaces = [
            {"name": "enp0s3", "automatic": True, "ip": "automático", "netmask": "automático", "network": "automático", "gateway": "automático", "broadcast": "automático"},
            {"name": "enp0s8", "automatic": True, "ip": "automático", "netmask": "automático", "network": "automático", "gateway": "automático", "broadcast": "automático"}
        ]
        QGraphicsRectItem.__init__(self, x, y, width, height)
        NetworkShape.__init__(self, interfaces, ip_forward=1, language=language)
        
        # Criando um dicionário para armazenar conexões por interface
        self.connections_by_interface = {
            "enp0s3": [],
            "enp0s8": []
        }
        # Mantendo a lista genérica para compatibilidade
        self.connections = []
        
        self.setZValue(1)
