from PyQt5 import QtWidgets as QtW


class MainWindow(QtW.QWidget):
    TITLE = "KeyNai"

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.TITLE)
        self.config_layout()
        self.show()

    def config_layout(self):
        self.setLayout(QtW.QVBoxLayout())


if __name__ == '__main__':
    app = QtW.QApplication([])
    mw = MainWindow()
    app.exec_()