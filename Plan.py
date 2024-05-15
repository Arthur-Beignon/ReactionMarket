import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStatusBar, QLabel, QFileDialog, QPushButton
from PyQt6.QtGui import QIcon, QAction, QPixmap 
from PyQt6.QtCore import Qt, QSize


# --- class widget: hérite de QLabel ------------------------------------------
class Image(QLabel):

    def __init__(self, chemin: str):
        '''Constructeur de la classe'''

        # appel au constructeur de la classe mère
        super().__init__() 
        
        self.image = QPixmap(chemin)
        self.setPixmap(self.image)




# -----------------------------------------------------------------------------
# --- class FenetreAppli
# -----------------------------------------------------------------------------
class FenetreAppli(QMainWindow):
    def __init__(self, chemin: str = None):
        super().__init__()
        self.__chemin = chemin
        self.taille =QSize()
        
        self.setWindowTitle("Votre première application à l'IUT")
        self.setWindowIcon(QIcon(sys.path[0] + '/icones/logo_but.png'))
        self.setGeometry(100, 100, 500, 300)
        
        # barre d'état
        self.barre_etat = QStatusBar()
        self.setStatusBar(self.barre_etat)
        self.barre_etat.showMessage("L'application est démarrée...", 2000)

        # barre de menu
        menu_bar = self.menuBar()

        menu_fichier = menu_bar.addMenu('&Fichier')
        menu_edition = menu_bar.addMenu('&Edition')
        menu_aide = menu_bar.addMenu('&Aide')

        menu_fichier.addAction('Nouveau', self.nouveau)
        menu_fichier.addAction('Ouvrir', self.ouvrir)
        menu_fichier.addAction('Enregistrer', self.enregistrer)
        menu_fichier.addSeparator()
        menu_fichier.addAction('Quitter', self.destroy)



        self.showMaximized()


    def nouveau(self):
        self.barre_etat.showMessage('Créer un nouveau ....', 2000)
        boite = QFileDialog()
        chemin, validation = boite.getOpenFileName(directory = sys.path[0])
        if validation:
            self.__chemin = chemin


    def ouvrir(self):
        self.barre_etat.showMessage('Ouvrir un nouveau....', 2000)
        boite = QFileDialog()
        chemin, validation = boite.getOpenFileName(directory = sys.path[0])
        if validation:
            self.__chemin = chemin
            self.affiche_image()
        


    def enregistrer(self):
        self.barre_etat.showMessage('Enregistrer....', 2000 )
        boite = QFileDialog()
        chemin, validation = boite.getSaveFileName(directory = sys.path[0])
        if validation:
            self.__chemin = chemin

        
    def affiche_image(self):
        self.image = Image(self.__chemin)
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.image)
        self.taille = self.image.size()
        self.largeur= self.taille.width()
        self.hauteur= self.taille.height()
        



        #self.largeur_parcouru=0
        #self.hauteur_parcouru=0

        #self.dictionnaire_cases_cliquables={}
        #nb_case = 0

        #while self.hauteur_parcouru < self.hauteur :
        #    while self.largeur_parcouru < self.largeur :
        #        case_cliquable = "case_cliquable" + str(nb_case)
        #        self.dictionnaire_cases_cliquables[case_cliquable] = [self.largeur_parcouru,self.hauteur_parcouru,self.largeur_parcouru+10,self.hauteur_parcouru+10]
        #        nb_case = nb_case +1
        #        self.largeur_parcouru= self.largeur_parcouru +10
        #    self.hauteur_parcouru=self.hauteur_parcouru +10

        #for self.hauteur_parcouru in range (0,self.hauteur,20):
        #    for self.largeur_parcouru in range (0,self.largeur,20):
        #        case_cliquable = "case_cliquable" + str(nb_case)
        #        self.dictionnaire_cases_cliquables[case_cliquable] = [self.largeur_parcouru,self.hauteur_parcouru,self.largeur_parcouru+20,self.hauteur_parcouru+20]
        #        nb_case = nb_case +1
        

        #print(self.dictionnaire_cases_cliquables)





# --- main --------------------------------------------------------------------
if __name__ == "__main__":

    # création d'une QApplication
    app = QApplication(sys.argv)
    
    fenetre = FenetreAppli(sys.path[0])

    # lancement de l'application
    sys.exit(app.exec())