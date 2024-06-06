from modelPlan import modelPlan
from datetime import datetime
from PyQt6.QtWidgets import QFileDialog, QMessageBox
import json

class controleur:
    def __init__(self, modele, vue):
        self.model = modele
        self.vue = vue
        self.fichier_enregistrement = ""

    # Créer un nouveau fichier
    def fichier_nouveau(self):
        dialogue = self.vue.nv_fichier()
        if dialogue.exec():
            infos = dialogue.get_infos()
            self.model = modelPlan(
                infos['nom_projet'], 
                infos['auteur'], 
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                infos['nom_magasin'], 
                infos['adresse_magasin'], 
                infos['fichier_produits'], 
                infos['largeur_grille'], 
                infos['longueur_grille'], 
                infos['chemin_image']
            )
            self.vue.afficher_informations_plan(self.model)

    # Ouvrir un fichier json plan
    def fichier_ouvrir(self):
        fichier, _ = QFileDialog.getOpenFileName(self.vue, "Ouvrir un projet", "", "JSON Files (*.json);;All Files (*)")
        if fichier:
            self.fichier_enregistrement = fichier
            with open(fichier, 'r', encoding='utf-8') as file:
                fichierjson = json.load(file)
            self.model = modelPlan(
                fichierjson['nom_projet'],
                fichierjson['auteur'],
                fichierjson['date_creation'],
                fichierjson['nom_magasin'],
                fichierjson['adresse_magasin'],
                None,
                fichierjson['grille']['largeur'],
                fichierjson['grille']['longueur'],
                fichierjson['chemin_image']
            )
            self.model.produits = fichierjson['produits']
            self.model.produit_coos = fichierjson['produit_coos']
            self.vue.afficher_informations_plan(self.model)

            largeur_image = self.vue.central_widget.width()
            hauteur_image = self.vue.central_widget.height()
            largeur_cases = largeur_image // fichierjson['grille']['largeur']
            hauteur_cases = hauteur_image // fichierjson['grille']['longueur']
            self.vue.afficher_image_central_widget(self.model.chemin_image, largeur_cases, hauteur_cases)
            
            for categorie in self.model.produit_coos:
                for _, (x, y) in self.model.produit_coos[categorie].items():
                    self.vue.central_widget.colorier_case(x, y)

    # Enregister un plan au format json
    def fichier_enregistrer(self):
        fichier, _ = QFileDialog.getSaveFileName(self.vue, "Enregistrer un projet", "", "JSON Files (*.json);;All Files (*)")
        if fichier:
            self.model.sauvegarder(fichier)

    # Ajouter une colonne sur le quadrillage
    def ajouter_colonne(self):
        if not self.model.contient_produits():
            self.model.augmenter_largeur_grille()
            self.mettre_a_jour_grille()
            self.vue.label_largeur_grille.setText(str(self.model.largeur_grille))
        else:
            self.afficher_message_erreur("Impossible de changer la taille du quadrillage lorsque des produits sont placés.")

    # Ajouter une ligne sur le quadrillage
    def ajouter_ligne(self):
        if not self.model.contient_produits():
            self.model.augmenter_longueur_grille()
            self.mettre_a_jour_grille()
            self.vue.label_longueur_grille.setText(str(self.model.longueur_grille))
        else:
            self.afficher_message_erreur("Impossible de changer la taille du quadrillage lorsque des produits sont placés.")

    # Supprimer une colonne sur le quadrillage
    def supprimer_colonne(self):
        if not self.model.contient_produits():
            self.model.diminuer_largeur_grille()
            self.mettre_a_jour_grille()
            self.vue.label_largeur_grille.setText(str(self.model.largeur_grille))
        else:
            self.afficher_message_erreur("Impossible de changer la taille du quadrillage lorsque des produits sont placés.")

    # Supprimer une ligne sur le quadrillage
    def supprimer_ligne(self):
        if not self.model.contient_produits():
            self.model.diminuer_longueur_grille()
            self.mettre_a_jour_grille()
            self.vue.label_longueur_grille.setText(str(self.model.longueur_grille))
        else:
            self.afficher_message_erreur("Impossible de changer la taille du quadrillage lorsque des produits sont placés.")

    # Méthode pour afficher un message d'erreur
    def afficher_message_erreur(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("Erreur")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    # Mettre à jour la grille après modification
    def mettre_a_jour_grille(self):
        largeur_image = self.vue.central_widget.width()
        hauteur_image = self.vue.central_widget.height()
        largeur_cases = largeur_image // self.model.largeur_grille
        hauteur_cases = hauteur_image // self.model.longueur_grille
        self.vue.afficher_image_central_widget(self.model.chemin_image, largeur_cases, hauteur_cases)

    # Placer un produit sur une case
    def placer_produit(self, categorie, produit, case_x, case_y):
        self.model.ajt_produit(categorie, produit, case_x, case_y)
        
    # Attribuer des coordonnées à un produit dans une case   
    def attribuer_coordonnes_produits(self, produits, case_x, case_y):
        for produit in produits:
            categorie = "default"
            self.model.ajt_produit(categorie, produit, case_x, case_y)
            self.vue.central_widget.colorier_case(case_x, case_y)

    # Récupére les produits dans une case
    def get_produits_case(self, case_x, case_y):
        produits_dans_case = []
        for categorie, produits in self.model.produit_coos.items():
            for produit, coords in produits.items():
                if coords == (case_x, case_y):
                    produits_dans_case.append(produit)
        return produits_dans_case