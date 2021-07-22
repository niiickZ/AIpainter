from keras.models import Model
from keras.layers import Dropout, Conv2D, UpSampling2D, LeakyReLU, Input, Concatenate
from NeuralNet.NormalizationLayer import InstanceNormalization
import cv2
import numpy as np

class Generator:
    def __init__(self):
        self.img_row = 256
        self.img_col = 256
        self.img_channels = 3
        self.img_shape = (self.img_row, self.img_col, self.img_channels)

    def buildGenerator(self):
        def EnConv2D(lastLayer, filters, k_size=4, norm=True):
            layer = Conv2D(filters, kernel_size=k_size, strides=2, padding='same')(lastLayer)
            layer = LeakyReLU(alpha=0.2)(layer)
            if norm:
                layer = InstanceNormalization()(layer)
            return layer

        def DeConv2D(lastLayer, skipLayer, filters, k_size=4, drop_rate=0.0):
            layer = UpSampling2D()(lastLayer)
            layer = Conv2D(filters, kernel_size=k_size, padding='same', activation='relu')(layer)
            if drop_rate:
                layer = Dropout(drop_rate)(layer)
            layer = InstanceNormalization()(layer)
            layer = Concatenate()([layer, skipLayer])
            return layer

        img_sket = Input(shape=self.img_shape)
        img_style = Input(shape=self.img_shape)

        img_input = Concatenate()([img_sket, img_style])

        encoder1 = EnConv2D(img_input, 64, norm=False)
        encoder2 = EnConv2D(encoder1, 128)
        encoder3 = EnConv2D(encoder2, 256)
        encoder4 = EnConv2D(encoder3, 512)
        encoder5 = EnConv2D(encoder4, 512)
        encoder6 = EnConv2D(encoder5, 512)
        encoder7 = EnConv2D(encoder6, 512)

        decoder1 = DeConv2D(encoder7, encoder6, 512)
        decoder2 = DeConv2D(decoder1, encoder5, 512)
        decoder3 = DeConv2D(decoder2, encoder4, 512)
        decoder4 = DeConv2D(decoder3, encoder3, 256)
        decoder5 = DeConv2D(decoder4, encoder2, 128)
        decoder6 = DeConv2D(decoder5, encoder1, 64)

        decoder7 = UpSampling2D()(decoder6)
        outputLayer = Conv2D(filters=self.img_channels, kernel_size=4, padding='same', activation='tanh')(decoder7)

        return Model([img_sket, img_style], outputLayer)


class Sketch2BGR(Generator):
    def __init__(self, modelPath):
        super().__init__()
        self.generator = self.buildGenerator()
        self.generator.load_weights(modelPath)

    def preWork(self, img):
        img = cv2.resize(img, (256, 256))
        img = np.expand_dims(img, 0)
        img = (img.astype(np.float32) - 127.5) / 127.5
        return img

    def colorizeImage(self, img_sket, img_style):
        img_sket = self.preWork(img_sket)

        img_style = cv2.GaussianBlur(img_style, ksize=(255, 255), sigmaX=18, sigmaY=18)
        # cv2.imwrite('style.png', img_style) # del
        img_style = self.preWork(img_style)

        img_bgr = self.generator.predict([img_sket, img_style])[0]
        img_bgr = img_bgr * 127.5 + 127.5
        img_bgr = img_bgr.astype(np.uint8)

        return img_bgr