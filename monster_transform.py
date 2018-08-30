# This file initializes the widgets and the layout for the transform tab of the GUI. It interfaces
# with the TransformThread to run the transform processes.
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
from QRoundProgressBar import QRoundProgressBar # for the progress bar on the transform page
from PyQt4.QtGui import * # for the GUI
from ClickableLineEdit import * # for all the line edit fields
from monster_queueloader import * # for saving the transform page as a macro
from MONster import displayError # to display errors as message boxes
import monster_queueloader as mq  # for saving the transform page as a macro

# None -> None
# Generates the widgets for the transform tab
def generateTransformWidgets(self):
    pixmap = QPixmap('images/SLAC_LogoSD.png')
    self.raw_image = QLabel()
    self.raw_image.setPixmap(pixmap.scaled(self.imageWidth, self.imageWidth, Qt.KeepAspectRatio))
    self.raw_image.setStyleSheet("QLabel { border-style:outset; border-width:10px;  border-radius: 10px; border-color: rgb(34, 200, 157); color:rgb(0, 0, 0); background-color: rgb(200, 200, 200); } ")

    self.data_label = QLabel("Current data source: (folder)")
    self.data_label.setStyleSheet(self.textStyleSheet)
    self.data_source = ClickableLineEdit()
    self.data_source.setStyleSheet(self.lineEditStyleSheet)
    
    self.data_source.setFixedWidth(580)


    self.folder_button = QPushButton("Select a folder")
    self.folder_button.setFixedSize(self.folder_button.sizeHint().width(), self.folder_button.sizeHint().height())
    self.folder_button.setStyleSheet("background-color: rgb(159, 97, 100); color: black;")
    
    self.file_button = QPushButton("Select one or more files")
    self.file_button.setFixedSize(self.file_button.sizeHint().width(), self.file_button.sizeHint().height())
    self.file_button.setStyleSheet("background-color: rgb(248, 222, 189); color: black;")

    self.t_files_to_process = []
    self.calib_label = QLabel("Current calibration file source:")
    self.calib_label.setStyleSheet(self.textStyleSheet)
    self.calib_source = ClickableLineEdit()
    self.calib_source.setStyleSheet(self.lineEditStyleSheet)
    
    self.calib_source.setFixedWidth(580)
    self.calib_folder_button = QPushButton()
    self.calib_folder_button.setIcon(QIcon('images/folder_select.png'))
    self.calib_folder_button.setIconSize(QSize(25, 25))
    self.calib_folder_button.setFixedSize(35, 35)
    self.calib_folder_button.setStyleSheet('background-color: rgba(34, 200, 157, 100)');     
    
    self.processed_location_label = QLabel("Destination for processed files:")
    self.processed_location_label.setStyleSheet(self.textStyleSheet)
    self.processed_location = ClickableLineEdit(os.path.join(str(self.data_source.text()), "Processed_Transform"))
    self.processed_location.setStyleSheet(self.lineEditStyleSheet)
    self.processed_location.setFixedWidth(580)
    self.processed_location_folder_button = QPushButton()
    self.processed_location_folder_button.setIcon(QIcon('images/folder_select.png'))
    self.processed_location_folder_button.setIconSize(QSize(25, 25))
    self.processed_location_folder_button.setFixedSize(35, 35)
    self.processed_location_folder_button.setStyleSheet('background-color: rgba(34, 200, 157, 100)');     

    self.start_button = QPushButton("Begin Transform")
    self.start_button.setStyleSheet("background-color: rgb(80, 230, 133); color: black;")    
    # self.start_button.setFixedSize(160, 30)
    self.start_button.resize(self.start_button.sizeHint().width(), self.start_button.sizeHint().height())

    self.abort = QPushButton('Abort Transform')
    self.abort.setStyleSheet("background-color: rgb(255, 140, 140); color: black;")              
    # self.abort.setFixedSize(100, 30)
    self.abort.resize(self.abort.sizeHint().width(), self.abort.sizeHint().height())

    self.console = QTextBrowser()
    self.console.setMinimumHeight(150)
    self.console.setMaximumHeight(400)
    self.console.setFont(QFont("Avenir", 14))
    self.console.moveCursor(QTextCursor.End)
    self.console.setStyleSheet("margin:3px; border:1px solid rgb(0, 0, 0); background-color: rgb(240, 255, 240); color: black;")                

    self.custom_calib_label = QLabel("Customize your calibration here: ")
    self.custom_calib_label.setStyleSheet("QLabel {background-color : rgb(29, 30, 50); color: white; }")
    self.dcenterx_label = QLabel("Detector Center X:")
    self.dcenterx_label.setStyleSheet(self.textStyleSheet)
    #self.dcenterx = QLineEdit("1041.58114546")
    self.dcenterx = ClickableLineEdit()
    self.dcenterx.setStyleSheet(self.lineEditStyleSheet)

    self.dcentery_label = QLabel("Detector Center Y:")
    self.dcentery_label.setStyleSheet(self.textStyleSheet)
    #self.dcentery = QLineEdit("2206.61923488")
    self.dcentery = ClickableLineEdit()
    self.dcentery.setStyleSheet(self.lineEditStyleSheet)
    
    self.detectordistance_label = QLabel("Detector Distance:")
    self.detectordistance_label.setStyleSheet(self.textStyleSheet)
    #self.detectordistance = QLineEdit("2521.46747904")
    self.detectordistance = ClickableLineEdit()
    self.detectordistance.setStyleSheet(self.lineEditStyleSheet)
    
    self.detect_tilt_alpha_label = QLabel("Detector Tilt Alpha:")
    self.detect_tilt_alpha_label.setStyleSheet(self.textStyleSheet)
    #self.detect_tilt_alpha = QLineEdit("1.57624384738")
    self.detect_tilt_alpha = ClickableLineEdit()
    self.detect_tilt_alpha.setStyleSheet(self.lineEditStyleSheet)
    
    self.detect_tilt_delta_label = QLabel("Detector Tilt Delta:")
    self.detect_tilt_delta_label.setStyleSheet(self.textStyleSheet)
    #self.detect_tilt_delta = QLineEdit("-0.540278539838")
    self.detect_tilt_delta = ClickableLineEdit()
    self.detect_tilt_delta.setStyleSheet(self.lineEditStyleSheet)
    
    self.wavelength_label = QLabel("Wavelength:")
    self.wavelength_label.setStyleSheet(self.textStyleSheet)
    self.wavelength = ClickableLineEdit()
    self.wavelength.setStyleSheet(self.lineEditStyleSheet)

    self.saveCustomCalib = QPushButton("Save this calibration!")
    self.saveCustomCalib.setStyleSheet("QPushButton {background-color : rgb(60, 60, 60); color: white; }")
    
    # self.saveCustomCalib.setMaximumWidth(170)     
    self.saveCustomCalib.resize(self.saveCustomCalib.sizeHint().width(), self.saveCustomCalib.sizeHint().height())
   
    
    self.transform_saveMacroButton = QPushButton("Save as a macro")
    # self.transform_saveMacroButton.setMaximumWidth(160)
    # self.transform_saveMacroButton.setFixedHeight(30)
    self.transform_saveMacroButton.setStyleSheet("background-color: rgb(255, 251, 208); color: black;")
    self.transform_addToQueueButton = QPushButton("Add this configuration to the queue")
    # self.transform_addToQueueButton.setMaximumWidth(220)
    # self.transform_addToQueueButton.setFixedHeight(30)
    self.transform_saveMacroButton.resize(self.transform_saveMacroButton.sizeHint().width(), self.transform_saveMacroButton.sizeHint().height())

    self.transform_addToQueueButton.setStyleSheet("background-color: rgb(255, 207, 117); color: black;")
    self.transform_addToQueueButton.resize(self.transform_addToQueueButton.sizeHint().width(), self.transform_addToQueueButton.sizeHint().height())

    
    self.bar = QRoundProgressBar()
    self.bar.setFixedSize(150, 150)
    self.bar.setDataPenWidth(.01)
    self.bar.setOutlinePenWidth(.01)
    self.bar.setDonutThicknessRatio(0.85)
    self.bar.setDecimals(1)
    self.bar.setFormat('%p %')
    # self.bar.resetFormat()
    self.bar.setNullPosition(90)
    self.bar.setBarStyle(QRoundProgressBar.StyleDonut)
    self.bar.setDataColors([(0, QColor(qRgb(34, 200, 157))), (1, QColor(qRgb(34, 200, 157)))])
    self.bar.setRange(0, 100)
    #self.bar.setValue(30)
    self.bar.setValue(0)
    
    self.detector_label = QLabel("Select your detector (Only matters for .raw files)")
    self.detector_label.setStyleSheet(self.textStyleSheet)
    self.detectorList = []
    # addDetectorToList(self.detectorList, "PILATUS3 X 100K-A", 487, 195)
    # addDetectorToList(self.detectorList, "PILATUS3 X 200K-A", 487, 407)
    # addDetectorToList(self.detectorList, "PILATUS3 X 300K", 487, 619)
    # addDetectorToList(self.detectorList, "PILATUS3 X 300K-W", 1475, 195)
    # addDetectorToList(self.detectorList, "PILATUS3 X 1M", 981, 1043)
    # addDetectorToList(self.detectorList, "PILATUS3 X 2M", 1475, 1679)
    # addDetectorToList(self.detectorList, "PILATUS3 X 6M", 2463, 2527)
    self.detector_combo = QComboBox()
    self.detector_combo.setStyleSheet("QComboBox { border-radius: 4px;  color:rgb(0, 0, 0); background-color: rgb(255, 255, 255); border-style:outset; border-width:4px;  border-radius: 4px; border-color: rgb(34, 200, 157); color:rgb(0, 0, 0); background-color: rgb(200, 200, 200); } QAbstractItemView{background: pink;}")
    # for detector in self.detectorList:
    #     self.detector_combo.addItem(str(detector))
        
# def addDetectorToList(lst, name, width, height):
#     det = Detector(name, width, height)
#     lst.append(det)

# None -> QVBoxLayout()
# Returns the layout for the transform tab
def generateTransformLayout(self):
    h_box1 = QHBoxLayout()
    h_box1.addStretch()
    h_box1.addWidget(self.bar)
    h_box1.addStretch()
    h_box1.addWidget(self.raw_image)
    h_box1.addStretch()
    #h_box1.addWidget(self.one_d_graph)

    h_box2 = QHBoxLayout()
    h_box2.addWidget(self.data_source)
    #h_box2.addStretch()
    h_box2.addWidget(self.folder_button)
    h_box2.addWidget(self.file_button)
    h_box2.addStretch()


    h_box3 = QHBoxLayout()
    h_box3.addWidget(self.calib_source)
    #h_box3.addStretch()
    h_box3.addWidget(self.calib_folder_button)
    h_box3.addStretch()
    

    h_box4 = QHBoxLayout()
    h_box4.addWidget(self.start_button)
    h_box4.addWidget(self.abort)
    h_box4.addWidget(self.transform_saveMacroButton)
    h_box4.addWidget(self.transform_addToQueueButton)

    h_box4.addStretch()

    h_box5 = QHBoxLayout()
    h_box5.addWidget(self.dcenterx_label)
    h_box5.addWidget(self.dcentery_label)
    h_box5.addWidget(self.detectordistance_label)
    h_box5.addWidget(self.detect_tilt_alpha_label)
    h_box5.addWidget(self.detect_tilt_delta_label)
    h_box5.addWidget(self.wavelength_label)
    #h_box5.addStretch()
    
    h_box7 = QHBoxLayout()
    h_box7.addWidget(self.processed_location)
    h_box7.addWidget(self.processed_location_folder_button)
    
    h_box7.addStretch()
    

    h_box6 = QHBoxLayout()
    h_box6.addWidget(self.dcenterx)
    h_box6.addWidget(self.dcentery)
    h_box6.addWidget(self.detectordistance)
    h_box6.addWidget(self.detect_tilt_alpha)
    h_box6.addWidget(self.detect_tilt_delta)
    h_box6.addWidget(self.wavelength)

    v_box = QVBoxLayout()
    v_box.addLayout(h_box1)
    v_box.addWidget(self.data_label)
    x = QLabel("Data source directory:")
    x.setStyleSheet("color: white;")
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setStyleSheet("color: white;")
    v_box.addWidget(line)
    v_box.addWidget(x)
    v_box.addLayout(h_box2)
    v_box.addWidget(self.calib_label)
    v_box.addLayout(h_box3)
    v_box.addWidget(self.custom_calib_label)
    v_box.addLayout(h_box5)
    v_box.addLayout(h_box6)
    hi = QHBoxLayout()
    hi.addWidget(self.saveCustomCalib)    
    hi.addStretch()
    hi.addWidget(self.detector_label)
    v_box.addLayout(hi)
    h = QHBoxLayout()
    h.addWidget(self.processed_location_label)
    h.addWidget(self.detector_combo)
    v_box.addLayout(h)
    v_box.addLayout(h_box7)


    v_box.addLayout(h_box4)
    v_box.addWidget(self.console)
    return v_box

# None -> None
# Compiles the information on the current transform tab page into a macro and adds it to the queue
def addTransformCurrentToQueue(self):
    cur_time = datetime.datetime.now().strftime('%Y-%m-%d--%H-%M-%S')
    name = (os.path.join(self.mPath, 'transform-macro-%s' %(cur_time)))
    self.addToConsole("Saving this page in directory \"~/macros\" as \"transform-macro-%s\" and adding to the queue..." % (cur_time))
    saved = saveTransformMacro(self, name)
    if saved is None:
        return
    self.macroQueue.append( self.editor.curMacro )       
    macro = QListWidgetItem("Process %s: Added macro \"%s\"" % (mq.curIndex, os.path.basename(str(self.editor.curMacro.getFilename()))))
    mq.curIndex+= 1 
    self.queue.addItem(macro)
    self.editor.close()
    QApplication.processEvents()
    self.addToConsole("Macro saved and added to queue!")
    
# string -> int
# Adds functionality to the transform page "save macro" button; takes all the information currently
# on the transform page and compiles it into a macro to be loaded into the queue. Returns an int if successfully saved.
def saveTransformMacro(self, fileName=''):
    # CHECKING VALUES TO MAKE SURE EVERYTHING IS OKAY BEFORE MACRO CAN BE SAVED
    macrodict = {"workflow" : "False"}
    macrodict["transform"] = "True"
    macrodict["integrate"] = "False"
    macrodict["stitch"] = "False"
    macrodict['transform_integrate'] = 'False'
    try:
        calib_source = str(self.calib_source.text())
        dx = len(str(self.dcenterx.text()))
        dy = len(str(self.dcentery.text()))
        dd = len(str(self.detectordistance.text()))
        wav = len(str(self.wavelength.text()))
        da = len(str(self.detect_tilt_alpha.text()))
        dp = len(str(self.detect_tilt_delta.text()))
        if (not os.path.exists(calib_source)) or dp == 0 or dy == 0 or dx == 0 or dd == 0 or wav == 0 or da == 0:
            displayError(self, "Was not able to locate calibration information.")
            return
        if str(self.calib_source.text()) == '':
            displayError(self, "Please make sure you select a calibration source or save your custom calibration!")
            return        
        if str(self.processed_location.text()) == "":
                self.processed_location.setText(os.path.join(str(self.data_source.text()), "Processed_Transform"))

        if self.t_files_to_process == []:
            self.t_files_to_process = [str(self.data_source.text())]
            t_filenames = self.t_files_to_process
        else:
            t_filenames = self.t_files_to_process    
        t_calib_source = str(self.calib_source.text())

        data_source = str(self.data_source.text())
        #if self.data_source_check.isChecked() and os.path.isfile(self.t_files_to_process[0]):
            #displayError(self, "Please either check the \"I'm going to select a folder\" option or select at least one file.")
            #return
        #elif not self.data_source_check.isChecked() and os.path.isdir(self.t_files_to_process[0]):
            #displayError(self, "Please either check the \"I'm going to select a folder\" option or select at least one file.")
            #return
        if data_source == "":
            displayError(self, "Please select a transform data source!")
            return
        t_proc_dir = str(self.processed_location.text())
        checked_values = (t_filenames, t_calib_source, t_proc_dir)
        macrodict ["t_data_source"] = checked_values[0]
        macrodict['t_calib_source'] = checked_values[1]
        detector = str(self.detector_combo.currentText())
        macrodict["detector_type"] = detector.split(', ')[0]
        t_proc_dir = str(self.processed_location.text())
        macrodict["t_proc_dir"] = checked_values[2]
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
   
 
    with open(fileName, 'wb') as macro:
        writer = csv.writer(macro)
        for key, value in macrodict.items():
            writer.writerow([key, value])
            
    self.editor.curMacro = Macro(fileName, macrodict)
    self.addToConsole("Macro saved successfully!")
    return 1
    
# None -> None
# Begins transform processing, parsing the relevant fields, making sure that the user has entered
# all fields correctly, and then loading and starting the TransformThread
def transformThreadStart(self):

    if self.stitchThread.isRunning() or self.stitchThread.isRunning():
        self.addToConsole("Stop! You're giving me too much to do! Cannot run multiple processes at once.")
        return    
    # Check if the user has correctly selected either a folder or a group of files
    if self.t_files_to_process == []:
        self.addToConsole("Please make sure you select the files you wish to process.")
        self.t_files_to_process = [str(self.data_source.text())]
        self.enableWidgets()
        return        
    #if not self.data_source_check.isChecked() and os.path.isdir(self.t_files_to_process[0]):
        #self.addToConsole("Please make sure you select the files you wish to process, or check the \"I'm going to select a folder\" box.")
        #self.enableWidgets()
        #return

    self.console.moveCursor(QTextCursor.End)
    QApplication.processEvents()
    self.console.clear()
    self.addToConsole('********************************************************')
    self.addToConsole('********** Beginning Transform Processing... ***********')
    self.addToConsole('********************************************************')
    QApplication.processEvents()
    # grab monitor folder
    #root = Tkinter.Tk()
    #root.withdraw()


    save_path = str(self.processed_location.text())
    self.overwrite = False
    self.clicked = False
    if os.path.exists(save_path):
        message = QLabel("Warning! This processed file destination already exists! Are you sure you want to overwrite it?")
        self.win = QWidget()
        self.win.setWindowTitle('Careful!')
        self.yes = QPushButton('Yes')
        self.no = QPushButton('No')
        self.ly = QVBoxLayout()
        self.ly.addWidget(message)
        h = QHBoxLayout()
        h.addWidget(self.yes)
        h.addWidget(self.no)
        self.ly.addLayout(h)
        self.win.setLayout(self.ly)    
        def n():
            self.clicked = True
            self.win.close()
            self.raise_()        
        self.no.clicked.connect(n)
       
        def y():
            self.overwrite = True
            self.clicked = True
            self.win.close()
            self.raise_()
        self.yes.clicked.connect(y)
        self.win.show()
        self.win.raise_()
        while not self.clicked:
            time.sleep(.3)
            QApplication.processEvents()
        if not self.overwrite: 
            return
    self.disableWidgets()
    
    calibPath = str(self.calib_source.text())
    dataPath = str(self.data_source.text())
    #if  os.path.isdir(dataPath) and self.data_source_check.isChecked():
        #self.t_files_to_process = [dataPath]
    # Check if entered calibration information is correctly entered
    if (calibPath is '' and str(self.detectordistance.text()) == '' and str(self.dcenterx.text()) == '' and str(self.dcentery.text()) == '' and str(self.detect_tilt_alpha.text()) == '' and str(self.detect_tilt_delta.text()) == '' and str(self.wavelength.text()) == '') or dataPath is '':

        self.addToConsole("Please make sure you have entered valid data or calibration source information.")
        self.enableWidgets()
        return

    #bkgdPath = os.path.expanduser('~/monHiTp/testBkgdImg/bg/a40_th2p0_t45_center_bg_0001.tif')
    #configPath = tkFileDialog.askopenfilename(title='Select Config File')
    #if bkgdPath is '':
        #self.win.addToConsole('No bkgd file supplied, aborting...')
        #return

   
    self.addToConsole('Calibration File: ' + calibPath)
    self.addToConsole('Folder to process: ' + dataPath)
    self.addToConsole('')        

        # detectorData is just the current calibration attributes that the user has loaded/tweaked
    detectorData = (str(self.detectordistance.text()), str(self.detect_tilt_alpha.text()), str(self.detect_tilt_delta.text()), str(self.wavelength.text()), str(self.dcenterx.text()), str(self.dcentery.text()), str(self.detector_combo.currentText()))
    # Initialize transform thread
    self.transformThread = TransformThread(self, str(self.processed_location.text()), calibPath, detectorData, self.t_files_to_process, 0)
    self.transformThread.setAbortFlag(False)
    # make sure that if the abort button is clicked, it is aborting the current running transform thread, so this needs to be run for every new transform thread
    self.abort.clicked.connect(self.transformThread.abortClicked)
    self.int_abort.clicked.connect(self.transformThread.abortClicked)

    # these connections are the only way the thread can communicate with the MONster
    self.connect(self.transformThread, SIGNAL("addToConsole(PyQt_PyObject)"), self.addToConsole)
    self.connect(self.transformThread, SIGNAL("setRawImage(PyQt_PyObject)"), self.setRawImage)
    self.connect(self.transformThread, SIGNAL("enableWidgets()"), self.enableWidgets)
    self.connect(self.transformThread, SIGNAL("bar(int, PyQt_PyObject)"), self.setRadialBar)
    self.connect(self.transformThread, SIGNAL("finished(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"), self.done)
    self.connect(self.transformThread, SIGNAL("enable()"), self.enableWidgets)
    self.connect(self.transformThread, SIGNAL("resetTransform(PyQt_PyObject)"), resetTransform)
    self.connect(self.transformThread, SIGNAL("incrementBar(PyQt_PyObject)"), self.incrementBar)
    self.transformThread.start()
        
# None -> None
# Resets the transform image to the SLAC Logo
def resetTransform(self):
    self.setRawImage("images/SLAC_LogoSD.png")
    self.bar.setValue(0)