import sys
sys.path.append('../')
from PyQt5 import QtCore, QtGui, QtWidgets
import imagesize
import os
import Constants

class cropImageDialog(QtWidgets.QDialog):
    def __init__(self, imagePath, imgIdx):
        super(cropImageDialog, self).__init__(None, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.imagePath = imagePath
        self.imgIdx = imgIdx
        self.processImage()
        self.buildDialog()
        self.sensetivty = 5

    def processImage(self):
        self.tempPath = ""
        startI = self.imagePath.rfind('/', 0, len(self.imagePath)) + 1
        self.image = self.imagePath[startI:]
        self.CropedDone = False
        dotIdx = self.image.find('.', 0, len(self.image))
        self.imageName = self.image[: dotIdx]
        self.imageExtension = self.image[dotIdx:]
        self.ImageDir = self.imagePath[:startI]
        self.imgW, self.imgH = imagesize.get(self.imagePath)
        self.new_imgW, self.new_imgH = self.scaleImage(self.imgW, self.imgH)
        print(self.scale)

    def buildDialog(self):
        iconImage = QtGui.QIcon()
        iconImage.addPixmap(QtGui.QPixmap("Resources/Images/crop-white.png"))
        #self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, True)
        self.setWindowTitle("Crop Image")
        self.setWindowIcon(iconImage)
        self.setFixedSize(self.new_imgW + 180, self.new_imgH + 40)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalimageWidget = QtWidgets.QWidget()
        self.verticalImageLayout = QtWidgets.QVBoxLayout(self.verticalimageWidget)
        self.verticalimageWidget.setGeometry(QtCore.QRect(20, 20, self.new_imgW, self.new_imgH + 20))
        self.imagelabel = QtWidgets.QLabel(self.verticalimageWidget)
        self.verticalImageLayout.addWidget(self.imagelabel)
        self.CropPixmap = QtGui.QPixmap(self.imagePath).scaled(self.new_imgW, self.new_imgH)
        self.imagelabel.setPixmap(self.CropPixmap)

        self.verticalButon = QtWidgets.QWidget()
        self.verticalButon.setGeometry(QtCore.QRect(self.new_imgW + 10, 20, self.new_imgW + 30, self.new_imgH + 20))
        self.verticalButtonsLayout = QtWidgets.QVBoxLayout(self.verticalButon)
        self.verticalButtonsLayout.setAlignment(QtCore.Qt.AlignBottom)
        self.saveButton = QtWidgets.QPushButton("Save")
        self.saveButton.setText("Save")
        self.closeButton = QtWidgets.QPushButton("Close")

        self.horizontalLayout.addWidget(self.verticalimageWidget)
        self.horizontalLayout.addWidget(self.verticalButon)

        self.setLayout(self.horizontalLayout)

        self.verticalButtonsLayout.addWidget(self.saveButton)
        self.verticalButtonsLayout.addWidget(self.closeButton)

        self.saveButton.clicked.connect(self.saveButtonClicked)
        self.closeButton.clicked.connect(self.closeButtonClicked)

        self.RubberPosition_X = 20 + 0.1 * self.new_imgW
        self.RubberPosition_Y = 20 + 0.1 * self.new_imgH
        self.Rubber_Width = 0.8 * self.new_imgW
        self.Rubber_Height = 0.8 * self.new_imgH
        print(self.new_imgW)

        self.currentQRubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)
        self.currentQRubberBand.setGeometry(QtCore.QRect(self.RubberPosition_X, self.RubberPosition_Y,
                                                         self.Rubber_Width, self.Rubber_Height))
        self.currentQRubberBand.show()
        self.dragState = "Mouse Free"


    def mousePressEvent (self, eventQMouseEvent):

        currentPoint = eventQMouseEvent.pos()
        left = False
        right = False
        top = False
        bottom = False
        self.dragState = ""
        print(currentPoint.x(), " ", currentPoint.y())
        if (currentPoint.x() >= self.RubberPosition_X - self.sensetivty and
                currentPoint.x() <= self.RubberPosition_X + self.sensetivty):
            left = True

            self.dragState = self.dragState +"Left"
        if (currentPoint.y() >= self.RubberPosition_Y - self.sensetivty and
                currentPoint.y() <= self.RubberPosition_Y + self.sensetivty):
            top = True

            self.dragState = self.dragState + "Top"
        if ((currentPoint.x() >= self.RubberPosition_X +self.Rubber_Width+ - self.sensetivty) and
                (currentPoint.x() <= self.RubberPosition_X +self.Rubber_Width+ self.sensetivty)):
            if not right:
                right = True
                self.dragState = self.dragState + "Right"

        if (currentPoint.y() >= self.RubberPosition_Y + self.Rubber_Height - self.sensetivty and
                currentPoint.y() <= self.RubberPosition_Y + self.Rubber_Height + self.sensetivty):
            if not top:
                buttom = True
                self.dragState = self.dragState + "Bottom"

        if self.dragState == "":
            self.dragState = "Mouse Free"

    def mouseMoveEvent (self, eventQMouseEvent):

        if not self.dragState == "Mouse Free":
            point =(eventQMouseEvent.pos())
            x = point.x()
            y = point.y()

            if x >= 25 and x <= 25 + self.new_imgW and y >= 25 and y <= 20+ self.new_imgH:
                if self.dragState == "Left":
                    y = self.RubberPosition_Y
                    diff_x = self.RubberPosition_X - x
                    self.RubberPosition_X = x
                    width = self.Rubber_Width + diff_x
                    self.Rubber_Width = width
                    height = self.Rubber_Height

                elif self.dragState == "Right":
                    y = self.RubberPosition_Y
                    width =  x - self.RubberPosition_X
                    self.Rubber_Width = width
                    x = self.RubberPosition_X
                    height = self.Rubber_Height

                elif self.dragState == "Top":
                    x = self.RubberPosition_X
                    width = self.Rubber_Width
                    diff_y = self.RubberPosition_Y - y
                    self.RubberPosition_Y = y
                    height = self.Rubber_Height + diff_y
                    self.Rubber_Height = height

                elif self.dragState == "Bottom":
                    x = self.RubberPosition_X
                    height = y - self.RubberPosition_Y
                    self.Rubber_Height = height
                    width = self.Rubber_Width
                    y = self.RubberPosition_Y

                elif self.dragState == "LeftTop":
                    diff_x = self.RubberPosition_X - x
                    self.RubberPosition_X = x
                    width = self.Rubber_Width + diff_x
                    self.Rubber_Width = width

                    diff_y = self.RubberPosition_Y - y
                    self.RubberPosition_Y = y
                    height = self.Rubber_Height + diff_y
                    self.Rubber_Height = height

                elif self.dragState == "LeftBottom":
                    diff_x = self.RubberPosition_X - x
                    self.RubberPosition_X = x
                    width = self.Rubber_Width + diff_x
                    self.Rubber_Width = width

                    height = y - self.RubberPosition_Y
                    self.Rubber_Height = height
                    y = self.RubberPosition_Y

                elif self.dragState == "TopRight":
                    width = x - self.RubberPosition_X
                    self.Rubber_Width = width

                    x = self.RubberPosition_X
                    diff_y = self.RubberPosition_Y - y
                    self.RubberPosition_Y = y
                    height = self.Rubber_Height + diff_y
                    self.Rubber_Height = height


                elif self.dragState == "RightBottom":
                    width = x - self.RubberPosition_X
                    self.Rubber_Width = width
                    x = self.RubberPosition_X

                    height = y - self.RubberPosition_Y
                    self.Rubber_Height = height
                    y = self.RubberPosition_Y

                self.currentQRubberBand.setGeometry(QtCore.QRect(x, y, width, height))

    def mouseReleaseEvent (self, eventQMouseEvent):
        self.dragState = "Mouse Free"

    def saveButtonClicked(self):

        self.currentQRubberBand.hide()
        self.Rubber_Width = self.Rubber_Width / self.scale
        self.Rubber_Height = self.Rubber_Height / self.scale
        self.RubberPosition_X = (self.RubberPosition_X / self.new_imgW) * self.imgW
        self.RubberPosition_Y = (self.RubberPosition_Y / self.new_imgH) * self.imgH
        finalRect = QtCore.QRect(self.RubberPosition_X, self.RubberPosition_Y,
                                 self.Rubber_Width, self.Rubber_Height)
        self.currentQRubberBand.deleteLater()
        RealPixmap = QtGui.QPixmap(self.imagePath)
        copypixmap = RealPixmap.copy(finalRect)
        copypixmap.save(self.imagePath)
        self.close()

    def closeButtonClicked(self):
        self.close()

    def scaleImage(self, imgW, imgH):
        self.scale = 1
        new_imgW = imgW
        new_imgH = imgH
        if imgH > (Constants.MONITOR_HEIGHT - 300):
            self.scale = self.scale * (Constants.MONITOR_HEIGHT - 300) / imgH
            new_imgW = imgW * self.scale
            new_imgH = imgH * self.scale

        if new_imgW > (Constants.MONITOR_WIDTH - 300):
            self.scale = self.scale * (Constants.MONITOR_WIDTH - 300) / imgW
            new_imgW = imgW * self.scale
            new_imgH = imgH * self.scale

        return new_imgW ,new_imgH