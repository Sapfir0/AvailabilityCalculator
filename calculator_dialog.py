import os
from qgis.PyQt import QtGui, uic
from qgis.PyQt.QtCore import Qt, QFileInfo
from qgis.PyQt.QtWidgets import QMessageBox, QFrame, QDialog, QFileDialog

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'form.ui'))


class CalculatorDialog(QDialog, FORM_CLASS):

    def __init__(self, parent=None):
        super(CalculatorDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        self.setupUi(self)
        

