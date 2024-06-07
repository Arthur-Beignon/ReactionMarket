import sys
from PyQt6.QtWidgets import QApplication, QDialog, QLineEdit, QFileDialog, QDockWidget, QInputDialog, QMessageBox, QVBoxLayout, QSpinBox, QHBoxLayout, QPushButton, QLabel, QMainWindow, QWidget, QGridLayout, QStatusBar, QListWidget
from PyQt6.QtGui import QIcon, QPixmap, QFont, QAction, QPainter, QPen
from PyQt6.QtCore import Qt
import json
import heapq
from SelecteurProduit import SelecteurProduit
from CoordonnéesDialog import CoordonneesDialog
from dev_algo import *
import json

class MainWindow(QMainWindow):
    def __init__(self, controleur_instance):
        super().__init__()
        self.setWindowTitle("ReactionMarket : Gagne du temps !")
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
        self.dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        dock_widget = QWidget()
        self.dock_layout = QVBoxLayout()
        dock_widget.setLayout(self.dock_layout)
        self.dock.setWidget(dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)
        self.dock.setFixedSize(300, self.height())

        self.selecteur_produit = SelecteurProduit()
        self.dock_layout.addWidget(self.selecteur_produit)

        self.central_widget = QLabel('Importer un plan', alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.central_widget.setScaledContents(True)  # Permet le redimensionnement automatique
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
        bouton_coordonnees.setFixedSize(200, 30)
        bouton_coordonnees.clicked.connect(self.demander_coordonnees_depart)
        self.dock_layout.addWidget(bouton_coordonnees)

        bouton_coordonnees_caisse = QPushButton("Coordonnées de la caisse", self)
        bouton_coordonnees_caisse.setFixedSize(200, 30)
        bouton_coordonnees_caisse.clicked.connect(self.demander_coordonnees_caisse)
        self.dock_layout.addWidget(bouton_coordonnees_caisse)

        bouton_coordonnees_caisse = QPushButton("Coordonnées de la caisse", self)
        bouton_coordonnees_caisse.setFixedSize(200, 30)
        bouton_coordonnees_caisse.clicked.connect(self.demander_coordonnees_caisse)
        self.dock_layout.addWidget(bouton_coordonnees_caisse)

        # Charger les données depuis le fichier JSON
        with open("jsonType.json", "r") as f:
            data = json.load(f)

        # Extraire les coordonnées des produits
        produit_coos = data["produit_coos"]

        # Initialiser le dictionnaire de coordonnées des produits
        self.coordonnees_produits = {}

        # Parcourir les catégories de produits
        for categorie, produits in produit_coos.items():
            # Parcourir les produits dans chaque catégorie
            for produit, coordonnees in produits.items():
                # Ajouter les coordonnées du produit au dictionnaire
                self.coordonnees_produits[produit] = coordonnees

        bouton_envoie = QPushButton("OK", self)
        bouton_envoie.setFixedSize(200, 30)
        bouton_envoie.clicked.connect(self.envoyerchemin)
        self.dock_layout.addWidget(bouton_envoie)

        self.coordonnees_depart = [0, 0]
        self.coordonnees_caisse = [0, 0]

        self.label_largeur_grille = QLabel()
        self.label_longueur_grille = QLabel()

        self.showMaximized()

    def fichier_ouvrir(self):
        fichier, _ = QFileDialog.getOpenFileName(self, "Choisir un fichier JSON", "", "JSON Files (*.json);;All Files (*)")
        if fichier:
            with open(fichier, 'r') as f:
                data = json.load(f)
                self.mise_a_jour_vue(data)
                self.__grille=data.get("grille","")
                self.__grille_largeur=self.__grille.get("largeur", "")
                self.__grille_longueur=self.__grille.get("longueur", "")
                self.selecteur_produit.charger_donnees_depuis_fichier(fichier)

    def demander_coordonnees_caisse(self):
        coord, ok = QInputDialog.getText(self, "Coordonnées de la caisse", "Entrez les coordonnées de la caisse (x, y):")
        if ok:
            try:
                x, y = map(int, coord.split(','))
                self.coordonnees_caisse = (x, y)
                QMessageBox.information(self, "Coordonnées de la caisse", f"Coordonnées de la caisse : {self.coordonnees_caisse}")
            except ValueError:
                QMessageBox.warning(self, "Erreur", "Coordonnées invalides, veuillez entrer des valeurs numériques séparées par une virgule.")

    def mise_a_jour_vue(self, data):
        chemin_image = data.get("chemin_image", "")
        if chemin_image:
            self.afficher_image_central_widget(chemin_image)

    def afficher_image_central_widget(self, chemin_image):
        self.__pixmap = QPixmap(chemin_image)
        self.central_widget.setPixmap(self.__pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio))  # Redimensionnement pour occuper tout l'espace disponible

    def theme1(self):
        qss = ""
        self.setStyleSheet(qss)

    def theme2(self):
        fichier_style = open(sys.path[0] + "/fichiers_qss/Takezo.qss", 'r')
        with fichier_style:
            qss = fichier_style.read()
            self.setStyleSheet(qss)

    def aide(self):
        message_aide = QMessageBox()
        message_aide.setWindowTitle("Aide")
        message_aide.setText(
            "Bienvenue dans le Gestionnaire de Plan !\n\n"
            "Voici quelques instructions pour utiliser l'application :\n\n"
            "1. Nouveau : Créez un nouveau projet en fournissant les informations requises.\n"
            "2. Ouvrir : Ouvrez un projet existant à partir d'un fichier JSON.\n"
            "3. Thème : Changez le thème de l'application entre clair et sombre.\n\n"
            "Pour plus d'aide, veuillez consulter la documentation ou contacter le support technique")
        message_aide.setIcon(QMessageBox.Icon.Information)
        message_aide.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_aide.exec()

    def demander_coordonnees_depart(self):
        coord, ok = QInputDialog.getText(self, "Coordonnées de départ", "Entrez les coordonnées de départ (x, y):")
        if ok:
            try:
                x, y = map(int, coord.split(','))
                self.coordonnees_depart = [x, y]
                QMessageBox.information(self, "Coordonnées de départ", f"Coordonnées de départ : {self.coordonnees_depart}")
            except ValueError:
                QMessageBox.warning(self, "Erreur", "Coordonnées invalides, veuillez entrer des valeurs numériques séparées par une virgule.")

    def dijkstra_dialog(self):
        reply = QMessageBox.question(self, 'Utiliser l\'algorithme de Dijkstra',
                                     "Voulez-vous utiliser l'algorithme de Dijkstra pour déterminer le chemin le plus court ?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.dijsktra()
        else:
            print("Algorithme de Dijkstra désactivé")

    def envoyerchemin(self):
        coordonnees_produits = self.selecteur_produit.creer_dictionnaire_produits_avec_coos()
        liste = [self.coordonnees_depart]  # Ajouter les coordonnées de départ
        for produit in coordonnees_produits.keys():
            if produit in self.coordonnees_produits:
                liste.append(self.coordonnees_produits[produit])
        liste.append(self.coordonnees_caisse)  # Ajouter les coordonnées de la caisse

        self.trace_ligne(liste)

    def trace_ligne(self, points):
        if self.__pixmap:
            pixmap = self.__pixmap.copy()
            painter = QPainter(pixmap)
            pen = QPen(Qt.GlobalColor.black, 3)
            painter.setPen(pen)
            height=pixmap.size().height()
            width=pixmap.size().width()

            for i in range(len(points) - 1):
                start_point = points[i]
                end_point = points[i + 1] 
                start_point = (start_point[0] * int(width/int(self.__grille_largeur))+ int(width/int((self.__grille_largeur/2))), start_point[1] * int(height/int(self.__grille_longueur)) + int(height/int((self.__grille_longueur/2))))
                end_point = (end_point[0] * int(width/int(self.__grille_largeur)) + int(width/int((self.__grille_largeur/2))), end_point[1] * int(height/int(self.__grille_longueur)) + int(height/int((self.__grille_longueur/2))))
                painter.drawLine(start_point[0], start_point[1], end_point[0], end_point[1])
                print(start_point)
                print(end_point)

            painter.end()
            self.central_widget.setPixmap(pixmap)

    def parcours(dico_graphe: dict, depart: tuple, arrivee: tuple) -> list:
        '''La fonction explore le labyrinthe à partir de son graphe associé et renvoie une liste des
        chemins possibles entre depart et arrivee.'''

        # Initialisation de la liste des noeuds et des chemins
        liste_noeuds = [depart]
        liste_chemins = [[depart]]

        # Liste du chemin entre le depart et l'arrivée
        chemins = []

        plus_court_chemin = None

        while liste_noeuds:

            # On supprime le noeud et le chemin où nous nous trouvons 
            noeud_actuel = liste_noeuds.pop()
            chemin = liste_chemins.pop()

            # Si on se trouve à l'arrivée on l'ajoute au chemin 
            if noeud_actuel == arrivee:
                # Si le chemin est le plus court ou le premier trouver
                if plus_court_chemin is None or len(chemin) < len(plus_court_chemin):
                    plus_court_chemin = chemin

            else:
                for voisin in dico_graphe[noeud_actuel]:
                    if voisin not in chemin:
                        liste_noeuds.append(voisin)
                        liste_chemins.append(chemin + [voisin])

        if plus_court_chemin:
            chemins.append(plus_court_chemin)

        return chemins


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controleur = None  # Passez une instance de votre contrôleur ici
    main_window = MainWindow(controleur)
    main_window.show()
    sys.exit(app.exec())
