import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDockWidget, QWidget, QLabel, QFileDialog, QDialog, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton, QSpinBox, QGridLayout, QFormLayout, QStatusBar
from PyQt6.QtCore import Qt, QUrl, QSize
from PyQt6.QtGui import QFont, QPixmap, QDesktopServices, QAction, QPen, QPainter, QMouseEvent



# Classe dédié à l'affichage de l'image et du quadrillage
class image(QLabel):
        def __init__(self, chemin: str, taille: QSize, largeur_cases=50, hauteur_cases=50):
            super().__init__()
            self.image = QPixmap(chemin).scaled(taille, Qt.AspectRatioMode.KeepAspectRatio)
            self.setPixmap(self.image)
            self.largeur_case = largeur_cases
            self.hauteur_case = hauteur_cases
            self.dessiner_quadrillage()

            
        def dessiner_quadrillage(self):
            if self.image.isNull():
                return

            pixmap_with_grid = QPixmap(self.image)
            painter = QPainter(pixmap_with_grid)
            painter.setPen(QPen(Qt.GlobalColor.black))

            for x in range(0, pixmap_with_grid.width(), self.largeur_case):
                painter.drawLine(x, 0, x, pixmap_with_grid.height())

            for y in range(0, pixmap_with_grid.height(), self.hauteur_case):
                painter.drawLine(0, y, pixmap_with_grid.width(), y)

            painter.end()
            self.setPixmap(pixmap_with_grid)
            self.setFixedSize(pixmap_with_grid.size())
            
        def set_taille_cases(self, largeur_cases, hauteur_cases):
            self.largeur_case = largeur_cases
            self.hauteur_case = hauteur_cases
            self.dessiner_quadrillage()

        def set_largeur_case(self, largeur):
            self.largeur_case = largeur
            self.dessiner_quadrillage()

        def set_hauteur_case(self, hauteur):
            self.hauteur_case = hauteur
            self.dessiner_quadrillage()

        def mousePressEvent(self, event: QMouseEvent):
            if event.button() == Qt.MouseButton.LeftButton:
                x = event.position().x()
                y = event.position().y()

                case_x = int(x // self.largeur_case)
                case_y = int(y // self.hauteur_case)

                print(f"Clic dans la case: ({case_x}, {case_y})")
                self.window().barre_etat.showMessage(f"Clic dans la case: ({case_x}, {case_y})", 2000)


# Classe principale de l'application
class MainWindow(QMainWindow):
    def __init__(self, controleur):
        super().__init__()
        self.controleur = controleur
        self.setWindowTitle("Gestionnaire de plan")
        
        # Barre de menu
        menu_bar = self.menuBar()
        menu_fichier = menu_bar.addMenu('&Fichier')
        menu_edition = menu_bar.addMenu('&Edition')
        menu_theme = menu_bar.addMenu('&Thème')
        menu_aide = menu_bar.addMenu('&Aide')
        
        # Options du menu fichier
        menu_fichier.addAction('Nouveau', self.controleur.fichier_nouveau)
        menu_fichier.addAction('Ouvrir', self.controleur.fichier_ouvrir)
        menu_fichier.addAction('Enregistrer', self.controleur.fichier_enregistrer)
        menu_fichier.addSeparator()
        menu_fichier.addAction('Quitter', self.close)
        
        # Options du menu thème
        menu_theme.addAction('Thème clair', self.theme1)
        menu_theme.addAction('Thème sombre', self.theme2)
        
        # Options du menu aide
        action_aide = QAction("Documentation", self)
        action_aide.triggered.connect(self.aide)
        menu_aide.addAction(action_aide)
        
        # Dock informations sur le plan
        self.dock = QDockWidget('Informations')
        dock_widget = QWidget()
        self.dock.setWidget(dock_widget)
        dock_layout = QFormLayout(dock_widget)
        dock_widget.setLayout(dock_layout)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)
        self.dock.setMinimumSize(200, 120)
        
        # Zone centrale avec l'image
        self.central_widget = QLabel('Importer un plan', alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.setCentralWidget(self.central_widget)
        font = QFont()
        font.setPointSize(40)
        self.central_widget.setFont(font)
        
        # Barre d'etat situé en bas de l'application
        self.barre_etat = QStatusBar()
        self.setStatusBar(self.barre_etat)
        
        #Afficher l'application en plein écran
        self.showMaximized()
    
    # Changer le thème
    def theme1(self):
        qss = ""
        self.setStyleSheet(qss)

    def theme2(self):
        fichier_style = open(sys.path[0] + "/fichiers_qss/Takezo.qss", 'r')
        with fichier_style :
            qss = fichier_style.read()
            self.setStyleSheet(qss)
            
    def aide(self):
        QDesktopServices.openUrl(QUrl("https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
    
    # Afficher une image sur la partie centrale de l'application
    def afficher_image_central_widget(self, chemin, largeur_cases, hauteur_cases):
        taille_fixe = QSize(self.central_widget.width(), self.central_widget.height())
        self.central_widget = image(chemin, taille_fixe, largeur_cases, hauteur_cases)
        self.central_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.central_widget)
        
    # Mettre à jour la vue avec les informations du plan
    def afficher_informations_plan(self, modele):
        self.vider_dock_informations()
        layoutInfo = self.dock.widget().layout()
        
        layoutInfo.addRow("Nom du projet:", QLabel(modele.nom_projet))
        layoutInfo.addRow("Auteur:", QLabel(modele.auteur))
        layoutInfo.addRow("Date de création:", QLabel(modele.date_creation))
        layoutInfo.addRow("Nom du magasin:", QLabel(modele.nom_magasin))
        layoutInfo.addRow("Adresse du magasin:", QLabel(modele.adresse_magasin))
        if modele.chemin_image:
            largeur_image = self.central_widget.width()
            hauteur_image = self.central_widget.height()
            largeur_cases = largeur_image // modele.largeur_grille
            hauteur_cases = hauteur_image // modele.longueur_grille
            self.afficher_image_central_widget(modele.chemin_image, largeur_cases, hauteur_cases)
            
    # Vider le contenu du dock d'informations
    def vider_dock_informations(self):
        layoutInfoVide = self.dock.widget().layout()
        if layoutInfoVide is not None:
            while layoutInfoVide.count() > 0:
                item = layoutInfoVide.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()            
        
    # Interface s'affichant lors de la création d'un nouveau fichier
    class nv_fichier(QDialog):
        def __init__(self):
            super().__init__()

            self.setWindowTitle("Nouveau fichier")
            self.setFixedSize(500, 300)
            
            intituleNomProjet = QLabel("Nom du fichier : ")
            self.nomProjet = QLineEdit()
            intituleAuteur = QLabel("Nom de l'auteur : ")
            self.nomAuteur = QLineEdit()
            intituleNomMagasin = QLabel("Nom du magasin : ")
            self.nomMagasin = QLineEdit()
            intituleAdresseMagasin = QLabel("Adresse du magasin : ")
            self.adresseMagasin = QLineEdit()
            intituleLargeurGrille = QLabel("Largeur de la grille : ")
            self.largeurGrille = QSpinBox()
            self.largeurGrille.setRange(1, 1000)
            intituleLongueurGrille = QLabel("Longueur de la grille : ")
            self.longueurGrille = QSpinBox()
            self.longueurGrille.setRange(1, 1000)
            intituleProduits = QLabel("Fichier JSON des produits : ")
            self.importerProduits = QPushButton('importer')
            intituleImage = QLabel("Image du plan : ")
            self.importerImage = QPushButton('importer')
            
            self.importerProduits.clicked.connect(self.ouvrir_fichier_produits)
            self.importerImage.clicked.connect(self.ouvrir_fichier_image)
            
            layoutPrincipal = QGridLayout()

            # Ajout des widgets au layout principal
            layoutPrincipal.addWidget(intituleNomProjet, 0, 0)
            layoutPrincipal.addWidget(self.nomProjet, 0, 1)
            
            layoutPrincipal.addWidget(intituleAuteur, 1, 0)
            layoutPrincipal.addWidget(self.nomAuteur, 1, 1)
            
            layoutPrincipal.addWidget(intituleNomMagasin, 2, 0)
            layoutPrincipal.addWidget(self.nomMagasin, 2, 1)
            
            layoutPrincipal.addWidget(intituleAdresseMagasin, 3, 0)
            layoutPrincipal.addWidget(self.adresseMagasin, 3, 1)
            
            layoutPrincipal.addWidget(intituleLongueurGrille, 4, 0)
            layoutPrincipal.addWidget(self.longueurGrille, 4, 1)
            
            layoutPrincipal.addWidget(intituleLargeurGrille, 5, 0)
            layoutPrincipal.addWidget(self.largeurGrille, 5, 1)
            
            layoutPrincipal.addWidget(intituleProduits, 6, 0)
            layoutPrincipal.addWidget(self.importerProduits, 6, 1)
            
            layoutPrincipal.addWidget(intituleImage, 7, 0)
            layoutPrincipal.addWidget(self.importerImage, 7, 1)
            
            validation = QPushButton("Valider")
            validation.setFixedSize(70, 30)
            validation.clicked.connect(self.accept)
            
            validationLayout = QHBoxLayout()
            validationLayout.addStretch(1)
            validationLayout.addWidget(validation)

            layoutComplet = QVBoxLayout()
            layoutComplet.addLayout(layoutPrincipal)
            layoutComplet.addStretch(1)
            layoutComplet.addLayout(validationLayout)
            
            self.setLayout(layoutComplet)
            
            self.fichier_produits = ""
            self.fichier_image = ""
            
        def ouvrir_fichier_produits(self):
            fichier, _ = QFileDialog.getOpenFileName(self, "Choisir un JSON avec les produits", "", "JSON Files (*.json);;All Files (*)")
            if fichier:
                self.fichier_produits = fichier
        
        def ouvrir_fichier_image(self):
            fichier, _ = QFileDialog.getOpenFileName(self, "Choisir une image de plan", "", "Images Files (*.png *.jpg *.jpeg *.gif);;All Files (*)")
            if fichier:
                self.fichier_image = fichier
        
        def get_infos(self):
            return {
                'nom_projet': self.nomProjet.text(),
                'auteur': self.nomAuteur.text(),
                'nom_magasin': self.nomMagasin.text(),
                'adresse_magasin': self.adresseMagasin.text(),
                'largeur_grille': self.largeurGrille.value(),
                'longueur_grille': self.longueurGrille.value(),
                'fichier_produits': self.fichier_produits,
                'chemin_image': self.fichier_image
            }
        
# Main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())