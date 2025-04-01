from PyQt6.QtWidgets import QVBoxLayout, QDialog, QComboBox, QDialogButtonBox, QFrame, QLabel

from prog.nodes import MovableRect
from prog.translations import TRANSLATIONS


class InterfaceSelectionDialog(QDialog):
    def __init__(self, gateway1, gateway2=None, language="en"):
        super().__init__()
        self.language = language
        self.translations = TRANSLATIONS
        texts = self.translations[self.language]
        self.gateway1 = gateway1
        self.gateway2 = gateway2
        self.selected_interface1 = None
        self.selected_interface2 = None
        
        layout = QVBoxLayout(self)
        
        # Interface selection for the first gateway
        gateway1_label = QLabel(texts["select_interface"] + " " + (getattr(gateway1, 'name', '') or texts["device"] + " " + texts["up"]))
        layout.addWidget(gateway1_label)
        
        self.combo1 = QComboBox()
        for interface in gateway1.interfaces:
            self.combo1.addItem(interface['name'])
        layout.addWidget(self.combo1)
        
        # Interface selection for the second gateway (if provided)
        if gateway2 and isinstance(gateway2, MovableRect):
            # Add a separator
            layout.addSpacing(10)
            separator = QFrame()
            separator.setFrameShape(QFrame.Shape.HLine)
            separator.setFrameShadow(QFrame.Shadow.Sunken)
            layout.addWidget(separator)
            layout.addSpacing(10)
            
            # Add interface selection for gateway2
            gateway2_label = QLabel(texts["select_interface"] + " " + (getattr(gateway2, 'name', '') or texts["device"] + " " + texts["down"]))
            layout.addWidget(gateway2_label)
            
            self.combo2 = QComboBox()
            for interface in gateway2.interfaces:
                self.combo2.addItem(interface['name'])
            layout.addWidget(self.combo2)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setWindowTitle(texts["select_interfaces"] if gateway2 else texts["select_interface"])
    
    def get_selected_interfaces(self):
        interface1 = self.combo1.currentText()
        interface2 = self.combo2.currentText() if hasattr(self, 'combo2') else None
        return interface1, interface2