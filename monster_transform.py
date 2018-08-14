# This file initializes the widgets and the layout for the transform tab of the GUI. It interfaces
# with the TransformThread to run the transform processes.
#
# This is one of the seven main files (IntegrateThread, MONster, monster_queueloader, monster_transform, monster_stitch, TransformThread, StitchThread) that controls the MONster GUI. 
#
# Runs with PyQt4, SIP 4.19.3, Python version 2.7.5
# 
# Author: Arun Shriram
# Written for my SLAC Internship at SSRL
# File Start Date: June 25, 2018
# File End Date: 
#
#
from QRoundProgressBar import QRoundProgressBar
from PyQt4.QtGui import *
from ClickableLineEdit import *
from monster_queueloader import *

# Generates the widgets for the transform tab
def generateTransformWidgets(self):
    pixmap = QPixmap('images/SLAC_LogoSD.png')
    self.raw_image = QLabel()
    self.raw_image.setPixmap(pixmap.scaled(self.imageWidth, self.imageWidth, Qt.KeepAspectRatio))
    self.raw_image.setStyleSheet("QLabel { border-style:outset; border-width:10px;  border-radius: 10px; border-color: rgb(34, 200, 157); color:rgb(0, 0, 0); background-color: rgb(200, 200, 200); } ")

    self.data_label = QLabel("Current data source:")
    self.data_label.setStyleSheet(self.textStyleSheet)
    self.data_source = ClickableLineEdit()
    self.data_source.setStyleSheet(self.lineEditStyleSheet)
    
    self.data_source.setFixedWidth(580)
    self.data_folder_button = QPushButton()
    self.data_folder_button.setIcon(QIcon('images/folder_select.png'))
    self.data_folder_button.setIconSize(QSize(25, 25))
    self.data_folder_button.setFixedSize(25, 25)
    self.data_folder_button.setStyleSheet('border: none;')

    self.data_source_check = QCheckBox("I'm going to select a folder")
    self.data_source_check.setStyleSheet("QCheckBox {color: white; }")
    
    self.data_source_check.setChecked(True)

    self.files_to_process = []
    self.calib_label = QLabel("Current calibration file source:")
    self.calib_label.setStyleSheet(self.textStyleSheet)
    self.calib_source = ClickableLineEdit()
    self.calib_source.setStyleSheet(self.lineEditStyleSheet)
    
    self.calib_source.setFixedWidth(580)
    self.calib_folder_button = QPushButton()
    self.calib_folder_button.setIcon(QIcon('images/folder_select.png'))
    self.calib_folder_button.setIconSize(QSize(25, 25))
    self.calib_folder_button.setFixedSize(25, 25)
    self.calib_folder_button.setStyleSheet('border: none;')
    
    self.processed_location_label = QLabel("Current location for processed files:")
    self.processed_location_label.setStyleSheet(self.textStyleSheet)
    self.processed_location = ClickableLineEdit(str(self.data_source.text()) + "/Processed_Transform")
    self.processed_location.setStyleSheet(self.lineEditStyleSheet)
    self.processed_location.setFixedWidth(580)
    self.processed_location_folder_button = QPushButton()
    self.processed_location_folder_button.setIcon(QIcon('images/folder_select.png'))
    self.processed_location_folder_button.setIconSize(QSize(25, 25))
    self.processed_location_folder_button.setFixedSize(25, 25)
    self.processed_location_folder_button.setStyleSheet('border: none;')

    self.start_button = QPushButton("Begin Transform")
    self.start_button.setStyleSheet("background-color: rgb(80, 230, 133);")    
    self.start_button.setFixedSize(160, 30)
    self.abort = QPushButton('Abort Transform')
    self.abort.setStyleSheet("background-color: rgb(255, 140, 140);")              
    self.abort.setFixedSize(100, 30)

    self.console = QTextBrowser()
    self.console.setMinimumHeight(150)
    self.console.setMaximumHeight(300)
    self.console.setFont(QFont("Avenir", 14))
    self.console.moveCursor(QTextCursor.End)
    self.console.setStyleSheet("margin:3px; border:1px solid rgb(0, 0, 0); background-color: rgb(240, 255, 240);")                

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
    
    self.saveCustomCalib.setMaximumWidth(170)        
    
    self.saveMacroButton = QPushButton("Save as a macro")
    self.saveMacroButton.setMaximumWidth(160)
    self.saveMacroButton.setFixedHeight(30)
    self.saveMacroButton.setStyleSheet("background-color: rgb(255, 251, 208);")
    self.addToQueueButton = QPushButton("Add this configuration to the queue")
    self.addToQueueButton.setMaximumWidth(220)
    self.addToQueueButton.setFixedHeight(30)
    self.addToQueueButton.setStyleSheet("background-color: rgb(255, 207, 117);")
    
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
        
def addDetectorToList(lst, name, width, height):
    det = Detector(name, width, height)
    lst.append(det)

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
    h_box2.addWidget(self.data_folder_button)
    h_box2.addWidget(self.data_source_check)
    h_box2.addStretch()


    h_box3 = QHBoxLayout()
    h_box3.addWidget(self.calib_source)
    #h_box3.addStretch()
    h_box3.addWidget(self.calib_folder_button)
    h_box3.addStretch()
    

    h_box4 = QHBoxLayout()
    h_box4.addWidget(self.start_button)
    h_box4.addWidget(self.abort)
    h_box4.addWidget(self.saveMacroButton)
    h_box4.addWidget(self.addToQueueButton)

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
    v_box.addLayout(h_box2)
    v_box.addWidget(self.calib_label)
    v_box.addLayout(h_box3)
    v_box.addWidget(self.custom_calib_label)
    v_box.addLayout(h_box5)
    v_box.addLayout(h_box6)
    v_box.addWidget(self.saveCustomCalib)    
    h = QHBoxLayout()
    h.addWidget(self.processed_location_label)
    h.addWidget(self.detector_combo)
    v_box.addLayout(h)
    v_box.addLayout(h_box7)


    v_box.addLayout(h_box4)
    v_box.addWidget(self.console)
    return v_box

# Adds functionality to the "save macro" button; takes all the information currently
# on the transform page and compiles it into a macro to be loaded into the queue
def saveMacro(self, fileName=''):
    if (str(self.calib_source.text()) == '' and str(self.dcenterx.text()) == '') or str(self.data_source.text()) == '' or str(self.q_min.text()) == '' or str(self.q_max.text()) == '' or str(self.chi_min.text()) == '' or str(self.chi_max.text()) == '':
        displayError(self, "Unable to save macro! Please make sure all values are correctly filled in.")    
        return
    try:
        q1 = float(str(self.q_min.text()))
        q2 = float(str(self.q_max.text()))
        c1 = float(str(self.chi_min.text()))
        
        c2 = float(str(self.chi_max.text()))
    except:
        displayError(self, "Please make sure you have entered in appropriate values for the QRange and the ChiRange.")
        return        
    transform = True
    stitch = False
    integrate = False
    self.editor.transformCheck.setChecked(True)
    self.editor.stitchCheck.setChecked(False)
    self.editor.integrateCheck.setChecked(False)
    if str(self.calib_source.text()) == '':
        displayError(self, "Please make sure you select a calibration source or save your custom calibration!")
        return        
    if fileName == '':
        cur_time = datetime.datetime.now().strftime('%Y-%m-%d--%H-%M-%S')
        name = ('/Users/arunshriram/Documents/SLAC Internship/monhitp-gui/macros/transform-macro-%s') %(cur_time)        
        fileName = QFileDialog.getSaveFileName(self, 'Save your new macro!', name)
        fileName = str(fileName)
    if fileName == '': # If the user has clicked cancel in the file dialog
        self.raise_()
        return

    self.editor.curMacro = Macro(fileName, (str(self.q_min.text()), str(self.q_max.text())), (str(self.chi_min.text()), str(self.chi_max.text())), None, str(self.detector_combo.currentText()), str(self.processed_location.text()), None, transform, stitch, integrate)

    
    with open(fileName, 'w') as macro:
        macro.write("qmin, qmax, chimin, chimax, calib_source, detectortype, filename, processed_file_source, folder?, data_source_file(s)/directory\n")
        data_source = "1"
        filenames = tuple([])
        calib_filename = ''
        
     
        calib_filename = str(self.calib_source.text())
        if os.path.isdir(self.files_to_process[0]):
            data_source = "0"
            filenames += tuple(self.files_to_process)
        else:
            filenames += (str(self.data_source.text()),)
        
        
        self.editor.curMacro.setCalibInfo(calib_filename)
        self.editor.curMacro.setDataInfo(data_source, filenames)
        macro.write(("%s, %s, %s, %s, %s, %s, ") % (self.editor.curMacro.getQRange()[0], self.editor.curMacro.getQRange()[1], self.editor.curMacro.getChiRange()[0], self.editor.curMacro.getChiRange()[1], str(self.editor.curMacro.getCalibInfo()), str(self.detector_combo.currentText())) + "%s, " % str(self.editor.curMacro.getProcessedFileDir()) + ", ".join([str(s) for s in list(self.editor.curMacro.getDataFiles())]))
        macro.write('\n%s\n' % transform)
        macro.write('%s\n' % stitch)
        macro.write('%s' % integrate)
    self.editor.macroSelected.setText("Current macro selected: %s" % (os.path.join(os.path.dirname(fileName).split("/")[-1], os.path.basename(fileName))))
        

# Begins the transform thread
def transformThreadStart(self):
    # Check if the user has correctly selected either a folder or a group of files
    
    if not self.data_source_check.isChecked() and os.path.isdir(self.files_to_process[0]):
        self.addToConsole("Please make sure you select the files you wish to process, or check the \"I'm going to select a folder\" box.")
        self.enableWidgets()
        return

    self.disableWidgets()
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



    calibPath = str(self.calib_source.text())
    dataPath = str(self.data_source.text())
    if  os.path.isdir(dataPath) and self.data_source_check.isChecked():
        self.files_to_process = [dataPath]
    # Check if entered calibration information is correctly entered
    if (calibPath is '' and str(self.detectordistance.text()) == '' and str(self.dcenterx.text()) == '' and str(self.dcentery.text()) == '' and str(self.detect_tilt_alpha.text()) == '' and str(self.detect_tilt_delta.text()) == '' and str(self.wavelength.text()) == '') or dataPath is '':

        self.addToConsole("Please make sure you have entered valid data or calibration source information.")
        self.enableWidgets()
        return

    bkgdPath = os.path.expanduser('~/monHiTp/testBkgdImg/bg/a40_th2p0_t45_center_bg_0001.tif')
    #configPath = tkFileDialog.askopenfilename(title='Select Config File')
    if bkgdPath is '':
        self.win.addToConsole('No bkgd file supplied, aborting...')
        return

    self.addToConsole('Calibration File: ' + calibPath)
    self.addToConsole('Folder to process: ' + dataPath)
    self.addToConsole('')        

        # detectorData is just the current calibration attributes that the user has loaded/tweaked
    detectorData = (str(self.detectordistance.text()), str(self.detect_tilt_alpha.text()), str(self.detect_tilt_delta.text()), str(self.wavelength.text()), str(self.dcenterx.text()), str(self.dcentery.text()), str(self.detector_combo.currentText()))
    # Initialize transform thread
    self.transformThread = TransformThread(self, str(self.processed_location.text()), calibPath, detectorData, self.files_to_process)
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
    self.transformThread.start()
        
def resetTransform(self):
    self.setRawImage("images/SLAC_LogoSD.png")
    self.bar.setValue(0)