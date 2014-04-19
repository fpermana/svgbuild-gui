# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/fpermana/repositories/SVGBuild/ui/SettingsDialog.ui'
#
# Created: Sat Apr 19 16:14:48 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 231)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.inkscapeLineEdit = QtGui.QLineEdit(self.groupBox)
        self.inkscapeLineEdit.setObjectName(_fromUtf8("inkscapeLineEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.inkscapeLineEdit)
        self.temporaryDirectoryLabel = QtGui.QLabel(self.groupBox)
        self.temporaryDirectoryLabel.setObjectName(_fromUtf8("temporaryDirectoryLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.temporaryDirectoryLabel)
        self.temporaryDirectoryLineEdit = QtGui.QLineEdit(self.groupBox)
        self.temporaryDirectoryLineEdit.setObjectName(_fromUtf8("temporaryDirectoryLineEdit"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.temporaryDirectoryLineEdit)
        self.convertLineEdit = QtGui.QLineEdit(self.groupBox)
        self.convertLineEdit.setObjectName(_fromUtf8("convertLineEdit"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.convertLineEdit)
        self.identifyLineEdit = QtGui.QLineEdit(self.groupBox)
        self.identifyLineEdit.setObjectName(_fromUtf8("identifyLineEdit"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.identifyLineEdit)
        self.inkscapeLabel = QtGui.QLabel(self.groupBox)
        self.inkscapeLabel.setObjectName(_fromUtf8("inkscapeLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.inkscapeLabel)
        self.convertLabel = QtGui.QLabel(self.groupBox)
        self.convertLabel.setObjectName(_fromUtf8("convertLabel"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.convertLabel)
        self.identifyLabel = QtGui.QLabel(self.groupBox)
        self.identifyLabel.setObjectName(_fromUtf8("identifyLabel"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.identifyLabel)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.temporaryDirectoryLabel.setText(QtGui.QApplication.translate("Dialog", "Temporary Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.inkscapeLabel.setText(QtGui.QApplication.translate("Dialog", "Inkscape", None, QtGui.QApplication.UnicodeUTF8))
        self.convertLabel.setText(QtGui.QApplication.translate("Dialog", "Convert", None, QtGui.QApplication.UnicodeUTF8))
        self.identifyLabel.setText(QtGui.QApplication.translate("Dialog", "Identify", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

