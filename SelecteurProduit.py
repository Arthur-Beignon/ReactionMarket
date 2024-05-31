import json
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QCheckBox, QGroupBox, QScrollArea, QPushButton, QMessageBox
from PyQt6.QtCore import Qt

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
        bouton_envoyer.clicked.connect(self.afficher_produits_selectionnes)

        # Ajouter les layouts au layout principal
        mise_en_page_principale.addLayout(layout_categories)
        mise_en_page_principale.addLayout(layout_produits)
        mise_en_page_principale.addLayout(layout_produits_selectionnes)
        mise_en_page_principale.addWidget(bouton_envoyer)

        self.setLayout(mise_en_page_principale)
        
        self.data = self.charger_donnees_depuis_fichier("jsonType.json")
        self.produits = self.data.get("produits", {})
        self.produits_coos = self.data.get("produit_coos", {})

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
                self.liste_produits_selectionnes.addItem(produit)

    def remplir_liste_categories(self):
        # Remplir la liste des catégories avec les clés du dictionnaire de produits
        self.liste_categories.addItems(self.produits.keys())

    def creer_dictionnaire_produits_selectionnes(self):
        # Créer un dictionnaire des produits sélectionnés
        dict_produits_selectionnes = set()
        for produits in self.selections_enregistrees.values():
            dict_produits_selectionnes.update(produits)
        return dict_produits_selectionnes

    def creer_dictionnaire_produits_avec_coos(self):
        # Créer un dictionnaire des produits sélectionnés avec leurs coordonnées
        produits_selectionnes = self.creer_dictionnaire_produits_selectionnes()
        dict_produits_avec_coos = {}
        
        for categorie, produits in self.produits_coos.items():
            for produit, coos in produits.items():
                if produit in produits_selectionnes:
                    dict_produits_avec_coos[produit] = coos
        
        return dict_produits_avec_coos

    def afficher_produits_selectionnes(self):
        # Afficher le dictionnaire des produits sélectionnés avec leurs coordonnées dans une boîte de message
        dict_produits_avec_coos = self.creer_dictionnaire_produits_avec_coos()
        message = json.dumps(dict_produits_avec_coos, indent=4, ensure_ascii=False)
        msg_box = QMessageBox()
        msg_box.setText(message)
        msg_box.exec()

    @staticmethod
    def charger_donnees_depuis_fichier(nom_fichier):
        with open(nom_fichier, 'r') as fichier:
            return json.load(fichier)

if __name__ == "__main__":
    app = QApplication([])
    fenetre = SelecteurProduit()
    fenetre.show()
    app.exec()
