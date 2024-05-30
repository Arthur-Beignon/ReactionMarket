import sys
from PyQt6.QtWidgets import QApplication
from modelPlan import modelPlan
from vueAppliA import MainWindow
from controleur import controleur

if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = modelPlan("", "", "", "", "", None, 0, 0, "")
    controleur_instance = controleur(model, None)
    window = MainWindow(controleur_instance)
    controleur_instance.vue = window
    window.show()
    sys.exit(app.exec())