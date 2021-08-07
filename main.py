import sys
from PyQt5.QtWidgets import QApplication, QWidget
from gui import Ui_Home
from Initializer import Initializer

class MyWindow(QWidget, Ui_Home, Initializer):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initialize(self)

def main():
    app = QApplication(sys.argv)

    myWin = MyWindow()
    myWin.showMaximized()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()