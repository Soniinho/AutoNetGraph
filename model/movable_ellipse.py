from PyQt6.QtWidgets import QGraphicsEllipseItem

from .network_shape import NetworkShape


class MovableEllipse(NetworkShape, QGraphicsEllipseItem):
    def __init__(self, x, y, width, height, language="en"):
        interfaces = [
            {"name": "enp0s3", "automatic": True, "ip": "automático", "netmask": "automático", "network": "automático", "gateway": "automático", "broadcast": "automático"}
        ]
        QGraphicsEllipseItem.__init__(self, x, y, width, height)
        NetworkShape.__init__(self, interfaces, ip_forward=0, language=language)
        self.connections = []
        self.setZValue(1)
