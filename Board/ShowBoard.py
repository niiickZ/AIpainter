from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QPainter, QImage
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

    def paintEvent(self, QPaintEvent):
        super().paintEvent(QPaintEvent)

        if self.imgLayer != None:
            self.revealImg()

    def loadImg(self, img):
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)

        QImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(QImg)

        self.imgLayer = pixmap
        self.update()