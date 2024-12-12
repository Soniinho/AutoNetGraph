import sys
import os

# Caminho relativo para a pasta do VirtualBox SDK
sdk_path = os.path.join(os.path.dirname(__file__), 'sdk/bindings/xpcom/python')
sys.path.append(sdk_path)
import vboxapi

from PyQt6 import QtCore, QtGui, QtWidgets

from interface import Ui_DrawInterface  # Importe a nova janela

class Ui_MainWindow(object):
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
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignJustify|QtCore.Qt.AlignmentFlag.AlignVCenter)
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
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Array de máquinas virtuais
        mgr = vboxapi.VirtualBoxManager(None, None)
        vbox = mgr.getVirtualBox()
        self.vm_names = [m.name for m in mgr.getArray(vbox, 'machines')]
        self.populate_list_widget()

        # Conectar o botão ao método
        self.button_select.clicked.connect(self.select_vm)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Seleção de Máquina Virtual"))
        self.label.setText(_translate("MainWindow", "Selecione a máquina virtual original, ela será o template de cópia para gerar as máquinas da rede."))
        self.button_select.setText(_translate("MainWindow", "Selecionar Máquina"))

    def populate_list_widget(self):
        """Preenche o QListWidget com os nomes das máquinas virtuais."""
        self.listWidget_VM.addItems(self.vm_names)

    def select_vm(self):
        """Captura a máquina virtual selecionada e troca o conteúdo da janela."""
        selected_items = self.listWidget_VM.selectedItems()
        if selected_items:
            selected_vm = selected_items[0].text()  # Obtém o texto do primeiro item selecionado
            print(f"Máquina virtual selecionada: {selected_vm}")
            self.selected_vm_name = selected_vm  # Grava o nome em uma variável

            # Instanciar e carregar a nova janela na mesma MainWindow
            self.ui_second = Ui_DrawInterface(selected_vm)
            self.ui_second.setupUi(MainWindow)  # Reaproveita a janela principal
        else:
            print("Nenhuma máquina virtual selecionada.")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
