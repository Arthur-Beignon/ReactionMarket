import sys
import json
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QCheckBox, QGroupBox, QScrollArea, QMainWindow, QDockWidget, QMessageBox, QLabel, QFileDialog, QDialog, QLineEdit, QHBoxLayout, QPushButton, QStatusBar
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFont, QPixmap, QDesktopServices, QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Application_A")
        self.initUI()

    def initUI(self):
        # Barre de menu
        self.createMenuBar()

        # Dock informations sur le plan
        self.createDock()

        # Zone centrale avec l'image
        self.createCentralWidget()

        # Barre de statut
        self.createStatusBar()

    def createMenuBar(self):
        menu_bar = self.menuBar()
        menu_fichier = menu_bar.addMenu('&Fichier')
        menu_fichier.addAction('Nouveau', self.fichier_nouveau)
        menu_fichier.addAction('Ouvrir', self.fichier_ouvrir)
        menu_fichier.addAction('Enregistrer', self.fichier_enregistrer)
        menu_fichier.addSeparator()
        menu_fichier.addAction('Quitter', QApplication.quit)

        menu_theme = menu_bar.addMenu('&Thème')
        menu_theme.addAction('Thème clair', self.theme1)
        menu_theme.addAction('Thème sombre', self.theme2)

        menu_aide = menu_bar.addMenu('&Aide')
        action_aide = QAction("Documentation", self)
        action_aide.triggered.connect(self.aide)
        menu_aide.addAction(action_aide)

    def createDock(self):
        self.dock = QDockWidget('Sélecteur de Produit', self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)
        self.selecteur_produit = SelecteurProduit()
        self.dock.setWidget(self.selecteur_produit)

    def createCentralWidget(self):
        self.central_widget = QLabel('Importer un plan', alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.setCentralWidget(self.central_widget)
        font = QFont()
        font.setPointSize(40)
        self.central_widget.setFont(font)

    def createStatusBar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Prêt")

    def fichier_nouveau(self):
        self.status_bar.showMessage("Création d'un nouveau fichier")
        fenetre_dialogue = self.nv_fichier()
        fenetre_dialogue.exec()
        self.status_bar.showMessage("Prêt", 2000)

    def fichier_ouvrir(self):
        self.status_bar.showMessage("Ouverture d'un fichier")
        ouvrir_image = QFileDialog(self)
        ouvrir_image.setNameFilter("Images (*.png *.jpg *.jpeg *.gif)")
        if ouvrir_image.exec():
            chemin = ouvrir_image.selectedFiles()[0]
            self.afficher_image_central_widget(chemin)
            self.status_bar.showMessage(f"Fichier ouvert : {chemin}", 5000)
        else:
            self.status_bar.showMessage("Ouverture de fichier annulée", 2000)

    def fichier_enregistrer(self):
        self.status_bar.showMessage("Enregistrement du fichier")
        QMessageBox.information(self, "Enregistrer", "Développement en cours . . .")
        self.status_bar.showMessage("Prêt", 2000)

    def fichier_aide(self):
        self.status_bar.showMessage("Affichage de l'aide")
        QMessageBox.information(self, "Aide", "Développement en cours . . .")
        self.status_bar.showMessage("Prêt", 2000)

    def theme1(self):
        self.status_bar.showMessage("Passage au thème clair")
        qss = ""
        self.setStyleSheet(qss)
        self.status_bar.showMessage("Thème clair appliqué", 2000)

    def theme2(self):
        self.status_bar.showMessage("Passage au thème sombre")
        fichier_style = open(sys.path[0] + "/fichiers_qss/Takezo.qss", 'r')
        with fichier_style:
            qss = fichier_style.read()
            self.setStyleSheet(qss)
        self.status_bar.showMessage("Thème sombre appliqué", 2000)

    def aide(self):
        self.status_bar.showMessage("Ouverture de la documentation")
        QDesktopServices.openUrl(QUrl("https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
        self.status_bar.showMessage("Documentation ouverte", 2000)

    def afficher_image_central_widget(self, chemin):
        pixmap = QPixmap(chemin)
        self.central_widget.clear()
        self.central_widget.setPixmap(pixmap.scaled(self.central_widget.size(), Qt.AspectRatioMode.KeepAspectRatio))
        self.central_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

        layout_categories = QVBoxLayout()
        self.liste_categories = QListWidget()
        self.liste_categories.currentItemChanged.connect(self.sauvegarder_et_mettre_a_jour_cases)
        layout_categories.addWidget(self.liste_categories)

        layout_produits = QVBoxLayout()
        self.groupe_cases = QGroupBox("Produits")
        self.disposition_cases = QVBoxLayout()
        self.groupe_cases.setLayout(self.disposition_cases)

        self.zone_defilement = QScrollArea()
        self.zone_defilement.setWidgetResizable(True)
        self.zone_defilement.setWidget(self.groupe_cases)
        layout_produits.addWidget(self.zone_defilement)

        layout_produits_selectionnes = QVBoxLayout()
        self.liste_produits_selectionnes = QListWidget()
        layout_produits_selectionnes.addWidget(self.liste_produits_selectionnes)

        bouton_envoyer = QPushButton("Envoyer")
        bouton_envoyer.clicked.connect(self.envoyer_selections)

        mise_en_page_principale.addLayout(layout_categories)
        mise_en_page_principale.addLayout(layout_produits)
        mise_en_page_principale.addLayout(layout_produits_selectionnes)
        mise_en_page_principale.addWidget(bouton_envoyer)

        self.setLayout(mise_en_page_principale)

        self.produits = self.charger_produits_depuis_fichier("jsonType.json")
        self.produits_coordonnees = self.charger_coordonnees_produits_depuis_fichier("jsonType.json")

        self.selections_enregistrees = {categorie: set() for categorie in self.produits.keys()}

        self.remplir_liste_categories()

    def sauvegarder_et_mettre_a_jour_cases(self):
        self.sauvegarder_selections()
        self.mettre_a_jour_cases()
        self.mettre_a_jour_liste_produits_selectionnes()

    def sauvegarder_selections(self):
        item_courant = self.liste_categories.currentItem()
        if item_courant:
            categorie = item_courant.text()
            selections_actuelles = {case.text() for case in self.findChildren(QCheckBox) if case.isChecked()}
            self.selections_enregistrees[categorie] = selections_actuelles

    def mettre_a_jour_cases(self):
        for i in reversed(range(self.disposition_cases.count())):
            widget = self.disposition_cases.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        item_courant = self.liste_categories.currentItem()
        if item_courant:
            categorie = item_courant.text()

            for produit in self.produits.get(categorie, []):
                case = QCheckBox(produit)
                case.stateChanged.connect(self.mettre_a_jour_liste_produits_selectionnes)
                if produit in self.selections_enregistrees[categorie]:
                    case.setChecked(True)
                self.disposition_cases.addWidget(case)

        self.disposition_cases.addStretch()

    def mettre_a_jour_liste_produits_selectionnes(self):
        self.liste_produits_selectionnes.clear()

        for categorie, selections in self.selections_enregistrees.items():
            for produit in selections:
                self.liste_produits_selectionnes.addItem(f"{categorie}: {produit}")

    def remplir_liste_categories(self):
        self.liste_categories.addItems(self.produits.keys())

    @staticmethod
    def charger_produits_depuis_fichier(nom_fichier):
        with open(nom_fichier, 'r') as fichier:
            data = json.load(fichier)
            return data.get("produits", {})

    @staticmethod
    def charger_coordonnees_produits_depuis_fichier(nom_fichier):
        with open(nom_fichier, 'r') as fichier:
            data = json.load(fichier)
            return data.get("produit_coos", {})

    def envoyer_selections(self):
        coord_produits_selectionnes = self.trouver_coordonnees_selectionnees()
        self.ajouter_coordonnees_dans_json(coord_produits_selectionnes)
        print(coord_produits_selectionnes)
        return coord_produits_selectionnes

    def trouver_coordonnees_selectionnees(self):
        coord_produits_selectionnes = {}
        for categorie, produits in self.produits_coordonnees.items():
            for produit, coordonnees in produits.items():
                if produit in self.selections_enregistrees.get(categorie, set()):
                    coord_produits_selectionnes[produit] = coordonnees
        return coord_produits_selectionnes

    def ajouter_coordonnees_dans_json(self, coordonnees):
        with open("jsonType.json", "r+") as fichier:
            data = json.load(fichier)
            data["produit_coos"].update(coordonnees)
            fichier.seek(0)
            json.dump(data, fichier, indent=4)
            fichier.truncate()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

