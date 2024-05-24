import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStatusBar, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QSpinBox, QPushButton
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QPen , QMouseEvent
from PyQt6.QtCore import Qt, QSize


# --- class widget: hérite de QLabel ------------------------------------------
class Image(QLabel):

    def __init__(self, chemin: str):
        '''Constructeur de la classe'''
        super().__init__() 
        
        self.image = QPixmap(chemin)
        self.setPixmap(self.image)
        self.largeur_case = 50
        self.hauteur_case = 50

    def dessiner_quadrillage(self):
        if self.image.isNull():
            return
        
        # Crée un nouveau QPixmap basé sur l'image originale
        pixmap_with_grid = QPixmap(self.image)
        painter = QPainter(pixmap_with_grid)
        painter.setPen(QPen(Qt.GlobalColor.black))

        # Dessine les lignes verticales
        for x in range(0, pixmap_with_grid.width(), self.largeur_case):
            painter.drawLine(x, 0, x, pixmap_with_grid.height())

        # Dessine les lignes horizontales
        for y in range(0, pixmap_with_grid.height(), self.hauteur_case):
            painter.drawLine(0, y, pixmap_with_grid.width(), y)

        painter.end()
        
        # Met à jour l'image avec le quadrillage
        self.setPixmap(pixmap_with_grid)
        self.setFixedSize(pixmap_with_grid.size())

    def set_largeur_case(self, largeur):
        self.largeur_case = largeur
        self.dessiner_quadrillage()

    def set_hauteur_case(self, hauteur):
        self.hauteur_case = hauteur
        self.dessiner_quadrillage()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            # Position du clic relatif à l'image
            x = event.position().x()
            y = event.position().y()

            # Calcul de la case cliquée
            case_x = int(x // self.largeur_case)
            case_y = int(y // self.hauteur_case)

            print(f"Clic dans la case: ({case_x}, {case_y})")
            self.window().barre_etat.showMessage(f"Clic dans la case: ({case_x}, {case_y})", 2000)

    def rajouter_produits(self,coord_x:int,coord_y:int):
        appli=QWidget()
        label_coord=QLabel("("+ coord_x + "," +coord_y + ")")
        label_coord
        layout_bouton=QHBoxLayout()
        ok=QPushButton("Ok")
        annuler=QPushButton("Annuler")
        layout_bouton.addWidget(ok)
        layout_bouton.addWidget(annuler)




# -----------------------------------------------------------------------------
# --- class FenetreAppli
# -----------------------------------------------------------------------------
class FenetreAppli(QMainWindow):
    def __init__(self, chemin: str = None):
        super().__init__()
        self.__chemin = chemin
        
        self.setWindowTitle("Votre première application à l'IUT")
        self.setWindowIcon(QIcon(sys.path[0] + '/icones/logo_but.png'))
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        self.setGeometry(screen_geometry)
        
        # barre d'état
        self.barre_etat = QStatusBar()
        self.setStatusBar(self.barre_etat)
        self.barre_etat.showMessage("L'application est démarrée...", 2000)

        # barre de menu
        menu_bar = self.menuBar()

        menu_fichier = menu_bar.addMenu('&Fichier')
        menu_edition = menu_bar.addMenu('&Edition')
        menu_aide = menu_bar.addMenu('&Aide')

        menu_fichier.addAction('Nouveau', self.nouveau)
        menu_fichier.addAction('Ouvrir', self.ouvrir)
        menu_fichier.addAction('Enregistrer', self.enregistrer)
        menu_fichier.addSeparator()
        menu_fichier.addAction('Quitter', self.destroy)

        # Ajoute les contrôles pour ajuster la taille des cellules du quadrillage
        self.control_widget = QWidget()
        self.setCentralWidget(self.control_widget)
        self.layout = QVBoxLayout()
        self.control_widget.setLayout(self.layout)

        self.image = None

        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        self.setGeometry(screen_geometry)

        self.show()

    def nouveau(self):
        self.barre_etat.showMessage('Créer un nouveau ....', 2000)
        boite = QFileDialog()
        chemin, validation = boite.getOpenFileName(directory=sys.path[0])
        if validation:
            self.__chemin = chemin

    def ouvrir(self):
        self.barre_etat.showMessage('Ouvrir un nouveau....', 2000)
        boite = QFileDialog()
        chemin, validation = boite.getOpenFileName(directory=sys.path[0])
        if self.image:
            self.layout.removeWidget(self.image)
            self.image.deleteLater()
            self.image = None
        if validation:
            self.__chemin = chemin
            self.affiche_image()
        
    def enregistrer(self):
        self.barre_etat.showMessage('Enregistrer....', 2000)
        boite = QFileDialog()
        chemin, validation = boite.getSaveFileName(directory=sys.path[0])
        if validation:
            self.__chemin = chemin
        
    def affiche_image(self):
        self.image = Image(self.__chemin)
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.image)
        self.image.dessiner_quadrillage()



# --- main --------------------------------------------------------------------
if __name__ == "__main__":

    # création d'une QApplication
    app = QApplication(sys.argv)
    
    fenetre = FenetreAppli(sys.path[0])

    # lancement de l'application
    sys.exit(app.exec())
