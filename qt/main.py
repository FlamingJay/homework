from PyQt5.QtWidgets import QApplication, QMainWindow
from shortVideo import Ui_MainWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()

    ui_components = Ui_MainWindow()
    ui_components.setupUi(mainWindow)

    mainWindow.show()
    sys.exit(app.exec_())