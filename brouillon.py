 def fichier_nouveau(self):
        fenetre_dialogue = self.nv_fichier()
        fenetre_dialogue.exec()

    # -----------------------------TEMPORAIRE, SEUL IMAGE POUR L'INSTANT, FICHIER ENTIER PLUS TARD-----------------------------
    # Seul les fichiers en .png, .jpg, .jpeg et .gif sont autorisés
    def fichier_ouvrir(self):
        ouvrir_image = QFileDialog(self)
        ouvrir_image.setNameFilter("Images (*.png *.jpg *.jpeg *.gif)")
        if ouvrir_image.exec():
            chemin = ouvrir_image.selectedFiles()[0]
            self.afficher_image_central_widget(chemin)

    def fichier_enregistrer(self):
        QMessageBox.information(self, "Enregistrer", "Développement en cours . . .")
        
    def fichier_aide(self):
        QMessageBox.information(self, "Enregistrer", "Développement en cours . . .")
    