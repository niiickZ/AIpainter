from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QPoint, QThread, QMutex
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from .ImgProcessor import ImgProcessor
import threading

'''backup code 001: 子线程执行AI上色方案2——QThread
class ColorizeThread(QThread):
    def __init__(self, drawingBoard, img_sket, img_style):
        super().__init__()
        self.mutex = QMutex()
        self.drawingBoard = drawingBoard
        self.img_sket = img_sket
        self.img_style = img_style

    def run(self):
        self.mutex.lock()

        img_org = self.drawingBoard.orgImg.copy()
        img_bgr = self.drawingBoard.colorizeAI.colorizeImage(self.img_sket, self.img_style, img_org)
        self.drawingBoard.paintSignal.showSignal.emit(img_bgr)

        self.mutex.unlock()
'''

class DrawingBoard(QLabel):
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
        self.paintSignal = None

        self.threadLock = threading.Lock()

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
                self.getColorScheme()
                self.paintLog.append(self.paintLayer.copy())

    def mouseMoveEvent(self, QMouseEvent):
        if self.leftMousePress:
            self.endPos = QMouseEvent.pos()
            self.update()

    def resizeEvent(self, QResizeEvent):
        self.resizeImg()

    def colorizeThread(self, img_bottom, img_style):
        self.threadLock.acquire()
        img_bgr = self.colorizeAI.colorizeImage(img_bottom, img_style, self.orgImg.copy())
        self.paintSignal.showSignal.emit(img_bgr)
        self.threadLock.release()

    def getColorScheme(self):
        """获取用户涂色后的图片并传递给上色AI"""
        img_bottom = ImgProcessor.Qimg2opencv(self.imgLayer) # 将QPixmap对象转化为opencv对象
        img_top = ImgProcessor.Qimg2opencv(self.paintLayer)
        img_style = ImgProcessor.coverImg(img_bottom.copy(), img_top.copy()) # 画板覆盖在原线稿上

        ''' backup code 001: 子线程执行AI上色方案2——QThread
        self.colThread = ColorizeThread(self, img_bottom, img_style)
        self.colThread.start()
        '''

        # 在子线程中执行AI上色，避免AI上色时ui界面假死
        threading.Thread(target=self.colorizeThread,
                         args=(img_bottom, img_style),
                         daemon=True).start()

    def resizeImg(self):
        if self.imgLayer == None:
            return

        self.imgLayer = self.orgPixmap.copy()
        self.paintLayer = self.paintLayer.scaled(
            self.imgLayer.width(), self.imgLayer.height())

        scale_x = (self.width() - 80) / self.imgLayer.width()
        scale_y = (self.height() - 80) / self.imgLayer.height()
        scale = min(scale_x, scale_y)
        scale = min(scale, 2.2)

        size = self.imgLayer.size()
        self.imgLayer = self.imgLayer.scaled(scale * size)
        self.paintLayer = self.paintLayer.scaled(scale * size)

        # 图片居中，记录左上角坐标
        x = int((self.width() - self.imgLayer.width()) / 2)
        y = int((self.height() - self.imgLayer.height()) / 2)
        self.imgLoc = (x, y)

        self.update()

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
        self.orgImg = img.copy()
        self.orgPixmap = ImgProcessor.opencv2Qimg(img.copy())

        self.imgLayer = self.orgPixmap.copy()

        self.paintLayer.fill(Qt.transparent)
        self.paintLayer = self.paintLayer.scaled(
            self.imgLayer.width(), self.imgLayer.height())

        self.paintLog.clear()
        self.paintLog.append(self.paintLayer.copy())

        self.resizeImg()
        self.update()