from PyQt5.QtWidgets import QColorDialog, QFileDialog
from PyQt5.QtGui import QPixmap, QCursor, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QPoint
import os
import numpy as np
import cv2
from NeuralNet.Generator import Sketch2BGR

class Function:
    def getColor(self):
        """从调色板获取画笔颜色"""
        col = QColorDialog.getColor(QColor(self.drawingBoard.penCol))
        if col.isValid():
            self.colorSelector.setStyleSheet("#colorSelector\n"
                "{\n"
                "    border: 3px solid white;\n"
                "    border-radius: 8px;\n"
                "    background-color: %s;\n"
                "}" % col.name())

            self.drawingBoard.penCol = col.name()
            self.changeUse(self.drawingBoard.pen)

    def uploadImg(self, Home):
        """上传图片到画板"""
        fpath, _ = QFileDialog.getOpenFileName(
            Home, "选择图片",
            os.path.join(os.path.expanduser('~'), "Desktop"),
            "所有文件(*.jpg *.png *.jpeg);;(*.jpg);;(*.png);;(*.jepg)"
        )
        if fpath == '':
            return

        # 避免路径中包含中文时报错
        img = cv2.imdecode(np.fromfile(fpath, dtype=np.uint8), 1)
        self.drawingBoard.loadImg(img)
        self.showBoard.loadImg(img)

        # 第一次上传图片后将画笔等按钮激活
        if self.downloadButton.isEnabled() == False:
            self.downloadButton.setEnabled(True)
            self.brush.setEnabled(True)
            self.eraser.setEnabled(True)
            self.resetButton.setEnabled(True)
            self.undoButton.setEnabled(True)
            self.colorSelector.setEnabled(True)
            self.diameterSlider.setEnabled(True)

            self.changeUse(self.drawingBoard.pen)

    def getDiameter(self):
        """从滑动槽控件diameterSlider获取画笔直径"""
        value = self.diameterSlider.value()
        self.diameterLabel.setText("{}".format(value))
        self.drawingBoard.penDiameter = value

    def changeUse(self, flag):
        """画笔/橡皮转换"""
        self.drawingBoard.using = flag

        if flag == self.drawingBoard.pen:
            icon = QPixmap("img/cursor/pen.png")
        else:
            icon = QPixmap("img/cursor/eraser.png")

        cursor = QCursor(icon, 0, icon.height())  # 参数2,3为光标作用位置
        self.drawingBoard.setCursor(cursor)

    def resetDrawingBoard(self):
        """删除所有画笔痕迹，重置为原图"""
        self.drawingBoard.paintLayer.fill(Qt.transparent)
        self.drawingBoard.update()
        self.drawingBoard.getColorScheme()
        del(self.drawingBoard.paintLog[1:])

    def undo(self):
        """撤销上一次操作"""
        if len(self.drawingBoard.paintLog) <= 1:
            return

        if len(self.drawingBoard.paintLog) == 2:
            self.drawingBoard.paintLayer.fill(Qt.transparent)
        else:
            self.drawingBoard.paintLayer = self.drawingBoard.paintLog[-2].copy()

        del(self.drawingBoard.paintLog[-1])
        self.drawingBoard.update()
        self.drawingBoard.getColorScheme()

    def downloadImg(self, Home):
        """将AI上色后的图片下载到本地"""
        fpath, _ = QFileDialog.getSaveFileName(
            Home, "选择保存目录",
            os.path.join(os.path.expanduser('~'), "Desktop"),
            "PNG(*.png);;JPG(*.jpg);;JEPG(*.jepg)"
        )
        if fpath != '':
            self.showBoard.saveImg(fpath)

    def waitMsg(self):
        self.showBoard.waiting()

    def colorize(self, img_sket, img_style, img_org):
        """将原图和配色图传递给AI上色"""
        img_bgr = self.colorizeAI.colorizeImage(img_sket, img_style, img_org)
        self.showBoard.loadImg(img_bgr)

class Signal(QObject):
    waitSignal = pyqtSignal()
    colorizeSignal = pyqtSignal(np.ndarray, np.ndarray, np.ndarray)

class Initializer(Function):
    def __init__(self):
        modelPath = os.path.join(os.getcwd(), "NeuralNet\\model\\weights.h5")
        self.colorizeAI = Sketch2BGR(modelPath)

    def initialize(self, Home):
        self.initWidget()
        self.eventBond(Home)

    def initWidget(self):
        """初始未上传图片时画笔/橡皮/重置/下载按钮不可用"""
        self.downloadButton.setDisabled(True)
        self.brush.setDisabled(True)
        self.eraser.setDisabled(True)
        self.resetButton.setDisabled(True)
        self.undoButton.setDisabled(True)
        self.colorSelector.setDisabled(True)
        self.diameterSlider.setDisabled(True)

    def eventBond(self, Home):
        """关联按钮点击事件和涂色事件"""
        self.colorSelector.clicked.connect(self.getColor)
        self.diameterSlider.valueChanged.connect(self.getDiameter)

        self.brush.clicked.connect(lambda: self.changeUse(self.drawingBoard.pen))
        self.eraser.clicked.connect(lambda: self.changeUse(self.drawingBoard.eraser))
        self.resetButton.clicked.connect(self.resetDrawingBoard)
        self.undoButton.clicked.connect(self.undo)

        self.uploadButton.clicked.connect(lambda: self.uploadImg(Home))
        self.downloadButton.clicked.connect(lambda: self.downloadImg(Home))

        self.drawingBoard.paintComplete = Signal()
        self.drawingBoard.paintComplete.waitSignal.connect(self.waitMsg)
        self.drawingBoard.paintComplete.colorizeSignal.connect(self.colorize)
