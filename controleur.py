class controleur:
    def __init__(self, modele, vue):
        self.model = modele
        self.vue = vue

    def fichier_nouveau(self):
        dialogue = self.vue.nv_fichier()
        if dialogue.exec():
            # a dev
            pass

    def fichier_ouvrir(self):
        # a dev
        pass

    def fichier_enregistrer(self):
        # a dev
        pass

