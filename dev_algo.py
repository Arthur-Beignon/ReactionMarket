from filepile import *
import json, os

liste_produit = []
liste_placement = []
nb_produits = 0

#Permet de demander au client combien de produits doit-il aller chercher dans le magasin
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


#Permet de demander au client quelles sont les produits qu'il a besoin dans le magasin
def demande_produit(nb_produits):
    for n in range(nb_produits):
        produit = input(f"Quel est le produit n°{n+1} que vous souhaitez prendre ? ")
        liste_produit.append(produit)
    return liste_produit



def dijkstra(graphe: dict, depart: str, bk_liste: list = []) -> dict:
    '''La fonction renvoie un dictionnaire dont les clés sont les sommets que l'on peut atteindre
à partir du sommet_depart.
A chaque clé est associée la distance qui sépare ce sommet du sommet_depart.

:param: graphe, dictionnaire des voisions du graphe
:param: depart, type str, sommet à partir duquel sont calculées les distances
:param: bk_liste, liste de sommets à éviter
:return: dictionnaire des distances par rapport aux sommets
:CU: Respect des types
:bord_effect: None
'''
    file1: File = File(len(graphe.keys()))
    file1.enfiler(depart)
    distance: dict = {depart : [0, depart]}

    while not file1.est_vide():

        chemin: str = file1.defiler()
        sommet: str = chemin[-1]
        voisins: dict = graphe[sommet]

        for voisin in voisins :

            if voisin not in bk_liste :                                   

                nouvelle_distance: int = distance[sommet][0] + voisins[voisin]
                
                if voisin not in distance or nouvelle_distance < distance[voisin][0] :
                    distance[voisin] = [nouvelle_distance, chemin + voisin]
                    file1.enfiler(chemin + voisin)
                    
    return distance


def demander_nom_fichier():
    while True:
        nom_fichier = input("Quel est le nom du fichier que vous voulez lire ? \n")
        if nom_fichier.strip() :  
            if os.path.isfile(nom_fichier) :  
                return nom_fichier
            else:
                print("Le fichier spécifié n'existe pas. Veuillez réessayer.\n")
        else:
            print("Le nom du fichier ne peut pas être vide. Veuillez réessayer.\n")




def lire_fichier(nom_fichier) :
    with open(nom_fichier) as f:
        data = json.load(f)
        print("Légumes : ",data['Légumes'])
        print("Poissons : ", data['Poissons'])
        print("Viandes : ", data['Viandes'])
        print("Épicerie : ", data['Épicerie'])
        print("Épicerie sucrée : ", data['Épicerie sucrée'])
        print("Petit déjeuner : ", data['Petit déjeuner'])
        print("Fruits : ", data['Fruits'])
        print("Rayon frais : ", data['Rayon frais'])
        print("Crèmerie : ", data['Crèmerie'])
        print("Conserves : ", data['Conserves'])
        print("Apéritifs : ", data['Apéritifs'])
        print("Boissons : ", data['Boissons'])
        print("Articles Maison : ", data['Articles Maison'])
        print("Hygiène : ", data['Hygiène'])
        print("Bureau : ", data['Bureau'])
        print("Animaux : ", data['Animaux'])



def main():
    nb_produits = dmd_nb_produit()
    nom_fichier = demander_nom_fichier()
    lire_fichier(nom_fichier)
    demande_produit(nb_produits)

if __name__ == "__main__":
    main()
nb_produits < 9999999