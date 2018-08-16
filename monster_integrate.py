# This file initializes the widgets, layouts, and various functions necessary to run
# the "integrate" tab in MONster.
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
from PyQt4.QtCore import *
from ClickableLineEdit import *
import os, datetime
from IntegrateThread import *
from input_file_parsing import parse_calib
import pyqtgraph as pg
import csv
import numpy as np
# Adds functionality to right-clicking the graph (autoscaling it to bring it to view) and to dragging the mouse (adds a rectangle and zooms into whatever's in that rectangle)
class CustomViewBox(pg.ViewBox):
    def __init__(self, *args, **kwds):
        pg.ViewBox.__init__(self, *args, **kwds)
        self.setMouseMode(self.RectMode)

    ## reimplement right-click to zoom out
    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.autoRange()

    def mouseDragEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            ev.ignore()
        else:
            pg.ViewBox.mouseDragEvent(self, ev)
            


# Generates the widgets for the integrate tab.
def generateIntegrateWidgets(self):
    self.vb = CustomViewBox()
    self.one_d_graph = pg.PlotWidget(viewBox=self.vb, enableMenu=True, title="")
    # Crosshair stuff
    self.label = pg.TextItem(anchor=(1, 1))
    self.one_d_graph.addItem(self.label)
    self.region = pg.LinearRegionItem()
    self.region.setZValue(100)
    self.vLine = pg.InfiniteLine(angle=90, movable=False)
    self.hLine = pg.InfiniteLine(angle=0, movable=False)
    self.one_d_graph.addItem(self.vLine, ignoreBounds=True)
    self.one_d_graph.addItem(self.hLine, ignoreBounds=True)     
    self.one_d_graph.autoRange() 
    self.one_d_graph.sigRangeChanged.connect(self.updateRegion)
    self.region.sigRegionChanged.connect(self.update)
    self.one_d_graph.sigRangeChanged.connect(self.updateRegion)
    self.proxy = pg.SignalProxy(self.one_d_graph.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)   
    self.one_d_graph.setFixedWidth(self.imageWidth)
    self.one_d_graph.setMaximumHeight(self.imageWidth)

    self.miconsole = QTextBrowser()
    self.miconsole.setMinimumHeight(150)
    self.miconsole.setMaximumHeight(300)
    self.miconsole.moveCursor(QTextCursor.End)

    self.miconsole.setFont(QFont("Avenir", 14))
    self.miconsole.setStyleSheet("margin:3px; border:1px solid rgb(0, 0, 0); background-color: rgb(240, 255, 240);")               
    self.q_min_label = QLabel('Q Min:')
    self.q_min_label.setStyleSheet("QLabel {background-color : rgb(29, 30, 50); color: white; }")
    self.q_min = ClickableLineEdit('0.0')
    self.q_min.setStyleSheet(self.lineEditStyleSheet)
    
    self.q_min.setFixedWidth(65)

    self.q_max_label = QLabel('Q Max:')
    self.q_max_label.setStyleSheet("QLabel {background-color : rgb(29, 30, 50); color: white; }")
    self.q_max = ClickableLineEdit('0.0')
    self.q_max.setStyleSheet(self.lineEditStyleSheet)
    
    self.q_max.setFixedWidth(65)

    self.chi_min_label = QLabel("Chi min:")
    self.chi_min_label.setStyleSheet("QLabel {background-color : rgb(29, 30, 50); color: white; }")
    self.chi_min = ClickableLineEdit('0.0')
    self.chi_min.setStyleSheet(self.lineEditStyleSheet)
    
    self.chi_min.setFixedWidth(65)

    self.chi_max_label = QLabel("Chi max:")
    self.chi_max_label.setStyleSheet("QLabel {background-color : rgb(29, 30, 50); color: white; }")
    self.chi_max = ClickableLineEdit('0.0')
    self.chi_max.setStyleSheet(self.lineEditStyleSheet)
    
    self.chi_max.setFixedWidth(65)    
    
    self.int_start_button = QPushButton("Begin Integration")
    self.int_start_button.setStyleSheet("background-color: rgb(80, 230, 133);")    
    self.int_start_button.setFixedSize(160, 30)
    self.int_abort = QPushButton('Abort Integration')
    self.int_abort.setStyleSheet("background-color: rgb(255, 140, 140);")              
    self.int_abort.setFixedSize(150, 30)
    
    self.int_data_label = QLabel("Current data source:")
    self.int_data_label.setStyleSheet(self.textStyleSheet)
    self.int_data_source = ClickableLineEdit()
    self.int_data_source.setStyleSheet(self.lineEditStyleSheet)
    
    self.int_data_source.setFixedWidth(580)
    self.int_data_folder_button = QPushButton()
    self.int_data_folder_button.setIcon(QIcon('images/folder_select.png'))
    self.int_data_folder_button.setIconSize(QSize(25, 25))
    self.int_data_folder_button.setFixedSize(25, 25)
    self.int_data_folder_button.setStyleSheet('border: none;')
    self.int_data_source_check = QCheckBox("I'm going to select a folder")
    self.int_data_source_check.setStyleSheet("QCheckBox {background-color : rgb(29, 30, 50); color: white; }")
    
    self.int_data_source_check.setChecked(True)
    
    self.int_processed_location_label = QLabel("Current location for processed files:")
    self.int_processed_location_label.setStyleSheet(self.textStyleSheet)
    self.int_processed_location = ClickableLineEdit(str(self.int_data_source.text())  + "/Processed_Integrate")
    self.int_processed_location.setStyleSheet(self.lineEditStyleSheet)
    
    self.int_processed_location.setFixedWidth(580)
    self.int_processed_location_folder_button = QPushButton()
    self.int_processed_location_folder_button.setIcon(QIcon('images/folder_select.png'))
    self.int_processed_location_folder_button.setIconSize(QSize(25, 25))
    self.int_processed_location_folder_button.setFixedSize(25, 25)
    self.int_processed_location_folder_button.setStyleSheet('border: none;')    
    
    self.int_custom_calib_label = QLabel("Customize your calibration here: ")
    self.int_custom_calib_label.setStyleSheet(self.textStyleSheet)
    self.int_dcenterx_label = QLabel("Detector Center X:")
    self.int_dcenterx_label.setStyleSheet(self.textStyleSheet)
    #self.int_dcenterx = QLineEdit("1041.58114546")
    self.int_dcenterx = ClickableLineEdit()
    self.int_dcenterx.setStyleSheet(self.lineEditStyleSheet)
    
    self.int_dcentery_label = QLabel("Detector Center Y:")
    self.int_dcentery_label.setStyleSheet(self.textStyleSheet)
    #self.int_dcentery = QLineEdit("2206.61923488")
    self.int_dcentery = ClickableLineEdit()
    self.int_dcentery.setStyleSheet(self.lineEditStyleSheet)
    
    self.int_detectordistance_label = QLabel("Detector Distance:")
    self.int_detectordistance_label.setStyleSheet(self.textStyleSheet)
    #self.int_detectordistance = QLineEdit("2521.46747904")
    self.int_detectordistance = ClickableLineEdit()
    self.int_detectordistance.setStyleSheet(self.lineEditStyleSheet)
    
    self.int_detect_tilt_alpha_label = QLabel("Detector Tilt Alpha:")
    self.int_detect_tilt_alpha_label.setStyleSheet(self.textStyleSheet)
    #self.int_detect_tilt_alpha = QLineEdit("1.57624384738")
    self.int_detect_tilt_alpha = ClickableLineEdit()
    self.int_detect_tilt_alpha.setStyleSheet(self.lineEditStyleSheet)
    
    self.int_detect_tilt_delta_label = QLabel("Detector Tilt Delta:")
    self.int_detect_tilt_delta_label.setStyleSheet(self.textStyleSheet)
    #self.int_detect_tilt_delta = QLineEdit("-0.540278539838")
    self.int_detect_tilt_delta = ClickableLineEdit()
    self.int_detect_tilt_delta.setStyleSheet(self.lineEditStyleSheet)
    
    self.int_wavelength_label = QLabel("Wavelength:")
    self.int_wavelength_label.setStyleSheet(self.textStyleSheet)
    self.int_wavelength = ClickableLineEdit()
    self.int_wavelength.setStyleSheet(self.lineEditStyleSheet)
    
    self.int_saveCustomCalib = QPushButton("Save this calibration!")
    self.int_saveCustomCalib.setStyleSheet("QPushButton {background-color : rgb(60, 60, 60); color: white; }")
    self.int_saveCustomCalib.setMaximumWidth(170)            
    
    self.int_calib_label = QLabel("Current calibration file source:")
    self.int_calib_label.setStyleSheet(self.textStyleSheet)
    self.int_calib_source = ClickableLineEdit()
    self.int_calib_source.setStyleSheet(self.lineEditStyleSheet)
    self.int_calib_source.setFixedWidth(580)
    self.int_calib_folder_button = QPushButton()
    self.int_calib_folder_button.setIcon(QIcon('images/folder_select.png'))
    self.int_calib_folder_button.setIconSize(QSize(25, 25))
    self.int_calib_folder_button.setFixedSize(25, 25)
    self.int_calib_folder_button.setStyleSheet('border: none;')
    self.int_bar = QRoundProgressBar()
    self.int_bar.setFixedSize(150, 150)
    self.int_bar.setDataPenWidth(.01)
    self.int_bar.setOutlinePenWidth(.01)
    self.int_bar.setDonutThicknessRatio(0.85)
    self.int_bar.setDecimals(1)
    self.int_bar.setFormat('%p %')
    self.int_bar.setNullPosition(90)
    self.int_bar.setBarStyle(QRoundProgressBar.StyleDonut)
    self.int_bar.setDataColors([(0, QColor(qRgb(34, 200, 157))), (1, QColor(qRgb(34, 200, 157)))])
    self.int_bar.setRange(0, 100)
    self.int_bar.setValue(0)    
    
    self.centerButton = QPushButton("Center Graph to Q and Chi Range")
    self.centerButton.setStyleSheet("QPushButton {background-color: olive;}")
    

    
# Takes a filename and displays the 1D image specified by the filename on the GUI.
def set1DImage(self, filename):
    try:
        with open(filename, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            qArray = []
            integrated_cake = []
            for row in reader:
                x = 0 # do something to skip line
                break
            for row in reader:
                qArray.append(float(row[0]))
                integrated_cake.append(float(row[1]))
                
            #qArray = reader['x0000']
            #integrated_cake = reader['y0000']
        self.one_d_graph.plot(qArray, integrated_cake)
        # pixmap = QPixmap(filename)
        # if filename == "":
        #     pixmap = QPixmap("images/SLAC_LogoSD.png", "1")        
        # self.one_d_graph.setPixmap(pixmap.scaled(self.imageWidth, self.imageWidth, Qt.KeepAspectRatio))  
        QApplication.processEvents()
    except:
        traceback.print_exc()
        self.addToConsole("Could not load integrated image.")
        

# Generates the layout for the integrate tab.
def generateIntegrateLayout(self):
    v_box1 = QVBoxLayout()
    h_box1 = QHBoxLayout()
    h1 = QHBoxLayout()
    h2 = QHBoxLayout()
    h3 = QHBoxLayout()
    h4 = QHBoxLayout()
    h1.addWidget(self.q_min_label)
    h1.addStretch()
    h1.addWidget(self.q_min)
    v_box1.addLayout(h1)
    h2.addWidget(self.q_max_label)
    h2.addStretch()
    h2.addWidget(self.q_max)
    v_box1.addLayout(h2)
    h3.addWidget(self.chi_min_label)
    h3.addStretch()
    h3.addWidget(self.chi_min)
    v_box1.addLayout(h3)
    h4.addWidget(self.chi_max_label)
    h4.addStretch()
    h4.addWidget(self.chi_max)
    v_box1.addLayout(h4)
    v_box1.addWidget(self.centerButton)
    h_box1.addStretch()
    h_box1.addWidget(self.int_bar)
    h_box1.addStretch()
    h_box1.addWidget(self.one_d_graph)
    h_box1.addStretch()
    h_box1.addLayout(v_box1)
    layout = QVBoxLayout()
    layout.addLayout(h_box1)
    h_box2 = QHBoxLayout()
    h_box2.addWidget(self.int_data_source)
    #h_box2.addStretch()
    h_box2.addWidget(self.int_data_folder_button)
    h_box2.addWidget(self.int_data_source_check)
    h_box2.addStretch()
    layout.addWidget(self.int_data_label)
    layout.addLayout(h_box2)
    layout.addWidget(self.int_calib_label)
    h_box3 = QHBoxLayout()
    h_box3.addWidget(self.int_calib_source)
    #h_box3.addStretch()
    h_box3.addWidget(self.int_calib_folder_button)
    h_box3.addStretch()
    layout.addLayout(h_box3)
    layout.addWidget(self.int_custom_calib_label)
    h_box5 = QHBoxLayout()
    h_box5.addWidget(self.int_dcenterx_label)
    h_box5.addWidget(self.int_dcentery_label)
    h_box5.addWidget(self.int_detectordistance_label)
    h_box5.addWidget(self.int_detect_tilt_alpha_label)
    h_box5.addWidget(self.int_detect_tilt_delta_label)
    h_box5.addWidget(self.int_wavelength_label)    
    layout.addLayout(h_box5)
    h_box6 = QHBoxLayout()
    h_box6.addWidget(self.int_dcenterx)
    h_box6.addWidget(self.int_dcentery)
    h_box6.addWidget(self.int_detectordistance)
    h_box6.addWidget(self.int_detect_tilt_alpha)
    h_box6.addWidget(self.int_detect_tilt_delta)
    h_box6.addWidget(self.int_wavelength)
    layout.addLayout(h_box6)
    layout.addWidget(self.int_saveCustomCalib)
    h_box7 = QHBoxLayout()
    h_box7.addWidget(self.int_processed_location)
    h_box7.addWidget(self.int_processed_location_folder_button)
    h_box7.addStretch()
    layout.addWidget(self.int_processed_location_label)
    layout.addLayout(h_box7)
    h = QHBoxLayout()
    h.addWidget(self.int_start_button)
    h.addWidget(self.int_abort)
    h.addStretch()
    layout.addLayout(h)
    layout.addWidget(self.miconsole)
    return layout

# Begins integration processing, parsing the relevant calibration fields, making sure that the user has entered
# all fields correctly, and then loading and starting the IntegrateThread
def integrateThreadStart(self):

    if not self.int_data_source_check.isChecked() and os.path.isdir(self.files_to_process[0]):
        self.addToConsole("Please make sure you select the files you wish to process, or check the \"I'm going to select a folder\" box.")
        self.enableWidgets()
        return
        
    self.disableWidgets()
    self.miconsole.moveCursor(QTextCursor.End)
    QApplication.processEvents()
    self.console.clear()
    self.addToConsole('********************************************************')
    self.addToConsole('********** Beginning Integrate Processing... ***********')
    self.addToConsole('********************************************************')
    QApplication.processEvents()
    # grab monitor folder
    #root = Tkinter.Tk()
    #root.withdraw()
    try:
        q1 = float(str(self.q_min.text()))
        q2 = float(str(self.q_max.text()))
        c1 = float(str(self.chi_min.text()))
        
        c2 = float(str(self.chi_max.text()))
    except:
        self.addToConsole("Please make sure you have entered in appropriate values for the QRange and the ChiRange.")
        self.enableWidgets()
        return
    
    calibPath = str(self.int_calib_source.text())
    dataPath = str(self.int_data_source.text())
    if  os.path.isdir(dataPath) and self.int_data_source_check.isChecked():
        self.files_to_process = [dataPath]        
    if (calibPath is '' and str(self.int_detectordistance.text()) == '' and str(self.int_dcenterx.text()) == '' and str(self.int_dcentery.text()) == '' and str(self.int_detect_tilt_alpha.text()) == '' and str(self.int_detect_tilt_delta.text()) == '' and str(self.int_wavelength.text()) == '') or dataPath is '':
            
        self.addToConsole("Please make sure you have entered valid data or calibration source information.")
        self.enableWidgets()
        return

    bkgdPath = os.path.expanduser('~/monHiTp/testBkgdImg/bg/a40_th2p0_t45_center_bg_0001.tif')
    #configPath = tkFileDialog.askopenfilename(title='Select Config File')
    if bkgdPath is '':
        self.win.addToConsole('No bkgd file supplied, aborting...')
        self.enableWidgets()
        return
        
    self.addToConsole('Calibration File: ' + calibPath)
    self.addToConsole('Folder to process: ' + dataPath)
    self.addToConsole('')        
    self.QRange = (float(str(self.q_min.text())), float(str(self.q_max.text())))
#            ChiRange = (config['ChiMin'],config['ChiMax'])
    self.ChiRange = (float(str(self.chi_min.text())), float(str(self.chi_max.text())))    
    if abs(self.QRange[1]-self.QRange[0]) < .01:
        self.addToConsole("Please select a Q range.")
        self.enableWidgets()
        return
    if abs(self.ChiRange[1] - self.ChiRange[0]) < 0.1:
        self.addToConsole("Please select a more reasonable Chi range.")
        self.enableWidgets()
        return        
    


    detectorData = (self.int_detectordistance.text(), self.int_detect_tilt_alpha.text(), self.int_detect_tilt_delta.text(), self.int_wavelength.text(), self.int_dcenterx.text(), self.int_dcentery.text())
    self.integrateThread = IntegrateThread(self, calibPath, str(self.int_processed_location.text()), detectorData, self.files_to_process, (self.QRange, self.ChiRange), 0)
    self.integrateThread.setAbortFlag(False)
    self.int_abort.clicked.connect(self.integrateThread.abortClicked)
    
    self.connect(self.integrateThread, SIGNAL("addToConsole(PyQt_PyObject)"), self.addToConsole)
    self.connect(self.integrateThread, SIGNAL("enableWidgets()"), self.enableWidgets)
    #self.connect(self.integrateThread, SIGNAL("set1DImage(PyQt_PyObject, PyQt_PyObject)"), set1DImage)
    self.connect(self.integrateThread, SIGNAL("finished(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"), self.done)
    self.connect(self.integrateThread, SIGNAL("bar(int, PyQt_PyObject)"), self.setRadialBar)
    self.connect(self.integrateThread, SIGNAL("resetIntegrate(PyQt_PyObject)"), resetIntegrate)
    self.connect(self.integrateThread, SIGNAL("incrementBar(PyQt_PyObject)"), self.incrementBar)
    self.disableWidgets()
    self.integrateThread.start()
    
def getIntCalibSourcePath(self):
    path = str(QFileDialog.getOpenFileName(self, "Select Calibration File", ('/Users/arunshriram/Documents/SLAC Internship/monhitp-gui/calib/')))
    if path !='':
        self.int_calib_source.setText(path)
        loadIntCalibration(self)
        
def getIntDataSourceDirectoryPath(self):
    if self.int_data_source_check.isChecked():
        try:
            folderpath = str(QFileDialog.getExistingDirectory())
            if folderpath != '':
                self.int_data_source.setText(folderpath)
                self.int_data_label.setText("Current data source:")
                self.int_processed_location.setText(os.path.join(folderpath, "Processed_Integrate"))
                self.files_to_process = [folderpath]
        except:
            self.addToConsole("Something went wrong when trying to open your directory.")
    else:
        try:
          
            filenames = QFileDialog.getOpenFileNames(self, "Select the files you wish to use.")
            filenames = [str(filename) for  filename in filenames]
            if len(filenames) < 2:
                self.int_data_label.setText("Current data source: %s" % os.path.basename(filenames[0]))
            else:
                self.int_data_label.setText("Current data source: (multiple files)")
            self.int_data_source.setText(os.path.dirname(filenames[0]))
            self.int_processed_location.setText(os.path.join(str(self.int_data_source.text()),  "Processed_Integrate"))
            self.files_to_process = filenames
        except:
            #traceback.print_exc()
            self.addToConsole("Something went wrong when trying to select your files.")
    
    
def centerButtonClicked(self):
    try:
        q1 = float(str(self.q_min.text()))
        q2 = float(str(self.q_max.text()))
        chi1 = float(str(self.chi_min.text()))
        chi2 = float(str(self.chi_max.text()))
    except:
        self.addToConsole("Please make sure you have correctly entered your Q and Chi ranges.")
        self.enableWidgets()
        return
    self.one_d_graph.autoRange()
    self.one_d_graph.setLimits(xMin=q1, xMax=q2)
    
        
def loadIntCalibration(self):
    if str(self.int_calib_source.text()) != '':
        try:
            d_in_pixel, Rotation_angle, tilt_angle, lamda, x0, y0 = parse_calib(str(self.int_calib_source.text()))
        except:
            self.addToConsole("Unable to locate calibration source file.")
            return
        self.int_wavelength.setText(str(lamda))
        self.int_detectordistance.setText(str(d_in_pixel))
        self.int_dcenterx.setText(str(x0))
        self.int_dcentery.setText(str(y0))
        self.int_detect_tilt_alpha.setText(str(Rotation_angle))
        self.int_detect_tilt_delta.setText(str(tilt_angle))

def setIntProcessedLocation(self):
    path = str(QFileDialog.getExistingDirectory(self, "Select a location for processed files", str(self.int_data_source.text())))
    #path = str(QFileDialog.getOpenFileName(self, "Select Calibration File", ('/Users/arunshriram/Documents/SLAC Internship/monhitp-gui/calib/')))
    if path !='':
        self.int_processed_location.setText(os.path.join(path, "Processed_Integrate"))
    
def saveIntCalibAction(self):
    name = ('/Users/arunshriram/Documents/SLAC Internship/monhitp-gui/calib/cal-%s.calib') %(datetime.datetime.now().strftime('%Y-%m-%d--%H-%M-%S'))
    fileName = QFileDialog.getSaveFileName(self, 'Save your new custom calibration!', name)
    try:
        with open(fileName, 'w') as calib:
            for i in range(6):
                calib.write('-\n')
            calib.write("bcenter_x=" + str(self.int_dcenterx.text()) + '\n')
            calib.write("bcenter_y=" + str(self.int_dcentery.text()) + '\n')
            calib.write("detect_dist=" + str(self.int_detectordistance.text()) + '\n')
            calib.write("detect_tilt_alpha=" + str(self.int_detect_tilt_alpha.text()) + '\n')
            calib.write("detect_tilt_delta=" + str(self.int_detect_tilt_delta.text()) + '\n')
            calib.write("wavelength=" + str(self.int_wavelength.text()) + '\n')
            calib.write('-\n')
        self.int_calib_source.setText(os.path.expanduser(str(fileName)))
    except:
        self.addToConsole("Calibration could not be saved!")
        return

    
    
def resetIntegrate(self):
    set1DImage(self, "images/SLAC_LogoSD.png")
    self.int_bar.setValue(0)