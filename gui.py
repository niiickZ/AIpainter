# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from Board.DrawingBoard import DrawingBoard
from Board.ShowBoard import ShowBoard

class Ui_Home(object):
    def setupUi(self, Home):
        Home.setObjectName("Home")
        Home.resize(1300, 820)
        Home.setMinimumSize(QtCore.QSize(1300, 820))
        Home.setStyleSheet("#Home\n"
"{\n"
"    background-color: #EED2EE;\n"
"}")
        self.gridLayout_2 = QtWidgets.QGridLayout(Home)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.boardFrame = QtWidgets.QFrame(Home)
        self.boardFrame.setMinimumSize(QtCore.QSize(1130, 0))
        self.boardFrame.setStyleSheet("")
        self.boardFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.boardFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.boardFrame.setObjectName("boardFrame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.boardFrame)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.showFrame = QtWidgets.QFrame(self.boardFrame)
        self.showFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.showFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.showFrame.setObjectName("showFrame")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.showFrame)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.showBoard = ShowBoard(self.showFrame)
        self.showBoard.setMinimumSize(QtCore.QSize(520, 650))
        self.showBoard.setStyleSheet("QLabel\n"
"{\n"
"    background-color: #E0EEEE;\n"
"    border-radius: 8px;\n"
"}")
        self.showBoard.setText("")
        self.showBoard.setObjectName("showBoard")
        self.gridLayout_5.addWidget(self.showBoard, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.downloadButton = QtWidgets.QPushButton(self.showFrame)
        self.downloadButton.setMinimumSize(QtCore.QSize(150, 55))
        self.downloadButton.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.downloadButton.setFont(font)
        self.downloadButton.setStyleSheet(".QPushButton\n"
"{\n"
"    border-radius: 6px;\n"
"    background-color: transparent;\n"
"    border: 2px solid gray;\n"
"}\n"
"\n"
".QPushButton:hover\n"
"{\n"
"    color: white;\n"
"    border-width: 1px;\n"
"}\n"
"\n"
".QPushButton:pressed\n"
"{ \n"
"    border-style: inset; \n"
"    border-width: 3px;\n"
"    /*color: black;*/\n"
"}")
        self.downloadButton.setObjectName("downloadButton")
        self.horizontalLayout_2.addWidget(self.downloadButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout_5.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.showFrame, 0, 1, 1, 1)
        self.drawingFrame = QtWidgets.QFrame(self.boardFrame)
        self.drawingFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.drawingFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.drawingFrame.setObjectName("drawingFrame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.drawingFrame)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.uploadButton = QtWidgets.QPushButton(self.drawingFrame)
        self.uploadButton.setMinimumSize(QtCore.QSize(150, 55))
        self.uploadButton.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.uploadButton.setFont(font)
        self.uploadButton.setStyleSheet(".QPushButton\n"
"{\n"
"    border-radius: 6px;\n"
"    background-color: transparent;\n"
"    border: 2px solid gray;\n"
"}\n"
"\n"
".QPushButton:hover\n"
"{\n"
"    color: white;\n"
"    border-width: 1px;\n"
"}\n"
"\n"
".QPushButton:pressed\n"
"{ \n"
"    border-style: inset; \n"
"    border-width: 3px;\n"
"    /*color: black;*/\n"
"}")
        self.uploadButton.setObjectName("uploadButton")
        self.horizontalLayout.addWidget(self.uploadButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.gridLayout_4.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.drawingBoard = DrawingBoard(self.drawingFrame)
        self.drawingBoard.setMinimumSize(QtCore.QSize(520, 650))
        self.drawingBoard.setStyleSheet("QLabel\n"
"{\n"
"    background-color: #E0EEEE;\n"
"    border-radius: 8px;\n"
"}")
        self.drawingBoard.setText("")
        self.drawingBoard.setObjectName("drawingBoard")
        self.gridLayout_4.addWidget(self.drawingBoard, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.drawingFrame, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.boardFrame, 0, 1, 1, 1)
        self.toolFrame = QtWidgets.QFrame(Home)
        self.toolFrame.setMinimumSize(QtCore.QSize(90, 0))
        self.toolFrame.setMaximumSize(QtCore.QSize(130, 16777215))
        self.toolFrame.setStyleSheet("")
        self.toolFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.toolFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.toolFrame.setObjectName("toolFrame")
        self.gridLayout = QtWidgets.QGridLayout(self.toolFrame)
        self.gridLayout.setObjectName("gridLayout")
        self.placeHolderTop = QtWidgets.QFrame(self.toolFrame)
        self.placeHolderTop.setMinimumSize(QtCore.QSize(48, 50))
        self.placeHolderTop.setMaximumSize(QtCore.QSize(16777215, 80))
        self.placeHolderTop.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.placeHolderTop.setFrameShadow(QtWidgets.QFrame.Raised)
        self.placeHolderTop.setObjectName("placeHolderTop")
        self.gridLayout.addWidget(self.placeHolderTop, 0, 0, 1, 2)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.colorSelector = QtWidgets.QPushButton(self.toolFrame)
        self.colorSelector.setMinimumSize(QtCore.QSize(75, 42))
        self.colorSelector.setMaximumSize(QtCore.QSize(80, 45))
        self.colorSelector.setStyleSheet("#colorSelector\n"
"{\n"
"    border: 3px solid white;\n"
"    border-radius: 8px;\n"
"    background-color: #87CEFA;\n"
"}\n"
"\n"
"#colorSelector:hover\n"
"{\n"
"    border-top: 3px solid qlineargradient(y0:0, y1:1,stop: 0 #ececef, stop: 1 white);\n"
"border-left: 3px solid qlineargradient(x0:0, x1:1,stop: 0 #ececef, stop: 1 white);\n"
" border-bottom: 3px solid qlineargradient(y0:0, y1:1,stop: 0 white, stop: 1  #ececef);\n"
"border-right: 3px solid qlineargradient(x0:0, x1:1,stop:  0 white, stop: 1 #ececef);\n"
"}\n"
"\n"
"#colorSelector:pressed\n"
"{ \n"
"    border-width: 4px;\n"
"}\n"
"")
        self.colorSelector.setText("")
        self.colorSelector.setObjectName("colorSelector")
        self.horizontalLayout_6.addWidget(self.colorSelector)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem5)
        self.gridLayout.addLayout(self.horizontalLayout_6, 1, 0, 1, 2)
        spacerItem6 = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem6, 2, 1, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem7)
        self.diameterSlider = QtWidgets.QSlider(self.toolFrame)
        self.diameterSlider.setMinimumSize(QtCore.QSize(75, 30))
        self.diameterSlider.setMaximumSize(QtCore.QSize(85, 35))
        self.diameterSlider.setMinimum(1)
        self.diameterSlider.setMaximum(50)
        self.diameterSlider.setProperty("value", 15)
        self.diameterSlider.setOrientation(QtCore.Qt.Horizontal)
        self.diameterSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.diameterSlider.setTickInterval(0)
        self.diameterSlider.setObjectName("diameterSlider")
        self.horizontalLayout_8.addWidget(self.diameterSlider)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem8)
        self.gridLayout.addLayout(self.horizontalLayout_8, 3, 0, 1, 2)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem9)
        self.diameterLabel = QtWidgets.QLabel(self.toolFrame)
        self.diameterLabel.setMinimumSize(QtCore.QSize(50, 0))
        self.diameterLabel.setMaximumSize(QtCore.QSize(70, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.diameterLabel.setFont(font)
        self.diameterLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.diameterLabel.setObjectName("diameterLabel")
        self.horizontalLayout_7.addWidget(self.diameterLabel)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem10)
        self.gridLayout.addLayout(self.horizontalLayout_7, 4, 0, 1, 2)
        spacerItem11 = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem11, 5, 1, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem12)
        self.brush = QtWidgets.QPushButton(self.toolFrame)
        self.brush.setMinimumSize(QtCore.QSize(48, 48))
        self.brush.setMaximumSize(QtCore.QSize(52, 52))
        self.brush.setStyleSheet("#brush\n"
"{\n"
"    border: 2px solid black;\n"
"    border-radius: 8px;\n"
"    background-image: url(img/icon/pen.png);\n"
"    background-color: #E8E8E8;\n"
"}\n"
"\n"
"#brush:hover\n"
"{\n"
"    background-color: #CDC9C9;\n"
"}\n"
"\n"
"#brush:pressed\n"
"{ \n"
"    border-style: inset; \n"
"    border-width: 3px;\n"
"    /*background-color: #8B8989;*/\n"
"}")
        self.brush.setText("")
        self.brush.setObjectName("brush")
        self.horizontalLayout_5.addWidget(self.brush)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem13)
        self.gridLayout.addLayout(self.horizontalLayout_5, 6, 0, 1, 2)
        spacerItem14 = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem14, 7, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem15)
        self.eraser = QtWidgets.QPushButton(self.toolFrame)
        self.eraser.setMinimumSize(QtCore.QSize(48, 48))
        self.eraser.setMaximumSize(QtCore.QSize(52, 52))
        self.eraser.setStyleSheet("#eraser\n"
"{\n"
"    border: 2px solid black;\n"
"    border-radius: 8px;\n"
"    background-image: url(img/icon/eraser.png);\n"
"    background-color: #E8E8E8;\n"
"}\n"
"\n"
"#eraser:hover\n"
"{\n"
"    background-color: #CDC9C9;\n"
"}\n"
"\n"
"#eraser:pressed\n"
"{ \n"
"    border-style: inset; \n"
"    border-width: 3px;\n"
"    /*background-color: #8B8989;*/\n"
"}")
        self.eraser.setText("")
        self.eraser.setObjectName("eraser")
        self.horizontalLayout_4.addWidget(self.eraser)
        spacerItem16 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem16)
        self.gridLayout.addLayout(self.horizontalLayout_4, 8, 0, 1, 2)
        spacerItem17 = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem17, 9, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem18 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem18)
        self.resetButton = QtWidgets.QPushButton(self.toolFrame)
        self.resetButton.setMinimumSize(QtCore.QSize(48, 48))
        self.resetButton.setMaximumSize(QtCore.QSize(52, 52))
        self.resetButton.setStyleSheet("#resetButton\n"
"{\n"
"    border: 2px solid black;\n"
"    border-radius: 8px;\n"
"    background-image: url(img/icon/reset.png);\n"
"    background-color: #E8E8E8;\n"
"}\n"
"\n"
"#resetButton:hover\n"
"{\n"
"    background-color: #CDC9C9;\n"
"}\n"
"\n"
"#resetButton:pressed\n"
"{ \n"
"    border-style: inset; \n"
"    border-width: 3px;\n"
"    /*background-color: #8B8989;*/\n"
"}")
        self.resetButton.setText("")
        self.resetButton.setObjectName("resetButton")
        self.horizontalLayout_3.addWidget(self.resetButton)
        spacerItem19 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem19)
        self.gridLayout.addLayout(self.horizontalLayout_3, 10, 0, 1, 2)
        self.placeHolderBottom = QtWidgets.QFrame(self.toolFrame)
        self.placeHolderBottom.setMinimumSize(QtCore.QSize(48, 35))
        self.placeHolderBottom.setMaximumSize(QtCore.QSize(16777215, 390))
        self.placeHolderBottom.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.placeHolderBottom.setFrameShadow(QtWidgets.QFrame.Raised)
        self.placeHolderBottom.setObjectName("placeHolderBottom")
        self.gridLayout.addWidget(self.placeHolderBottom, 11, 0, 1, 2)
        self.gridLayout_2.addWidget(self.toolFrame, 0, 0, 1, 1)

        self.retranslateUi(Home)
        QtCore.QMetaObject.connectSlotsByName(Home)

    def retranslateUi(self, Home):
        _translate = QtCore.QCoreApplication.translate
        Home.setWindowTitle(_translate("Home", "AIpainter"))
        self.downloadButton.setText(_translate("Home", "保存图片"))
        self.uploadButton.setText(_translate("Home", "上传线稿"))
        self.diameterLabel.setText(_translate("Home", "15"))
