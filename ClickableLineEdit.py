from PyQt4.QtCore import *
from PyQt4.QtGui import *

class ClickableLineEdit(QLineEdit):
    clicked = pyqtSignal() # signal when the text entry is left clicked

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton: 
            self.clicked.emit()
            self.selectAll()
        else: 
            super().mousePressEvent(event)
