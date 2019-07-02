# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'try.ui'
#
# Created by: PyQt UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import Constants as Constants

class previewWindowSkel(object):
    def setupUi(self, prev):
        self.xmlTabsverticalLayoutWidget = QtWidgets.QWidget(prev)
        self.xmlTabsverticalLayout = QtWidgets.QVBoxLayout()
        self.xmlTabs = QtWidgets.QTabWidget(self.xmlTabsverticalLayoutWidget)

        self.xmlTabsverticalLayout.addWidget(self.xmlTabs)

        self.activeImgVerticalLayoutWidget = QtWidgets.QWidget(prev)
        self.activeImgverticalLayout = QtWidgets.QVBoxLayout()

        self.activityListVerticalLayoutWidget = QtWidgets.QWidget(prev)
        self.listScrolVerticalLayout = QtWidgets.QVBoxLayout()
        self.scrollArea = QtWidgets.QScrollArea(self.activityListVerticalLayoutWidget)
        self.scrollArea.setWidgetResizable(True)
        self.activitysScrollArea = QtWidgets.QWidget()
        self.scrollArea.setWidget(self.activitysScrollArea)
        self.listScrolVerticalLayout.addWidget(self.scrollArea)
        #self.scrollArea.setMaximumWidth(300)
        self.activitysHLayouts = []

        #self.activitiesList = customListWidget()
        #self.activitiesList.setViewMode(QtWidgets.QListView.ListMode)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        #self.verticalLayout.addWidget(self.activitiesList)

        self.mainHLayout = QtWidgets.QHBoxLayout()
        self.mainHLayout.addLayout(self.verticalLayout)
        self.mainHLayout.addLayout(self.activeImgverticalLayout)
        self.mainHLayout.addLayout(self.xmlTabsverticalLayout)



class customListWidget(QtWidgets.QWidget):
    activated = QtCore.pyqtSignal(int)
    def __init__(self, path, imgName, index):
        super(customListWidget, self).__init__()

        self.setMaximumHeight(100)
        self.path = path
        self.index = index
        self.imgName = imgName
        self.horizontalBox = QtWidgets.QHBoxLayout()
        self.imageLabel = QtWidgets.QLabel()
        pmImg = QtGui.QPixmap(path).scaled( 50, 50)
        self.imageLabel.setPixmap(QtGui.QPixmap(pmImg))
        self.imageName = QtWidgets.QLabel(imgName)
        self.horizontalBox.addWidget(self.imageLabel)
        self.horizontalBox.addWidget(self.imageName)

        self.setLayout(self.horizontalBox)

    def mousePressEvent(self, event):

        print("clicked")
        try:
            self.activated.emit(10)
        except:
            print("error")
        print("2na b3t 2hoh f 2ntzar m3alik")





# class customListWidget(QtWidgets.QListWidget):
#     activated = QtCore.pyqtSignal(str)
#     def __init__(self):
#         QtWidgets.QListWidget.__init__(self)
#         self.itemClicked.connect(self.item_click)
#
#     def add_item(self, imgPath, imgName):
#         item = QtWidgets.QListWidgetItem()
#         item.widget.mouseReleaseEvent = self.myfunction
#
#         icon = QtGui.QIcon()
#         pmImg = QtGui.QPixmap(imgPath)
#         icon.addPixmap(pmImg, QtGui.QIcon.Normal, QtGui.QIcon.On)
#         item.setIcon(icon)
#         # item.imageLabel = QtWidgets.QLabel()
#         # item.imageLabel.setPixmap(pmImg)
#         item.setText(imgName)
#         item.setSizeHint(QtCore.QSize(150,65))
#
#         self.addItem(item)
#     def myfunction(self):
#         print("2na 8arib ")
#
#     def item_click(self, item):
#         print("sba7 2l2rf 3laik ya kaya ")
#         self.activated.emit(str(item.text))
#         print (item, str(item.text()))