import sys
from PyQt6.QtWidgets import QApplication
from appli_client import Appli_client

def main():
    # Création de l'application Qt
    app = QApplication(sys.argv)
    
    # Création de l'instance de la vue
    _ = Appli_client() 
    
    # Exécution de l'application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()