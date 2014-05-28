# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/fpermana/repositories/SVGBuild/ui/SettingsDialog.ui'
#
# Created: Sat May 24 08:40:49 2014
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
        Dialog.resize(400, 165)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.inkscapeLabel = QtGui.QLabel(self.groupBox)
        self.inkscapeLabel.setObjectName(_fromUtf8("inkscapeLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.inkscapeLabel)
        self.inkscapeLineEdit = QtGui.QLineEdit(self.groupBox)
        self.inkscapeLineEdit.setObjectName(_fromUtf8("inkscapeLineEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.inkscapeLineEdit)
        self.temporaryDirectoryLabel = QtGui.QLabel(self.groupBox)
        self.temporaryDirectoryLabel.setObjectName(_fromUtf8("temporaryDirectoryLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.temporaryDirectoryLabel)
        self.temporaryDirectoryLineEdit = QtGui.QLineEdit(self.groupBox)
        self.temporaryDirectoryLineEdit.setObjectName(_fromUtf8("temporaryDirectoryLineEdit"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.temporaryDirectoryLineEdit)
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
        self.inkscapeLabel.setText(QtGui.QApplication.translate("Dialog", "Inkscape", None, QtGui.QApplication.UnicodeUTF8))
        self.temporaryDirectoryLabel.setText(QtGui.QApplication.translate("Dialog", "Temporary Directory", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

