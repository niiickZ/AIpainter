from keras.models import Model
from keras.layers import Dropout, Conv2D, UpSampling2D, LeakyReLU, Input, Concatenate, Activation
from .NormalizationLayer import InstanceNormalization
import cv2
import numpy as np
import tensorflow as tf

class Generator:
    def __init__(self):
        self.img_row = None
        self.img_col = None
        self.img_channels = 3
        self.img_shape = (self.img_row, self.img_col, self.img_channels)

    def buildGenerator(self):
        def EnConv2D(inputs, filters, k_size=4, norm=True):
            x = Conv2D(filters, kernel_size=k_size, strides=2, padding='same')(inputs)
            if norm:
                x = InstanceNormalization()(x)
            x = LeakyReLU(alpha=0.2)(x)
            return x

        def DeConv2D(inputs, skipInputs, filters, k_size=4, drop_rate=0.0):
            x = UpSampling2D()(inputs)
            x = Conv2D(filters, kernel_size=k_size, padding='same')(x)
            x = InstanceNormalization()(x)
            x = Activation('relu')(x)
            outputs = Concatenate()([x, skipInputs])
            if drop_rate:
                outputs = Dropout(drop_rate)(outputs)
            return outputs

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
        img_output = Conv2D(filters=self.img_channels, kernel_size=4, padding='same', activation='tanh')(decoder7)

        return Model([img_sket, img_style], img_output)


class Sketch2BGR(Generator):
    def __init__(self, modelPath):
        super().__init__()
        self.generator = self.buildGenerator()
        self.generator.load_weights(modelPath)

        '''notice tag 001: ??????????????????predict?????????????????????'''
        self.graph = tf.get_default_graph()

    def preWork(self, img, orgShape, blur=False):
        """?????????????????????????????????????????????"""

        ''' ?????????????????????????????????????????????????????????'''
        if 512 / max(orgShape[:2]) <= 1.2:
            height, width = img.shape[:2]
            scale = 512 / max(height, width)
            img = cv2.resize(img, None, fx=scale, fy=scale)
        else:
            # ???????????????????????????????????????????????????????????????
            img = cv2.resize(img, (orgShape[1], orgShape[0]))

        height, width = img.shape[:2]

        # ???????????????128???????????????
        tmp = height % 128
        height = height - (tmp if tmp <= 64 else tmp-128)
        tmp = width % 128
        width = width - (tmp if tmp <= 64 else tmp-128)

        img = cv2.resize(img, (width, height))

        if blur:
            img = cv2.GaussianBlur(img, ksize=(133, 133), sigmaX=16, sigmaY=16)
        img = np.expand_dims(img, 0) # (1, height, width, channels)
        img = (img.astype(np.float32) - 127.5) / 127.5 # ?????????
        return img

    def colorizeImage(self, img_sket, img_style, orgImg):
        orgShape = orgImg.shape
        img_sket = self.preWork(img_sket, orgShape)
        img_style = self.preWork(img_style, orgShape, blur=True)

        '''notice tag 001: ??????????????????predict?????????????????????'''
        with self.graph.as_default():
            img_bgr = self.generator.predict([img_sket, img_style])[0]

        img_bgr = img_bgr * 127.5 + 127.5
        img_bgr = img_bgr.astype(np.uint8)

        return img_bgr