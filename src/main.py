from PyQt6.QtWidgets import QApplication
from desktop_pet.desktop_pet import DesktopPet

if __name__ == '__main__':
    app = QApplication([])
    pet = DesktopPet()
    app.exec()
