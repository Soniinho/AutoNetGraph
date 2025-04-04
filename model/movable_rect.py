from PyQt6.QtWidgets import QGraphicsRectItem

from .network_shape import NetworkShape


class MovableRect(NetworkShape, QGraphicsRectItem):
    def __init__(self, x, y, width, height, language="en"):
        interfaces = [
            {"name": "enp0s8", "ip": "automático", "netmask": "automático", "network": "automático", "gateway": "automático", "broadcast": "automático", "automatic": True},
            {"name": "enp0s3", "ip": "automático", "netmask": "automático", "network": "automático", "gateway": "automático", "broadcast": "automático", "automatic": True}
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
