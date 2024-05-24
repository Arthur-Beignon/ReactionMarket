from modelPlan import modelPlan
from datetime import datetime
from PyQt6.QtWidgets import QFileDialog
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

    def fichier_enregistrer(self):
        fichier, _ = QFileDialog.getSaveFileName(self.vue, "Enregistrer un projet", "", "JSON Files (*.json);;All Files (*)")
        if fichier:
            self.model.sauvegarder(fichier)

