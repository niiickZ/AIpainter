from PyQt5.QtWidgets import QColorDialog, QFileDialog
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import os
import numpy as np
import cv2
from NeuralNet.Generator import Sketch2BGR

class Function:
    def getColor(self, Home):
        col = QColorDialog.getColor()
        if col.isValid():
            Home.colorSelector.setStyleSheet("#colorSelector\n"
                "{\n"
                "    border: 3px solid white;\n"
                "    border-radius: 8px;\n"
                "    background-color: %s;\n"
                "}" % col.name())

            Home.drawingBoard.penCol = col.name()

    def uploadImg(self, Home):
        fpath, _ = QFileDialog.getOpenFileName(
            Home, "选择图片",
            os.path.join(os.path.expanduser('~'), "Desktop"),
            "所有文件(*.jpg *.png *.jpeg);;(*.jpg);;(*.png);;(*.jepg)"
        )
        if fpath == '':
            return

        Home.drawingBoard.loadImg(fpath)
        Home.showBoard.loadImg(cv2.imread(fpath, 1))

        if Home.downloadButton.isEnabled() == False:
            Home.downloadButton.setEnabled(True)
            Home.brush.setEnabled(True)
            Home.eraser.setEnabled(True)
            Home.resetButton.setEnabled(True)

            self.changeUse(Home, Home.drawingBoard.pen)

    def getDiameter(self, Home):
        value = Home.diameterSlider.value()
        Home.diameterLabel.setText("{}".format(value))
        Home.drawingBoard.penDiameter = value

    def changeUse(self, Home, flag):
        Home.drawingBoard.using = flag

        if flag == 0:
            icon = QPixmap('img/cursor/pen.png')
        else:
            icon = QPixmap('img/cursor/eraser.png')

        cursor = QCursor(icon, 0, icon.height()) # 参数2,3为光标作用位置
        Home.drawingBoard.setCursor(cursor)

    def resetDrawingBoard(self, Home):
        Home.drawingBoard.paintLayer.fill(Qt.transparent)
        Home.drawingBoard.update()
        Home.drawingBoard.downloadImg()

    def downloadImg(self, Home):
        fpath, _ = QFileDialog.getSaveFileName(
            Home, "选择保存目录",
            os.path.join(os.path.expanduser('~'), "Desktop"),
            "PNG(*.png);;JPG(*.jpg);;JEPG(*.jepg)"
        )
        if fpath != '':
            Home.showBoard.saveImg(fpath)

    def colorize(self, img_sket, img_style):
        self.img_bgr = self.colorizeAI.colorizeImage(img_sket, img_style)

    def sendImg(self, Home):
        Home.showBoard.loadImg(self.img_bgr)

class Signal(QObject):
    colorizeSignal = pyqtSignal(np.ndarray, np.ndarray)
    showSignal = pyqtSignal()

class Initializer(Function):
    def __init__(self):
        modelPath = os.path.join(os.getcwd(), "NeuralNet\\model\\weights.h5")
        self.colorizeAI = Sketch2BGR(modelPath)
        self.img_bgr = None

    def initWidget(self, Home):
        Home.downloadButton.setDisabled(True)
        Home.brush.setDisabled(True)
        Home.eraser.setDisabled(True)
        Home.resetButton.setDisabled(True)

    def eventBond(self, Home):
        Home.colorSelector.clicked.connect(lambda: self.getColor(Home))
        Home.diameterSlider.valueChanged.connect(lambda: self.getDiameter(Home))

        Home.brush.clicked.connect(lambda: self.changeUse(Home, Home.drawingBoard.pen))
        Home.eraser.clicked.connect(lambda: self.changeUse(Home, Home.drawingBoard.eraser))
        Home.resetButton.clicked.connect(lambda: self.resetDrawingBoard(Home))

        Home.uploadButton.clicked.connect(lambda: self.uploadImg(Home))
        Home.downloadButton.clicked.connect(lambda: self.downloadImg(Home))

        Home.drawingBoard.paintComplete = Signal()
        Home.drawingBoard.paintComplete.colorizeSignal.connect(self.colorize)
        Home.drawingBoard.paintComplete.showSignal.connect(lambda: self.sendImg(Home))
