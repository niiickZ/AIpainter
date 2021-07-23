from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage, QColor
import cv2
from Board.ImgProcess import ImgProcess
import time
import threading

class DrawingBoard(QLabel, ImgProcess):
    pen = 0
    eraser = 1
    def __init__(self, parent=None):
        super().__init__(parent)

        # 鼠标移动事件的起点与终点
        self.startPos = QPoint(0, 0)
        self.endPos = QPoint(0, 0)
        self.leftMousePress = False

        self.imgLayer = None # 线稿图层，用于显示原线稿(QPixmap对象)
        self.paintLayer = QPixmap(200, 200) # 画板图层，用于交互涂色
        self.paintLayer.fill(Qt.transparent)

        self.imgLoc = (0, 0) # 图层的左上角坐标

        # 画笔参数
        self.penCol = "#87CEFA"
        self.penDiameter = 15

        self.using = self.pen

        # 信号传递器
        self.paintComplete = None

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.leftMousePress = True
            self.startPos = QMouseEvent.pos()
            self.endPos = self.startPos

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.leftMousePress = False
            # 获取涂色后的线稿
            if self.imgLayer != None:
                self.downloadImg()

    def mouseMoveEvent(self, QMouseEvent):
        if self.leftMousePress:
            self.endPos = QMouseEvent.pos()
            self.update()

    def downloadImg(self):
        ''' 暂未完成的功能
        def colorizeThread(img_bottom, img_style):
            if cond.acquire():
                self.paintComplete.colorizeSignal.emit(img_bottom, img_style)
                cond.notify()
                cond.release()

        def showThread():
            if cond.acquire():
                cond.wait()
                self.paintComplete.showSignal.emit()
                cond.release()
        '''

        img_bottom = self.Qimg2opencv(self.imgLayer) # 将QPixmap对象转化为opencv对象
        img_top = self.Qimg2opencv(self.paintLayer)
        img_style = self.coverImg(img_bottom.copy(), img_top.copy()) # 画板覆盖在原线稿上

        ''' 暂未完成的功能——AI上色未完成时画板禁用
        cond = threading.Condition()
        threading.Thread(target=showThread, daemon=True).start()
        threading.Thread(target=colorizeThread, args=(img_bottom, img_style), daemon=True).start()
        '''

        self.paintComplete.colorizeSignal.emit(img_bottom, img_style)
        self.paintComplete.showSignal.emit()

    def revealImg(self):
        def checkPos(pos):
            '''检查画笔坐标是否越界'''
            if pos.x() < self.imgLoc[0]:
                return False
            if pos.x() > self.imgLoc[0] + self.paintLayer.width():
                return False
            if pos.y() < self.imgLoc[1]:
                return False
            if pos.y() > self.imgLoc[1] + self.paintLayer.height():
                return False
            return True

        # 图片适应画板大小
        scale_x = (self.width() - 80) / self.imgLayer.width()
        scale_y = (self.height() - 80) / self.imgLayer.height()
        scale = min(scale_x, scale_y)

        size = self.imgLayer.size()
        self.imgLayer = self.imgLayer.scaled(scale * size)
        self.paintLayer = self.paintLayer.scaled(scale * size)

        # 图片居中，记录左上角坐标
        x = int((self.width() - self.imgLayer.width()) / 2)
        y = int((self.height() - self.imgLayer.height()) / 2)
        self.imgLoc = (x, y)

        '''在画板图层涂色'''
        qp = QPainter(self.paintLayer)
        qp.begin(self.paintLayer)

        # 设置画笔
        if self.using == self.pen:
            col = QColor(self.penCol)
        elif self.using == self.eraser:
            col = QColor(Qt.white)
        pen = QPen(col, self.penDiameter, Qt.SolidLine)
        qp.setPen(pen)

        # 沿轨迹涂色
        if self.startPos != self.endPos and checkPos(self.startPos) and checkPos(self.endPos):
            diff = QPoint(self.imgLoc[0], self.imgLoc[1])
            qp.drawLine(self.startPos - diff, self.endPos - diff)

        qp.end()

        self.startPos = self.endPos

        '''重新显示线稿图层与画板图层'''
        painter = QPainter(self)
        painter.begin(self)

        x, y = self.imgLoc[:]
        painter.drawPixmap(x, y, self.imgLayer)
        painter.drawPixmap(x, y, self.paintLayer)

        painter.end()

    def paintEvent(self, QPaintEvent):
        super().paintEvent(QPaintEvent)

        if self.imgLayer != None:
            self.revealImg()

    def loadImg(self, fpath):
        img = cv2.imread(fpath, 1)

        height, width, channel = img.shape
        bytesPerLine = 3 * width
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)

        QImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(QImg)

        self.imgLayer = pixmap
        self.paintLayer = self.paintLayer.scaled(
            self.imgLayer.width(), self.imgLayer.height())

        self.update()