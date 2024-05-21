import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDockWidget, QMessageBox, QLabel, QFileDialog, QDialog, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton, QSpinBox
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFont, QPixmap, QDesktopServices, QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestionnaire de plan")
        
        # Obtenir la taille de l'écran pour afficher l'application en plein écran correctement
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        self.setGeometry(screen_geometry)
        
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
        
        # Options du menu aide
        action_aide = QAction("Documentation", self)
        action_aide.triggered.connect(self.aide)
        menu_aide.addAction(action_aide)
        
        # Dock informations sur le plan
        self.dock = QDockWidget('Informations')
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)
        self.dock.setMinimumSize(200, 120)
        
        # Zone centrale avec l'image
        self.central_widget = QLabel('Importer un plan', alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.setCentralWidget(self.central_widget)
        font = QFont()
        font.setPointSize(40)
        self.central_widget.setFont(font)
        
        
    # Mettre à jour la vue
    #def updateVue(self, outil: str) -> None:
    
    def fichier_nouveau(self):
        fenetre_dialogue = self.nv_fichier()
        fenetre_dialogue.exec()

    # -----------------------------TEMPORAIRE, SEUL IMAGE POUR L'INSTANT, FICHIER ENTIER PLUS TARD-----------------------------
    # Seul les fichiers en .png, .jpg, .jpeg et .gif sont autorisés
    def fichier_ouvrir(self):
        ouvrir_image = QFileDialog(self)
        ouvrir_image.setNameFilter("Images (*.png *.jpg *.jpeg *.gif)")
        if ouvrir_image.exec():
            chemin = ouvrir_image.selectedFiles()[0]
            self.afficher_image_central_widget(chemin)

    def fichier_enregistrer(self):
        QMessageBox.information(self, "Enregistrer", "Développement en cours . . .")
        
    def fichier_aide(self):
        QMessageBox.information(self, "Enregistrer", "Développement en cours . . .")
    
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
    def afficher_image_central_widget(self, chemin):
        pixmap = QPixmap(chemin)
        self.central_widget.setPixmap(pixmap.scaled(self.central_widget.size(), Qt.AspectRatioMode.KeepAspectRatio))
        self.central_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.central_widget.setText("")
        
        
    # Interface s'affichant lors de la création d'un nouveau fichier
    class nv_fichier(QDialog):
        def __init__(self):
            super().__init__()

            self.setWindowTitle("Nouveau fichier")
            self.setFixedSize(300, 300)
            
            intituleNomProjet = QLabel("Nom du fichier : ")
            nomProjet = QLineEdit()
            intituleAuteur = QLabel("Nom de l'auteur : ")
            nomAuteur = QLineEdit()
            intituleNomMagasin = QLabel("Nom du magasin : ")
            nomMagasin = QLineEdit()
            intituleAdresseMagasin = QLabel("Adresse du magasin : ")
            adresseMagasin = QLineEdit()
            intituleLargeurGrille = QLabel("Largeur de la grille : ")
            largeurGrille = QSpinBox()
            largeurGrille.setRange(1, 1000)
            intituleLongueurGrille = QLabel("Longueur de la grille : ")
            longueurGrille = QSpinBox()
            longueurGrille.setRange(1, 1000)
            intituleProduits = QLabel("Fichier JSON des produits : ")
            importerProduits = QPushButton('importer')
            intituleImage = QLabel("Image du plan : ")
            importerImage = QPushButton('importer')
            
            
            # RECUPERER DATE AUTOMATIQUEMENT
            
            layoutNomProjet = QHBoxLayout()
            layoutNomProjet.addWidget(intituleNomProjet)
            layoutNomProjet.addWidget(nomProjet)
            
            layoutAuteur = QHBoxLayout()
            layoutAuteur.addWidget(intituleAuteur)
            layoutAuteur.addWidget(nomAuteur)
            
            layoutNomMagasin = QHBoxLayout()
            layoutNomMagasin.addWidget(intituleNomMagasin)
            layoutNomMagasin.addWidget(nomMagasin)
            
            layoutAddMagasin = QHBoxLayout()
            layoutAddMagasin.addWidget(intituleAdresseMagasin)
            layoutAddMagasin.addWidget(adresseMagasin)
            
            layoutLargeurGrille = QHBoxLayout()
            layoutLargeurGrille.addWidget(intituleLargeurGrille)
            layoutLargeurGrille.addWidget(largeurGrille)
            
            layoutLongueurGrille = QHBoxLayout()
            layoutLongueurGrille.addWidget(intituleLongueurGrille)
            layoutLongueurGrille.addWidget(longueurGrille)
            
            layoutProduit = QHBoxLayout()
            layoutProduit.addWidget(intituleProduits)
            layoutProduit.addStretch(1)
            layoutProduit.addWidget(importerProduits)
            
            layoutImage = QHBoxLayout()
            layoutImage.addWidget(intituleImage)
            layoutImage.addStretch(1)
            layoutImage.addWidget(importerImage)
    
            validation = QPushButton("Valider")
            validation.setFixedSize(70, 30)
            validationLayout = QHBoxLayout()
            validationLayout.addStretch(1)
            validationLayout.addWidget(validation)
    
            layoutPrincipale = QVBoxLayout()
            layoutPrincipale.addLayout(layoutNomProjet)
            layoutPrincipale.addLayout(layoutAuteur)
            layoutPrincipale.addLayout(layoutNomMagasin)
            layoutPrincipale.addLayout(layoutAddMagasin)
            layoutPrincipale.addLayout(layoutLongueurGrille)
            layoutPrincipale.addLayout(layoutLargeurGrille)
            layoutPrincipale.addLayout(layoutProduit)
            layoutPrincipale.addLayout(layoutImage)
            layoutPrincipale.addLayout(validationLayout)
            
            self.setLayout(layoutPrincipale)
        
        
# Main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())