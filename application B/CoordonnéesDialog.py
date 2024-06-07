import json
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QCheckBox, QGroupBox, QScrollArea, QPushButton, QMessageBox, QDialog, QHBoxLayout, QLabel, QLineEdit
from PyQt6.QtCore import Qt


class CoordonneesDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Entrer les coordonnées de départ")
        
        layout = QVBoxLayout()

        # Label et champ pour la coordonnée x
        layout_x = QHBoxLayout()
        label_x = QLabel("Coordonnée X :")
        self.input_x = QLineEdit()
        layout_x.addWidget(label_x)
        layout_x.addWidget(self.input_x)

        # Label et champ pour la coordonnée y
        layout_y = QHBoxLayout()
        label_y = QLabel("Coordonnée Y :")
        self.input_y = QLineEdit()
        layout_y.addWidget(label_y)
        layout_y.addWidget(self.input_y)

        # Boutons
        layout_boutons = QHBoxLayout()
        bouton_ok = QPushButton("OK")
        bouton_annuler = QPushButton("Annuler")
        layout_boutons.addWidget(bouton_ok)
        layout_boutons.addWidget(bouton_annuler)

        # Ajouter les layouts à la disposition principale
        layout.addLayout(layout_x)
        layout.addLayout(layout_y)
        layout.addLayout(layout_boutons)

        self.setLayout(layout)

        # Connecter les boutons
        bouton_ok.clicked.connect(self.accept)
        bouton_annuler.clicked.connect(self.reject)

    def get_coordonnees(self):
        return (int(self.input_x.text()), int(self.input_y.text()))
