from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter
import cv2
from Board.ImgProcess import ImgProcess

class ShowBoard(QLabel, ImgProcess):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.imgLayer = None
        self.imgLoc = (0, 0)

    def saveImg(self, fpath):
        img = self.Qimg2opencv(self.imgLayer)
        cv2.imwrite(fpath, img)

    def revealImg(self):
        # if self.imgLayer.width() > self.width() or self.imgLayer.height() > self.height():
        scale_x = (self.width() - 80) / self.imgLayer.width()
        scale_y = (self.height() - 80) / self.imgLayer.height()
        scale = min(scale_x, scale_y)

        size = self.imgLayer.size()
        self.imgLayer = self.imgLayer.scaled(scale * size)

        # 图片居中，记录左上角坐标
        x = int((self.width() - self.imgLayer.width()) / 2)
        y = int((self.height() - self.imgLayer.height()) / 2)
        self.imgLoc = (x, y)

        painter = QPainter(self)
        painter.begin(self)
        x, y = self.imgLoc[:]
        painter.drawPixmap(x, y, self.imgLayer)
        painter.end()

    def waiting(self):
        """等待AI上色时展板模糊效果"""
        """不知道为啥不起作用，只能先注释掉了"""
        pass
        # img = self.Qimg2opencv(self.imgLayer)
        #
        # height, width = img.shape[:2]
        # k_size = int(min(height, width) / 2)
        # img = cv2.GaussianBlur(img, ksize=(k_size, k_size), sigmaX=15, sigmaY=15)
        #
        # self.imgLayer = self.opencv2Qimg(img)
        # self.update()

    def paintEvent(self, QPaintEvent):
        super().paintEvent(QPaintEvent)

        if self.imgLayer != None:
            self.revealImg()

    def loadImg(self, img):
        pixmap = self.opencv2Qimg(img)

        self.imgLayer = pixmap
        self.update()