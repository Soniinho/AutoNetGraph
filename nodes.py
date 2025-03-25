from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QBrush, QFont
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsLineItem, QGraphicsTextItem, QMenu, QDialog, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox

class NetworkShape:
    def __init__(self, interfaces, ip_forward=0, language="en"):
        # Atributos de rede
        self.interfaces = interfaces
        self.ip_forward = ip_forward
        self.language = language
        
        self.translations = {
            "br": {
                "interface": "Interface",
                "ip_forward": "IP Forward",
                "properties": "Propriedades",
                "delete": "Excluir",
                "configuration": "Configuração",
                "automatic": "Automático",
                "manual": "Manual",
                "ip": "IP",
                "netmask": "Máscara de Rede",
                "network": "Rede",
                "gateway": "Gateway",
                "broadcast": "Broadcast",
                "interface_config": "Interface {name} Configuração"
            },
            "en": {
                "interface": "Interface",
                "ip_forward": "IP Forward",
                "properties": "Properties",
                "delete": "Delete",
                "configuration": "Configuration",
                "automatic": "Automatic",
                "manual": "Manual",
                "ip": "IP",
                "netmask": "Netmask",
                "network": "Network",
                "gateway": "Gateway",
                "broadcast": "Broadcast",
                "interface_config": "Interface {name} Configuration"
            },
        }

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
            self.scene().removeItem(self)

    def show_properties_dialog(self):
        dialog = PropertiesDialog(self, self.language)
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


class MovableEllipse(NetworkShape, QGraphicsEllipseItem):
    def __init__(self, x, y, width, height, language="en"):
        interfaces = [
            {"name": "enp0s8", "ip": "automático", "netmask": "automático", "network": "automático", "gateway": "automático", "automatic": True}
        ]
        QGraphicsEllipseItem.__init__(self, x, y, width, height)
        NetworkShape.__init__(self, interfaces, ip_forward=0, language=language)
        self.connections = []
        self.setZValue(1)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.update_connections()


class MovableRect(NetworkShape, QGraphicsRectItem):
    def __init__(self, x, y, width, height, language="en"):
        interfaces = [
            {"name": "enp0s8", "ip": "automático", "netmask": "automático", "network": "automático", "gateway": "automático", "automatic": True},
            {"name": "enp0s3", "ip": "automático", "netmask": "automático", "network": "automático", "broadcast": "automático", "automatic": True}
        ]
        QGraphicsRectItem.__init__(self, x, y, width, height)
        NetworkShape.__init__(self, interfaces, ip_forward=1, language=language)
        self.connections = []
        self.setZValue(1)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.update_connections()


class PropertiesDialog(QDialog):
    def __init__(self, shape, language="en"):
        super().__init__()
        self.language = language  # Armazena o idioma escolhido
        self.translations = shape.translations  # Obtém o dicionário de traduções
        texts = self.translations[self.language]

        self.setWindowTitle(texts["properties"])
        layout = QFormLayout(self)
        self.interface_edits = []

        # Para cada interface, cria os campos e define os nomes
        for i, iface in enumerate(shape.interfaces):
            iface_layout = QFormLayout()

            # Nome da interface
            iface_name = QLineEdit(iface['name'])
            iface_name.setReadOnly(True)
            iface_layout.addRow(f"{texts['interface']} {i+1}:", iface_name)
            
            config_mode = QComboBox()
            config_mode.addItems([texts["automatic"], texts["manual"]])
            config_mode.setCurrentText(texts["automatic"] if iface.get("automatic", True) else texts["manual"])
            iface_layout.addRow(texts["configuration"], config_mode)

            # Campos de IP, Netmask, Network e Gateway/Broadcast
            ip_edit = QLineEdit(iface.get('ip', ''))
            netmask_edit = QLineEdit(iface.get('netmask', ''))
            network_edit = QLineEdit(iface.get('network', ''))
            gateway_or_broadcast_edit = QLineEdit(
                iface.get('gateway', '') if iface['name'] == "enp0s8" else iface.get('broadcast', '')
            )
            
            # Adiciona os campos de edição ao layout da interface
            iface_layout.addRow(texts["ip"], ip_edit)
            iface_layout.addRow(texts["netmask"], netmask_edit)
            iface_layout.addRow(texts["network"], network_edit)
            iface_layout.addRow(texts["gateway"] if iface['name'] == "enp0s8" else texts["broadcast"], gateway_or_broadcast_edit)
            
            # Armazena campos na lista e define o layout
            self.interface_edits.append({
                'config_mode': config_mode,
                'ip': ip_edit,
                'netmask': netmask_edit,
                'network': network_edit,
                'gateway_or_broadcast': gateway_or_broadcast_edit
            })
            layout.addRow(texts["interface_config"].format(name=iface['name']), iface_layout)
            
            # Define estado inicial dos campos com base no modo
            self.toggle_manual_fields(i)

            # Conecta sinal de mudança no combo box para atualizar os campos quando alterado
            config_mode.currentIndexChanged.connect(lambda _, idx=i: self.toggle_manual_fields(idx))
        
        # Botões OK e Cancelar
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def toggle_manual_fields(self, idx):
        """Habilita ou desabilita campos de acordo com o modo de configuração selecionado"""
        
        texts = self.translations[self.language]
        is_automatic = self.interface_edits[idx]['config_mode'].currentText() == texts["automatic"]
        
        for field_key in ['ip', 'netmask', 'network', 'gateway_or_broadcast']:
            field = self.interface_edits[idx][field_key]
            field.setReadOnly(is_automatic)  # Define o campo como somente leitura se for automático
            field.setText('' if is_automatic else field.text())


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
