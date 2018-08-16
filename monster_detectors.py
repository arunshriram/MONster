from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ClickableLineEdit import ClickableLineEdit
from TransformThread import Detector
import Properties
from MONster import displayError

class DetectorEditor(QWidget):
    def __init__(self, windowreference):
        QWidget.__init__(self)
    
        detectors = Properties.detectors 
        self.detectorlist = []
        for item in detectors:
            string = item.split(', ')
            name = string[0]
            width = string[1]
            height = string[2]
            detector = Detector(name, width, height)
            self.detectorlist.append(detector)

        self.listwidget = QListWidget()

        self.removeButton = QPushButton("Remove")
        self.nameLabel = QLabel("Name")
        self.name = ClickableLineEdit()
        self.widthLabel = QLabel("Width")
        self.width = ClickableLineEdit()
        self.heightLabel = QLabel("Height")
        self.height = ClickableLineEdit()
        self.addButton = QPushButton("Add to List!")
        self.closeButton = QPushButton("Close")

        hbox = QHBoxLayout()
        v1 = QVBoxLayout()
        v2 = QVBoxLayout()
        v2_h = QHBoxLayout()

        v1.addWidget(self.listwidget)
        v1.addWidget(self.removeButton)

        v2.addWidget(self.nameLabel)
        v2.addWidget(self.name)
        vx = QVBoxLayout()
        vy = QVBoxLayout()
        vx.addWidget(self.widthLabel)
        vx.addWidget(self.width)
        vy.addWidget(self.heightLabel)
        vy.addWidget(self.height)
        v2_h.addLayout(vx)
        v2_h.addLayout(vy)
        v2.addLayout(v2_h)
        v2.addWidget(self.addButton)
        h = QHBoxLayout()
        h.addStretch()
        h.addWidget(self.closeButton)
        v2.addLayout(h)
        hbox.addLayout(v1)
        hbox.addLayout(v2)
        self.setLayout(hbox)
    
        self.setWindowTitle("Add or edit a detector!")
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())    



        self.updateConnections()        

     

    def updateConnections(self):
        self.closeButton.clicked.connect(lambda: self.close())
        self.addDetector.clicked.connect(self.addDetector)

    def addDetector(self):
        if name.text().isEmpty() or width.text().isEmpty() or height.text().isEmpty():
            displayError(self, "Please make sure you fill out all the relevant information!")
            return
        try:
            nameLabel = str(self.name.text())
            width = float(str(self.width.text()))
            height = float(str(self.height.text()))
        except:
            displayError(self, "Could not add your values.")
            return
        detector = Detector(name, width, height)
        self.detectorlist.append(detector)
        properties = []
        inFile = open("Properties.py", 'r')
        for line in inFile:
            properties.append(line)
        inFile.close()
        outFile = open("Properties.py", 'w')
        properties[:-1].append(detector)
        for prop in properties:
            outFile.write(prop)
        ouFile.close()