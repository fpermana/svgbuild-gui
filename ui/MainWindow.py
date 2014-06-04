# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import re
from os.path import expanduser

from PyQt4.QtGui import QMainWindow, QFileDialog, QColorDialog, QDialog, QApplication
from PyQt4.QtCore import pyqtSignature, QDir, QString, QRegExp, Qt, QThread

from Ui_MainWindow import Ui_MainWindow

from SettingsDialog import SettingsDialog

from SVGBuild.SVGBuild import SVGBuild

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    lineColorName = ""
    
    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        
#        self.checkBox.setVisible(False)
#        self.circlePathCheckBox.setVisible(False)
        self.buildPathGroupBox.setEnabled(False)
        
        self.svgbuild = SVGBuild()
        self.lineColorName = self.svgbuild.getSingleOption('line')
        self.svgbuild.printText.connect(self.appendText)
    
    @pyqtSignature("")
    def on_lineToolButton_clicked(self):
        """
        Slot documentation goes here.
        """
        lineColorDialog = QColorDialog(self)
        if lineColorDialog.exec_() == QDialog.Accepted:
            self.lineColorName = str(lineColorDialog.selectedColor().name())
            self.lineColorWidget.setStyleSheet("QWidget { background-color: %s }" % self.lineColorName)
            self.svgbuild.setSingleOption('line',  self.lineColorName)
        # TODO: not implemented yet
#        raise NotImplementedError
    
    @pyqtSignature("")
    def on_backgroundToolButton_clicked(self):
        """
        Slot documentation goes here.
        """
        backgroundColorDialog = QColorDialog(self)
        if backgroundColorDialog.exec_() == QDialog.Accepted:
            backgroundColorName = str(backgroundColorDialog.selectedColor().name())
            self.backgroundColorWidget.setStyleSheet("QWidget { background-color: %s }" % backgroundColorName)
            self.svgbuild.setSingleOption('background',  backgroundColorName)
        # TODO: not implemented yet
#        raise NotImplementedError
    
    @pyqtSignature("")
    def on_cameraFrameToolButton_clicked(self):
        """
        Slot documentation goes here.
        """
        frameColorDialog = QColorDialog(self)
        if frameColorDialog.exec_() == QDialog.Accepted:
            frameColorName = str(frameColorDialog.selectedColor().name())
            self.cameraFrameColorWidget.setStyleSheet("QWidget { background-color: %s }" % frameColorName)
            self.svgbuild.setSingleOption('frame',  frameColorName)
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
        selectedFileName = QFileDialog.getOpenFileName(self, "Open file", expanduser("~"), "SVG files (*.svg)", QString("SVG files (*.svg)"));
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
                    self.svgbuild.setFilename(str(self.openFileLineEdit.text()))
                    workingDirectory = re.sub(r'[^\/]*$', '', str(self.openFileLineEdit.text()))
                    self.svgbuild.setSingleOption("folder",  "%s%s" % (workingDirectory, str(self.folderNameLineEdit.text())))
                    
                    self.svgbuild.setSingleOption('path',  self.buildPathCheckBox.checkState() == Qt.Checked)
                    self.svgbuild.setSingleOption('fullpath',  self.fullPathCheckBox.checkState() == Qt.Checked)
                    self.svgbuild.setSingleOption('fillpath',  self.fillPathCheckBox.checkState() == Qt.Checked)
                    self.svgbuild.setSingleOption('circlepath',  self.circlePathCheckBox.checkState() == Qt.Checked)
                    self.svgbuild.setSingleOption('closepath',  self.circlePathCheckBox.checkState() == Qt.Checked and self.closePathCheckBox.checkState() == Qt.Checked)
                    self.svgbuild.setSingleOption('text',  self.buildTextCheckBox.checkState() == Qt.Checked)
                    self.svgbuild.setSingleOption('image',  self.buildImageCheckBox.checkState() == Qt.Checked)
                    
                    self.svgbuild.setSingleOption('page', self.pageCheckBox.checkState() == Qt.Checked)
#                    self.svgbuild.setSingleOption('combine', self.combineCheckBox.checkState() == Qt.Checked)
                    self.svgbuild.setSingleOption('camera', self.cameraCheckBox.checkState() == Qt.Checked)
                    self.svgbuild.setSingleOption('backward', self.backwardCheckBox.checkState() == Qt.Checked)
                    self.svgbuild.setSingleOption('top', self.topCheckBox.checkState() == Qt.Checked)
                    
                    self.svgbuild.setSingleOption('from', self.fromSpinBox.value())
                    self.svgbuild.setSingleOption('until', self.untilSpinBox.value())
                    self.svgbuild.setSingleOption('height', self.heightSpinBox.value())
                    self.svgbuild.setSingleOption('width', self.widthSpinBox.value())
                    
                    #self.svgbuild.setSingleOption('marker', self.markerComboBox.itemData(self.markerComboBox.currentIndex()).toString())
                    self.svgbuild.setSingleOption('marker', str(self.markerComboBox.currentText().toLower()))
                    self.svgbuild.setSingleOption('objectline', self.objectLineCheckBox.checkState() == Qt.Checked)
                    self.svgbuild.setSingleOption('nobackground', self.transparentCheckBox.checkState() == Qt.Checked)
                    
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
        
