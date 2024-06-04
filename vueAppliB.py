import sys
from PyQt6.QtWidgets import QApplication, QMessageBox, QMainWindow, QDockWidget, QWidget, QLabel, QFileDialog, QDialog, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton, QSpinBox, QGridLayout, QFormLayout, QStatusBar
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QAction, QPixmap
from SelecteurProduit import SelecteurProduit
from CoordonnéesDialog import CoordonneesDialog
from dev_algo import dmd_nb_produit, demande_produit, comparer_produits, dijkstra

class Image(QLabel):
    def __init__(self, chemin: str, taille: QSize, largeur_cases=50, hauteur_cases=50):
        super().__init__()
        self.image = QPixmap(chemin).scaled(taille, Qt.AspectRatioMode.KeepAspectRatio)
        self.setPixmap(self.image)
        self.largeur_case = largeur_cases
        self.hauteur_case = hauteur_cases

class MainWindow(QMainWindow):
    def __init__(self, controleur_instance):
        super().__init__()
        self.setWindowTitle("Gestionnaire de plan")
        self.controleur = controleur_instance
        self.setWindowIcon(QIcon('image/logo.png'))

        menu_bar = self.menuBar()
        menu_fichier = menu_bar.addMenu('&Fichier')
        menu_edition = menu_bar.addMenu('&Edition')
        menu_theme = menu_bar.addMenu('&Thème')
        menu_aide = menu_bar.addMenu('&Aide')

        menu_fichier.addAction('Ouvrir', self.fichier_ouvrir)
        menu_fichier.addAction('Enregistrer', self.fichier_enregistrer)
        menu_fichier.addSeparator()
        menu_fichier.addAction('Quitter', self.close)

        menu_theme.addAction('Thème clair', self.theme1)
        menu_theme.addAction('Thème sombre', self.theme2)

        action_aide = QAction("Documentation", self)
        action_aide.triggered.connect(self.aide)
        menu_aide.addAction(action_aide)

        self.dock = QDockWidget('Informations')
        dock_widget = QWidget()
        self.dock.setWidget(dock_widget)
        dock_layout = QFormLayout(dock_widget)
        dock_widget.setLayout(dock_layout)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)
        self.dock.setMinimumSize(200, 120)

        self.selecteur_produit = SelecteurProduit()
        self.dock.setWidget(self.selecteur_produit)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)

        self.central_widget = QLabel('Importer un plan', alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.setCentralWidget(self.central_widget)
        font = QFont()
        font.setPointSize(40)
        self.central_widget.setFont(font)

        # Ajoutez l'action pour ouvrir la boîte de dialogue des coordonnées de départ
        coord_action = QAction("Coordonnées de départ", self)
        coord_action.triggered.connect(self.open_coord_dialog)
        menu_edition.addAction(coord_action)

        # Ajouter des boutons pour gérer les produits
        bouton_nb_produits = QPushButton("Demander nombre de produits", self)
        bouton_nb_produits.clicked.connect(self.demander_nb_produits)
        dock_layout.addWidget(bouton_nb_produits)

        bouton_demande_produits = QPushButton("Demander produits", self)
        bouton_demande_produits.clicked.connect(self.demander_produits)
        dock_layout.addWidget(bouton_demande_produits)

        bouton_calculer_distances = QPushButton("Calculer distances", self)
        bouton_calculer_distances.clicked.connect(self.calculer_distances)
        dock_layout.addWidget(bouton_calculer_distances)

        self.coordonnees_depart = None  # Valeur par défaut

        self.showMaximized()

    def fichier_ouvrir(self):
        self.vider_dock_informations()
        fichier, _ = QFileDialog.getOpenFileName(self, "Choisir un fichier JSON", "", "JSON Files (*.json);;All Files (*)")
        if fichier:
            self.controleur.ouvrir_plan(fichier)
            self.mise_a_jour_vue()

    def fichier_enregistrer(self):
        fichier, _ = QFileDialog.getSaveFileName(self, "Enregistrer le fichier JSON", "", "JSON Files (*.json);;All Files (*)")
        if fichier:
            self.controleur.enregistrer_plan(fichier)

    def open_coord_dialog(self):
        dialog = CoordonneesDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.coordonnees_depart = dialog.get_coordonnees() 
            QMessageBox.information(self, "Coordonnées de départ", f"Coordonnées saisies : {self.coordonnees_depart}")

    def mise_a_jour_vue(self):
        modele = self.controleur.modele
        layout_info = self.dock.widget().layout()

        layout_info.addRow("Nom du projet:", QLabel(modele.nom_projet))
        layout_info.addRow("Auteur:", QLabel(modele.auteur))
        layout_info.addRow("Date de création:", QLabel(modele.date_creation))
        layout_info.addRow("Nom du magasin:", QLabel(modele.nom_magasin))
        layout_info.addRow("Adresse du magasin:", QLabel(modele.adresse_magasin))

        self.label_largeur_grille = QLabel(str(modele.largeur_grille))
        self.label_longueur_grille = QLabel(str(modele.longueur_grille))
        layout_info.addRow("Nombre de colonne:", self.label_largeur_grille)
        layout_info.addRow("Nombre de ligne:", self.label_longueur_grille)

        if modele.chemin_image:
            largeur_image = self.central_widget.width()
            hauteur_image = self.central_widget.height()
            largeur_cases = largeur_image // modele.largeur_grille
            hauteur_cases = hauteur_image // modele.longueur_grille
            self.afficher_image_central_widget(modele.chemin_image, largeur_cases, hauteur_cases)

        espace = QLabel("")
        espace.setFixedHeight(20)
        layout_info.addRow(espace)

    def theme1(self):
        qss = ""
        self.setStyleSheet(qss)

    def theme2(self):
        fichier_style = open(sys.path[0] + "/fichiers_qss/Takezo.qss", 'r')
        with fichier_style:
            qss = fichier_style.read()
            self.setStyleSheet(qss)

    def vider_dock_informations(self):
        layout_info_vide = self.dock.widget().layout()
        if layout_info_vide is not None:
            while layout_info_vide.count() > 0:
                item = layout_info_vide.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

    def aide(self):
        message_aide = QMessageBox()
        message_aide.setWindowTitle("Aide")
        message_aide.setText(
            "Bienvenue dans le Gestionnaire de Plan !\n\n"
            "Voici quelques instructions pour utiliser l'application :\n\n"
            "1. Nouveau : Créez un nouveau projet en fournissant les informations requises.\n"
            "2. Ouvrir : Ouvrez un projet existant à partir d'un fichier JSON.\n"
            "3. Enregistrer : Enregistrez le projet actuel dans un fichier JSON.\n"
            "4. Thème : Changez le thème de l'application entre clair et sombre.\n\n"
            "Pour plus d'aide, veuillez consulter la documentation ou contacter le support technique."
        )
        message_aide.setIcon(QMessageBox.Icon.Information)
        message_aide.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_aide.exec()

    def demander_nb_produits(self):
        nb_produits = dmd_nb_produit()
        QMessageBox.information(self, "Nombre de produits", f"Nombre de produits : {nb_produits}")
        self.nb_produits = nb_produits

    def demander_produits(self):
        if hasattr(self, 'nb_produits'):
            self.liste_produits = demande_produit(self.nb_produits)
            QMessageBox.information(self, "Liste des produits", f"Produits sélectionnés : {self.liste_produits}")
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez d'abord demander le nombre de produits.")

    def calculer_distances(self):
        if hasattr(self, 'liste_produits') and self.coordonnees_depart:
            distances = dijkstra(self.coordonnees_depart, self.liste_produits)
            QMessageBox.information(self, "Distances", f"Distances calculées : {distances}")
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez d'abord demander les produits et saisir les coordonnées de départ.")

class NvFichier(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Nouveau fichier")
        self.setFixedSize(500, 300)
        
        intitule_nom_projet = QLabel("Nom du fichier : ")
        self.nom_projet = QLineEdit()
        intitule_auteur = QLabel("Nom de l'auteur : ")
        self.nom_auteur = QLineEdit()
        intitule_nom_magasin = QLabel("Nom du magasin : ")
        self.nom_magasin = QLineEdit()
        intitule_adresse_magasin = QLabel("Adresse du magasin : ")
        self.adresse_magasin = QLineEdit()
        intitule_largeur_grille = QLabel("Largeur de la grille : ")
        self.largeur_grille = QSpinBox()
        self.largeur_grille.setRange(1, 1000)
        intitule_longueur_grille = QLabel("Longueur de la grille : ")
        self.longueur_grille = QSpinBox()
        self.longueur_grille.setRange(1, 1000)
        intitule_produits = QLabel("Fichier JSON des produits : ")
        self.importer_produits = QPushButton('importer')
        intitule_image = QLabel("Image du plan : ")
        self.importer_image = QPushButton('importer')
        
        self.importer_produits.clicked.connect(self.ouvrir_fichier_produits)
        self.importer_image.clicked.connect(self.ouvrir_fichier_image)
        
        layout_principal = QGridLayout()

        layout_principal.addWidget(intitule_nom_projet, 0, 0)
        layout_principal.addWidget(self.nom_projet, 0, 1)
        layout_principal.addWidget(intitule_auteur, 1, 0)
        layout_principal.addWidget(self.nom_auteur, 1, 1)
        layout_principal.addWidget(intitule_nom_magasin, 2, 0)
        layout_principal.addWidget(self.nom_magasin, 2, 1)
        layout_principal.addWidget(intitule_adresse_magasin, 3, 0)
        layout_principal.addWidget(self.adresse_magasin, 3, 1)
        layout_principal.addWidget(intitule_largeur_grille, 4, 0)
        layout_principal.addWidget(self.largeur_grille, 4, 1)
        layout_principal.addWidget(intitule_longueur_grille, 5, 0)
        layout_principal.addWidget(self.longueur_grille, 5, 1)
        layout_principal.addWidget(intitule_produits, 6, 0)
        layout_principal.addWidget(self.importer_produits, 6, 1)
        layout_principal.addWidget(intitule_image, 7, 0)
        layout_principal.addWidget(self.importer_image, 7, 1)
        
        validation = QPushButton("Valider")
        validation.setFixedSize(70, 30)
        validation.clicked.connect(self.accept)
        
        validation_layout = QHBoxLayout()
        validation_layout.addStretch(1)
        validation_layout.addWidget(validation)

        layout_complet = QVBoxLayout()
        layout_complet.addLayout(layout_principal)
        layout_complet.addStretch(1)
        layout_complet.addLayout(validation_layout)
        
        self.setLayout(layout_complet)
        
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
            'nom_projet': self.nom_projet.text(),
            'auteur': self.nom_auteur.text(),
            'nom_magasin': self.nom_magasin.text(),
            'adresse_magasin': self.adresse_magasin.text(),
            'largeur_grille': self.largeur_grille.value(),
            'longueur_grille': self.longueur_grille.value(),
            'fichier_produits': self.fichier_produits,
            'chemin_image': self.fichier_image
        }

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(None)  # Remplacez `None` par l'instance de votre contrôleur
    window.show()
    sys.exit(app.exec())
