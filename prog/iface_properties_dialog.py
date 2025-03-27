from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox

from translations import TRANSLATIONS


class InterfacePropertiesDialog(QDialog):
    def __init__(self, shape, language="en"):
        super().__init__()
        self.language = language
        self.translations = TRANSLATIONS  # Use centralized translations
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

