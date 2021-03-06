"""
    训练时使用的模型，改编自pix2pix
"""

from keras.models import Model
from keras.layers import Dropout, Conv2D, UpSampling2D, LeakyReLU, Input, Concatenate, Activation
from keras.optimizers import Adam
from keras.initializers import RandomNormal
from .NormalizationLayer import InstanceNormalization
import os
import cv2
import numpy as np
import random

class ImageProcessor:
    @staticmethod
    def norm(x):
        """ 归一化 """
        return (x.astype(np.float32) - 127.5) / 127.5

    @staticmethod
    def unNorm(x):
        """ 去归一化 """
        return x * 127.5 + 127.5

    @staticmethod
    def preprocess(img):
        '''将原彩色图处理为配色方案'''

        # 随机挖空一部分16x16的patch，模拟损坏的信息
        patchs = 16
        for i in range(128):
            x = random.randint(0, img.shape[0] - patchs)
            y = random.randint(0, img.shape[1] - patchs)

            img[x: x + patchs, y: y + patchs, :] = 255

        # 将图片加上强模糊
        colScheme = cv2.GaussianBlur(img, ksize=(113, 113), sigmaX=15, sigmaY=15)
        return colScheme

class DataLoader:
    def __init__(self, dir_A, dir_B, batch_size, img_shape):
        self.dir_A = dir_A
        self.dir_B = dir_B

        self.flist = os.listdir(dir_A)
        self.fnum = len(self.flist)

        self.batch_size = batch_size
        self.img_shape = img_shape

        self.idx_cur = 0

    def getNumberOfBatch(self):
        num = self.fnum / self.batch_size
        if self.fnum % self.batch_size != 0:
            num += 1
        return int(num)

    def reset(self):
        self.idx_cur = 0
        random.shuffle(self.flist)

    def __iter__(self):
        return self

    def __next__(self):
        if self.idx_cur >= self.fnum:
            self.reset()
            raise StopIteration

        if self.idx_cur+self.batch_size-1 < self.fnum:
            length = self.batch_size
            idx_nxt = self.idx_cur+self.batch_size
        else:
            length = self.fnum-self.idx_cur
            idx_nxt = self.fnum

        imgBGR = np.zeros((length, *self.img_shape))
        imgSketch = np.zeros((length, *self.img_shape))
        imgStyle = np.zeros((length, *self.img_shape))

        for k in range(length):
            fpath_A = os.path.join(self.dir_A, self.flist[self.idx_cur+k])
            fpath_B = os.path.join(self.dir_B, self.flist[self.idx_cur+k])

            img_bgr = cv2.imread(fpath_A, 1)
            img_sketch = cv2.imread(fpath_B, 1)

            img_blur = ImageProcessor.preprocess(np.copy(img_bgr))

            imgBGR[k] = ImageProcessor.norm(img_bgr)
            imgSketch[k] = ImageProcessor.norm(img_sketch)
            imgStyle[k] = ImageProcessor.norm(img_blur)

        self.idx_cur = idx_nxt

        return imgBGR, imgSketch, imgStyle

class Sketch2BGR:
    def __init__(self):
        self.img_row = 256
        self.img_col = 256
        self.img_channels = 3
        self.input_shape = (None, None, self.img_channels)

        patch = int(self.img_row / 2 ** 3)
        self.discPatch = (patch, patch, 1)

        self.buildGAN()

    def buildGenerator(self):
        """ 构造generator
            encoder: C64-C128-C256-C512-C512-C512-C512
            decoder: C512-C512-C512-C256-C128-C64
            encoder与decoder间包含skip connections
            最后upsample(factor=2) - C3
        """

        initWeight = RandomNormal(stddev=0.02)

        def EnConv2D(inputs, filters, k_size=4, norm=True):
            ''' 构造encoder的一层
                Conv-InstanceNorm-LeakyReLu
            '''
            x = Conv2D(filters, kernel_size=k_size, strides=2, padding='same', kernel_initializer=initWeight)(inputs)
            if norm:
                x = InstanceNormalization()(x)
            x = LeakyReLU(alpha=0.2)(x)
            return x

        def DeConv2D(inputs, skipInputs, filters, k_size=4, drop_rate=0.0):
            ''' 构造decoder的一层
                upsample-Conv-InstanceNorm-ReLU-Concat-(DropOut)
            '''
            x = UpSampling2D()(inputs)
            x = Conv2D(filters, kernel_size=k_size, padding='same', kernel_initializer=initWeight)(x)
            x = InstanceNormalization()(x)
            x = Activation('relu')(x)
            outputs = Concatenate()([x, skipInputs])
            if drop_rate:
                outputs = Dropout(drop_rate)(outputs)
            return outputs

        # 直接concat原线稿与配色方案图作为输入
        img_sket = Input(shape=self.input_shape)
        img_style = Input(shape=self.input_shape)

        img_input = Concatenate()([img_sket, img_style])

        # encoder
        encoder1 = EnConv2D(img_input, 64, norm=False)
        encoder2 = EnConv2D(encoder1, 128)
        encoder3 = EnConv2D(encoder2, 256)
        encoder4 = EnConv2D(encoder3, 512)
        encoder5 = EnConv2D(encoder4, 512)
        encoder6 = EnConv2D(encoder5, 512)
        encoder7 = EnConv2D(encoder6, 512)

        # decoder
        decoder1 = DeConv2D(encoder7, encoder6, 512)
        decoder2 = DeConv2D(decoder1, encoder5, 512)
        decoder3 = DeConv2D(decoder2, encoder4, 512)
        decoder4 = DeConv2D(decoder3, encoder3, 256)
        decoder5 = DeConv2D(decoder4, encoder2, 128)
        decoder6 = DeConv2D(decoder5, encoder1, 64)

        # upsample + C3
        decoder7 = UpSampling2D()(decoder6)
        img_output = Conv2D(filters=self.img_channels, kernel_size=4, padding='same', activation='tanh', kernel_initializer=initWeight)(decoder7)

        return Model([img_sket, img_style], img_output)

    def buildDiscriminator(self):
        """ 构造discriminator
            C64-C128-C256-C512-C1
        """
        initWeight = RandomNormal(stddev=0.02)

        def discLayer(inputs, filters, k_size=4, stride=2, norm=True):
            ''' 构造disc的一层
                Conv-InstanceNorm-LeakyRelu
            '''
            x = Conv2D(filters, kernel_size=k_size, strides=stride, padding='same', kernel_initializer=initWeight)(inputs)
            if norm:
                x = InstanceNormalization()(x)
            outputs = LeakyReLU(alpha=0.2)(x)
            return outputs

        # 根据cgan结构，concat彩色图、线稿图和配色方案图作为输入
        img_bgr = Input(shape=self.input_shape)
        img_sket = Input(shape=self.input_shape)
        img_style = Input(shape=self.input_shape)

        img_input = Concatenate()([img_bgr, img_sket, img_style])

        # 构造disc
        disc1 = discLayer(img_input, 64, norm=False)
        disc2 = discLayer(disc1, 128)
        disc3 = discLayer(disc2, 256)
        disc4 = discLayer(disc3, 512, stride=1)

        validity = Conv2D(filters=1, kernel_size=4, padding='same', activation='sigmoid', kernel_initializer=initWeight)(disc4)

        return Model([img_bgr, img_sket, img_style], validity)

    def buildGAN(self):
        # 获得生成器和判别器
        self.generator = self.buildGenerator()
        self.discriminator = self.buildDiscriminator()

        optimizer = Adam(2e-4, 0.5)
        self.discriminator.compile(loss='mse', optimizer=optimizer, metrics=['accuracy'])
        self.discriminator.trainable = False  # disc在compile之后设置trainable为False，使得训练combined时冻结disc

        # 原线稿和配色方案的输入张量
        img_sket = Input(shape=self.input_shape)
        img_style = Input(shape=self.input_shape)

        img_fake = self.generator([img_sket, img_style])  # generator输出的假彩色图张量
        validity = self.discriminator([img_fake, img_sket, img_style])  # discriminator输出的包含每个patch的二分类张量

        # combined model的loss为 G = arg min_G max_D ( L_cgan(G, D) + λL1 )
        self.combined = Model([img_sket, img_style], [validity, img_fake])
        self.combined.compile(loss=['mse', 'mae'], loss_weights=[1, 100], optimizer=optimizer)

    def trainModel(self, epochs, batch_size=1):
        """训练模型 generator每轮都训练，discriminator每两轮训练一次"""

        self.dataLoader = DataLoader(
            dir_A='../input/anime-sketch-colorization/data/trainA',
            dir_B='../input/anime-sketch-colorization/data/trainB',
            batch_size=batch_size,
            img_shape=(self.img_row, self.img_col, self.img_channels)
        )

        totalStep = self.dataLoader.getNumberOfBatch()  # 每个epoch训练轮数
        for epoch in range(epochs):
            for step, (img_bgr, img_sket, img_style) in enumerate(self.dataLoader):
                # 为训练准备的全0张量和全1张量
                valid = np.ones((img_bgr.shape[0],) + self.discPatch)
                fake = np.zeros((img_bgr.shape[0],) + self.discPatch)

                # generator先生成假图片
                img_fake = self.generator.predict([img_sket, img_style])

                # 训练discriminator
                if step % 2 == 0:
                    D_loss_real = self.discriminator.train_on_batch([img_bgr, img_sket, img_style], valid)
                    D_loss_fake = self.discriminator.train_on_batch([img_fake, img_sket, img_style], fake)
                    D_loss = 0.5 * np.add(D_loss_real, D_loss_fake)

                # 训练combined model
                G_loss = self.combined.train_on_batch([img_sket, img_style], [valid, img_bgr])

                # 打印loss
                if step % 2 == 0:
                    print('Epoch {}/{} : Batch {}/{} -- D loss: {:.6f}, acc: {:.2f} , G loss: {:.6f}, MAE loss: {:.6f}'.format(
                        epoch+1, epochs, step+1, totalStep, D_loss[0], D_loss[1] * 100, G_loss[0], G_loss[1]))
                else:
                    print('Epoch {}/{} : Batch {}/{} -- D loss: --------, acc: ----- , G loss: {:.6f}, MAE loss: {:.6f}'.format(
                        epoch+1, epochs, step+1, totalStep, G_loss[0], G_loss[1]))

                # 上色测试
                if (step + 1) % 200 == 0:
                    fpathA = '../input/anime-sketch-colorization/data/testA/1047028.png'
                    fpathB = '../input/anime-sketch-colorization/data/testB/1047028.png'
                    fname = 'output{}.png'.format(epoch)
                    self.colorizeImage(fpathA=fpathA, fpathB=fpathB, outputDir='./', fname=fname)

            self.generator.save_weights('./generator{}.h5'.format(epoch))

    def colorizeImage(self, fpathA, fpathB, outputDir, fname):
        """ 用generator上色"""

        def preWork(img):
            '''预处理图片'''
            img = cv2.resize(img, (256, 256))
            img = np.expand_dims(img, 0)
            img = ImageProcessor.norm(img)

            return img

        img_input = cv2.imread(fpathB, 1)
        # img_style = cv2.imread('tmp/style.png', 1)
        img_style = ImageProcessor.preprocess(cv2.imread(fpathA, 1))

        img_input = preWork(img_input)
        img_style = preWork(img_style)

        img_output = self.generator.predict([img_input, img_style])[0]
        img_output = ImageProcessor.unNorm(img_output)
        img_output = img_output.astype(np.uint8)

        outputPath = os.path.join(outputDir, fname)
        cv2.imwrite(outputPath, img_output)