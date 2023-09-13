import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from main_window import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ui = MainWindow()
    # app.setStyle("fusion")
    ui.show()
    sys.exit(app.exec_())
