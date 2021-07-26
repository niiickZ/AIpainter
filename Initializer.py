from PyQt5.QtWidgets import QColorDialog, QFileDialog
from PyQt5.QtGui import QPixmap, QCursor, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QPoint
import os
import numpy as np
import cv2
from NeuralNet.Generator import Sketch2BGR

class Function:
    def getColor(self, Home):
        """从调色板获取画笔颜色"""
        col = QColorDialog.getColor(QColor(Home.drawingBoard.penCol))
        if col.isValid():
            Home.colorSelector.setStyleSheet("#colorSelector\n"
                "{\n"
                "    border: 3px solid white;\n"
                "    border-radius: 8px;\n"
                "    background-color: %s;\n"
                "}" % col.name())

            Home.drawingBoard.penCol = col.name()
            self.changeUse(Home, Home.drawingBoard.pen)

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
        Home.drawingBoard.loadImg(img)
        Home.showBoard.loadImg(img)

        # 第一次上传图片后将画笔等按钮激活
        if Home.downloadButton.isEnabled() == False:
            Home.downloadButton.setEnabled(True)
            Home.brush.setEnabled(True)
            Home.eraser.setEnabled(True)
            Home.resetButton.setEnabled(True)

            self.changeUse(Home, Home.drawingBoard.pen)

    def getDiameter(self, Home):
        """从滑动槽控件diameterSlider获取画笔直径"""
        value = Home.diameterSlider.value()
        Home.diameterLabel.setText("{}".format(value))
        Home.drawingBoard.penDiameter = value

    def changeUse(self, Home, flag):
        """画笔/橡皮转换"""
        Home.drawingBoard.using = flag

        if flag == Home.drawingBoard.pen:
            icon = QPixmap("img/cursor/pen.png")
        else:
            icon = QPixmap("img/cursor/eraser.png")

        cursor = QCursor(icon, 0, icon.height()) # 参数2,3为光标作用位置
        Home.drawingBoard.setCursor(cursor)

    def resetDrawingBoard(self, Home):
        """删除所有画笔痕迹，重置为原图"""
        Home.drawingBoard.paintLayer.fill(Qt.transparent)
        Home.drawingBoard.update()
        Home.drawingBoard.downloadImg()

    def downloadImg(self, Home):
        """将AI上色后的图片下载到本地"""
        fpath, _ = QFileDialog.getSaveFileName(
            Home, "选择保存目录",
            os.path.join(os.path.expanduser('~'), "Desktop"),
            "PNG(*.png);;JPG(*.jpg);;JEPG(*.jepg)"
        )
        if fpath != '':
            Home.showBoard.saveImg(fpath)

    def waitMsg(self, Home):
        Home.showBoard.waiting()

    def colorize(self, img_sket, img_style, img_org):
        """将原图和配色图传递给AI上色"""
        self.img_bgr = self.colorizeAI.colorizeImage(img_sket, img_style, img_org)

    def sendImg(self, Home):
        """将AI上色后的图片显示在右侧展示板"""
        Home.showBoard.loadImg(self.img_bgr)

class Signal(QObject):
    waitSignal = pyqtSignal()
    colorizeSignal = pyqtSignal(np.ndarray, np.ndarray, np.ndarray)
    showSignal = pyqtSignal()

class Initializer(Function):
    def __init__(self):
        modelPath = os.path.join(os.getcwd(), "NeuralNet\\model\\weights.h5")
        self.colorizeAI = Sketch2BGR(modelPath)
        self.img_bgr = None

    def initWidget(self, Home):
        """初始未上传图片时画笔/橡皮/重置/下载按钮不可用"""
        Home.downloadButton.setDisabled(True)
        Home.brush.setDisabled(True)
        Home.eraser.setDisabled(True)
        Home.resetButton.setDisabled(True)

    def eventBond(self, Home):
        """关联按钮点击事件和涂色事件"""
        Home.colorSelector.clicked.connect(lambda: self.getColor(Home))
        Home.diameterSlider.valueChanged.connect(lambda: self.getDiameter(Home))

        Home.brush.clicked.connect(lambda: self.changeUse(Home, Home.drawingBoard.pen))
        Home.eraser.clicked.connect(lambda: self.changeUse(Home, Home.drawingBoard.eraser))
        Home.resetButton.clicked.connect(lambda: self.resetDrawingBoard(Home))

        Home.uploadButton.clicked.connect(lambda: self.uploadImg(Home))
        Home.downloadButton.clicked.connect(lambda: self.downloadImg(Home))

        Home.drawingBoard.paintComplete = Signal()
        Home.drawingBoard.paintComplete.waitSignal.connect(lambda: self.waitMsg(Home))
        Home.drawingBoard.paintComplete.colorizeSignal.connect(self.colorize)
        Home.drawingBoard.paintComplete.showSignal.connect(lambda: self.sendImg(Home))
