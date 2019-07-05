# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AppSkelton.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import Constants

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(800, 600)
        # mainWindow.setStyleSheet("""background-color:#515781;""")
        iconLogo = QtGui.QIcon()
        iconLogo.addPixmap(QtGui.QPixmap(Constants.ICONS_PATH + "finish-white.png"), QtGui.QIcon.Normal,
                           QtGui.QIcon.Off)
        mainWindow.setWindowIcon(iconLogo)
        mainWindow.setWindowTitle("TagIt")
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuImage_Grid = QtWidgets.QMenu(self.menuView)
        self.menuImage_Grid.setObjectName("menuImage_Grid")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuProject = QtWidgets.QMenu(self.menubar)
        self.menuProject.setObjectName("menuProject")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(mainWindow)
        self.toolBar.setEnabled(True)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolBar.setObjectName("toolBar")
        mainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionExit = QtWidgets.QAction(mainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(Constants.ICONS_PATH + "exit-white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon)
        self.actionExit.setObjectName("actionExit")
        self.actionGenerateXML = QtWidgets.QAction(mainWindow)
        self.actionGenerateXML.setEnabled(False)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(Constants.ICONS_PATH +"run-white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGenerateXML.setIcon(icon1)
        self.actionGenerateXML.setObjectName("actionGenerateXML")
        self.actionConnectCmpts = QtWidgets.QAction(mainWindow)
        self.actionConnectCmpts.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(Constants.ICONS_PATH +"connect-white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionConnectCmpts.setIcon(icon2)
        self.actionConnectCmpts.setObjectName("actionConnectCmpts")
        self.actionShow_Results = QtWidgets.QAction(mainWindow)
        self.actionShow_Results.setObjectName("actionShow_Results")
        self.action6_images_per_row = QtWidgets.QAction(mainWindow)
        self.action6_images_per_row.setCheckable(True)
        self.action6_images_per_row.setObjectName("action6_images_per_row")
        self.action8_images_per_row = QtWidgets.QAction(mainWindow)
        self.action8_images_per_row.setCheckable(True)
        self.action8_images_per_row.setChecked(True)
        self.action8_images_per_row.setObjectName("action8_images_per_row")
        self.action4_images_per_row = QtWidgets.QAction(mainWindow)
        self.action4_images_per_row.setCheckable(True)
        self.action4_images_per_row.setObjectName("action4_images_per_row")
        self.actionCoustom = QtWidgets.QAction(mainWindow)
        self.actionCoustom.setCheckable(True)
        self.actionCoustom.setObjectName("actionCoustom")
        self.actionUpdateCmpts = QtWidgets.QAction(mainWindow)
        self.actionUpdateCmpts.setEnabled(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(Constants.ICONS_PATH +"update-white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionUpdateCmpts.setIcon(icon3)
        self.actionUpdateCmpts.setObjectName("actionUpdateCmpts")
        self.actionFinish = QtWidgets.QAction(mainWindow)
        self.actionFinish.setEnabled(False)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(Constants.ICONS_PATH +"finish-white.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFinish.setIcon(icon4)
        self.actionFinish.setObjectName("actionFinish")
        self.actionView_Doccument = QtWidgets.QAction(mainWindow)
        self.actionView_Doccument.setObjectName("actionView_Doccument")
        self.actionAdd_Images = QtWidgets.QAction(mainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(Constants.ICONS_PATH +"addImages.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdd_Images.setIcon(icon5)
        self.actionAdd_Images.setObjectName("actionAdd_Images")
        self.menuFile.addAction(self.actionAdd_Images)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuImage_Grid.addSeparator()
        self.menuImage_Grid.addAction(self.action4_images_per_row)
        self.menuImage_Grid.addAction(self.action6_images_per_row)
        self.menuImage_Grid.addAction(self.action8_images_per_row)
        self.menuImage_Grid.addAction(self.actionCoustom)
        self.menuView.addAction(self.menuImage_Grid.menuAction())
        self.menuHelp.addAction(self.actionView_Doccument)
        self.menuProject.addAction(self.actionGenerateXML)
        self.menuProject.addAction(self.actionUpdateCmpts)
        self.menuProject.addAction(self.actionConnectCmpts)
        self.menuProject.addAction(self.actionFinish)
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.actionShow_Results)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuProject.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionExit)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionAdd_Images)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionGenerateXML)
        self.toolBar.addAction(self.actionUpdateCmpts)
        self.toolBar.addAction(self.actionConnectCmpts)
        self.toolBar.addAction(self.actionFinish)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.menuFile.setTitle(_translate("mainWindow", "File"))
        self.menuView.setTitle(_translate("mainWindow", "View"))
        self.menuImage_Grid.setTitle(_translate("mainWindow", "Image Grid"))
        self.menuHelp.setTitle(_translate("mainWindow", "Help"))
        self.menuProject.setTitle(_translate("mainWindow", "Run"))
        self.toolBar.setWindowTitle(_translate("mainWindow", "toolBar"))
        self.actionExit.setText(_translate("mainWindow", "Exit"))
        self.actionGenerateXML.setText(_translate("mainWindow", "Generate XML"))
        self.actionGenerateXML.setShortcut(_translate("mainWindow", "F5"))
        self.actionConnectCmpts.setText(_translate("mainWindow", "Connect"))
        self.actionConnectCmpts.setShortcut(_translate("mainWindow", "F7"))
        self.actionShow_Results.setText(_translate("mainWindow", "Show Results"))
        self.actionShow_Results.setShortcut(_translate("mainWindow", "Ctrl+R"))
        self.action6_images_per_row.setText(_translate("mainWindow", "6 images per row"))
        self.action8_images_per_row.setText(_translate("mainWindow", "8 images per row "))
        self.action4_images_per_row.setText(_translate("mainWindow", "4 images per row "))
        self.actionCoustom.setText(_translate("mainWindow", "Coustom..."))
        self.actionUpdateCmpts.setText(_translate("mainWindow", "Update Components"))
        self.actionUpdateCmpts.setShortcut(_translate("mainWindow", "F6"))
        self.actionFinish.setText(_translate("mainWindow", "Finish"))
        self.actionFinish.setShortcut(_translate("mainWindow", "F8"))
        self.actionView_Doccument.setText(_translate("mainWindow", "View Doccument"))
        self.actionAdd_Images.setText(_translate("mainWindow", "Add Images"))
        self.actionAdd_Images.setShortcut(_translate("mainWindow", "Ctrl+A"))

