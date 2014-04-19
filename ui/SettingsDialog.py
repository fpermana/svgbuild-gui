# -*- coding: utf-8 -*-

"""
Module implementing SettingsDialog.
"""

from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature

from Ui_SettingsDialog import Ui_Dialog
from SVGBuild.Settings import Settings

class SettingsDialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.inkscapeLineEdit.setText(Settings.inkscape)
        self.temporaryDirectoryLineEdit.setText(Settings.temporary)
    
    @pyqtSignature("")
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        self.accept()
        # TODO: not implemented yet
#        raise NotImplementedError
    
    @pyqtSignature("")
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        self.reject()
        # TODO: not implemented yet
#        raise NotImplementedError
