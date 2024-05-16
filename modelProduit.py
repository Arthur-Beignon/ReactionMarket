import json

class modelProduit:
    
    # Constructeur de la classe
    def __init__(self, json_file):
        self.produits = {}
        self.produit_coos = {}
        self.lire_fichier(json_file)

    # Lire le fichier json
    def lire_fichier(self, json_file):
        with open(json_file, 'r') as file:
            self.produits = json.load(file)

    # Ajouter un produit sur une case
    def add_produit(self, categorie, produit_nom, x, y):
        if categorie not in self.produit_coos:
            self.produit_coos[categorie] = {}
        self.produit_coos[categorie][produit_nom] = (x, y)

    # Récupérer les coordonnées de la case du produit
    def get_coo_produit(self, categorie, produit_nom):
        return self.produit_coos.get(categorie, {}).get(produit_nom)

    # Récupérer le dictionnaire des catégories et des produits
    def get_categories_produits(self):
        return self.produits

    # Récupérer le dictionnaire des produits et leurs coordonnées
    def get_coos_produits(self):
        return self.produit_coos