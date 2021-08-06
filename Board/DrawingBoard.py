from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QPoint, QThread, QMutex
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from .ImgProcessor import ImgProcessor
import threading

'''暂未完成的功能(1)
class ColorizeThread(QThread):
    def __init__(self, colSignal, showSignal, img_sket, img_style):
        super().__init__()
        self.mutex = QMutex()
        self.colSignal = colSignal
        self.showSignal = showSignal
        self.img_sket = img_sket
        self.img_style = img_style

    def run(self):
        self.mutex.lock()
        self.colSignal.emit(self.img_sket, self.img_style)
        self.showSignal.emit()
        self.mutex.unlock()
'''

class DrawingBoard(QLabel, ImgProcessor):
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
        self.paintLog = [] #画板图层历史

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
                self.paintLog.append(self.paintLayer.copy())

    def mouseMoveEvent(self, QMouseEvent):
        if self.leftMousePress:
            self.endPos = QMouseEvent.pos()
            self.update()

    def downloadImg(self):
        """获取用户涂色后的图片并传递给上色AI"""

        ''' 暂未完成的功能(2)
        def colorizeThread(img_bottom, img_style):
            self.paintComplete.colorizeSignal.emit(img_bottom, img_style)
            self.paintComplete.showSignal.emit()
        '''

        img_bottom = self.Qimg2opencv(self.imgLayer) # 将QPixmap对象转化为opencv对象
        img_top = self.Qimg2opencv(self.paintLayer)
        img_style = self.coverImg(img_bottom.copy(), img_top.copy()) # 画板覆盖在原线稿上

        ''' 暂未完成的功能(1)——AI上色时左侧画板可继续涂写(QThread)
        self.colThread = ColorizeThread(
            self.paintComplete.colorizeSignal,
            self.paintComplete.showSignal,
            img_bottom, img_style)
        self.colThread.start()
        '''

        ''' 暂未完成的功能(2)——AI上色时左侧画板可继续涂写(threading)
        threading.Thread(target=colorizeThread, args=(img_bottom, img_style), daemon=True).start()
        '''

        self.paintComplete.waitSignal.emit()
        self.paintComplete.colorizeSignal.emit(img_bottom, img_style, self.orgImg)
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
        self.imgLayer = self.opencv2Qimg(self.orgImg)
        self.paintLayer = self.paintLayer.scaled(
            self.imgLayer.width(), self.imgLayer.height())

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
        col = QColor(self.penCol) if self.using == self.pen else QColor(Qt.white)
        qpen = QPen(col, self.penDiameter, Qt.SolidLine)
        qp.setPen(qpen)

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

    def loadImg(self, img):
        self.orgImg = img
        pixmap = self.opencv2Qimg(img)

        self.imgLayer = pixmap

        self.paintLayer.fill(Qt.transparent)
        self.paintLayer = self.paintLayer.scaled(
            self.imgLayer.width(), self.imgLayer.height())

        self.paintLog.clear()
        self.paintLog.append(self.paintLayer.copy())

        self.update()