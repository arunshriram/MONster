# This file initializes the widgets and the layout for the stitch tab of the GUI. It interfaces
# with the StitchThread to run the stitching processes.
#
# This is one of the nine main files (HelpDialog, monster_integrate, monster_stitch, 
# monster_transform, MONster, TransformThread, StitchThread, IntegrateThread, monster_queueloader) 
# that control the MONster GUI. 
#
# Runs with PyQt4, SIP 4.19.3, Python version 2.7.5
# 
# Author: Arun Shriram
# Written for my SLAC Internship at SSRL
# File Start Date: June 25, 2018
# File End Date: August 31, 2018
#
#
from PyQt4.QtGui import * # for the GUI
from PyQt4.QtCore import * # for the GUI
import os, datetime, csv # for file saving
from ClickableLineEdit import ClickableLineEdit # for all the line edit fields
from StitchThread import * # for stitch processing
from QRoundProgressBar import QRoundProgressBar # for progress bar on stitch page
import monster_queueloader as mq # for saving the stitch page as a macro

# None -> None
# Generates the widgets for the stitch tab.
def generateStitchWidgets(self):
    self.stitchImage = QLabel()
    pixmap = QPixmap('images/SLAC_LogoSD.png')
    self.stitchImage.setPixmap(pixmap.scaled(self.imageWidth, self.imageWidth, Qt.KeepAspectRatio))
    self.stitchImage.setStyleSheet('QLabel { border-style:outset; border-width:10px;  border-radius: 10px; border-color: rgb(34, 200, 157); color:rgb(0, 0, 0); background-color: rgb(200, 200, 200); } ')
    self.images_select = ClickableLineEdit()
    self.images_select.setFixedWidth(580)
    self.images_select.setStyleSheet(self.lineEditStyleSheet)
    self.images_select_files_button = QLabel()
    self.images_select_files_button.setFixedSize(25, 25)    
    self.images_select_files_button.setPixmap(QPixmap('images/folder_select.png').scaled(self.images_select_files_button.sizeHint().width(), self.images_select_files_button.sizeHint().height()))
    self.images_select_files_button.setStyleSheet('border: none;')
    self.stitch_folder_button = QPushButton("Select a folder")
    self.stitch_folder_button.setFixedSize(self.stitch_folder_button.sizeHint().width(), self.stitch_folder_button.sizeHint().height())
    self.stitch_folder_button.setStyleSheet("background-color: rgb(159, 97, 100); color: black;")
     
    self.stitch_abort = QPushButton('Abort Stitching')
    self.stitch_abort.setStyleSheet("background-color: rgb(255, 140, 140); color: black;")              
    self.stitch_abort.resize(self.stitch_abort.sizeHint().width(), self.stitch_abort.sizeHint().height())

    # self.stitch_abort.setFixedSize(150, 30)    
    
    self.saveLabel = QLabel("File Save Location:")
    self.saveLabel.setStyleSheet("QLabel {color: white;}")
    self.stitch_saveLocation = ClickableLineEdit()
    self.stitch_saveLocation.setStyleSheet(self.lineEditStyleSheet)
    self.stitch_saveLocation.setFixedWidth(580)
    self.stitch_saveLocation_button = QPushButton()
    self.stitch_saveLocation_button.setIcon(QIcon("images/folder_select.png"))
    self.stitch_saveLocation_button.setFixedSize(35 ,35)
    self.stitch_saveLocation_button.setIconSize(QSize(25, 25))
    self.stitch_saveLocation_button.setStyleSheet('background-color: rgba(34, 200, 157, 100)');     

    self.stitch_start_button = QPushButton('Begin Stitching!')
    self.stitch_start_button.setStyleSheet('background-color: rgb(80, 230, 133); color: black;')
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
    self.stitch_console.setMaximumHeight(400)
    self.stitch_console.moveCursor(QTextCursor.End)
    self.stitch_data_label = QLabel("Current data folder:")
    self.stitch_data_label.setStyleSheet("QLabel {color: white;}")
    self.stitch_console.setFont(QFont('Avenir', 14))
    self.stitch_console.setStyleSheet('margin:3px; border:1px solid rgb(0, 0, 0); background-color: rgb(240, 255, 240);  color: black;')
    
    self.stitch_saveMacroButton = QPushButton("Save as a macro")
    # self.stitch_saveMacroButton.setMaximumWidth(160)
    # self.stitch_saveMacroButton.setFixedHeight(30)
    self.stitch_saveMacroButton.resize(self.stitch_saveMacroButton.sizeHint().width(), self.stitch_saveMacroButton.sizeHint().height())

    self.stitch_saveMacroButton.setStyleSheet("background-color: rgb(255, 251, 208);color: black;")
    self.stitch_addToQueueButton = QPushButton("Add this configuration to the queue")
    # self.stitch_addToQueueButton.setMaximumWidth(220)
    # self.stitch_addToQueueButton.setFixedHeight(30)
    self.stitch_addToQueueButton.setStyleSheet("background-color: rgb(255, 207, 117); color: black;")
    self.stitch_addToQueueButton.resize(self.stitch_addToQueueButton.sizeHint().width(), self.stitch_addToQueueButton.sizeHint().height())

    self.stitch_files_to_process = None

# None -> QVBoxLayout
# Generates the layout for the integrate tab.
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
    fileSelect.addWidget(self.stitch_folder_button)
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

# None -> None
# Compiles the information on the current stitch tab page into a macro and adds it to the queue
def addStitchCurrentToQueue(self):
    cur_time = datetime.datetime.now().strftime('%Y-%m-%d--%H-%M-%S')
    name = (os.path.join(self.mPath, 'stitch-macro-%s' %(cur_time)))
    self.addToConsole("Saving this page in directory \"~/macros\" as \"stitch-macro-%s\" and adding to the queue..." % (cur_time))
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
    
# None -> int
# Adds functionality to the stitch page "save macro" button; takes all the information currently
# on the stitch page and compiles it into a macro to be loaded into the queue. Returns an int if successfully saved.
def saveStitchMacro(self, fileName=''):
    # CHECKING VALUES TO MAKE SURE EVERYTHING IS OKAY BEFORE MACRO CAN BE SAVED
    macrodict = {"workflow" : "False"}
    macrodict["transform"] = 'False'
    macrodict["integrate"] = 'False'
    macrodict["stitch"] = 'True'
    macrodict['transform_integrate'] = 'False'
    try:
        data_source = str(self.images_select.text()).lstrip().rstrip()
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
    final_dir = os.path.join(current, self.mPath)
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)
            
    cur_time = datetime.datetime.now().strftime('%Y-%m-%d--%H-%M-%S')
    name = (final_dir + '/macro-%s.csv') %(cur_time)        
    fileName = QFileDialog.getSaveFileName(self, 'Save your new macro!', name)
    fileName = str(fileName)
    self.raise_()
    if fileName == '':
        self.raise_()
        return
    if not fileName.endswith(".csv"):
        fileName += ".csv"        
    # If anything else is changed after this, the editor won't let you add to the queue without saving again

    s_data_source = str(self.images_select.text()).lstrip().rstrip()
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

# None -> None
# Begins stitch processing, parsing the relevant fields, making sure that the user has entered
# all fields correctly, and then loading and starting the StitchThread
def beginStitch(self):
    self.stitch_console.moveCursor(QTextCursor.End)
    QApplication.processEvents()
    # self.console.clear()

    if self.transformThread.isRunning() or self.integrateThread.isRunning():
        self.addToConsole("Stop! You're giving me too much to do! Cannot run multiple processes at once.")
        return
    self.addToConsole('****************************************************')
    self.addToConsole('********** Beginning Stitch Processing... ***********')
    self.addToConsole('****************************************************')
    QApplication.processEvents()

    # dialog that opens to check if user wants to overwrite/appendto/cancel for existing processed directory   
    save_path = str(self.stitch_saveLocation.text())
    self.overwrite = False
    self.clicked = False
    self.addToFolder = False
    if os.path.exists(save_path):
        message = QLabel("Warning! This processed file destination already exists! Are you sure you want to overwrite the entire folder?")
        self.win = QWidget()
        self.win.setWindowTitle('Careful!')
        self.yes = QPushButton('Yes, overwrite it')
        self.add = QPushButton("Just add new files to the same folder")
        self.no = QPushButton('Cancel')
        self.ly = QVBoxLayout()
        self.ly.addWidget(message)
        h = QHBoxLayout()
        h.addWidget(self.yes)
        h.addWidget(self.add)
        h.addWidget(self.no)
        self.ly.addLayout(h)
        self.win.setLayout(self.ly)    
        def n():
            self.clicked = True
            self.overwrite = False
            self.addToFolder = False
            self.win.close()
            self.raise_()        
        self.no.clicked.connect(n)
       
        def y():
            self.overwrite = True
            self.addToFolder = False
            self.clicked = True
            self.win.close()
            self.raise_()
        self.yes.clicked.connect(y)
        def add():
            self.addToFolder = True
            self.clicked = True
            self.overwrite = False
            self.win.close()
            self.raise_()
        self.add.clicked.connect(add)
        self.win.show()
        self.win.raise_()
        while not self.clicked:
            time.sleep(.3)
            QApplication.processEvents()
        if not self.addToFolder and not self.overwrite:
            return
    self.disableWidgets()
    # data checking before starting stitch
    if not os.path.exists(str(self.images_select.text()).lstrip().rstrip()):
        self.addToConsole("Please select a valid data source!")
        self.enableWidgets()
        return
    else:
        self.stitch_files_to_process = str(self.images_select.text()).lstrip().rstrip()
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
    self.connect(self.stitchThread, SIGNAL("enableWidgets()"), self.enableWidgets)
    self.stitchThread.start()    

# None -> None
# Retreives and stores the data source path for stitch processing
def stitchImageSelect(self):
    try:
        folderpath = str(QFileDialog.getExistingDirectory(self, "Select your data source", self.home))
        if folderpath != '':
            self.images_select.setText(folderpath)
            self.stitch_saveLocation.setText(os.path.join(folderpath, "Processed_Stitch"))
            self.stitch_files_to_process = folderpath
        self.raise_()
    except:
        self.addToConsole("Something went wrong when trying to open your directory.")
        return

# list -> None
# Calculates the output message for what should be done after a stitch thread is finished
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

# string -> None
# Adds the current stitched image to the stitch page, takes a filename for the image to display.
def setStitchImage(self, filename):
    try:
        pixmap = QPixmap(filename)   
        if filename == "" or not os.path.exists(filename):
            pixmap = QPixmap("images/SLAC_LogoSD.png", "1")
            self.addToConsole("Could not load stitched image.")
            
        self.stitchImage.setPixmap(pixmap.scaled(self.imageWidth, self.imageWidth, Qt.KeepAspectRatio))  
        QApplication.processEvents()
    except:
        self.addToConsole("Could not load stitched image.")
        return
        
    
# None -> None
# Sets the processed file location for stitch
def setStitchSaveLocation(self):
    path = str(QFileDialog.getExistingDirectory(self, "Select a location for processed files", self.home))
    if path !='':
        self.stitch_saveLocation.setText(os.path.join(path, "Processed_Stitch"))
    self.raise_()
# None -> None
# Resets the stitch image to the SLAC Logo
def resetStitch(self):
    setStitchImage(self, "images/SLAC_LogoSD.png")
    self.stitchbar.setValue(0)
    
# string -> None
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

    frameGm = self.frameGeometry()
    screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
    centerPoint = QApplication.desktop().screenGeometry(screen).center()
    frameGm.moveCenter(centerPoint)
    self.win.move(frameGm.topLeft())