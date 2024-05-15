import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDockWidget, QMessageBox, QLabel
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices, QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Application_A")
        self.setGeometry(0, 0, 1920, 1080)
        
        # Barre de menu
        menu_bar = self.menuBar()
        menu_fichier = menu_bar.addMenu('&Fichier')
        menu_edition = menu_bar.addMenu('&Edition')
        menu_theme = menu_bar.addMenu('&Thème')
        menu_aide = menu_bar.addMenu('&Aide')
        
        # Options du menu fichier
        menu_fichier.addAction('Nouveau', self.fichier_nouveau)
        menu_fichier.addAction('Ouvrir', self.fichier_ouvrir)
        menu_fichier.addAction('Enregistrer', self.fichier_enregistrer)
        menu_fichier.addSeparator()
        menu_fichier.addAction('Quitter', self.destroy)
        
        # Options du menu thème
        menu_theme.addAction('Thème clair', self.theme1)
        menu_theme.addAction('Thème sombre', self.theme2)
        
        # Dock liste des outils
        self.dock = QDockWidget('Informations')
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)
        self.dock.setMinimumSize(100, 100)
        self.dock.setMaximumSize(500, 500)
        
        self.central_widget = QLabel('Importer un plan', alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.setCentralWidget(self.central_widget)
        font = QFont()
        font.setPointSize(40)
        self.central_widget.setFont(font)
        
        
    # Mettre à jour la vue
    #def updateVue(self, outil: str) -> None:
    
    def fichier_nouveau(self):
        QMessageBox.information(self, "Nouveau", "Développement en cours . . .")

    def fichier_ouvrir(self):
        QMessageBox.information(self, "Ouvrir", "Développement en cours . . .")

    def fichier_enregistrer(self):
        QMessageBox.information(self, "Enregistrer", "Développement en cours . . .")
        
    def fichier_aide(self):
        QDesktopServices.openUrl(QUrl("https://chat.openai.com"))
    
    # Changer le thème
    def theme1(self):
        qss = ""
        self.setStyleSheet(qss)

    def theme2(self):
        fichier_style = open(sys.path[0] + "/fichiers_qss/Diffnes.qss", 'r')
        with fichier_style :
            qss = fichier_style.read()
            self.setStyleSheet(qss)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
