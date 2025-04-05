from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox

from model.translations import TRANSLATIONS


class InterfacePropertiesDialog(QDialog):
    def __init__(self, shape, language="en"):
        super().__init__()
        self.language = language
        self.translations = TRANSLATIONS
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

            # Modo de configuração
            config_mode = QComboBox()
            config_mode.addItems([texts["automatic"], texts["manual"]])
            config_mode.setCurrentText(
                texts["automatic"] if iface.get("automatic", True) else texts["manual"]
            )
            iface_layout.addRow(texts["configuration"], config_mode)

            # Campos de edição
            ip_edit = QLineEdit(iface.get('ip', ''))
            netmask_edit = QLineEdit(iface.get('netmask', ''))
            network_edit = QLineEdit(iface.get('network', ''))
            gateway_edit = QLineEdit(iface.get('gateway', ''))
            broadcast_edit = QLineEdit(iface.get('broadcast', ''))

            # Adiciona ao layout
            iface_layout.addRow(texts["ip"], ip_edit)
            iface_layout.addRow(texts["netmask"], netmask_edit)
            iface_layout.addRow(texts["network"], network_edit)
            iface_layout.addRow(texts["gateway"], gateway_edit)
            iface_layout.addRow(texts["broadcast"], broadcast_edit)

            # Salva os campos em uma lista de edição
            self.interface_edits.append({
                'config_mode': config_mode,
                'ip': ip_edit,
                'netmask': netmask_edit,
                'network': network_edit,
                'gateway': gateway_edit,
                'broadcast': broadcast_edit
            })

            layout.addRow(texts["interface_config"].format(name=iface['name']), iface_layout)

            # Inicializa estado dos campos
            self.toggle_manual_fields(i)
            config_mode.currentIndexChanged.connect(lambda _, idx=i: self.toggle_manual_fields(idx))

        # Botões OK/Cancelar
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def toggle_manual_fields(self, idx):
        """Habilita/desabilita os campos conforme o modo de configuração"""
        texts = self.translations[self.language]
        is_automatic = self.interface_edits[idx]['config_mode'].currentText() == texts["automatic"]

        for key, field in self.interface_edits[idx].items():
            if key == 'config_mode':
                continue
            field.setReadOnly(is_automatic)
            field.setText('' if is_automatic else field.text())
