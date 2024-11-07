from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QBrush, QFont
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsLineItem, QGraphicsTextItem, QMenu, QDialog, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox

class NetworkShape:
    def __init__(self, ip, interface, netmask, network, broadcast, ip_forward):
        # Atributos de rede
        self.ip = ip
        self.interface = interface
        self.netmask = netmask
        self.network = network
        self.broadcast = broadcast
        self.ip_forward = ip_forward

        # Exibe as informações ao lado da forma
        self.text_item = QGraphicsTextItem(self.info_text(), self)
        self.text_item.setFont(QFont("Arial", 8))
        self.text_item.setPos(self.boundingRect().width() + 5, 0)

    def info_text(self):
        return f"IP: {self.ip}\nInterface: {self.interface}\nNetmask: {self.netmask}\nNetwork: {self.network}\nBroadcast: {self.broadcast}\nIP Forward: {self.ip_forward}"

    def contextMenuEvent(self, event):
        menu = QMenu()
        properties_action = menu.addAction("Propriedades")
        delete_action = menu.addAction("Excluir")  # Adiciona a opção de exclusão
        action = menu.exec(event.screenPos())
        
        if action == properties_action:
            self.show_properties_dialog()
        elif action == delete_action:
            self.scene().removeItem(self)  # Remove a forma da cena

    def show_properties_dialog(self):
        dialog = PropertiesDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.update_properties(dialog)

    def update_properties(self, dialog):
        self.ip = dialog.ip_edit.text()
        self.interface = dialog.interface_edit.text()
        self.netmask = dialog.netmask_edit.text()
        self.network = dialog.network_edit.text()
        self.broadcast = dialog.broadcast_edit.text()
        #self.ip_forward = int(dialog.ip_forward_combo.currentText())
        self.text_item.setPlainText(self.info_text())

    def update_connections(self):
        for line in self.connections:
            line.update_position()


class MovableEllipse(NetworkShape, QGraphicsEllipseItem):
    def __init__(self, x, y, width, height, ip, interface, netmask, network, broadcast, ip_forward):
        QGraphicsEllipseItem.__init__(self, x, y, width, height)
        NetworkShape.__init__(self, ip, interface, netmask, network, broadcast, ip_forward)
        self.connections = []
        self.setZValue(1)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.update_connections()  # Atualiza as linhas ao mover a forma

    def update_connections(self):
        for line in self.connections:
            line.update_position()  # Atualiza a posição das linhas associadas


class MovableRect(NetworkShape, QGraphicsRectItem):
    def __init__(self, x, y, width, height, ip, interface, netmask, network, broadcast, ip_forward):
        QGraphicsRectItem.__init__(self, x, y, width, height)
        NetworkShape.__init__(self, ip, interface, netmask, network, broadcast, ip_forward)
        self.connections = []
        self.setZValue(1)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.update_connections()  # Atualiza as linhas ao mover a forma

    def update_connections(self):
        for line in self.connections:
            line.update_position()  # Atualiza a posição das linhas associadas


class PropertiesDialog(QDialog):
    def __init__(self, shape):
        super().__init__()
        self.setWindowTitle("Propriedades")
        
        layout = QFormLayout(self)
        
        # Campos de edição para cada propriedade
        self.ip_edit = QLineEdit(shape.ip)
        self.interface_edit = QLineEdit(shape.interface)
        self.netmask_edit = QLineEdit(shape.netmask)
        self.network_edit = QLineEdit(shape.network)
        self.broadcast_edit = QLineEdit(shape.broadcast)
        
        # # Combo box para ip_forward
        # self.ip_forward_combo = QComboBox()
        # self.ip_forward_combo.addItems(["0", "1"])
        # self.ip_forward_combo.setCurrentText(str(shape.ip_forward))
        
        layout.addRow("IP:", self.ip_edit)
        layout.addRow("Interface:", self.interface_edit)
        layout.addRow("Netmask:", self.netmask_edit)
        layout.addRow("Network:", self.network_edit)
        layout.addRow("Broadcast:", self.broadcast_edit)
        # layout.addRow("IP Forward:", self.ip_forward_combo)
        
        # Botões OK e Cancelar
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)


class ConnectionLine(QGraphicsLineItem):
    def __init__(self, start_item, end_item):
        super().__init__()
        self.start_item = start_item
        self.end_item = end_item
        self.setPen(QPen(Qt.GlobalColor.black, 2))
        self.start_item.connections.append(self)
        self.end_item.connections.append(self)
        self.setZValue(0)
        self.update_position()

    def update_position(self):
        start_point = self.start_item.sceneBoundingRect().center()
        end_point = self.end_item.sceneBoundingRect().center()
        self.setLine(start_point.x(), start_point.y(), end_point.x(), end_point.y())
