from PyQt6.QtWidgets import QVBoxLayout, QDialog, QComboBox, QDialogButtonBox

from prog.translations import TRANSLATIONS


class InterfaceSelectionDialog(QDialog):
    def __init__(self, gateway, language="en"):
        super().__init__()
        self.language = language
        self.translations = TRANSLATIONS
        texts = self.translations[self.language]

        self.gateway = gateway
        self.selected_interface = None
        
        layout = QVBoxLayout(self)
        
        self.combo = QComboBox()
        for interface in gateway.interfaces:
            self.combo.addItem(interface['name'])
            
        layout.addWidget(self.combo)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setWindowTitle(texts["select_interface"])