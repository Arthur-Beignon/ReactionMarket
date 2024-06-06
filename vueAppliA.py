import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDockWidget, QWidget, QLabel, QFileDialog, QDialog, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton, QSpinBox, QGridLayout, QFormLayout, QStatusBar, QMessageBox, QListWidget, QGroupBox, QScrollArea, QListWidgetItem
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QAction, QPen, QPainter, QMouseEvent, QColor, QBrush



# Classe dédié à l'affichage de l'image et du quadrillage
class image(QLabel):
    
    case_clicked = pyqtSignal(int, int)

    # Constructeur de la classe image
    def __init__(self, chemin: str, taille: QSize, largeur_cases=50, hauteur_cases=50):
        super().__init__()
        self.image = QPixmap(chemin).scaled(taille, Qt.AspectRatioMode.KeepAspectRatio)
        self.setPixmap(self.image)
        self.largeur_case = largeur_cases
        self.hauteur_case = hauteur_cases
        self.cases_colorees = [] 
        self.dessiner_quadrillage()

    # Fonction permettant de tracer le quadrillage
    def dessiner_quadrillage(self):
        if self.image.isNull():
            return

        pixmap_with_grid = QPixmap(self.image)
        painter = QPainter(pixmap_with_grid)
        painter.setPen(QPen(Qt.GlobalColor.black))

        for x in range(0, pixmap_with_grid.width(), self.largeur_case):
            painter.drawLine(x, 0, x, pixmap_with_grid.height())

        for y in range(0, pixmap_with_grid.height(), self.hauteur_case):
            painter.drawLine(0, y, pixmap_with_grid.width(), y)

        # Colorier les cases qui contiennent des produits
        couleur = QColor(0, 255, 0, 128) 
        painter.setBrush(QBrush(couleur))
        for case in self.cases_colorees:
            painter.drawRect(case[0] * self.largeur_case, case[1] * self.hauteur_case, self.largeur_case, self.hauteur_case)

        painter.end()
        self.setPixmap(pixmap_with_grid)
        self.setFixedSize(pixmap_with_grid.size())

    # Détecter sur quelle case l'utilisateur clique
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            x = event.position().x()
            y = event.position().y()

            case_x = int(x // self.largeur_case)
            case_y = int(y // self.hauteur_case)

            self.window().barre_etat.showMessage(f"Clic dans la case: ({case_x}, {case_y})", 2000)
            self.case_clicked.emit(case_x, case_y)

    # Colorier une case, ajoute la case à la liste des cases colorées
    def colorier_case(self, case_x, case_y):
        if (case_x, case_y) not in self.cases_colorees:
            self.cases_colorees.append((case_x, case_y))
        self.dessiner_quadrillage()
                


# Interface qui s'affiche quand on clique sur une case
class SelecteurProduit_special(QWidget):
    produits_attribues = pyqtSignal(list, list, int, int)

    # Constructeur de la classe SelecteurProduit_special
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sélecteur de Produit")
        self.resize(400, 600)

        self.mise_en_page_principale = QVBoxLayout()

        # Layout supérieur avec les catégories
        self.layout_categories = QVBoxLayout()
        self.label_categorie = QLabel("Categorie")
        self.liste_categories = QListWidget()
        self.liste_categories.itemClicked.connect(self.afficher_produits)
        self.layout_categories.addWidget(self.label_categorie)
        self.layout_categories.addWidget(self.liste_categories)

        # Layout inférieur avec les produits
        self.layout_produits = QVBoxLayout()
        self.groupe_cases = QGroupBox("Produits")
        self.disposition_cases = QVBoxLayout()
        self.groupe_cases.setLayout(self.disposition_cases)

        self.zone_defilement = QScrollArea()
        self.zone_defilement.setWidgetResizable(True)
        self.zone_defilement.setWidget(self.groupe_cases)
        self.layout_produits.addWidget(self.zone_defilement)

        # Bouton de validation
        self.bouton_attribuer = QPushButton("Placer les produits")
        self.bouton_attribuer.clicked.connect(self.attribuer_coordonnes)

        self.mise_en_page_principale.addLayout(self.layout_categories)
        self.mise_en_page_principale.addLayout(self.layout_produits)
        self.mise_en_page_principale.addWidget(self.bouton_attribuer)

        self.setLayout(self.mise_en_page_principale)

    # Afficher les catégories et les produits du magasin sur le sélecteur
    def afficher_produits(self, item):
        categorie = item.text()
        produits = self.produits.get(categorie, [])
        for i in reversed(range(self.disposition_cases.count())): 
            widget = self.disposition_cases.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.liste_produits = QListWidget()
        self.liste_produits.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for produit in produits:
            item_produit = QListWidgetItem(produit)
            self.liste_produits.addItem(item_produit)
        self.disposition_cases.addWidget(self.liste_produits)
        self.disposition_cases.setContentsMargins(0, 0, 0, 0)
        self.disposition_cases.setSpacing(0)
        self.groupe_cases.setLayout(self.disposition_cases)

    # Attribuer les coordonnées d'une case à un produit
    def attribuer_coordonnes(self):
        produits_selectionnes = [item.text() for item in self.liste_produits.selectedItems()]
        if produits_selectionnes:
            categorie_selectionnee = self.liste_categories.currentItem().text()
            categories_selectionnees = [categorie_selectionnee] * len(produits_selectionnes)
            self.produits_attribues.emit(produits_selectionnes, categories_selectionnees, self.case_x, self.case_y)
            self.close()
        else:
            self.afficher_message_erreur("Veuillez sélectionner au moins un produit avant de placer.")
            
    # Charger les catégories de produits dans le sélecteur
    def charger_categories(self, categories_produits):
        self.produits = categories_produits
        self.liste_categories.clear()
        for categorie in categories_produits:
            self.liste_categories.addItem(categorie)

    # Définir les coordonnées d'une case, prend une abscisse et une ordonnée en paramètre
    def definir_coordonnes_case(self, case_x, case_y):
        self.case_x = case_x
        self.case_y = case_y
        self.effacer_selections()
    
    # Effacer les sélections dans la liste des produits et des catégories
    def effacer_selections(self):
        if hasattr(self, 'liste_produits'):
            self.liste_produits.clearSelection()
            self.liste_produits.clear()
        self.liste_categories.clearSelection()
        for i in reversed(range(self.disposition_cases.count())): 
            widget = self.disposition_cases.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    # Afficher un message d'erreur, le contenu du message est placé en paramètre
    def afficher_message_erreur(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("Erreur")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()



# Classe principale de l'application
class MainWindow(QMainWindow):
    
    # Constructeur de l'interface principale
    def __init__(self, controleur):
        super().__init__()
        self.controleur = controleur
        self.setWindowTitle("Gestionnaire de plan")
        
        self.selecteur_produit = SelecteurProduit_special()
        self.selecteur_produit.produits_attribues.connect(self.produits_attribues)
        
        # Barre de menu
        menu_bar = self.menuBar()
        menu_fichier = menu_bar.addMenu('&Fichier')
        menu_edition = menu_bar.addMenu('&Edition')
        menu_theme = menu_bar.addMenu('&Thème')
        menu_aide = menu_bar.addMenu('&Aide')
        
        # Options du menu fichier
        action_nouveau = QAction('Nouveau', self)
        action_nouveau.setShortcut('Ctrl+N')
        action_nouveau.triggered.connect(self.controleur.fichier_nouveau)
        menu_fichier.addAction(action_nouveau)
        
        action_ouvrir = QAction('Ouvrir', self)
        action_ouvrir.setShortcut('Ctrl+O')
        action_ouvrir.triggered.connect(self.controleur.fichier_ouvrir)
        menu_fichier.addAction(action_ouvrir)
        
        action_enregistrer = QAction('Enregistrer', self)
        action_enregistrer.setShortcut('Ctrl+S')
        action_enregistrer.triggered.connect(self.controleur.fichier_enregistrer)
        menu_fichier.addAction(action_enregistrer)
        
        menu_fichier.addSeparator()
        menu_fichier.addAction('Quitter', self.close)
        
        # Options du menu édition
        self.action_plusColonne = QAction('+1 Colonne', self)
        self.action_plusColonne.triggered.connect(self.controleur.ajouter_colonne)
        menu_edition.addAction(self.action_plusColonne)
        
        self.action_plusLigne = QAction('+1 Ligne', self)
        self.action_plusLigne.triggered.connect(self.controleur.ajouter_ligne)
        menu_edition.addAction(self.action_plusLigne)
        
        self.action_moinsColonne = QAction('-1 Colonne', self)
        self.action_moinsColonne.triggered.connect(self.controleur.supprimer_colonne)
        menu_edition.addAction(self.action_moinsColonne)
        
        self.action_moinsLigne = QAction('-1 Ligne', self)
        self.action_moinsLigne.triggered.connect(self.controleur.supprimer_ligne)
        menu_edition.addAction(self.action_moinsLigne)
        
        # Désactiver les actions d'édition initialement, quand aucun plan n'est chargé
        self.set_actions_enabled(False)
        
        # Options du menu thème
        menu_theme.addAction('Thème clair', self.theme1)
        menu_theme.addAction('Thème sombre', self.theme2)
        
        # Options du menu aide
        action_aide = QAction("Documentation", self)
        action_aide.triggered.connect(self.aide)
        menu_aide.addAction(action_aide)
        
        # Dock informations sur le plan
        self.dock = QDockWidget('Informations')
        dock_widget = QWidget()
        self.dock.setWidget(dock_widget)
        dock_layout = QFormLayout(dock_widget)
        dock_widget.setLayout(dock_layout)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)
        self.dock.setMinimumSize(200, 120)
        
        # Zone centrale avec l'image
        self.central_widget = QLabel('Importer un plan', alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.setCentralWidget(self.central_widget)
        font = QFont()
        font.setPointSize(40)
        self.central_widget.setFont(font)
        
        # Barre d'etat situé en bas de l'application
        self.barre_etat = QStatusBar()
        self.setStatusBar(self.barre_etat)
        
        #Afficher l'application en plein écran
        self.showMaximized()

    # Méthode pour activer ou désactiver les actions d'édition
    def set_actions_enabled(self, enabled):
        self.action_plusColonne.setEnabled(enabled)
        self.action_plusLigne.setEnabled(enabled)
        self.action_moinsColonne.setEnabled(enabled)
        self.action_moinsLigne.setEnabled(enabled)

    # Changer le thème
    def theme1(self):
        qss = ""
        self.setStyleSheet(qss)

    def theme2(self):
        fichier_style = open(sys.path[0] + "/fichiers_qss/Takezo.qss", 'r')
        with fichier_style :
            qss = fichier_style.read()
            self.setStyleSheet(qss)
    
    # Afficher les indications quand le bouton aide est cliqué       
    def aide(self):
        message_aide = QMessageBox()
        message_aide.setWindowTitle("Aide")
        message_aide.setText(
            "Bienvenue dans le gestionnaire de plan !\n\n"
            "Voici quelques instructions pour utiliser l'application :\n\n"
            "1. Nouveau : Créez un nouveau projet en fournissant les informations requises, "
            "comme le nom du projet, l'auteur, le nom du magasin, l'adresse du magasin, "
            "les dimensions de la grille, le fichier JSON des produits, et l'image du plan.\n"
            "2. Ouvrir : Ouvrez un projet existant à partir d'un fichier JSON.\n"
            "3. Enregistrer : Enregistrez le projet actuel dans un fichier JSON.\n"
            "4. Ajouter/Supprimer Colonne/Ligne : Modifiez la taille du quadrillage tant qu'aucun produit n'est placé.\n"
            "5. Thème : Changez le thème de l'application entre clair et sombre.\n\n"
            "Pour plus d'aide, veuillez consulter la documentation ou contacter le support technique."
        )
        message_aide.setIcon(QMessageBox.Icon.Information)
        message_aide.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_aide.exec()
    
    # Afficher une image sur la partie centrale de l'application
    def afficher_image_central_widget(self, chemin, largeur_cases, hauteur_cases):
        taille_fixe = QSize(self.central_widget.width(), self.central_widget.height())
        self.central_widget = image(chemin, taille_fixe, largeur_cases, hauteur_cases)
        self.central_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.central_widget.case_clicked.connect(self.ouvrir_selecteur_produit)
        self.setCentralWidget(self.central_widget)

    # Ouvrir le sélecteur de produit quand on clique sur une case
    def ouvrir_selecteur_produit(self, case_x, case_y):
        produits = self.controleur.get_produits_case(case_x, case_y)
        if produits:
            self.afficher_produits_dans_case(produits, case_x, case_y)
        else:
            self.selecteur_produit.definir_coordonnes_case(case_x, case_y)
            self.selecteur_produit.show()
        
    # Mettre à jour la vue avec les informations du plan
    def afficher_informations_plan(self, modele):
        self.vider_dock_informations()
        layoutInfo = self.dock.widget().layout()

        layoutInfo.addRow("Nom du projet:", QLabel(modele.nom_projet))
        layoutInfo.addRow("Auteur:", QLabel(modele.auteur))
        layoutInfo.addRow("Date de création:", QLabel(modele.date_creation))
        layoutInfo.addRow("Nom du magasin:", QLabel(modele.nom_magasin))
        layoutInfo.addRow("Adresse du magasin:", QLabel(modele.adresse_magasin))

        self.label_largeur_grille = QLabel(str(modele.largeur_grille))
        self.label_longueur_grille = QLabel(str(modele.longueur_grille))
        layoutInfo.addRow("Nombre de colonne:", self.label_largeur_grille)
        layoutInfo.addRow("Nombre de ligne:", self.label_longueur_grille)

        if modele.chemin_image:
            largeur_image = self.central_widget.width()
            hauteur_image = self.central_widget.height()
            largeur_cases = largeur_image // modele.largeur_grille
            hauteur_cases = hauteur_image // modele.longueur_grille
            self.afficher_image_central_widget(modele.chemin_image, largeur_cases, hauteur_cases)
        
        espace = QLabel("")
        espace.setFixedHeight(20)
        layoutInfo.addRow(espace)
        
        # Ajout des boutons pour manipuler le quadrillage
        ajouter_colonne_btn = QPushButton("Ajouter Colonne")
        ajouter_ligne_btn = QPushButton("Ajouter Ligne")
        supprimer_colonne_btn = QPushButton("Supprimer Colonne")
        supprimer_ligne_btn = QPushButton("Supprimer Ligne")
        infos_btn = QLabel("Si vous enregistrez un produit sur une case, vous ne pourrez plus modifier la taille du quadrillage")
        font = QFont()
        font.setItalic(True)
        infos_btn.setFont(font)

        ajouter_colonne_btn.clicked.connect(self.controleur.ajouter_colonne)
        ajouter_ligne_btn.clicked.connect(self.controleur.ajouter_ligne)
        supprimer_colonne_btn.clicked.connect(self.controleur.supprimer_colonne)
        supprimer_ligne_btn.clicked.connect(self.controleur.supprimer_ligne)

        layoutInfo.addRow(ajouter_colonne_btn)
        layoutInfo.addRow(ajouter_ligne_btn)
        layoutInfo.addRow(supprimer_colonne_btn)
        layoutInfo.addRow(supprimer_ligne_btn)
        layoutInfo.addRow(infos_btn)
        
        espace2 = QLabel("")
        espace2.setFixedHeight(20)
        layoutInfo.addRow(espace2)
        
        tuto = QLabel("Cliquez sur une case pour ajouter un produit")
        tuto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutInfo.addRow(tuto)
        
        self.selecteur_produit.charger_categories(modele.get_categories_produits())
        
        # Activer les actions d'édition maintenant que le plan est chargé
        self.set_actions_enabled(True)
            
    # Vider le contenu du dock d'informations
    def vider_dock_informations(self):
        layoutInfoVide = self.dock.widget().layout()
        if layoutInfoVide is not None:
            while layoutInfoVide.count() > 0:
                item = layoutInfoVide.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
    
    # Emettre le signal qu'un produit est sélectionné vers le contrôleur
    def produits_attribues(self, produits, categories, case_x, case_y):
        self.controleur.attribuer_coordonnes_produits(produits, categories, case_x, case_y)
        
    # Interface s'affichant lors de la création d'un nouveau fichier
    class nv_fichier(QDialog):
        def __init__(self):
            super().__init__()

            self.setWindowTitle("Nouveau fichier")
            self.setFixedSize(500, 300)
            
            intituleNomProjet = QLabel("Nom du fichier : ")
            self.nomProjet = QLineEdit()
            intituleAuteur = QLabel("Nom de l'auteur : ")
            self.nomAuteur = QLineEdit()
            intituleNomMagasin = QLabel("Nom du magasin : ")
            self.nomMagasin = QLineEdit()
            intituleAdresseMagasin = QLabel("Adresse du magasin : ")
            self.adresseMagasin = QLineEdit()
            intituleLargeurGrille = QLabel("Largeur de la grille : ")
            self.largeurGrille = QSpinBox()
            self.largeurGrille.setRange(1, 1000)
            intituleLongueurGrille = QLabel("Longueur de la grille : ")
            self.longueurGrille = QSpinBox()
            self.longueurGrille.setRange(1, 1000)
            intituleProduits = QLabel("Fichier JSON des produits : ")
            self.importerProduits = QPushButton('importer')
            intituleImage = QLabel("Image du plan : ")
            self.importerImage = QPushButton('importer')
            
            self.importerProduits.clicked.connect(self.ouvrir_fichier_produits)
            self.importerImage.clicked.connect(self.ouvrir_fichier_image)
            
            layoutPrincipal = QGridLayout()

            # Ajout des widgets au layout principal
            layoutPrincipal.addWidget(intituleNomProjet, 0, 0)
            layoutPrincipal.addWidget(self.nomProjet, 0, 1)
            
            layoutPrincipal.addWidget(intituleAuteur, 1, 0)
            layoutPrincipal.addWidget(self.nomAuteur, 1, 1)
            
            layoutPrincipal.addWidget(intituleNomMagasin, 2, 0)
            layoutPrincipal.addWidget(self.nomMagasin, 2, 1)
            
            layoutPrincipal.addWidget(intituleAdresseMagasin, 3, 0)
            layoutPrincipal.addWidget(self.adresseMagasin, 3, 1)
            
            layoutPrincipal.addWidget(intituleLongueurGrille, 4, 0)
            layoutPrincipal.addWidget(self.longueurGrille, 4, 1)
            
            layoutPrincipal.addWidget(intituleLargeurGrille, 5, 0)
            layoutPrincipal.addWidget(self.largeurGrille, 5, 1)
            
            layoutPrincipal.addWidget(intituleProduits, 6, 0)
            layoutPrincipal.addWidget(self.importerProduits, 6, 1)
            
            layoutPrincipal.addWidget(intituleImage, 7, 0)
            layoutPrincipal.addWidget(self.importerImage, 7, 1)
            
            validation = QPushButton("Valider")
            validation.setFixedSize(70, 30)
            validation.clicked.connect(self.accept)
            
            validationLayout = QHBoxLayout()
            validationLayout.addStretch(1)
            validationLayout.addWidget(validation)

            layoutComplet = QVBoxLayout()
            layoutComplet.addLayout(layoutPrincipal)
            layoutComplet.addStretch(1)
            layoutComplet.addLayout(validationLayout)
            
            self.setLayout(layoutComplet)
            
            self.fichier_produits = ""
            self.fichier_image = ""
        
        # Boite de dialogue demandant un fichier json qui contient la liste des produits du magasin
        def ouvrir_fichier_produits(self):
            fichier, _ = QFileDialog.getOpenFileName(self, "Choisir un JSON avec les produits", "", "JSON Files (*.json);;All Files (*)")
            if fichier:
                self.fichier_produits = fichier
        
        # Boite de dialogue demandant un fichier image, le plan du magasin
        def ouvrir_fichier_image(self):
            fichier, _ = QFileDialog.getOpenFileName(self, "Choisir une image de plan", "", "Images Files (*.png *.jpg *.jpeg *.gif);;All Files (*)")
            if fichier:
                self.fichier_image = fichier
        
        # Récupérer les informations du plan
        def get_infos(self):
            return {
                'nom_projet': self.nomProjet.text(),
                'auteur': self.nomAuteur.text(),
                'nom_magasin': self.nomMagasin.text(),
                'adresse_magasin': self.adresseMagasin.text(),
                'largeur_grille': self.largeurGrille.value(),
                'longueur_grille': self.longueurGrille.value(),
                'fichier_produits': self.fichier_produits,
                'chemin_image': self.fichier_image
            }