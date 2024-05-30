from modelPlan import modelPlan
from datetime import datetime
from PyQt6.QtWidgets import QFileDialog
from vueAppliA import image
import json

class controleur:
    def __init__(self, modele, vue):
        self.model = modele
        self.vue = vue

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

    def fichier_ouvrir(self):
        fichier, _ = QFileDialog.getOpenFileName(self.vue, "Ouvrir un projet", "", "JSON Files (*.json);;All Files (*)")
        if fichier:
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
            
            # Calculer la taille des cases
            largeur_image = self.vue.central_widget.width()
            hauteur_image = self.vue.central_widget.height()
            largeur_cases = largeur_image // fichierjson['grille']['largeur']
            hauteur_cases = hauteur_image // fichierjson['grille']['longueur']

            # Afficher l'image et dessiner le quadrillage avec les dimensions correctes
            self.vue.afficher_image_central_widget(self.model.chemin_image, largeur_cases, hauteur_cases)

    def fichier_enregistrer(self):
        fichier, _ = QFileDialog.getSaveFileName(self.vue, "Enregistrer un projet", "", "JSON Files (*.json);;All Files (*)")
        if fichier:
            self.model.sauvegarder(fichier)
            
    def ajouter_ligne(self):
        self.model.augmenter_longueur_grille()
        self.mettre_a_jour_grille()
        self.vue.label_longueur_grille.setText(str(self.model.longueur_grille))

    def ajouter_colonne(self):
        self.model.augmenter_largeur_grille()
        self.mettre_a_jour_grille()
        self.vue.label_largeur_grille.setText(str(self.model.largeur_grille))

    def supprimer_ligne(self):
        self.model.diminuer_longueur_grille()
        self.mettre_a_jour_grille()
        self.vue.label_longueur_grille.setText(str(self.model.longueur_grille))

    def supprimer_colonne(self):
        self.model.diminuer_largeur_grille()
        self.mettre_a_jour_grille()
        self.vue.label_largeur_grille.setText(str(self.model.largeur_grille))

    def mettre_a_jour_grille(self):
        largeur_image = self.vue.central_widget.width()
        hauteur_image = self.vue.central_widget.height()
        largeur_cases = largeur_image // self.model.largeur_grille
        hauteur_cases = hauteur_image // self.model.longueur_grille
        self.vue.afficher_image_central_widget(self.model.chemin_image, largeur_cases, hauteur_cases)

