from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QBrush, QPen
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsScene
from computerNode import NodeItem

class Ui_DrawWindow(object):
    def __init__(self):
        self.current_scale = 1.0  # Fator de escala atual
    
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
        
        # Conectando o evento de roda do mouse
        self.graphicsView.setMouseTracking(True)  # Para rastrear movimento do mouse
        self.graphicsView.wheelEvent = self.wheel_event  # Redefinindo o evento de roda do mouse
        
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
        # Obter o centro da área visível do QGraphicsView em coordenadas de cena
        center_view = self.graphicsView.viewport().rect().center()
        center_scene = self.graphicsView.mapToScene(center_view)
        
        # Dados do nó
        node_name = "Computador"  # Nome do nó
        node_ip = "192.168.1.1"    # Endereço IP do nó
        
        # Criar e configurar o círculo como um nó
        node_circle = NodeItem(center_scene.x() - 25, center_scene.y() - 25, 50, node_name, node_ip)
        
        # Adicionar o círculo à cena
        self.scene.addItem(node_circle)

    def wheel_event(self, event):
        # Implementando o zoom com a roda do mouse
        zoom_in_factor = 1.2
        zoom_out_factor = 1 / zoom_in_factor
        
        # Limites de zoom
        min_scale = 0.1  # Fator mínimo de zoom
        max_scale = 4.5  # Fator máximo de zoom
        
        # Verifica a direção da roda do mouse
        if event.angleDelta().y() > 0:  # Rolou para cima
            if self.current_scale < max_scale:  # Verifica se está dentro do limite máximo
                self.graphicsView.scale(zoom_in_factor, zoom_in_factor)
                self.current_scale *= zoom_in_factor  # Atualiza o fator de escala atual
        else:  # Rolou para baixo
            if self.current_scale > min_scale:  # Verifica se está dentro do limite mínimo
                self.graphicsView.scale(zoom_out_factor, zoom_out_factor)
                self.current_scale *= zoom_out_factor  # Atualiza o fator de escala atual

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DrawWindow = QtWidgets.QMainWindow()
    ui = Ui_DrawWindow()
    ui.setupUi(DrawWindow)
    DrawWindow.show()
    sys.exit(app.exec())
