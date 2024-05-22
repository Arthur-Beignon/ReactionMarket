import sys
from PyQt6.QtWidgets import QApplication
from modelPlan import modelPlan
from vueAppliA import MainWindow
from controleur import controleur

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    modele = modelPlan("", "", "", "", "", None, 0, 0, "")
    controleur = controleur(modele, None)
    main_window = MainWindow(controleur)
    controleur.vue = main_window
    
    main_window.show()
    sys.exit(app.exec())