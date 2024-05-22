import sys
import json
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QCheckBox, QGroupBox, QScrollArea, QMainWindow, QDockWidget, QMessageBox, QLabel, QFileDialog, QDialog, QLineEdit, QHBoxLayout, QPushButton, QCheckBox, QScrollArea
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFont, QPixmap, QDesktopServices, QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Application_A")

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
        self.dock = QDockWidget('Sélecteur de Produit', self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)
        self.selecteur_produit = SelecteurProduit()
        self.dock.setWidget(self.selecteur_produit)

        # Zone centrale avec l'image
        self.central_widget = QLabel('Importer un plan', alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.setCentralWidget(self.central_widget)
        font = QFont()
        font.setPointSize(40)
        self.central_widget.setFont(font)

    # Mettre à jour la vue
    # def updateVue(self, outil: str) -> None:

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
        with fichier_style:
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

            intituleNomFichier = QLabel("Nom du fichier : ")
            nomFichier = QLineEdit()
            layoutNom = QHBoxLayout()
            layoutNom.addWidget(intituleNomFichier)
            layoutNom.addWidget(nomFichier)

            intitulePlan = QLabel("Choisir un plan : ")
            Plan = QPushButton("test")
            layoutPlan = QHBoxLayout()
            layoutPlan.addWidget(intitulePlan)
            layoutPlan.addWidget(Plan)

            layoutPrincipale = QVBoxLayout()
            layoutPrincipale.addLayout(layoutNom)
            layoutPrincipale.addLayout(layoutPlan)

            self.setLayout(layoutPrincipale)
            self.setFixedSize(400, 200)


class SelecteurProduit(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sélecteur de Produit")
        self.resize(300, 900)

        mise_en_page_principale = QVBoxLayout()

        # Layout pour les catégories
        layout_categories = QVBoxLayout()

        self.liste_categories = QListWidget()
        self.liste_categories.currentItemChanged.connect(self.sauvegarder_et_mettre_a_jour_cases)
        layout_categories.addWidget(self.liste_categories)

        # Layout pour les produits
        layout_produits = QVBoxLayout()

        self.groupe_cases = QGroupBox("Produits")
        self.disposition_cases = QVBoxLayout()
        self.groupe_cases.setLayout(self.disposition_cases)

        # Ajouter une zone de défilement pour le groupe de cases à cocher
        self.zone_defilement = QScrollArea()
        self.zone_defilement.setWidgetResizable(True)
        self.zone_defilement.setWidget(self.groupe_cases)

        layout_produits.addWidget(self.zone_defilement)

        # Layout pour les produits sélectionnés
        layout_produits_selectionnes = QVBoxLayout()

        self.liste_produits_selectionnes = QListWidget()
        layout_produits_selectionnes.addWidget(self.liste_produits_selectionnes)

        # Bouton Envoyer
        bouton_envoyer = QPushButton("Envoyer")
        bouton_envoyer.clicked.connect(self.envoyer_selections)

        # Ajouter les layouts au layout principal
        mise_en_page_principale.addLayout(layout_categories)
        mise_en_page_principale.addLayout(layout_produits)
        mise_en_page_principale.addLayout(layout_produits_selectionnes)
        mise_en_page_principale.addWidget(bouton_envoyer)

        self.setLayout(mise_en_page_principale)

        self.produits = self.charger_produits_depuis_fichier("jsonType.json")

        self.selections_enregistrees = {categorie: set() for categorie in self.produits.keys()}

        self.remplir_liste_categories()

    def sauvegarder_et_mettre_a_jour_cases(self):
        self.sauvegarder_selections()
        self.mettre_a_jour_cases()
        self.mettre_a_jour_liste_produits_selectionnes()

    def sauvegarder_selections(self):
        # Enregistrer les sélections actuelles
        item_courant = self.liste_categories.currentItem()
        if item_courant:
            categorie = item_courant.text()
            selections_actuelles = {case.text() for case in self.findChildren(QCheckBox) if case.isChecked()}
            self.selections_enregistrees[categorie] = selections_actuelles

    def mettre_a_jour_cases(self):
        # Effacer les cases à cocher actuelles
        for i in reversed(range(self.disposition_cases.count())):
            widget = self.disposition_cases.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Obtenir la catégorie sélectionnée
        item_courant = self.liste_categories.currentItem()
        if item_courant:
            categorie = item_courant.text()

            # Ajouter des cases à cocher pour la catégorie sélectionnée
            for produit in self.produits.get(categorie, []):
                case = QCheckBox(produit)
                case.stateChanged.connect(self.mettre_a_jour_liste_produits_selectionnes)
                if produit in self.selections_enregistrees[categorie]:
                    case.setChecked(True)
                self.disposition_cases.addWidget(case)

        # Ajouter un étirement à la disposition des cases pour que les produits occupent plus d'espace
        self.disposition_cases.addStretch()

    def mettre_a_jour_liste_produits_selectionnes(self):
        # Effacer la liste actuelle
        self.liste_produits_selectionnes.clear()

        # Ajouter tous les produits sélectionnés de toutes les catégories
        for categorie, selections in self.selections_enregistrees.items():
            for produit in selections:
                self.liste_produits_selectionnes.addItem(f"{categorie}: {produit}")

    def remplir_liste_categories(self):
        # Remplir la liste des catégories avec les clés du dictionnaire de produits
        self.liste_categories.addItems(self.produits.keys())

    @staticmethod
    def charger_produits_depuis_fichier(nom_fichier):
        with open(nom_fichier, 'r') as fichier:
            data = json.load(fichier)
            return data.get("produits", {})

    def envoyer_selections(self):
        # Implémentez ici la logique pour envoyer les sélections
        print("Sélections envoyées !")


# Main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())