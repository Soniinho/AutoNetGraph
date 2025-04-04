from PyQt6 import QtCore, QtGui, QtWidgets
from view.visual_interface import Ui_DrawInterface  # Import the second interface
# import virtualbox

# TODO: mudar projeto para MVC e design patterns
class Ui_MainWindow(object):
    def __init__(self):
        self.language = "br"  # Default language is Portuguese
        self.translations = {
            "br": {
                "title": "Seleção de Máquina Virtual",
                "label": "Selecione a máquina virtual original, ela será o template de cópia para gerar as máquinas da rede.",
                "select_button": "Selecionar Máquina",
                "language_label": "Idioma:",
            },
            "en": {
                "title": "Virtual Machine Selection",
                "label": "Select the original virtual machine, which will serve as the copy template to generate the network machines.",
                "select_button": "Select Machine",
                "language_label": "Language:",
            },
        }

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(518, 469)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignJustify | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.listWidget_VM = QtWidgets.QListWidget(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.listWidget_VM.setFont(font)
        self.listWidget_VM.setObjectName("listWidget_VM")
        self.verticalLayout.addWidget(self.listWidget_VM)
        self.button_select = QtWidgets.QPushButton(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.button_select.setFont(font)
        self.button_select.setObjectName("button_select")
        self.verticalLayout.addWidget(self.button_select)

        # Language Selection Dropdown
        language_layout = QtWidgets.QHBoxLayout()
        self.language_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.language_label.setFont(font)
        language_layout.addWidget(self.language_label)

        self.language_dropdown = QtWidgets.QComboBox(parent=self.centralwidget)
        self.language_dropdown.setFont(font)
        self.language_dropdown.addItems(["Português Brasil", "English"])  # Add language options
        self.language_dropdown.setObjectName("language_dropdown")
        language_layout.addWidget(self.language_dropdown)
        self.verticalLayout.addLayout(language_layout)

        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Array of virtual machines
        # vbox = virtualbox.VirtualBox()
        # self.vm_names = [m.name for m in vbox.machines]
        self.vm_names = ["VM1", "VM2"]
        self.populate_list_widget()

        # Connect buttons and dropdown to methods
        self.button_select.clicked.connect(self.select_vm)
        self.language_dropdown.currentIndexChanged.connect(self.change_language)

    def retranslateUi(self, MainWindow):
        """Update UI text based on the selected language."""
        texts = self.translations[self.language]
        MainWindow.setWindowTitle(texts["title"])
        self.label.setText(texts["label"])
        self.button_select.setText(texts["select_button"])
        self.language_label.setText(texts["language_label"])

    def populate_list_widget(self):
        """Fill the QListWidget with virtual machine names."""
        self.listWidget_VM.addItems(self.vm_names)

    def select_vm(self):
        """Capture the selected virtual machine and switch to the next interface."""
        selected_items = self.listWidget_VM.selectedItems()
        if selected_items:
            selected_vm = selected_items[0].text()
            print(f"Selected virtual machine: {selected_vm}")
            self.selected_vm_name = selected_vm

            # Instantiate and load the new window in the same MainWindow
            self.ui_second = Ui_DrawInterface(selected_vm, self.language)
            self.ui_second.setupUi(MainWindow)  # Reuse the main window

            # Center the MainWindow on the screen
            screen_geometry = QtWidgets.QApplication.primaryScreen().geometry()
            window_geometry = MainWindow.geometry()
            x = (screen_geometry.width() - window_geometry.width()) // 2
            y = (screen_geometry.height() - window_geometry.height()) // 2
            MainWindow.move(x, y - 40) # 40 for the bar
        else:
            print("No virtual machine selected.")

    def change_language(self):
        """Change the language based on the dropdown selection."""
        index = self.language_dropdown.currentIndex()
        self.language = "pt" if index == 0 else "en"
        self.retranslateUi(MainWindow)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    """ 
    # Center the MainWindow on the screen
    screen_geometry = app.primaryScreen().geometry()
    window_geometry = MainWindow.geometry()
    x = (screen_geometry.width() - window_geometry.width()) // 2
    y = (screen_geometry.height() - window_geometry.height()) // 2
    MainWindow.move(x, y)
    """

    sys.exit(app.exec())
