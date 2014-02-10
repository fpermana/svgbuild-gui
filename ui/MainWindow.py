# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4.QtGui import QMainWindow, QFileDialog, QColorDialog, QDialog, QApplication
from PyQt4.QtCore import pyqtSignature, QDir, QString, QRegExp, Qt, QThread

from Ui_MainWindow import Ui_MainWindow

from SettingsDialog import SettingsDialog

from SVGBuild.SVGBuild import SVGBuild

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        
        self.svgbuild = SVGBuild()
        self.svgbuild.printText.connect(self.appendText)
    
    @pyqtSignature("")
    def on_lineToolButton_clicked(self):
        """
        Slot documentation goes here.
        """
        lineColorDialog = QColorDialog(self)
        if lineColorDialog.exec_() == QDialog.Accepted:
            self.lineColorWidget.setStyleSheet("QWidget { background-color: %s }" % lineColorDialog.selectedColor().name())
            self.svgbuild.setSingleOption('line',  lineColorDialog.selectedColor().name())
        # TODO: not implemented yet
#        raise NotImplementedError
    
    @pyqtSignature("")
    def on_backgroundToolButton_clicked(self):
        """
        Slot documentation goes here.
        """
        backgroundColorDialog = QColorDialog(self)
        if backgroundColorDialog.exec_() == QDialog.Accepted:
            self.backgroundColorWidget.setStyleSheet("QWidget { background-color: %s }" % backgroundColorDialog.selectedColor().name())
            self.svgbuild.setSingleOption('background',  backgroundColorDialog.selectedColor().name())
        # TODO: not implemented yet
#        raise NotImplementedError
    
    @pyqtSignature("")
    def on_cameraFrameToolButton_clicked(self):
        """
        Slot documentation goes here.
        """
        frameColorDialog = QColorDialog(self)
        if frameColorDialog.exec_() == QDialog.Accepted:
            self.cameraFrameColorWidget.setStyleSheet("QWidget { background-color: %s }" % frameColorDialog.selectedColor().name())
            self.svgbuild.setSingleOption('frame',  frameColorDialog.selectedColor().name())
        # TODO: not implemented yet
#        raise NotImplementedError
    
    @pyqtSignature("")
    def on_openFileLineEdit_returnPressed(self):
        """
        Slot documentation goes here.
        """
        self.selectFile()
        # TODO: not implemented yet
#        raise NotImplementedError
    
    @pyqtSignature("")
    def on_openFilePushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.selectFile()
        # TODO: not implemented yet
#        raise NotImplementedError
        
    def selectFile(self):
        #selectedFileName = QtGui.QFileDialog.getOpenFileName(self,"Open file",QtCore.QDir.currentPath(), "SVG files (*.svg);;All files (*.*)", QtCore.QString("SVG files (*.svg)"));
        selectedFileName = QFileDialog.getOpenFileName(self,"Open file",QDir.currentPath(), "SVG files (*.svg)", QString("SVG files (*.svg)"));
        if selectedFileName:
            foldername = QString(selectedFileName)
            foldername.remove(QRegExp("^.*/")).remove(QRegExp("\.[^\.]*$"))
            self.openFileLineEdit.setText(selectedFileName)
            self.folderNameLineEdit.setText(foldername)
    
    @pyqtSignature("")
    def on_buildPushButton_clicked(self):
        """
        SVG Build started.
        """
        if self.buildPushButton.text() == "Build!":
            if not self.openFileLineEdit.text():
                print "no file selected"
            else:
                if not self.svgbuild.isRunning:
                    self.outputTextEdit.setText("")
                    self.svgbuild.setIsRunning(True)
                    self.svgbuild.setFilename(self.openFileLineEdit.text())
                    self.svgbuild.setSingleOption("folder",  self.folderNameLineEdit.text())
                    
                    self.svgbuild.setSingleOption('path',  self.simplePathCheckBox.checkState() == Qt.Checked)
                    self.svgbuild.setSingleOption('fullpath',  self.fullPathCheckBox.checkState() == Qt.Checked)
                    self.svgbuild.setSingleOption('text',  self.textCheckBox.checkState() == Qt.Checked)
                    self.svgbuild.setSingleOption('image',  self.imageCheckBox.checkState() == Qt.Checked)
                    
                    self.svgbuild.setSingleOption('page', self.pageCheckBox.checkState() == Qt.Checked)
#                    self.svgbuild.setSingleOption('combine', self.combineCheckBox.checkState() == Qt.Checked)
                    self.svgbuild.setSingleOption('camera', self.cameraCheckBox.checkState() == Qt.Checked)
                    self.svgbuild.setSingleOption('backward', self.backwardCheckBox.checkState() == Qt.Checked)
                    self.svgbuild.setSingleOption('top', self.topCheckBox.checkState() == Qt.Checked)
                    
                    self.svgbuild.setSingleOption('from', self.fromSpinBox.value())
                    self.svgbuild.setSingleOption('until', self.untilSpinBox.value())
                    self.svgbuild.setSingleOption('height', self.heightSpinBox.value())
                    self.svgbuild.setSingleOption('width', self.widthSpinBox.value())
                    
                    self.svgbuild.setSingleOption('marker', self.markerComboBox.itemData(self.markerComboBox.currentIndex()).toString())
                    
                    #self.svgBuild.setSingleOption(key,  value)
                    
                    self.thread = QThread()
                    
                    self.buildPushButton.setText("Stop")
                    self.buildPushButton.clicked.connect(self.thread.quit)
                    
                    self.svgbuild.moveToThread(self.thread)
                    
                    self.thread.started.connect(self.svgbuild.startBuildUp)
                    self.svgbuild.finished.connect(self.finished)
                    #self.svgBuild.canceled.connect(self.thread.quit)
                    #self.svgBuild.canceled.connect(self.thread.terminate)
                    self.svgbuild.finished.connect(self.thread.quit)
                    self.thread.finished.connect(self.thread.deleteLater)
                    self.thread.destroyed.connect(self.resetThread)
                    
                    self.thread.start()
                
        else:
            self.svgbuild.setIsRunning(False)
            self.buildPushButton.setText("Build!")
        # TODO: not implemented yet
#        raise NotImplementedError
    
    @pyqtSignature("")
    def on_actionSetting_triggered(self):
        """
        Slot documentation goes here.
        """
        settingsDialog = SettingsDialog(self)
        if settingsDialog.exec_() == QDialog.Accepted:
            print 'ok'
        # TODO: not implemented yet
#        raise NotImplementedError
    
    @pyqtSignature("")
    def on_actionExit_triggered(self):
        """
        Slot documentation goes here.
        """
        self.close()
        # TODO: not implemented yet
#        raise NotImplementedError
    
    @pyqtSignature("")
    def on_actionSVGBuild_Help_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSignature("")
    def on_actionAbout_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    def appendText(self, line):
        self.outputTextEdit.append(line)
        
    def finished(self):
        self.svgbuild.setIsRunning(False)
        self.buildPushButton.setText("Build!")

    def resetThread(self):
        self.svgbuild.moveToThread(QApplication.instance().thread())
