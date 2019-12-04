import sys

from PyQt5.QtWidgets import QApplication
from client_controller import Controller

if __name__ == "__main__":
    app = QApplication([])  # Instantiate the QApplication
    window = Controller()  # Instantiate the controller (the QMainWindow)
    window.show()  # Show the window
    sys.exit(app.exec())  # Start the application thread
