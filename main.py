import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from modelPlanB import modelPlan
from vueAppliB import MainWindow
from controleurB import controleur

if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = modelPlan("", "", "", "", "", None, 0, 0, "")
    controleur_instance = controleur(model, None)
    window = MainWindow(controleur_instance)
    controleur_instance.vue = window
    window.show()
    sys.exit(app.exec())
    