import sys
from PyQt6.QtWidgets import QApplication, QMessageBox,QInputDialog ,QMainWindow, QDockWidget, QWidget, QLabel, QFileDialog, QDialog, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton, QSpinBox, QGridLayout, QFormLayout, QStatusBar, QListWidget, QCheckBox, QGroupBox, QScrollArea
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap, QIcon, QAction
from SelecteurProduit import SelecteurProduit
from dev_algo import *
import json

# Classe dédiée à l'affichage de l'image et du quadrillage
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
        menu_outils = menu_bar.addMenu('&Outils')
        menu_theme = menu_bar.addMenu('&Thème')
        menu_aide = menu_bar.addMenu('&Aide')

        menu_fichier.addAction('Ouvrir', self.fichier_ouvrir)
        menu_fichier.addSeparator()
        menu_fichier.addAction('Quitter', self.close)

        menu_theme.addAction('Thème clair', self.theme1)
        menu_theme.addAction('Thème sombre', self.theme2)

        action_aide = QAction("Documentation", self)
        action_aide.triggered.connect(self.aide)
        menu_aide.addAction(action_aide)

        self.dock = QDockWidget()
        self.dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetVerticalTitleBar)
        self.dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        dock_widget = QWidget()
        dock_layout = QVBoxLayout()  # Utilisez un QVBoxLayout pour organiser les widgets verticalement
        dock_widget.setLayout(dock_layout)
        self.dock.setWidget(dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)

        # Ajoutez d'abord le sélecteur de produits au layout du dock widget
        self.selecteur_produit = SelecteurProduit()
        dock_layout.addWidget(self.selecteur_produit)

        # Ajoutez ensuite le bouton "Envoyer"
        bouton_envoyer = QPushButton("Envoyer")
        dock_layout.addWidget(bouton_envoyer)

        bouton_envoyer.clicked.connect(self.selecteur_produit.afficher_produits_selectionnes)

        self.central_widget = QLabel('Importer un plan', alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.setCentralWidget(self.central_widget)
        font = QFont()
        font.setPointSize(40)
        self.central_widget.setFont(font)

        coord_action = QAction("Coordonnées de départ", self)
        coord_action.triggered.connect(self.demander_coordonnees_depart)
        menu_outils.addAction(coord_action)

        coord_caisse = QAction("Coordonnées de la caisse", self)
        coord_caisse.triggered.connect(self.demander_coordonnees_caisse)
        menu_outils.addAction(coord_caisse)

        algo_action = QAction("Utiliser l'algorithme de Dijkstra", self)
        algo_action.triggered.connect(self.dijkstra_dialog)
        menu_outils.addAction(algo_action)

        self.barre_etat = QStatusBar()
        self.setStatusBar(self.barre_etat)

        bouton_coordonnees = QPushButton("Coordonnées de départ", self)
        bouton_coordonnees.clicked.connect(self.demander_coordonnees_depart)
        dock_layout.addWidget(bouton_coordonnees)

        bouton_coordonnees_caisse = QPushButton("Coordonnées de la caisse", self)
        bouton_coordonnees_caisse.clicked.connect(self.demander_coordonnees_depart)
        dock_layout.addWidget(bouton_coordonnees_caisse)

        self.coordonnees_depart = (0, 0)

        self.label_largeur_grille = QLabel()
        self.label_longueur_grille = QLabel()

        self.showMaximized()

    def fichier_ouvrir(self):
        self.vider_dock_informations()
        fichier, _ = QFileDialog.getOpenFileName(self, "Choisir un fichier JSON", "", "JSON Files (*.json);;All Files (*)")
        if fichier:
            with open(fichier, 'r') as f:
                data = json.load(f)
                self.mise_a_jour_vue(data)
                self.selecteur_produit.charger_donnees_depuis_fichier(fichier)
                self.dock.setFeatures(QDockWidget.NoDockWidgetFeatures)

    def demander_coordonnees_caisse(self):
        coord, ok = QInputDialog.getText(self, "Coordonnées de la caisse", "Entrez les coordonnées de départ (x, y):")
        if ok:
            try:
                x, y = map(int, coord.split(','))
                self.coordonnees_depart = (x, y)
                QMessageBox.information(self, "Coordonnées de la caise", f"Coordonnées de la caisse : {self.coordonnees_depart}")
            except ValueError:
                QMessageBox.warning(self, "Erreur", "Coordonnées invalides, veuillez entrer des valeurs numériques séparées par une virgule.")

    def mise_a_jour_vue(self, data):
        chemin_image = data.get("chemin_image", "")
        if chemin_image:
            self.afficher_image_central_widget(chemin_image)

    def afficher_image_central_widget(self, chemin_image):
        largeur_image = self.central_widget.width()
        hauteur_image = self.central_widget.height()
        largeur_cases = largeur_image // 10  # Placeholder values
        hauteur_cases = hauteur_image // 10  # Placeholder values
        image_label = Image(chemin_image, QSize(largeur_image, hauteur_image), largeur_cases, hauteur_cases)
        self.setCentralWidget(image_label)

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
            ". Enregistrer : Enregistrez le projet actuel dans un fichier JSON.\n"
            "3. Thème : Changez le thème de l'application entre clair et sombre.\n\n"
            "Pour plus d'aide, veuillez consulter la documentation ou contacter le support technique."
        )
        message_aide.setIcon(QMessageBox.Icon.Information)
        message_aide.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_aide.exec()

    def demander_coordonnees_depart(self):
        coord, ok = QInputDialog.getText(self, "Coordonnées de départ", "Entrez les coordonnées de départ (x, y):")
        if ok:
            try:
                x, y = map(int, coord.split(','))
                self.coordonnees_depart = (x, y)
                QMessageBox.information(self, "Coordonnées de départ", f"Coordonnées de départ : {self.coordonnees_depart}")
            except ValueError:
                QMessageBox.warning(self, "Erreur", "Coordonnées invalides, veuillez entrer des valeurs numériques séparées par une virgule.")

    def dijkstra_dialog(self):
        reply = QMessageBox.question(self, 'Utiliser l\'algorithme de Dijkstra',
                                     "Voulez-vous utiliser l'algorithme de Dijkstra pour déterminer le chemin le plus court ?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            # Appeler la fonction pour utiliser l'algorithme de Dijkstra ici
            self.utiliser_djiskstra()
        else:
            print("Algorithme de Dijkstra désactivé")

    def utiliser_djiskstra(self):
        graphe = self.construire_graphe_depuis_donnees()
        coord_depart = self.coordonnees_depart
        dict_produits_avec_coos = self.selecteur_produit.creer_dictionnaire_produits_avec_coos()

        coords_produits_selectionnes = list(dict_produits_avec_coos.values())

        chemins, distances = dijkstra(graphe, coord_depart, coords_produits_selectionnes)
        self.afficher_chemins(chemins, distances)

    def construire_graphe_depuis_donnees(self):
            data = self.charger_donnees_graphe('graphe_donnees.json')

            graphe = {}

            # Initialiser les noeuds dans le graphe
            for noeud in data["noeuds"]:
                graphe[noeud] = []

            # Ajouter les arêtes avec les poids dans le graphe
            for arete in data["aretes"]:
                de = arete["de"]
                vers = arete["vers"]
                poids = arete["poids"]
                graphe[de].append((vers, poids))
                graphe[vers].append((de, poids))  # Si le graphe est non dirigé

            return graphe

    def afficher_chemins(self, chemins, distances):
        # Méthode pour afficher ou traiter les chemins et les distances
        print("Chemins:", chemins)
        print("Distances:", distances)

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
        self.importer_produits = QPushButton('Importer')
        intitule_image = QLabel("Image du plan : ")
        self.importer_image = QPushButton('Importer')
        
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

        # Ajout du bouton envoyer
        envoyer = QPushButton("Envoyer")
        envoyer.setFixedSize(70, 30)
        envoyer.clicked.connect(self.envoyer_infos)
        layout_principal.addWidget(envoyer, 8, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        
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

    def envoyer_infos(self):
        infos = self.get_infos()
        # Ajoutez ici la logique pour envoyer les infos où vous le souhaitez
        print("Informations envoyées :", infos)
    
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

class ListeProduitsWindow(QDialog):
    def __init__(self, liste_produits):
        super().__init__()
        self.setWindowTitle("Liste des Produits à Récupérer")
        layout = QVBoxLayout()
        self.liste_widget = QListWidget()
        
        # Extraire les noms des produits à partir des tuples
        noms_produits = [produit for produit, _ in liste_produits]
        
        self.liste_widget.addItems(noms_produits)
        layout.addWidget(self.liste_widget)
        bouton_fermer = QPushButton("Fermer")
        bouton_fermer.clicked.connect(self.close)
        layout.addWidget(bouton_fermer)
        self.setLayout(layout)

# Main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(None)  # Remplacez `None` par l'instance de votre contrôleur
    window.show()
    sys.exit(app.exec())

