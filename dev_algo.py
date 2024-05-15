from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from filepile import *


liste_produit = []
liste_placement = []
nb_produits = 0

#Permet de demander au client combien de produits doit-il aller chercher dans le magasin
def dmd_nb_produit(): 
    
    condition_while = False
    while condition_while == False : 
        nb_produits = int(input("Combien de produits devez-vous aller chercher dans le magasin ReactionMarket ? \n"))
        if nb_produits < 9999999 and nb_produits > 0:
            condition_while = True
        else:
            print("Le nombre de produits doit être compris entre 1 et 9999999.")
    return nb_produits


#Permet de demander au client quelles sont les produits qu'il a besoin dans le magasin
def demande_produit():
    for n in range(nb_produits) :
        liste_produit[n] = input("qu'elle est le produit n°","que vous souhaitez prendre ?")
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

            if voisin not in bk_liste :                                          # ligne optionnelle

                nouvelle_distance: int = distance[sommet][0] + voisins[voisin]
                
                if voisin not in distance or nouvelle_distance < distance[voisin][0] :
                    distance[voisin] = [nouvelle_distance, chemin + voisin]
                    file1.enfiler(chemin + voisin)
                    
    return distance






