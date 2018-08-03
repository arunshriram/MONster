# 2018.07.26 16:07:07 PDT
#Embedded file name: /Users/arunshriram/Documents/SLAC Internship/MONster/monster_stitch.py
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import numpy as np
import os, scipy, math
import scipy.io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from ClickableLineEdit import ClickableLineEdit
from StitchThread import *
from QRoundProgressBar import QRoundProgressBar

def generateStitchWidgets(self):
    self.stitchImage = QLabel()
    pixmap = QPixmap('images/SLAC_LogoSD.png')
    self.stitchImage.setPixmap(pixmap.scaled(self.imageWidth, self.imageWidth, Qt.KeepAspectRatio))
    self.stitchImage.setStyleSheet('QLabel { border-style:outset; border-width:10px;  border-radius: 10px; border-color: rgb(34, 200, 157); color:rgb(0, 0, 0); background-color: rgb(200, 200, 200); } ')
    self.images_select_label = QLabel('Select the image folder that contains you wish to stitch:')
    self.images_select_label.setStyleSheet('QLabel {color: white;}')
    self.images_select = ClickableLineEdit()
    self.images_select.setFixedWidth(580)
    self.images_select.setStyleSheet(self.lineEditStyleSheet)
    self.images_select_files_button = QPushButton()
    self.images_select_files_button.setIcon(QIcon('images/folder_select.png'))
    self.images_select_files_button.setIconSize(QSize(25, 25))
    self.images_select_files_button.setFixedSize(25, 25)
    self.images_select_files_button.setStyleSheet('border: none;')
    self.stitch_abort = QPushButton('Abort Stitching')
    self.stitch_abort.setStyleSheet("background-color: rgb(255, 140, 140);")              
    self.stitch_abort.setFixedSize(150, 30)    
    
    self.saveLabel = QLabel("File Save Location:")
    self.saveLabel.setStyleSheet("QLabel {color: white;}")
    self.stitch_saveLocation = ClickableLineEdit()
    self.stitch_saveLocation.setStyleSheet(self.lineEditStyleSheet)
    self.stitch_saveLocation.setFixedWidth(580)
    self.stitch_saveLocation_button = QPushButton()
    self.stitch_saveLocation_button.setIcon(QIcon("images/folder_select.png"))
    self.stitch_saveLocation_button.setFixedSize(25 ,25)
    self.stitch_saveLocation_button.setIconSize(QSize(25, 25))
    self.stitch_saveLocation_button.setStyleSheet("border: none;")
    self.first_index_label = QLabel('First scan index:')
    self.first_index_label.setStyleSheet('QLabel {color: white;}')
    self.first_index = ClickableLineEdit('1')
    self.first_index.setMaximumWidth(30)
    self.first_index.setStyleSheet(self.lineEditStyleSheet)
    self.last_index_label = QLabel('Last scan index:')
    self.last_index_label.setStyleSheet('QLabel {color: white;}')
    self.last_index = ClickableLineEdit('9')
    self.last_index.setMaximumWidth(30)
    self.last_index.setStyleSheet(self.lineEditStyleSheet)
    self.stitch_start_button = QPushButton('Begin Stitching!')
    self.stitch_start_button.setStyleSheet('background-color: rgb(80, 230, 133);')
    self.stitch_start_button.setFixedSize(160, 30)
    
    self.stitchbar = QRoundProgressBar()
    self.stitchbar.setFixedSize(150, 150)
    self.stitchbar.setDataPenWidth(.01)
    self.stitchbar.setOutlinePenWidth(.01)
    self.stitchbar.setDonutThicknessRatio(0.85)
    self.stitchbar.setDecimals(1)
    self.stitchbar.setFormat('%p %')
    # self.bar.resetFormat()
    self.stitchbar.setNullPosition(90)
    self.stitchbar.setBarStyle(QRoundProgressBar.StyleDonut)
    self.stitchbar.setDataColors([(0, QColor(qRgb(34, 200, 157))), (1, QColor(qRgb(34, 200, 157)))])
    self.stitchbar.setRange(0, 100)
    #self.bar.setValue(30)
    self.stitchbar.setValue(0)
    
    self.stitch_console = QTextBrowser()
    self.stitch_console.setMinimumHeight(150)
    self.stitch_console.setMaximumHeight(300)
    
    self.stitch_console.setFont(QFont('Avenir', 14))
    self.stitch_console.setStyleSheet('margin:3px; border:1px solid rgb(0, 0, 0); background-color: rgb(240, 255, 240);')


def generateStitchLayout(self):
    v_box = QVBoxLayout()
    imagebox = QHBoxLayout()
    imagebox.addStretch()
    imagebox.addWidget(self.stitchbar)
    imagebox.addStretch()
    imagebox.addWidget(self.stitchImage)
    imagebox.addStretch()    
    v_box.addLayout(imagebox)
    indicesRow = QHBoxLayout()
    fileSelect = QHBoxLayout()
    findex = QHBoxLayout()
    findex.addWidget(self.first_index_label)
    findex.addWidget(self.first_index)
    findex.addStretch()
    lindex = QHBoxLayout()
    lindex.addWidget(self.last_index_label)
    lindex.addWidget(self.last_index)
    lindex.addStretch()
    v = QVBoxLayout()
    v.addLayout(findex)
    v.addLayout(lindex)
    v1 = QVBoxLayout()
    v1.addWidget(self.images_select_label)
    fileSelect.addWidget(self.images_select)
    fileSelect.addWidget(self.images_select_files_button)
    v1.addLayout(fileSelect)
    v1.addWidget(self.saveLabel)
    indicesRow.addLayout(v1)
    indicesRow.addLayout(v)
    v_box.addLayout(indicesRow)
    fileSave = QHBoxLayout()
    fileSave.addWidget(self.stitch_saveLocation)
    fileSave.addWidget(self.stitch_saveLocation_button)
    fileSave.addStretch()
    v_box.addLayout(fileSave)    
    control = QHBoxLayout()
    control.addWidget(self.stitch_start_button)
    control.addWidget(self.stitch_abort)
    control.addStretch()
    v_box.addLayout(control)
    v_box.addWidget(self.stitch_console)
    return v_box


def stitchImageSelect(self):
    folder = QFileDialog.getExistingDirectory(directory=os.getcwd())
    print folder


def beginStitch(self):
    self.disableWidgets()
    QApplication.processEvents()
    self.console.clear()
    self.addToConsole('****************************************************')
    self.addToConsole('********** Beginning Stitch Processing... ***********')
    self.addToConsole('****************************************************')
    QApplication.processEvents()
    
    if '.' in str(self.first_index.text()) or '.' in str(self.last_index.text()):
        self.addToConsole("Converting indices to integers %s and %s." % (int(str(self.first_index.text())), int(str(self.last_index.text()))))
    
    findex = int(str(self.first_index.text()))
    lindex = int(str(self.last_index.text()))
    
    if not os.path.exists(str(self.stitch_saveLocation.text())):
        self.addToConsole("Make sure you select a location to save files!")
        return

    self.stitchThread = StitchThread(self, None, str(self.stitch_saveLocation.text()), findex, lindex)
    self.stitchThread.setAbortFlag(False)
    # make sure that if the abort button is clicked, it is aborting the current running stitch thread, so this needs to be run for every new stitch thread
    self.stitchThread.setAbortFlag(False)
    self.stitch_abort.clicked.connect(self.stitchThread.abortClicked)
    
    # these connections are the only way the thread can communicate with the MONster
    self.connect(self.stitchThread, SIGNAL("addToConsole(PyQt_PyObject)"), self.addToConsole)
    self.connect(self.stitchThread, SIGNAL("bar(int, PyQt_PyObject)"), self.setRadialBar)
    self.connect(self.stitchThread, SIGNAL("finished(PyQt_PyObject, PyQt_PyObject)"), stitchDone)
    self.connect(self.stitchThread, SIGNAL("setImage(PyQt_PyObject, PyQt_PyObject)"), setStitchImage)
    self.connect(self.stitchThread, SIGNAL("resetStitch(PyQt_PyObject)"), resetStitch)
    self.stitchThread.start()    

# What should be done after a stitch thread is finished
def stitchDone(self, loopTime):
    avgTime = np.mean(loopTime)
    maxTime = np.max(loopTime)
    finishedMessage = ''
    finishedMessage += ('====================================================\n')
    finishedMessage += ('====================================================\n')
    finishedMessage += ('Files finished processing\n')
    finishedMessage += ('-----Avg {:.4f}s / file, max {:.4f}.s / file\n'.format(avgTime, maxTime))
    finishedMessage += ('-----Total Time Elapsed {:4f}s\n'.format(np.sum(loopTime)))
    finishedMessage += ('====================================================\n')
    finishedMessage += ('====================================================')        
    #QMessageBox.information(self, "Done!", finishedMessage)
    self.addToConsole(finishedMessage)
    QApplication.processEvents()            
    self.enableWidgets()
    self.stitchThread.quit()
    self.stitchThread.stop()
    self.processDone = True

# Adds the current stitched image to the stitch page.
def setStitchImage(self, filename):
    try:
        pixmap = QPixmap(filename)        
        self.stitchImage.setPixmap(pixmap.scaled(self.imageWidth, self.imageWidth, Qt.KeepAspectRatio))  
        QApplication.processEvents()
    except:
        self.addToConsole("Could not load stitched image.")
        
    
def setStitchSaveLocation(self):
    path = str(QFileDialog.getExistingDirectory(self, "Select a location for processed files"))
    if path !='':
        self.stitch_saveLocation.setText(path)
      
def resetStitch(self):
    setStitchImage(self, "images/SLAC_LogoSD.png")
    self.stitchbar.setValue(0)