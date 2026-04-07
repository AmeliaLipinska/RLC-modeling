import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():

    #creating an instalation of aplication /object of aplication
    app=QApplication(sys.argv)

    #creating an object of my window
    window=MainWindow()

    #displaying the window on the screen
    window.show()

    #event loop starts and waits for the app to close
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 