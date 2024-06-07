from filepile import *
import json, os

liste_produit = []
liste_placement = []

# Permet de demander au client combien de produits doit-il aller chercher dans le magasin
def dmd_nb_produit(): 
    while True: 
        try:
            nb_produits = int(input("Combien de produits devez-vous aller chercher dans le magasin ReactionMarket ? \n"))
            if nb_produits > 0:
                return nb_produits
            else:
                print("Le nombre de produits doit être supérieur à zéro.")
        except ValueError:
            print("Veuillez entrer un nombre valide.\n")


# Permet de demander au client quels sont les produits qu'il a besoin dans le magasin
def demande_produit(nb_produits):
    for n in range(nb_produits):
        produit = input(f"Quel est le produit n°{n+1} que vous souhaitez prendre ? ")
        liste_produit.append(produit)
    return liste_produit


def dijkstra(graphe: dict, depart: str, bk_liste: list = []) -> dict:
    '''La fonction renvoie un dictionnaire dont les clés sont les sommets que l'on peut atteindre
à partir du sommet_depart.
A chaque clé est associée la distance qui sépare ce sommet du sommet_depart.

:param: graphe, dictionnaire des voisins du graphe
:param: depart, type str, sommet à partir duquel sont calculées les distances
:param: bk_liste, liste de sommets à éviter
:return: dictionnaire des distances par rapport aux sommets
:CU: Respect des types
:bord_effect: None
'''
    file1 = File(len(graphe.keys()))
    file1.enfiler(depart)
    distance = {depart: [0, depart]}

    while not file1.est_vide():

        chemin = file1.defiler()
        sommet = chemin[-1]
        voisins = graphe[sommet]

        for voisin in voisins:

            if voisin not in bk_liste:                                   

                nouvelle_distance = distance[sommet][0] + voisins[voisin]
                
                if voisin not in distance or nouvelle_distance < distance.get(voisin, [float('inf')])[0]:
                    distance[voisin] = [nouvelle_distance, chemin + voisin]
                    file1.enfiler(chemin + voisin)
                    
    return distance

# Permet de demander le nom de fichier json et vérifie s'il est valide
def demander_nom_fichier():
    while True:
        nom_fichier = input("Quel est le nom du fichier que vous voulez lire ? \n")
        if nom_fichier.strip():  
            if os.path.isfile(nom_fichier):  
                return nom_fichier
            else:
                print("Le fichier spécifié n'existe pas. Veuillez réessayer.\n")
        else:
            print("Le nom du fichier ne peut pas être vide. Veuillez réessayer.\n")

# Permet de lire le fichier json et affiche les données.
def lire_fichier(nom_fichier):
    with open(nom_fichier) as f:
        data = json.load(f)
        for categorie, produits in data.items():
            print(f"{categorie} : {produits}")
        print()

# Permet de trouver si les produits existent bien dans le fichier json.
def comparer_produits(liste_produits, nom_fichier):
    with open(nom_fichier, 'r') as f:
        donnees_json = json.load(f)
    
    correspondances = {}

    for categorie, produits in donnees_json.items():
        for produit in liste_produits:
            if produit in produits:
                correspondances[produit] = categorie
    
    return correspondances

def main():
    nb_produits = dmd_nb_produit()
    nom_fichier = demander_nom_fichier()
    lire_fichier(nom_fichier)
    demande_produit(nb_produits)
    fichier_json = "liste_produits.json"
    resultat = comparer_produits(liste_produit, fichier_json)
    print(resultat)

if __name__ == "__main__":
    main()
