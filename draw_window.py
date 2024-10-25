from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QBrush, QPen
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsScene

class Ui_DrawWindow(object):
    def setupUi(self, DrawWindow):
        DrawWindow.setObjectName("DrawWindow")
        DrawWindow.resize(631, 439)
        self.centralwidget = QtWidgets.QWidget(parent=DrawWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Botão "Circulo"
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(0, 0, 75, 24))
        self.pushButton.setObjectName("pushButton")
        
        # QGraphicsView para exibir os círculos
        self.graphicsView = QtWidgets.QGraphicsView(parent=self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 30, 631, 391))
        self.graphicsView.setObjectName("graphicsView")
        
        # Adicionando cena gráfica à QGraphicsView
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        
        # Conectando o botão à função para adicionar círculos
        self.pushButton.clicked.connect(self.add_circle)
        
        DrawWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=DrawWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 631, 22))
        self.menubar.setDefaultUp(False)
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        self.menuTeste = QtWidgets.QMenu(parent=self.menubar)
        self.menuTeste.setObjectName("menuTeste")
        DrawWindow.setMenuBar(self.menubar)
        self.menubar.addAction(self.menuTeste.menuAction())

        self.retranslateUi(DrawWindow)
        QtCore.QMetaObject.connectSlotsByName(DrawWindow)

    def retranslateUi(self, DrawWindow):
        _translate = QtCore.QCoreApplication.translate
        DrawWindow.setWindowTitle(_translate("DrawWindow", "Draw Window"))
        self.pushButton.setText(_translate("DrawWindow", "Circulo"))
        self.menuTeste.setTitle(_translate("DrawWindow", "Teste"))
    
    def add_circle(self):
        # Criando e configurando o círculo
        circle = QGraphicsEllipseItem(0, 0, 50, 50)  # Definindo um círculo de 50x50
        circle.setBrush(QBrush(Qt.GlobalColor.red))  # Cor do círculo
        circle.setPen(QPen(Qt.GlobalColor.black))    # Cor da borda
        circle.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsMovable)  # Permite mover o círculo
        
        # Adicionando o círculo à cena
        self.scene.addItem(circle)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DrawWindow = QtWidgets.QMainWindow()
    ui = Ui_DrawWindow()
    ui.setupUi(DrawWindow)
    DrawWindow.show()
    sys.exit(app.exec())
