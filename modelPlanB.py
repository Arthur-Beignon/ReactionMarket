import json

class modelPlan:
    
    # Constructeur de la classe
    def __init__(self, nom_projet, auteur, date_creation, nom_magasin, adresse_magasin, fichier_produits, largeur_grille, longueur_grille, chemin_image):
        self.nom_projet = nom_projet
        self.auteur = auteur
        self.date_creation = date_creation
        self.nom_magasin = nom_magasin
        self.adresse_magasin = adresse_magasin
        self.produits = {}
        self.produit_coos = {}
        self.largeur_grille = largeur_grille
        self.longueur_grille = longueur_grille
        self.chemin_image = chemin_image
        if fichier_produits:
            self.lire_fichier(fichier_produits)
            self.creer_dictionnaire_produits_coos()

    # Lire le fichier json
    def lire_fichier(self, json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)
            self.nom_projet = data.get("nom_projet", self.nom_projet)
            self.auteur = data.get("auteur", self.auteur)
            self.date_creation = data.get("date_creation", self.date_creation)
            self.nom_magasin = data.get("nom_magasin", self.nom_magasin)
            self.adresse_magasin = data.get("adresse_magasin", self.adresse_magasin)
            self.produits = data.get("produits", {})
            self.produit_coos = data.get("produit_coos", {})
            self.largeur_grille = data.get("grille", {}).get("largeur", self.largeur_grille)
            self.longueur_grille = data.get("grille", {}).get("longueur", self.longueur_grille)
            self.chemin_image = data.get("chemin_image", self.chemin_image)

    # Créer un dictionnaire des produits et leurs coordonnées
    def creer_dictionnaire_produits_coos(self):
        for categorie, produits in self.produits.items():
            for produit_nom in produits:
                if categorie in self.produit_coos and produit_nom in self.produit_coos[categorie]:
                    x, y = self.produit_coos[categorie][produit_nom]
                    self.ajt_produit(categorie, produit_nom, x, y)

    # Ajouter un produit sur une case
    def ajt_produit(self, categorie, produit_nom, x, y):
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

    # Sauvegarder un plan
    def sauvegarder(self, fichier_sortie):
        infos = {
            "nom_projet": self.nom_projet,
            "auteur": self.auteur,
            "date_creation": self.date_creation,
            "nom_magasin": self.nom_magasin,
            "adresse_magasin": self.adresse_magasin,
            "produits": self.produits,
            "produit_coos": self.produit_coos,
            "grille": {
                "largeur": self.largeur_grille,
                "longueur": self.longueur_grille
            },
            "chemin_image": self.chemin_image
        }
        with open(fichier_sortie, 'w', encoding='utf-8') as file:
            json.dump(infos, file, indent=4, ensure_ascii=False)
    
    # Agrandir la largeur de la grille     
    def augmenter_largeur_grille(self):
        self.largeur_grille += 1

    # Diminuer la largeur de la grille  
    def diminuer_largeur_grille(self):
        if self.largeur_grille > 1:
            self.largeur_grille -= 1

    # Agrandir la longueur de la grille  
    def augmenter_longueur_grille(self):
        self.longueur_grille += 1

    # Diminuer la longueur de la grille  
    def diminuer_longueur_grille(self):
        if self.longueur_grille > 1:
            self.longueur_grille -= 1
