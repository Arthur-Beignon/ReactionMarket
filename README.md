# ReactionMarket

### Le supermarché du futur

Projet de SAE IHM et Graphes 

Membre du projet : TELLIEZ Luc, LESAGE Mathéo, COTAR Clément & BEIGNON Arthur

## Le but du projet

Le but de ce projet est de créé deux application.

### Appli A:

La premiere application, l'appli A a destination des magasins a pour but de permettre la gestion du magasins.

### Appli B:
La seconde application, l'appli B a destination des particuliers a pour but de les renseignaient en leur indiquant le chemin le plus court afin de récupérer tout les articles qu'ils auront préalablement sélectionnée.

## Comment sa marche


### Appli A:

Le fonctionnement de la première application est d'implementer un plan en choississant le nombre de case permmetant d'y placer différent produit.
Lorsqu'elle clique à un endroit du plan une fenêtre s'ouvre afin que l'utilisateur entre les info concernant ce plan.

Par la suite l'utilisateur peut ouvrir le plan et modifier le nombre de case ou modifier le contenu de ces cases les coordonnées se mettent dans 
un fichier Json ou s'on inscrit les différent produit.


### Appli B:

L'appli B appel à l'algorithme de Dijkstra pour déterminer le chemin le plus court et donc créer un chemin dans une liste de produits choisi

### Bibliothèque obligatoire pour le bon fonctionnement

Pour faire fonctionner le programme, il vous faut installer PyQt6 en suivant ce tuto : 

      -> LINUX -> https://www.pythonguis.com/installation/install-pyqt6-linux/
      -> MacOs -> https://www.pythonguis.com/installation/install-pyqt6-mac/
      -> Windows -> https://www.pythonguis.com/installation/install-pyqt6-windows/

      
