import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap

class ImgProcess:
    def opencv2Qimg(self, img):
        """将opencv对象转换为QPixmap对象"""
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        QImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(QImg)
        return pixmap

    def Qimg2opencv(self, pixmap):
        """将QPixmap对象转换为opencv对象"""
        # 复制的玄学代码
        Qimg = pixmap.toImage()
        temp_shape = (Qimg.height(), Qimg.bytesPerLine() * 8 // Qimg.depth())
        temp_shape += (4,)
        ptr = Qimg.bits()
        ptr.setsize(Qimg.byteCount())
        result = np.array(ptr, dtype=np.uint8).reshape(temp_shape)
        return result[..., :3]

    def coverImg(self, img_bottom, img_top):
        """将img_top覆盖在img_bottom上"""
        # 创建掩膜
        img_gray = cv2.cvtColor(img_top, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img_gray, 10, 255, cv2.THRESH_BINARY_INV)
        # 保留除img_bottom外的背景
        # bitwise_and将掩膜与原图进行与运算, AND=0的点为黑色(0), ADN=原值的不变
        img_bg = cv2.bitwise_and(img_bottom, img_bottom, mask=mask)
        dst = cv2.add(img_bg, img_top)  # 进行融合

        return dst