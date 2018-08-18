# 2018.07.26 16:07:07 PDT
#Embedded file name: /Users/arunshriram/Documents/SLAC Internship/MONster/monster_stitch.py
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os, datetime, csv
from ClickableLineEdit import ClickableLineEdit
from StitchThread import *
from QRoundProgressBar import QRoundProgressBar
import monster_queueloader as mq
def generateStitchWidgets(self):
    self.stitchImage = QLabel()
    pixmap = QPixmap('images/SLAC_LogoSD.png')
    self.stitchImage.setPixmap(pixmap.scaled(self.imageWidth, self.imageWidth, Qt.KeepAspectRatio))
    self.stitchImage.setStyleSheet('QLabel { border-style:outset; border-width:10px;  border-radius: 10px; border-color: rgb(34, 200, 157); color:rgb(0, 0, 0); background-color: rgb(200, 200, 200); } ')
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
    self.stitch_abort.resize(self.stitch_abort.sizeHint().width(), self.stitch_abort.sizeHint().height())

    # self.stitch_abort.setFixedSize(150, 30)    
    
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

    self.stitch_start_button = QPushButton('Begin Stitching!')
    self.stitch_start_button.setStyleSheet('background-color: rgb(80, 230, 133);')
    # self.stitch_start_button.setFixedSize(160, 30)
    self.stitch_start_button.resize(self.stitch_start_button.sizeHint().width(), self.stitch_start_button.sizeHint().height())

    
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
    self.stitch_console.moveCursor(QTextCursor.End)
    self.stitch_data_label = QLabel("Current data folder:")
    self.stitch_data_label.setStyleSheet("QLabel {color: white;}")
    self.stitch_console.setFont(QFont('Avenir', 14))
    self.stitch_console.setStyleSheet('margin:3px; border:1px solid rgb(0, 0, 0); background-color: rgb(240, 255, 240);')
    
    self.stitch_saveMacroButton = QPushButton("Save as a macro")
    # self.stitch_saveMacroButton.setMaximumWidth(160)
    # self.stitch_saveMacroButton.setFixedHeight(30)
    self.stitch_saveMacroButton.resize(self.stitch_saveMacroButton.sizeHint().width(), self.stitch_saveMacroButton.sizeHint().height())

    self.stitch_saveMacroButton.setStyleSheet("background-color: rgb(255, 251, 208);")
    self.stitch_addToQueueButton = QPushButton("Add this configuration to the queue")
    # self.stitch_addToQueueButton.setMaximumWidth(220)
    # self.stitch_addToQueueButton.setFixedHeight(30)
    self.stitch_addToQueueButton.setStyleSheet("background-color: rgb(255, 207, 117);")
    self.stitch_addToQueueButton.resize(self.stitch_addToQueueButton.sizeHint().width(), self.stitch_addToQueueButton.sizeHint().height())

    self.stitch_files_to_process = None

def generateStitchLayout(self):
    v_box = QVBoxLayout()
    imagebox = QHBoxLayout()
    imagebox.addStretch()
    imagebox.addWidget(self.stitchbar)
    imagebox.addStretch()
    imagebox.addWidget(self.stitchImage)
    imagebox.addStretch()    
    v_box.addLayout(imagebox)
    fileSelect = QHBoxLayout()
    v_box.addWidget(self.stitch_data_label)
    fileSelect.addWidget(self.images_select)
    fileSelect.addWidget(self.images_select_files_button)
    fileSelect.addStretch()
    v_box.addLayout(fileSelect)
    v_box.addWidget(self.saveLabel)
    fileSave = QHBoxLayout()
    fileSave.addWidget(self.stitch_saveLocation)
    fileSave.addWidget(self.stitch_saveLocation_button)
    fileSave.addStretch()
    v_box.addLayout(fileSave)    
    control = QHBoxLayout()
    control.addWidget(self.stitch_start_button)
    control.addWidget(self.stitch_abort)
    control.addWidget(self.stitch_saveMacroButton)
    control.addWidget(self.stitch_addToQueueButton)
    control.addStretch()
    v_box.addLayout(control)
    v_box.addWidget(self.stitch_console)
    return v_box

# Compiles the information on the current stitch tab page into a macro and adds it to the queue
def addStitchCurrentToQueue(self):
    cur_time = datetime.datetime.now().strftime('%Y-%m-%d--%H-%M-%S')
    name = ('/Users/arunshriram/Documents/SLAC Internship/monhitp-gui/macros/stitch-macro-%s') %(cur_time)
    self.addToConsole("Saving this page in directory \"macros\" as \"stitch-macro-%s\" and adding to the queue..." % (cur_time))
    saved = saveStitchMacro(self, name)
    if saved is None:
        return
    self.macroQueue.append( self.editor.curMacro )       
    macro = QListWidgetItem("Process %s: Added macro \"%s\"" % (mq.curIndex, os.path.basename(str(self.editor.curMacro.getFilename()))))
    mq.curIndex+= 1 
    self.queue.addItem(macro)
    self.editor.close()
    QApplication.processEvents()
    self.addToConsole("Macro saved and added to queue!")
    

# Adds functionality to the stitch page "save macro" button; takes all the information currently
# on the stitch page and compiles it into a macro to be loaded into the queue
def saveStitchMacro(self, fileName=''):
    # CHECKING VALUES TO MAKE SURE EVERYTHING IS OKAY BEFORE MACRO CAN BE SAVED
    macrodict = {"workflow" : "False"}
    macrodict["transform"] = 'False'
    macrodict["integrate"] = 'False'
    macrodict["stitch"] = 'True'
    try:
        data_source = str(self.images_select.text())
        if not os.path.exists(data_source):
            displayError(self, "Please select an existing stitch data source directory.")
            return
        s_proc_dir = os.path.join(data_source, "Processed_Stitch")

        if str(self.stitch_saveLocation.text()) == "":
            self.stitch_saveLocation.setText(s_proc_dir)
    
        values = (data_source, s_proc_dir)
        macrodict["s_data_source"] = values[0]
        macrodict["s_proc_dir"] = values[1]
    except:
        return


        # End of information checking *********************************

    # File saving ********************************
    current = os.getcwd()
    final_dir = os.path.join(current, r'macros')
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)
            
    cur_time = datetime.datetime.now().strftime('%Y-%m-%d--%H-%M-%S')
    name = (final_dir + '/macro-%s.csv') %(cur_time)        
    fileName = QFileDialog.getSaveFileName(self, 'Save your new macro!', name)
    fileName = str(fileName)

    if fileName == '':
        self.raise_()
        return
    if not fileName.endswith(".csv"):
        fileName += ".csv"        
    # If anything else is changed after this, the editor won't let you add to the queue without saving again

    s_data_source = str(self.images_select.text())
    if not os.path.exists(s_data_source):
        displayError(self, "Please select a stitch data source!")
        return
    macrodict["s_data_source"] = s_data_source

    macrodict["s_proc_dir"] = str(self.stitch_saveLocation.text())

    with open(fileName, 'wb') as macro:
        writer = csv.writer(macro)
        for key, value in macrodict.items():
            writer.writerow([key, value])
            
    self.editor.curMacro = mq.Macro(fileName, macrodict)
    self.addToConsole("Macro saved successfully!")
    return 1

def beginStitch(self):
    self.disableWidgets()
    self.stitch_console.moveCursor(QTextCursor.End)
    QApplication.processEvents()
    # self.console.clear()

    self.addToConsole('****************************************************')
    self.addToConsole('********** Beginning Stitch Processing... ***********')
    self.addToConsole('****************************************************')
    QApplication.processEvents()
    
    
    if not os.path.exists(str(self.images_select.text())):
        self.addToConsole("Please select a data source!")
        self.enableWidgets()
        return
    else:
        self.stitch_files_to_process = str(self.images_select.text())
    if  str(self.stitch_saveLocation.text()) == "":
        self.addToConsole("Make sure you select a location to save files!")
        self.enableWidgets()        
        return

    self.stitchThread = StitchThread(self, self.stitch_files_to_process, str(self.stitch_saveLocation.text()), 0)
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
    self.connect(self.stitchThread, SIGNAL("incrementBar(PyQt_PyObject)"), self.incrementBar)
    self.stitchThread.start()    

def stitchImageSelect(self):
    try:
        folderpath = str(QFileDialog.getExistingDirectory(directory=os.getcwd()))
        if folderpath != '':
            self.images_select.setText(folderpath)
            self.stitch_saveLocation.setText(os.path.join(folderpath, "Processed_Stitch"))
            self.stitch_files_to_process = folderpath
    except:
        self.addToConsole("Something went wrong when trying to open your directory.")
        return
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
        if filename == "":
            pixmap = QPixmap("images/SLAC_LogoSD.png", "1")
        self.stitchImage.setPixmap(pixmap.scaled(self.imageWidth, self.imageWidth, Qt.KeepAspectRatio))  
        QApplication.processEvents()
    except:
        self.addToConsole("Could not load stitched image.")
        
    
def setStitchSaveLocation(self):
    path = str(QFileDialog.getExistingDirectory(self, "Select a location for processed files"))
    if path !='':
        self.stitch_saveLocation.setText(os.path.join(path, "Processed_Stitch"))
      
def resetStitch(self):
    setStitchImage(self, "images/SLAC_LogoSD.png")
    self.stitchbar.setValue(0)
    
# Takes a message as an argument and displays it to the screen as a message box     
def displayError(self, message):
    message = QLabel(message)
    self.win = QWidget()
    self.win.setWindowTitle('Error')
    self.ok = QPushButton('Ok')
    self.ly = QVBoxLayout()
    self.ly.addWidget(message)
    self.ly.addWidget(self.ok)
    self.win.setLayout(self.ly)    
    self.ok.clicked.connect(lambda: self.win.close())
    self.win.show()
    self.win.raise_()