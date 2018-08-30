# This file initializes the various widgets used in the queue loader tab and its layout. It also
# includes a class that defines what a Macro is and a class for the macro editor itself, interfacing that
# with MONster.
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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os, traceback, glob
from ClickableLineEdit import *
import datetime
from input_file_parsing import parse_calib
from MONster import displayError
from IntegrateThread import *
from TransformThread import *
from StitchThread import *
import monster_stitch as ms
import monster_integrate as mi
from QRoundProgressBar import QRoundProgressBar
from TransformThread import Detector
import csv, ast, json
curIndex = 1

class Macro():
    def __init__(self, filename, dictionary):
        self.filename = filename
        self.mdict = dictionary

    def getMacroDict(self):
        return self.mdict
        
    def isWorkflow(self):
        return "True" in self.mdict['workflow']

    def isTransformIntegrate(self):
        return "True" in self.mdict['transform_integrate']

    def getFilename(self):
        return self.filename
    
    def setCalibInfo(self, calib_source):
        self.mdict['t_calib_source'] = calib_source
        self.parseDetectorData()

    def getTDataFiles(self):
        return self.mdict['t_data_source']
    
    def getSDataFiles(self):
        return self.mdict['s_data_source']
        
    def getIDataFiles(self):
        return self.mdict['i_data_source']
        
    def shouldTransform(self):
        return "True" in self.mdict['transform']
    
    def shouldStitch(self):
        return "True" in self.mdict['stitch']
    
    def shouldIntegrate(self):
        return "True" in self.mdict['integrate']
    
    def getQRange(self):
        return (self.mdict['qmin'], self.mdict['qmax'])
    
    def getTProcessedFileDir(self):
        return self.mdict['t_proc_dir']
    
    def getIProcessedFileDir(self):
        return self.mdict['i_proc_dir']
    
    def getSProcessedFileDir(self):
        return self.mdict['s_proc_dir']
    
    def getTCalibInfo(self):
        return self.mdict['t_calib_source']   
    
    def getChiRange(self):
        return (self.mdict['chimin'], self.mdict['chimax'])
    
    def parseDetectorData(self):
        try:
            d_in_pixel, Rotation_angle, tilt_angle, lamda, x0, y0 = parse_calib(self.mdict['t_calib_source'])
        except:
            traceback.print_exc()
            return
        return (d_in_pixel, Rotation_angle, tilt_angle, lamda, x0, y0, self.mdict['detector_type'])
            
    def getDetectorData(self):
        return self.parseDetectorData()
    
class MacroEditor(QWidget):
    def __init__(self, windowreference):
        QWidget.__init__(self)
        self.home = os.path.expanduser("~")
        self.bkpath = os.path.join(self.home, "MONster_Bookkeeping")
        self.pPath = os.path.join(self.bkpath, "Properties.csv")
        self.tPath = os.path.join(self.bkpath, "thisRun.txt")
        self.mPath = os.path.join(self.home, "macros")    
        self.fieldsChanged = False
        self.curMacro = None        
        self.t_files_to_process = []        
        self.s_files_to_process = []
        self.i_files_to_process = []
        self.detectorList = []
        
        self.windowreference = windowreference
        # Stack information (Qstack, that is)
        self.Stack = QStackedWidget(self)
        self.welcome = QWidget()
        self.transformStack = QWidget()
        self.stitchStack = QWidget()
        self.integrateStack = QWidget()
        self.Stack.addWidget(self.welcome)
        self.Stack.addWidget(self.transformStack)
        self.Stack.addWidget(self.stitchStack)
        self.Stack.addWidget(self.integrateStack)
        self.stackList = QListWidget()
        self.stackList.insertItem(0, "Macro Editor")
        self.stackList.insertItem(1, "Transform")
        self.stackList.insertItem(2, "Stitch")
        self.stackList.insertItem(3, "Integrate")
        self.stackList.setFont(QFont("Georgia", 20))
        self.stackList.setFixedWidth(200)
        self.stackList.setSpacing(20)
     
        self.saveButton = QPushButton("Save this macro")
        self.saveButton.setFixedSize(self.saveButton.sizeHint().width(), self.saveButton.sizeHint().height())
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setFixedSize(self.cancelButton.sizeHint().width(), self.cancelButton.sizeHint().height())
        self.addToQueueButton = QPushButton("Add this macro the queue!")
        self.addToQueueButton.setFixedSize(self.addToQueueButton.sizeHint().width(), self.addToQueueButton.sizeHint().height())
        self.loadMacroButton = QPushButton("Load a macro")
        self.loadMacroButton.setFixedSize(self.loadMacroButton.sizeHint().width(), self.loadMacroButton.sizeHint().height())
        self.macroSelected = QLabel("Current macro selected: ")
        self.tipLabel = QLabel("Note: Always save any changes you make before adding to the queue! Unsaved changes will not update the macro.")

        font = QFont()
        font.setBold(True)
        self.macroSelected.setFont(font)

        vbox = QVBoxLayout()
        vbox.addWidget(self.macroSelected)
        vbox.addWidget(self.tipLabel)
        hbox = QHBoxLayout()
        hbox.addWidget(self.stackList)
        hbox.addWidget(self.Stack)
        v = QVBoxLayout()
        v.addWidget(self.saveButton)
        v.addWidget(self.loadMacroButton)
        v.addWidget(self.addToQueueButton)
        v.addWidget(self.cancelButton)
        hbox.addLayout(v)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        
        self.stack1UI()
        self.stack2UI()
        self.stack3UI()        
        self.stack0UI() # needs to be done last because the other widgets need to be initialized before we can disable or enable them
        def hello():
            if self.integrateCheck.isChecked():
                self.int_data_source.setText(self.processed_location.text())

        self.integrateCheck.stateChanged.connect(hello)        
        
    
        self.setWindowTitle("Add or edit a macro!")
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())        
        self.updateConnections()        
        
    def display(self, i):
        self.Stack.setCurrentIndex(i)        
    
    def workflowClicked(self):
        self.transformCheck.setDisabled(True)
        self.stitchCheck.setDisabled(True)
        self.integrateCheck.setDisabled(True)
        self.images_select.setDisabled(True)
        self.images_select_files_button.setDisabled(True)
        self.stitch_saveLocation.setDisabled(True)
        self.stitch_saveLocation_button.setDisabled(True)
        self.int_data_source.setDisabled(True)
        self.int_data_folder.setDisabled(True)
        self.int_folder_button.setDisabled(True)
        self.int_file_button.setDisabled(True)        
        self.int_processed_location.setDisabled(True)
        self.int_processed_location_folder_button.setDisabled(True)
        

    def independentClicked(self):
        self.transformCheck.setEnabled(True)
        self.stitchCheck.setEnabled(True)
        self.integrateCheck.setEnabled(True)
        self.images_select.setEnabled(True)
        self.images_select_files_button.setEnabled(True)
        self.stitch_saveLocation.setEnabled(True)
        self.stitch_saveLocation_button.setEnabled(True)
        self.int_data_source.setEnabled(True)
        self.int_processed_location.setEnabled(True)
        self.int_data_folder.setEnabled(True)
        self.int_folder_button.setEnabled(True)
        self.int_file_button.setEnabled(True)
        self.int_processed_location_folder_button.setEnabled(True)

    def stack0UI(self):

        
        message = "The Macro Editor is a tool to help make large processes a little faster to put together and easier to automate. \nNow, you can Transform, Stitch, or Integrate your files easily! Simply check which of the processes you want \nto be performed, edit the appropriate settings within each field, save your macro, and add it to the \nqueue! You can also load previously saved macros and add them to the queue or edit them."
        self.infoLabel = QLabel(message)
        
        

        self.checkLabel = QLabel("Select at one of the following:")
        self.workflowCheckLabel = QLabel("Select a data source and set the appropriate calibration, \nprocessed location, and Q and Chi range parameters. The transform \nprocesss will output .mat files, which will be stitched together \nand then integrated.")

       

        self.transformCheck = QCheckBox("Transform")
        self.stitchCheck = QCheckBox("Stitch")
        self.integrateCheck = QCheckBox("Integrate") 
        self.transform_integrate = False
        def check():
            if self.transformCheck.isChecked() and self.integrateCheck.isChecked() and self.independent.isChecked():
                win = QWidget()
                layout = QVBoxLayout()
                message = "Would you like to integrate the files that you transform?"
                yes = QPushButton("Yes")
                no = QPushButton("No")
                layout.addWidget(QLabel(message))
                h = QHBoxLayout()
                h.addWidget(no)
                h.addWidget(yes)
                layout.addLayout(h)
                win.setLayout(layout)
                win.show()
                win.raise_()
                def yesclicked():
                    self.transform_integrate = True
                    self.int_data_source.setDisabled(True)
                    self.int_processed_location.setDisabled(True)
                    self.int_folder_button.setDisabled(True)
                    self.int_file_button.setDisabled(True)
                    self.int_processed_location_folder_button.setDisabled(True)
                    self.transform_integrate_label.setText("Integrate tranformed files: On")
                    win.close()
                def noclicked():
                    self.transform_integrate = False
                    win.close()
                yes.clicked.connect(yesclicked)
                no.clicked.connect(noclicked)
            else:
                self.transform_integrate = False
                self.int_data_source.setEnabled(True)
                self.int_processed_location.setEnabled(True)
                self.int_folder_button.setEnabled(True)
                self.int_file_button.setEnabled(True)
                self.int_processed_location_folder_button.setEnabled(True)
                self.transform_integrate_label.setText("Integrate tranformed files: Off")


        self.transformCheck.stateChanged.connect(check)
        self.integrateCheck.stateChanged.connect(check)

        self.workflow = QRadioButton("Workflow")
        self.independent = QRadioButton("Independent")
        self.workflow.setChecked(True)
        self.workflowClicked()
        self.workflow.clicked.connect(self.workflowClicked)
        self.independent.clicked.connect(self.independentClicked)
        self.transform_integrate_label = QLabel("Integrate tranformed files: Off")
        
        vbox = QVBoxLayout()
        h = QHBoxLayout()
        vbox.addStretch()
        vbox.addWidget(self.infoLabel)
        vbox.addStretch()
        vbox.addWidget(self.checkLabel)
        hbox = QHBoxLayout()
        workflow = QVBoxLayout()
        independent = QVBoxLayout()
        workflow.addWidget(self.workflow)
        workflow.addStretch()
        workflow.addWidget(self.workflowCheckLabel)
        hbox.addLayout(workflow)
        independent.addWidget(self.independent)
        independent.addStretch()
        independent.addWidget(self.transformCheck)
        independent.addWidget(self.stitchCheck)
        independent.addWidget(self.integrateCheck)
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        hbox.addWidget(line)
        hbox.addLayout(independent)
        hbox.addWidget(self.transform_integrate_label)
        vbox.addLayout(hbox)
        vbox.addWidget(self.transformCheck)
        vbox.addWidget(self.stitchCheck)
        vbox.addWidget(self.integrateCheck)
        h.addLayout(vbox)
        
        self.welcome.setLayout(h)
        
    def stack1UI(self):
        self.data_label = QLabel("Current data source: (folder)")
        #self.data_source = QLineEdit("/Users/arunshriram/Documents/SLAC Internship/test")
        self.data_source = ClickableLineEdit()
        self.data_source.setFixedWidth(580)
        self.data_folder = QLabel()
        self.data_folder.setFixedSize(25, 25)
        self.data_folder.setPixmap(QPixmap('images/folder_select_gray.png').scaled(25, 25))
        self.data_folder.setStyleSheet('border: none;')
        self.folder_button = QPushButton("Select a folder")
        self.folder_button.setFixedSize(self.folder_button.sizeHint().width(), self.folder_button.sizeHint().height())
        
        self.file_button = QPushButton("Select one or more files")
        self.file_button.setFixedSize(self.file_button.sizeHint().width(), self.file_button.sizeHint().height())
    
    
        self.calib_label = QLabel("Current calibration file source:")
        #self.calib_source = QLineEdit("/Users/arunshriram/Documents/SLAC Internship/calib/cal_28mar18.calib")
        self.calib_source = ClickableLineEdit()
        self.calib_source.setFixedWidth(580)
        self.calib_folder_button = QPushButton()
        self.calib_folder_button.setIcon(QIcon('images/folder_select_gray.png'))
        self.calib_folder_button.setIconSize(QSize(25, 25))
        self.calib_folder_button.setFixedSize(35, 35)
    
        self.processed_location_label = QLabel("Destination for processed files:")
        self.processed_location = ClickableLineEdit(self.data_source.text())
        self.processed_location.setFixedWidth(580)
        self.processed_location_folder_button = QPushButton()
        self.processed_location_folder_button.setIcon(QIcon('images/folder_select_gray.png'))
        self.processed_location_folder_button.setIconSize(QSize(25, 25))
        self.processed_location_folder_button.setFixedSize(35, 35)
    
        self.custom_calib_label = QLabel("Customize your calibration here: ")
        self.dcenterx_label = QLabel("Detector Center X:")
        #self.dcenterx = QLineEdit("1041.58114546")
        self.dcenterx = ClickableLineEdit()
        self.dcentery_label = QLabel("Detector Center Y:")
        #self.dcentery = QLineEdit("2206.61923488")
        self.dcentery = ClickableLineEdit()
        self.detectordistance_label = QLabel("Detector Distance:")
        #self.detectordistance = QLineEdit("2521.46747904")
        self.detectordistance = ClickableLineEdit()
        self.detect_tilt_alpha_label = QLabel("Detector Tilt Alpha:")
        #self.detect_tilt_alpha = QLineEdit("1.57624384738")
        self.detect_tilt_alpha = ClickableLineEdit()
        self.detect_tilt_delta_label = QLabel("Detector Tilt Delta:")
        #self.detect_tilt_delta = QLineEdit("-0.540278539838")
        self.detect_tilt_delta = ClickableLineEdit()
        self.wavelength_label = QLabel("Wavelength:")
        self.wavelength = ClickableLineEdit()
    
        self.saveCustomCalib = QPushButton("Save this calibration!")
        self.saveCustomCalib.setMaximumWidth(170)        
        self.addDetectorToList(self.detectorList, "PILATUS3 X 100K-A", 487, 195)
        self.addDetectorToList(self.detectorList, "PILATUS3 X 200K-A", 487, 407)
        self.addDetectorToList(self.detectorList, "PILATUS3 X 300K", 487, 619)
        self.addDetectorToList(self.detectorList, "PILATUS3 X 300K-W", 1475, 195)
        self.addDetectorToList(self.detectorList, "PILATUS3 X 1M", 981, 1043)
        self.addDetectorToList(self.detectorList, "PILATUS3 X 2M", 1475, 1679)
        self.addDetectorToList(self.detectorList, "PILATUS3 X 6M", 2463, 2527)
        self.detector_combo = QComboBox()
        for detector in self.detectorList:
            self.detector_combo.addItem(str(detector))        

        v_box1 = QVBoxLayout()
        v_box1.addWidget(self.data_label)
        x = QLabel("Data source directory:")
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        v_box1.addWidget(line)
        v_box1.addWidget(x)
        h_box2 = QHBoxLayout()
        h_box2.addWidget(self.data_source)
        h_box2.addWidget(self.folder_button)
        h_box2.addWidget(self.file_button)
        h_box2.addStretch()
        v_box1.addLayout(h_box2)
        v_box1.addWidget(self.calib_label)
        h_box3 = QHBoxLayout()
        h_box3.addWidget(self.calib_source)
        h_box3.addWidget(self.calib_folder_button)
        h_box3.addStretch()
        v_box1.addLayout(h_box3)
        h__box3 = QHBoxLayout()
        h__box3.addWidget(self.custom_calib_label)
        h__box3.addWidget(self.saveCustomCalib)
        h__box3.addStretch()
        v_box1.addLayout(h__box3)
        h_box4 = QHBoxLayout()
        h_box4.addWidget(self.dcenterx_label)
        h_box4.addWidget(self.dcentery_label)
        h_box4.addWidget(self.detectordistance_label)
        h_box4.addWidget(self.detect_tilt_alpha_label)
        h_box4.addWidget(self.detect_tilt_delta_label)
        h_box4.addWidget(self.wavelength_label)
        v_box1.addLayout(h_box4)
        h_box5 = QHBoxLayout()
        h_box5.addWidget(self.dcenterx)
        h_box5.addWidget(self.dcentery)
        h_box5.addWidget(self.detectordistance)
        h_box5.addWidget(self.detect_tilt_alpha)
        h_box5.addWidget(self.detect_tilt_delta)
        h_box5.addWidget(self.wavelength)
        v_box1.addLayout(h_box5)
        h = QHBoxLayout()
        h.addWidget(self.processed_location_label)
        h.addStretch()
        h.addWidget(self.detector_combo)
        v_box1.addLayout(h)
        h_box6 = QHBoxLayout()
        h_box6.addWidget(self.processed_location)
        h_box6.addWidget(self.processed_location_folder_button)
        h_box6.addStretch()
        v_box1.addLayout(h_box6)
        
        self.transformStack.setLayout(v_box1)
        
    def addDetectorToList(self, lst, name, width, height):
        det = Detector(name, width, height)
        lst.append(det)        
        
    def stack2UI(self):
        self.images_select = ClickableLineEdit()
        self.images_select.setFixedWidth(580)
        self.images_select_files_button = QPushButton()
        self.images_select_files_button.setIcon(QIcon('images/folder_select_gray.png'))
        self.images_select_files_button.setIconSize(QSize(25, 25))
        self.images_select_files_button.setFixedSize(35, 35)
        #self.images_select_files_button.setStyleSheet('border: none;')
        self.saveLabel = QLabel("File Save Location:")
        #self.saveLabel.setStyleSheet("QLabel {color: white;}")
        self.stitch_saveLocation = ClickableLineEdit()
        self.stitch_saveLocation.setFixedWidth(580) 
        self.stitch_saveLocation_button = QPushButton()
        self.stitch_saveLocation_button.setIcon(QIcon("images/folder_select_gray.png"))
        self.stitch_saveLocation_button.setFixedSize(35 ,35)
        self.stitch_saveLocation_button.setIconSize(QSize(25, 25))
        #self.stitch_saveLocation_button.setStyleSheet("border: none;")
    
        self.stitch_data_label = QLabel("Current data folder:")
        #self.stitch_data_label.setStyleSheet("QLabel {color: white;}")
        v_box = QVBoxLayout()
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
       
        self.stitchStack.setLayout( v_box)
        
    def stack3UI(self):
        self.q_min_label = QLabel('Q Min:')
        #self.q_min_label.setStyleSheet("QLabel {background-color : rgb(29, 30, 50); color: white; }")
        self.q_min = ClickableLineEdit('0.0')
        self.q_min.setFixedWidth(65)
    
        self.q_max_label = QLabel('Q Max:')
        #self.q_max_label.setStyleSheet("QLabel {background-color : rgb(29, 30, 50); color: white; }")
        self.q_max = ClickableLineEdit('0.0')
        
        self.q_max.setFixedWidth(65)
    
        self.chi_min_label = QLabel("Chi min:")
        #self.chi_min_label.setStyleSheet("QLabel {background-color : rgb(29, 30, 50); color: white; }")
        self.chi_min = ClickableLineEdit('0.0')
        
        self.chi_min.setFixedWidth(65)
    
        self.chi_max_label = QLabel("Chi max:")
        #self.chi_max_label.setStyleSheet("QLabel {background-color : rgb(29, 30, 50); color: white; }")
        self.chi_max = ClickableLineEdit('0.0')
        
        self.chi_max.setFixedWidth(65)    
        
        self.int_data_label = QLabel("Current data source: (folder)")
        self.int_data_source = ClickableLineEdit()
        self.int_folder_button = QPushButton("Select a folder")
        self.int_folder_button.setFixedSize(self.int_folder_button.sizeHint().width(), self.int_folder_button.sizeHint().height())
    
        self.int_file_button = QPushButton("Select one or more files")
        self.int_file_button.setFixedSize(self.int_file_button.sizeHint().width(), self.int_file_button.sizeHint().height())        
        self.int_data_source.setFixedWidth(580)
        self.int_data_folder = QLabel()
        self.int_data_folder.setPixmap(QPixmap('images/folder_select_gray.png').scaled(25, 25))
        self.int_data_folder.setFixedSize(25, 25)
        #self.int_data_folder_button.setStyleSheet('border: none;')
        
        
        self.int_processed_location_label = QLabel("Destination for processed files:")
        self.int_processed_location = ClickableLineEdit(self.int_data_source.text())
        
        self.int_processed_location.setFixedWidth(580)
        self.int_processed_location_folder_button = QPushButton()
        self.int_processed_location_folder_button.setIcon(QIcon('images/folder_select_gray.png'))
        self.int_processed_location_folder_button.setIconSize(QSize(25, 25))
        self.int_processed_location_folder_button.setFixedSize(35, 35)
        #self.int_processed_location_folder_button.setStyleSheet('border: none;')    
        
      
        hbox = QHBoxLayout()
        v_box1 = QVBoxLayout()
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
        
        layout = QVBoxLayout()
        x = QLabel("Data source directory:")
        line = QFrame()
        line.setFrameShape(QFrame.HLine)        
        h_box2 = QHBoxLayout()
        h_box2.addWidget(self.int_data_source)
        #h_box2.addStretch()
        h_box2.addWidget(self.int_data_folder)
        h_box2.addWidget(self.int_folder_button)
        h_box2.addWidget(self.int_file_button)
        h_box2.addStretch()
        layout.addWidget(self.int_data_label)
        layout.addWidget(line)
        layout.addWidget(x)
        layout.addLayout(h_box2)
        
        h_box7 = QHBoxLayout()
        h_box7.addWidget(self.int_processed_location)
        h_box7.addWidget(self.int_processed_location_folder_button)
        h_box7.addStretch()
        layout.addWidget(self.int_processed_location_label)
        layout.addLayout(h_box7)
        
        hbox.addLayout(layout)
        hbox.addStretch()
        hbox.addLayout(v_box1)
        self.integrateStack.setLayout(hbox)

       
     

    def updateConnections(self):
        self.cancelButton.clicked.connect(lambda: self.close())
        self.loadMacroButton.clicked.connect(self.loadMacro)
        self.addToQueueButton.clicked.connect(lambda: addMacroToQueue(self.windowreference))
        self.saveCustomCalib.clicked.connect(self.saveCalibAction)
        self.folder_button.clicked.connect(self.getTransformDataSourceDirectoryPath)
        self.file_button.clicked.connect(self.getTransformDataSourceFiles)
        self.int_folder_button.clicked.connect(self.getIntegrateDataSourceDirectoryPath)
        self.int_file_button.clicked.connect(self.getIntegrateDataSourceFiles)        
        self.calib_folder_button.clicked.connect(self.getCalibSourcePath)
        self.processed_location_folder_button.clicked.connect(self.setProcessedLocation)        
        self.int_processed_location_folder_button.clicked.connect(self.setIntProcessedLocation)
        self.saveButton.clicked.connect(self.saveMacro)
        self.stackList.currentRowChanged.connect(self.display)
        self.images_select_files_button.clicked.connect(self.stitchImageSelect)
        self.stitch_saveLocation_button.clicked.connect(self.setStitchSaveLocation)
        
        for editor in self.findChildren(ClickableLineEdit):
            editor.textChanged.connect(lambda: self.setFieldsChanged(True))
        for box in self.findChildren(QCheckBox):
            box.stateChanged.connect(lambda: self.setFieldsChanged(True))        
        self.detector_combo.currentIndexChanged.connect(lambda: self.setFieldsChanged(True))


    
    def setStitchSaveLocation(self):
        path = str(QFileDialog.getExistingDirectory(self, "Select a location for processed files", self.home))
        if path !='':
            self.stitch_saveLocation.setText(os.path.join(path, "Processed_Stitch"))
        self.raise_()
    def stitchImageSelect(self):
        try:
            folderpath = str(QFileDialog.getExistingDirectory(self, 'Select your data source', self.home))
            if folderpath != '':
                self.images_select.setText(folderpath)
                self.stitch_saveLocation.setText(os.path.join(folderpath, "Processed_Stitch"))
                self.s_files_to_process = [folderpath]
            self.raise_()
        except:
            displayError(self, "Something went wrong when trying to open your directory.")
            return
    
    def setFieldsChanged(self, boo):
        self.fieldsChanged = boo
        
      # Loads the appropriate files based on the data source the user selects
    def getTransformDataSourceDirectoryPath(self):
        try:
            folderpath = str(QFileDialog.getExistingDirectory(self, "Select your data source", self.home))
            if folderpath != '':
                self.data_source.setText(folderpath)
                self.data_label.setText("Current data source: (folder)")
                self.processed_location.setText(str(self.data_source.text()).lstrip().rstrip()  + "/Processed_Transform")
                self.t_files_to_process = [folderpath]
            self.raise_()
        except:
            self.addToConsole("Something went wrong when trying to open your directory.")
     
     # Loads the appropriate files based on the data source the user selects
    def getTransformDataSourceFiles(self):
        try:
            filenames = QFileDialog.getOpenFileNames(self, "Select the files you wish to use.", self.home)
            filenames = [str(filename) for  filename in filenames]
            if len(filenames) < 2:
                self.data_label.setText("Current data source: %s" % os.path.basename(filenames[0]))
            else:
                self.data_label.setText("Current data source: (multiple files)")
            print(filenames)
            self.data_source.setText(os.path.dirname(filenames[0]))
            self.processed_location.setText(str(self.data_source.text()).lstrip().rstrip()  + "/Processed_Transform")
            self.t_files_to_process = filenames
            self.raise_()
        except:
            #traceback.print_exc()
            self.addToConsole("Did not select a data source.")   
            
       # Loads the appropriate files based on the data source the user selects
    def getIntegrateDataSourceDirectoryPath(self):
        try:
            folderpath = str(QFileDialog.getExistingDirectory(self, "Select your data source.", self.home))
            if folderpath != '':
                self.int_data_source.setText(folderpath)
                self.int_data_label.setText("Current data source: (folder)")
                self.int_processed_location.setText(str(self.data_source.text()).lstrip().rstrip()  + "/Processed_Transform")
                self.i_files_to_process = [folderpath]
                self.raise_()
        except:
            self.addToConsole("Something went wrong when trying to open your directory.")

        # Loads the appropriate files based on the data source the user selects
    def getIntegrateDataSourceFiles(self):
        try:
            filenames = QFileDialog.getOpenFileNames(self, "Select the files you wish to use.", self.home)
            filenames = [str(filename) for  filename in filenames]
            if len(filenames) < 2:
                self.int_data_label.setText("Current data source: %s" % os.path.basename(filenames[0]))
            else:
                self.int_data_label.setText("Current data source: (multiple files)")
            print(filenames)
            self.int_data_source.setText(os.path.dirname(filenames[0]))
            self.int_processed_location.setText(str(self.data_source.text()).lstrip().rstrip()  + "/Processed_Transform")
            self.i_files_to_process = filenames
            self.raise_()
        except:
            #traceback.print_exc()
            self.addToConsole("Did not select a data source.")   
        
    def getCalibSourcePath(self):
        path = str(QFileDialog.getOpenFileName(self, "Select Calibration File", self.home))
        if path !='':
            self.calib_source.setText(path)
            self.loadCalibration()
        self.raise_()
            
    def setProcessedLocation(self):
        path = str(QFileDialog.getExistingDirectory(self, "Select a location for processed files", str(self.data_source.text()).lstrip().rstrip()))
        if path.endswith('/untitled'):
            path = path[:len(path) - 9]        
        if path !='':
            self.processed_location.setText(os.path.join(path, "Processed_Transform"))
        self.raise_()
        
    def setIntProcessedLocation(self):
        path = str(QFileDialog.getExistingDirectory(self, "Select a location for processed files", str(self.int_data_source.text()).lstrip().rstrip()))
        if path.endswith('/untitled'):
            path = path[:len(path) - 9]        
        if path !='':
            self.int_processed_location.setText(os.path.join(path, "Processed_Integrate"))
        self.raise_()
     
    def saveCalibAction(self):
        name = ('/Users/arunshriram/Documents/SLAC Internship/monhitp-gui/calib/cal-%s.calib') %(datetime.datetime.now().strftime('%Y-%m-%d--%H-%M-%S'))
        fileName = QFileDialog.getSaveFileName(self, 'Save your new custom calibration!', name)
        try:
            with open(fileName, 'w') as calib:
                for i in range(6):
                    calib.write('-\n')
                calib.write("bcenter_x=" + str(self.dcenterx.text()) + '\n')
                calib.write("bcenter_y=" + str(self.dcentery.text()) + '\n')
                calib.write("detect_dist=" + str(self.detectordistance.text()) + '\n')
                calib.write("detect_tilt_alpha=" + str(self.detect_tilt_alpha.text()) + '\n')
                calib.write("detect_tilt_delta=" + str(self.detect_tilt_delta.text()) + '\n')
                calib.write("wavelength=" + str(self.wavelength.text()) + '\n')
                calib.write('-\n')
            self.calib_source.setText(os.path.expanduser(str(fileName)))
            self.raise_()
        except:
            self.addToConsole("Calibration not saved!")
            return        
        
 
    
    def addToConsole(self, message):
        self.windowreference.addToConsole(message)
        
    def checkTransformValues(self):
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
                self.processed_location.setText(os.path.join(str(self.data_source.text()).lstrip().rstrip(), "Processed_Transform"))

        if self.t_files_to_process == []:
            self.t_files_to_process = [str(self.data_source.text()).lstrip().rstrip()]
            t_filenames = self.t_files_to_process
        else:
            t_filenames = self.t_files_to_process    
        t_calib_source = str(self.calib_source.text())

        data_source = str(self.data_source.text()).lstrip().rstrip()

        if data_source == "":
            displayError(self, "Please select a transform data source!")
            return
        t_proc_dir = str(self.processed_location.text())
        return (t_filenames, t_calib_source, t_proc_dir)

    def checkIntegrateValues(self):

        if str(self.int_processed_location.text()) == "":
                self.int_processed_location.setText(os.path.join(str(self.int_data_source.text()).lstrip().rstrip(), "Processed_Integrate"))

        if self.i_files_to_process == []:
            self.i_files_to_process = [str(self.int_data_source.text()).lstrip().rstrip()]
            i_filenames = self.i_files_to_process
        else:
            i_filenames = self.i_files_to_process    

        data_source = str(self.int_data_source.text()).lstrip().rstrip()
       
        if data_source == "":
            displayError(self, "Please select a integrate data source!")
            return
        i_proc_dir = str(self.int_processed_location.text())
        try:
            QRange = (float(str(self.q_min.text())), float(str(self.q_max.text())))
            #            ChiRange = (config['ChiMin'],config['ChiMax'])
            ChiRange = (float(str(self.chi_min.text())), float(str(self.chi_max.text())))    
            if abs(QRange[1]-QRange[0]) < .01:
                displayError(self, "Please select a more reasonable Q range.")
                return  
            if abs(ChiRange[1] - ChiRange[0]) < 0.1:  
                displayError(self, "Please select a more reasonable Chi range.")
                return        
        except:
            displayError(self, "Please make sure you enter appropriate Q and Chi range values!")
            return
        return (i_filenames, i_proc_dir)

    def checkStitchValues(self):
        data_source = str(self.images_select.text())
        if not os.path.exists(data_source):
            displayError(self, "Please select an existing stitch data source directory.")
            return
        s_proc_dir = os.path.join(data_source, "Processed_Stitch")

        if str(self.stitch_saveLocation.text()) == "":
            self.stitch_saveLocation.setText(s_proc_dir)
        return (data_source, s_proc_dir)



    def saveMacro(self):
        if not self.fieldsChanged and len(str(self.macroSelected.text())) > 25:
            return
        # CHECKING VALUES TO MAKE SURE EVERYTHING IS OKAY BEFORE MACRO CAN BE SAVED
        workflow = self.workflow.isChecked()
        macrodict = {"workflow" : str(workflow)}
        if workflow:
            try:
                checked_values = self.checkTransformValues()
                try:
                    QRange = (float(str(self.q_min.text())), float(str(self.q_max.text())))
                    ChiRange = (float(str(self.chi_min.text())), float(str(self.chi_max.text())))    
                    if abs(QRange[1]-QRange[0]) < .01:
                        displayError(self, "Please select a more reasonable Q range.")
                        return  
                    if abs(ChiRange[1] - ChiRange[0]) < 0.1:  
                        displayError(self, "Please select a more reasonable Chi range.")
                        return        
                except:
                    displayError(self, "Please make sure you enter appropriate Q and Chi range values!")
                    return
            except:
                return
                
            macrodict["t_data_source"] = checked_values[0]
            macrodict['t_calib_source'] = checked_values[1]
            detector = str(self.detector_combo.currentText())
            macrodict["detector_type"] = detector.split(', ')[0]
            t_proc_dir = str(self.processed_location.text())
            macrodict["t_proc_dir"] = checked_values[2]
            macrodict['transform'] = 'True'
        if not workflow:
            transform = self.transformCheck.isChecked()
            integrate = self.integrateCheck.isChecked()
            stitch = self.stitchCheck.isChecked()
            if not transform and not stitch and not integrate:
                displayError(self, "Please select at least one of the following: Transform, Stitch, or Integrate.")
                return
            macrodict["transform"] = 'False'
            macrodict["integrate"] = 'False'
            macrodict["stitch"] = 'False'
            if transform:
                try:
                    checked_values = self.checkTransformValues()
                    macrodict ["t_data_source"] = checked_values[0]
                    macrodict['t_calib_source'] = checked_values[1]
                    detector = str(self.detector_combo.currentText())
                    macrodict["detector_type"] = detector.split(', ')[0]
                    t_proc_dir = str(self.processed_location.text())
                    macrodict["t_proc_dir"] = checked_values[2]
                    macrodict['transform'] = 'True'
                except:
                    return
            if integrate:
                try:
                    values = self.checkIntegrateValues()
                    macrodict["i_data_source"] = values[0]
                    macrodict["i_proc_dir"] = values[1]
                    macrodict['integrate'] = 'True'
                except:
                    return

            if stitch:
                try:
                    values = self.checkStitchValues()
                    macrodict["s_data_source"] = values[0]
                    macrodict["s_proc_dir"] = values[1]
                    macrodict["stitch"] = 'True'
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
            self.fieldsChanged = True
            return
        if not fileName.endswith(".csv"):
            fileName += ".csv"        
        # If anything else is changed after this, the editor won't let you add to the queue without saving again
        self.setFieldsChanged(False)

        # If the user is editing a workflow: ****************

        # *******************WORKFLOW***********************

        if workflow:
            # macrodict will have the following keys: t_data_source, detector_type, t_proc_dir, chimin, chimax, qmin, qmax, workflow
            macrodict["chimin"] = float(str(self.chi_min.text()))
            macrodict["chimax"] = float(str(self.chi_max.text()))
            macrodict["qmin"] = float(str(self.q_min.text()))
            macrodict["qmax"] = float(str(self.q_max.text()))

            with open(fileName, 'wb') as macro:
                writer = csv.writer(macro)
                for key, value in macrodict.items():
                    writer.writerow([key, value])
                
            self.curMacro = Macro(fileName, macrodict)
            self.macroSelected.setText("Current macro selected: %s" % (os.path.join(os.path.dirname(fileName).split("/")[-1], os.path.basename(fileName))))
            return

        # If the user is editing individual actions: ***************

        #*******************INDEPENDENT********************

        transform = self.transformCheck.isChecked()
        stitch = self.stitchCheck.isChecked()
        integrate = self.integrateCheck.isChecked()
        if not transform and not stitch and not integrate:
            displayError(self, "Please select either Transform, Stitch, or Integrate!")        
            return
        if transform and not os.path.exists(str(self.data_source.text()).lstrip().rstrip()):
            displayError(self, "Please select an existing transform data source directory.")
            return
        else:
            self.t_files_to_process = [str(self.data_source.text()).lstrip().rstrip()]
        if integrate and not os.path.exists(str(self.int_data_source.text()).lstrip().rstrip()):
            displayError(self, "Please select an existing integrate data source directory.")
            return
        else:
            self.i_files_to_process = [str(self.int_data_source.text()).lstrip().rstrip()]
        
       
       
    
        macrodict['transform'] = str(transform)
        macrodict["stitch"] = str(stitch)
        macrodict["integrate"] = str(integrate)
        macrodict['transform_integrate'] = str(self.transform_integrate)
            
        if stitch:
            s_data_source = str(self.images_select.text())
            if not os.path.exists(s_data_source):
                displayError(self, "Please select a stitch data source!")
                return
            macrodict["s_data_source"] = s_data_source

            macrodict["s_proc_dir"] = str(self.stitch_saveLocation.text())

        
        if integrate:
            i_filenames = []    
            if os.path.isfile(self.i_files_to_process[0]):
                i_filenames += self.i_files_to_process
            elif os.path.isdir(self.i_files_to_process[0]):
                i_filenames = [str(self.int_data_source.text()).lstrip().rstrip()]
            else:
                displayError(self, "Could not locate integrate data source!")
                return
                
            macrodict["i_data_source"] = i_filenames
            i_proc_dir = str(self.int_processed_location.text())
            macrodict["i_proc_dir"] = i_proc_dir            
            try:
                macrodict["chimin"] = float(str(self.chi_min.text()))
                macrodict["chimax"] = float(str(self.chi_max.text()))
                macrodict["qmin"] = float(str(self.q_min.text()))
                macrodict["qmax"] = float(str(self.q_max.text()))
            except:
                displayError(self, "Could not resolve Q and Chi ranges")
                return
     
        with open(fileName, 'wb') as macro:
            writer = csv.writer(macro)
            for key, value in macrodict.items():
                writer.writerow([key, value])
                
        self.curMacro = Macro(fileName, macrodict)
        self.macroSelected.setText("Current macro selected: %s" % (os.path.join(os.path.dirname(fileName).split("/")[-1], os.path.basename(fileName))))
            
    
    def loadMacro(self, name=""):
        if name == False:
            current = os.getcwd()
            final_dir = os.path.join(current, self.mPath)
            if os.path.exists(final_dir):
                filename = QFileDialog.getOpenFileName(self, "Select your macro", directory=final_dir)
            else:   
                filename = QFileDialog.getOpenFileName(self, "Select your macro", directory=current)
        
            filename = str(filename)
            
        else:
            filename = str(name)
        self.macroSelected.setText("Current macro selected: %s" % (os.path.join(os.path.dirname(str(filename)).split("/")[-1], os.path.basename(str(filename)))))
        
        try:
            with open(filename, 'rb') as macro:
                reader = csv.reader(macro)
                macrodict = dict(reader)
            workflow = "True" in macrodict['workflow']
            if workflow:
                self.workflow.setChecked(True)
                self.workflowClicked()
                try:
                    macrodict['t_data_source'] = ast.literal_eval(macrodict['t_data_source'])
                except:
                    pass
                t_data_source = macrodict['t_data_source']
                t_calib_source = macrodict['t_calib_source']
                t_proc_dir = macrodict['t_proc_dir']
                if os.path.isdir(t_data_source[0]):
                    self.t_files_to_process = t_data_source
                    self.data_label.setText("Current data source: %s" % os.path.basename(t_data_source[0]))
                    self.data_source.setText(t_data_source[0])
                    #self.data_source_check.setChecked(True)
                elif os.path.isfile(t_data_source[0]):
                    self.t_files_to_process = t_data_source
                    self.data_label.setText("Current data source: (multiple files)")                        
                    self.data_source.setText(os.path.dirname(t_data_source[0]))
                    #self.data_source_check.setChecked(False)
                else:
                    displayError(self.windowreference, "Could not locate transform data source specified in macro!")
                    QApplication.processEvents()
                    return                    
                if os.path.exists(t_calib_source):
                    self.calib_source.setText(t_calib_source)
                    self.loadCalibration()
                else:
                    displayError(self.windowreference, "Could not locate transform calibration source specified in macro!")
                    QApplication.processEvents()
                    return                
                if os.path.exists(t_proc_dir):
                    self.processed_location.setText(t_proc_dir)
                else:
                    self.processed_location.setText(os.path.join(str(self.data_source.text()).lstrip().rstrip(), "Processed_Transform"))
                detector = macrodict['detector_type']
                index = 0
                for i in range(len(self.detectorList)):
                    if self.detectorList[i].getName() == detector:
                        index = i
                        break
                self.detector_combo.setCurrentIndex(index)
                self.q_min.setText(macrodict['qmin'])
                self.q_max.setText(macrodict['qmax'])
                self.chi_min.setText(macrodict['chimin'])
                self.chi_max.setText(macrodict['chimax'])
                
            else:
                self.independent.setChecked(True)
                self.independentClicked()
                transform = "True" in macrodict['transform']
                stitch = "True" in macrodict['stitch']
                integrate = "True" in macrodict['integrate']
                self.transform_integrate = "True" in macrodict['transform_integrate']
                if self.transform_integrate:
                    self.transform_integrate_label.setText("Integrate transformed files: On")
                else:
                    self.transform_integrate_label.setText("Integrate transformed files: Off")
                if transform:
                    self.transformCheck.setChecked(True)
                    try:
                        macrodict['t_data_source'] = ast.literal_eval(macrodict['t_data_source'])
                    except:
                        pass
                    t_data_source = macrodict['t_data_source']
                    t_calib_source = macrodict['t_calib_source']
                    t_proc_dir = macrodict['t_proc_dir']
                    if os.path.isdir(t_data_source[0]):
                        self.t_files_to_process = t_data_source
                        self.data_label.setText("Current data source: %s" % os.path.basename(t_data_source[0]))
                        self.data_source.setText(t_data_source[0])
                        #self.data_source_check.setChecked(True)
                    elif os.path.isfile(t_data_source[0]):
                        self.t_files_to_process = t_data_source
                        self.data_label.setText("Current data source: (multiple files)")                        
                        self.data_source.setText(os.path.dirname(t_data_source[0]))
                        #self.data_source_check.setChecked(False)
                    else:
                        displayError(self.windowreference, "Could not locate transform data source specified in macro!")
                        QApplication.processEvents()
                        return                    
                    if os.path.exists(t_calib_source):
                        self.calib_source.setText(t_calib_source)
                        self.loadCalibration()
                    else:
                        displayError(self.windowreference, "Could not locate transform calibration source specified in macro!")
                        QApplication.processEvents()
                        return                
                    if os.path.exists(t_proc_dir):
                        self.processed_location.setText(t_proc_dir)
                    else:
                        self.processed_location.setText(t_data_source)
                    detector = macrodict['detector_type']
                    index = 0
                    for i in range(len(self.detectorList)):
                        if self.detectorList[i].getName() == detector:
                            index = i
                            break
                    self.detector_combo.setCurrentIndex(index)
                        
                if integrate:
                    self.integrateCheck.setChecked(True)
                    try:
                        macrodict['i_data_source'] = ast.literal_eval(macrodict['i_data_source'])
                    except:
                        pass                
                    i_data_source = macrodict['i_data_source']
                    i_proc_dir = macrodict['i_proc_dir']
                    if os.path.isdir(i_data_source[0]):
                        self.i_files_to_process = i_data_source
                        self.int_data_label.setText("Current data source: %s" % os.path.basename(i_data_source[0]))
                        self.int_data_source.setText(i_data_source[0])            
                        #self.int_data_source_check.setChecked(True)
                    elif os.path.isfile(i_data_source[0]):
                        self.i_files_to_process = i_data_source
                        self.int_data_label.setText("Current data source: (multiple files)")                        
                        self.int_data_source.setText(os.path.dirname(i_data_source[0]))
                        #self.int_data_source_check.setChecked(False)
                    else:
                        displayError(self.windowreference, "Could not locate integrate data source specified in macro!")
                        return             
                    if os.path.exists(i_proc_dir):
                        self.processed_location.setText(i_proc_dir)
                    else:
                        self.processed_location.setText(i_data_source[0])                
                    self.q_min.setText(macrodict['qmin'])
                    self.q_max.setText(macrodict['qmax'])
                    self.chi_min.setText(macrodict['chimin'])
                    self.chi_max.setText(macrodict['chimax'])
                if stitch:
                    self.stitchCheck.setChecked(True)
                    s_data_source = macrodict['s_data_source']
                    s_proc_dir = macrodict['s_proc_dir']
                    if os.path.exists(s_data_source):
                        self.images_select.setText(s_data_source)
                    if os.path.exists(s_proc_dir):
                        self.stitch_saveLocation.setText(s_proc_dir)
                    else:
                        self.stitch_saveLocation.setText(s_data_source)
                        
                self.transformCheck.setChecked(transform)
                self.stitchCheck.setChecked(stitch)
                self.integrateCheck.setChecked(integrate)
                #if self.data_source_check.isChecked():
                    #self.data_label.setText("Current data source:")
                
                if not transform:
                    self.transformCheck.setChecked(False)
                if not stitch:
                    self.stitchCheck.setChecked(False)
                if not integrate:
                    self.integrateCheck.setChecked(False)
            self.curMacro = Macro(filename, macrodict)
            
            self.setFieldsChanged(False)
            self.raise_()
                                 
        except:
            traceback.print_exc()
            displayError(self, "Unable to load macro!")
                 
            
    def loadCalibration(self):
        if str(self.calib_source.text()) != '':
            try:
                d_in_pixel, Rotation_angle, tilt_angle, lamda, x0, y0 = parse_calib(str(self.calib_source.text()))
            except:
                #self.console.append("Unable to locate calibration source file.")
                return
            self.wavelength.setText(str(lamda))
            self.detectordistance.setText(str(d_in_pixel))
            self.dcenterx.setText(str(x0))
            self.dcentery.setText(str(y0))
            self.detect_tilt_alpha.setText(str(Rotation_angle))
            self.detect_tilt_delta.setText(str(tilt_angle))
            
            

def generateQueueWidgets(self):
    self.queue = QListWidget()
    self.queue.setFont(QFont("Avenir", 16))
    self.queue.setStyleSheet("background-color: rgba(34, 200, 157, 200);")
    self.queue.setMaximumHeight(500)
    self.addMacroButton = QPushButton(" + ")
    self.addMacroButton.setStyleSheet("QPushButton {background-color : rgb(60, 60, 60); color: white; }")
    self.removeButton = QPushButton(" - ")
    self.removeButton.setStyleSheet("QPushButton {background-color : rgb(60, 60, 60); color: white; }")
    self.addmacrotext = QLabel("<-- Click these to add/load macros to the queue or remove processes from the queue")
    self.addmacrotext.setStyleSheet("color: white;")
    self.qconsole = QTextBrowser()
    self.qconsole.setMinimumHeight(150)
    self.qconsole.setMaximumHeight(400)
    self.qconsole.moveCursor(QTextCursor.End)

    self.qconsole.setFont(QFont("Avenir", 14))
    self.qconsole.setStyleSheet("margin:3px; border:1px solid rgb(0, 0, 0); background-color: rgb(240, 255, 240);  color: black;")           
    self.startQueueButton = QPushButton("Start queue")
    # self.startQueueButton.setFixedWidth(150)
    self.startQueueButton.setStyleSheet("background-color: rgb(100, 215, 76); color: black;")
    self.startQueueButton.resize(self.startQueueButton.sizeHint().width(), self.startQueueButton.sizeHint().height())


    self.stopQueueButton = QPushButton("Terminate Queue")
    self.stopQueueButton.setStyleSheet("background: rgb(255, 100, 100); color: black;")
    # self.stopQueueButton.setFixedWidth(150)
    self.stopQueueButton.resize(self.stopQueueButton.sizeHint().width(), self.stopQueueButton.sizeHint().height())


    self.pauseQueueButton = QPushButton("Pause Queue")
    self.pauseQueueButton.setStyleSheet("background: rgb(230, 150, 150); color: black;")
    # self.pauseQueueButton.setFixedWidth(150)
    self.pauseQueueButton.resize(self.pauseQueueButton.sizeHint().width(), self.pauseQueueButton.sizeHint().height())

    self.resumeQueueButton = QPushButton("Resume Queue")
    self.resumeQueueButton.setStyleSheet("background: rgb(100, 255, 100); color: black;")
    # self.resumeQueueButton.setFixedWidth(150)
    self.resumeQueueButton.resize(self.resumeQueueButton.sizeHint().width(), self.resumeQueueButton.sizeHint().height())
   

    self.saveQueueButton = QPushButton("Save this queue")
    self.saveQueueButton.setStyleSheet("background: rgb(142, 210, 201); color: black;")
    # self.saveQueueButton.setFixedWidth(150)
    self.saveQueueButton.resize(self.saveQueueButton.sizeHint().width(), self.saveQueueButton.sizeHint().height())


    self.loadQueueButton = QPushButton("Load a queue")
    self.loadQueueButton.setStyleSheet("background: rgb(252, 244, 217);color: black;")
    # self.loadQueueButton.setFixedWidth(150)
    self.loadQueueButton.resize(self.loadQueueButton.sizeHint().width(), self.loadQueueButton.sizeHint().height())


    self.changeTabCheck = QCheckBox("Take me to each tab during each process")
    self.changeTabCheck.setStyleSheet("QCheckBox {color: white; }")
    self.changeTabCheck.setChecked(True)
    self.queue_bar = QRoundProgressBar()
    self.queue_bar.setFixedSize(150, 150)
    self.queue_bar.setDataPenWidth(.01)
    self.queue_bar.setOutlinePenWidth(.01)
    self.queue_bar.setDonutThicknessRatio(0.85)
    self.queue_bar.setDecimals(1)
    self.queue_bar.setFormat('%p %')
    self.queue_bar.setNullPosition(90)
    self.queue_bar.setBarStyle(QRoundProgressBar.StyleDonut)
    self.queue_bar.setDataColors([(0, QColor(qRgb(34, 200, 157))), (1, QColor(qRgb(34, 200, 157)))])
    self.queue_bar.setRange(0, 100)
    self.queue_bar.setValue(0)        
    
    self.queue_bar_label = QLabel("Percentage of queue completed")
    self.queue_bar_label.setFont(QFont("Avenir", 16))
    self.queue_bar_label.setStyleSheet("QLabel {color: rgb(34, 200, 157);}")

    self.queue_abort = False
    self.queue_pause = False

    
def generateQueueLayout(self):
    v_box = QVBoxLayout()
    add_remove_box = QHBoxLayout()
    v_box.addWidget(self.queue)
    add_remove_box.addWidget(self.addMacroButton)
    add_remove_box.addWidget(self.removeButton)
    add_remove_box.addWidget(self.addmacrotext)
    add_remove_box.addStretch()
    v_box.addLayout(add_remove_box)
    controls = QHBoxLayout()
    controls.addWidget(self.startQueueButton)
    controls.addWidget(self.pauseQueueButton)
    controls.addWidget(self.resumeQueueButton)
    controls.addWidget(self.stopQueueButton)
    controls.addStretch()
    controls.addWidget(self.changeTabCheck)
    v_box.addLayout(controls)
    queues = QHBoxLayout()
    queues.addWidget(self.saveQueueButton)
    queues.addWidget(self.loadQueueButton)
    queues.addStretch()
    v_box.addLayout(queues)
    # v2 = QVBoxLayout()
    v_box.addStretch()
    h = QHBoxLayout()
    h.addStretch()
    h.addWidget(self.queue_bar)
    h.addStretch()
    v_box.addLayout(h)
    h2 = QHBoxLayout()
    h2.addStretch()
    h2.addWidget(self.queue_bar_label)
    h2.addStretch()
    v_box.addLayout(h2)
    # v_box.addWidget(self.queue_bar_label)
    # v2.setSpacing(0)
    
    # h = QHBoxLayout()
    # h.addStretch()
    # h.addLayout(v2)
    # h.addStretch()
    # v_box.addLayout(h)
    
    v_box.addStretch()
    v_box.addWidget(self.qconsole)
    return v_box

def abortQueue(self):
    self.queue_abort = True
    self.addToConsole("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    self.addToConsole("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    self.addToConsole("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    self.addToConsole("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    self.addToConsole("Queue aborted! However, any processes that are currently running will complete before the queue stops.")

def pauseQueue(self):
    self.queue_pause = True
    self.enableWidgets()
    self.pauseQueueButton.setDisabled(True)
    self.addMacroButton.setDisabled(True)
    self.removeButton.setDisabled(True)
    self.start_button.setDisabled(True)
    self.int_start_button.setDisabled(True)
    self.stitch_start_button.setDisabled(True)
    self.editor.setDisabled(True)
    self.saveQueueButton.setDisabled(True)
    self.loadQueueButton.setDisabled(True)
    

    self.addToConsole("()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()")
    self.addToConsole("()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()")
    self.addToConsole("()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()")
    self.addToConsole("()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()")
    self.addToConsole("Queue paused! Any processes that are currently running will complete before the queue is able to pause.")

def resumeQueue(self):
    self.queue_pause = False
    self.disableWidgets()
    self.editor.setEnabled(True)
    self.pauseQueueButton.setEnabled(True)
    self.addToConsole("()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()")
    self.addToConsole("()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()")
    self.addToConsole("Queue shall resume!")

def beginQueue(self):
    if len(self.macroQueue) < 1:
        self.addToConsole("No elements in the queue!")
        return
    self.addToConsole("*****************************************************************")
    self.addToConsole("**********************Beginning Queue...************************")
    self.addToConsole("*****************************************************************")
    increment = calculateMacroQueueIncrement(self)
    progress = 0
    self.queue_bar.setValue(progress)
    macrindex = 0
    self.disableWidgets()
    if self.queue_pause:
        self.queue_pause = False
    if self.queue_abort:
        self.queue_abort = False
    for macro in self.macroQueue:
        self.queue.setCurrentRow(macrindex)
        self.addToConsole("Processing %s..." % os.path.basename(str(macro.getFilename())))
        if macro.isWorkflow() or macro.isTransformIntegrate():

            #  ************ TRANSFORM PROCESSING ******************
            if self.queue_abort:
                self.addToConsole("Aborting queue...")
                self.addToConsole("Congratulations, you just killed the queue.")
                break
            if self.queue_pause:
                self.addToConsole("Pausing queue...")
                self.addToConsole("Queue is paused!")
                while (self.queue_pause):
                    time.sleep(.4)
                    QApplication.processEvents()

            processed_filedir = macro.getTProcessedFileDir()
            calib_source = macro.getTCalibInfo()
            detectorData = macro.getDetectorData()
            dataFiles = macro.getTDataFiles()
            QRange = macro.getQRange()
            ChiRange = macro.getChiRange()
            processed_filedir = processed_filedir + "_Process_" + str(macrindex + 1)

            startTransformThread(self, dataFiles, calib_source, detectorData, processed_filedir, increment)
            while self.processDone == False:
                time.sleep(.2)
                QApplication.processEvents()
            time.sleep(1.5) # let the user have a chance to look at the graph lol
            #progress += increment
            #self.queue_bar.setValue(progress)
            if not macro.isTransformIntegrate():
                # **************** STITCH PROCESSING *********************
                if self.queue_abort:
                    self.addToConsole("Aborting queue...")
                    self.addToConsole("Congratulations, you just killed the queue.")
                    break
                if self.queue_pause:
                    self.addToConsole("Pausing queue...")
                    self.addToConsole("Queue is paused!")
                    while (self.queue_pause):
                        time.sleep(.4)
                        QApplication.processEvents()
                dataFiles = [os.path.join(processed_filedir, "Transformed_Mat")]    

                s_processed_filedir = os.path.join(processed_filedir, "Processed_Stitch")    
                
                startStitchThread(self, dataFiles[0], s_processed_filedir, increment)
                while self.processDone == False:
                    time.sleep(.2)
                    QApplication.processEvents()     
                time.sleep(1.5)
                    
                #progress += increment
                #self.queue_bar.setValue(progress)            

            # **************** INTEGRATE PROCESSING **************
            if self.queue_abort:
                self.addToConsole("Aborting queue...")
                self.addToConsole("Congratulations, you just killed the queue.")
                break
            if self.queue_pause:
                self.addToConsole("Pausing queue...")
                self.addToConsole("Queue is paused!")
                while (self.queue_pause):
                    time.sleep(.4)
                    QApplication.processEvents()
            dataFiles = [os.path.join(processed_filedir, "Transformed_Mat")]
            i_processed_filedir = os.path.join(processed_filedir ,"Processed_Integrate"    )

            startIntegrateThread(self, dataFiles, i_processed_filedir, QRange, ChiRange, increment)
            while self.processDone == False:
                time.sleep(.2)
                QApplication.processEvents()
            time.sleep(1.5)
            #progress += increment
            #self.queue_bar.setValue(progress)
        else:

            if macro.shouldTransform():
                if self.queue_abort:
                    self.addToConsole("Aborting queue...")
                    self.addToConsole("Congratulations, you just killed the queue.")
                    break
                if self.queue_pause:
                    self.addToConsole("Pausing queue...")
                    self.addToConsole("Queue is paused!")
                    while (self.queue_pause):
                        time.sleep(.4)
                        QApplication.processEvents()
                processed_filedir = macro.getTProcessedFileDir()
                calib_source = macro.getTCalibInfo()
                detectorData = macro.getDetectorData()
                dataFiles = macro.getTDataFiles()
                startTransformThread(self, dataFiles, calib_source, detectorData, processed_filedir, increment)     
                while self.processDone == False:
                    time.sleep(.2)
                    QApplication.processEvents()
                time.sleep(1.5) # let the user have a chance to look at the graph lol
                progress += increment
                # self.queue_bar.setValue(progress)
                        
                
            if macro.shouldStitch():
                if self.queue_abort:
                    self.addToConsole("Aborting queue...")
                    self.addToConsole("Congratulations, you just killed the queue.")
                    break
                if self.queue_pause:
                    self.addToConsole("Pausing queue...")
                    self.addToConsole("Queue is paused!")
                    while (self.queue_pause):
                        time.sleep(.4)
                        QApplication.processEvents()
                processed_filedir = macro.getSProcessedFileDir()
                dataFiles = macro.getSDataFiles()            
                startStitchThread(self, dataFiles, processed_filedir, increment)
                while self.processDone == False:
                    time.sleep(.2)
                    QApplication.processEvents()     
                time.sleep(1.5)
                    
                progress += increment
                # self.queue_bar.setValue(progress)            
            
            if macro.shouldIntegrate():
                if self.queue_abort:
                    self.addToConsole("Aborting queue...")
                    self.addToConsole("Congratulations, you just killed the queue.")
                    break
                if self.queue_pause:
                    self.addToConsole("Pausing queue...")
                    self.addToConsole("Queue is paused!")
                    while (self.queue_pause):
                        time.sleep(.4)
                        QApplication.processEvents()
                processed_filedir = macro.getIProcessedFileDir()
                dataFiles = macro.getIDataFiles() 
                QRange = macro.getQRange()
                ChiRange = macro.getChiRange()
                startIntegrateThread(self, dataFiles, processed_filedir, QRange, ChiRange, increment)      
                while self.processDone == False:
                    time.sleep(.2)
                    QApplication.processEvents()     
                time.sleep(1.5)                
                progress += increment
                # self.queue_bar.setValue(progress)
        macrindex += 1
    self.enableWidgets()
    self.queue_abort = False
    self.setCurrentIndex(3)

# list str tuple str float-> None
# Takes a list of datafiles (either a list with a string folder name inside or a list of pathnames), a calibration source, a tuple of detector data, and a processed file directory, and starts the transform thread. The float is the increment to push the queue radial bar
def startTransformThread(self, dataFiles, calib_source, detectorData, processed_filedir, increment):
    if self.changeTabCheck.isChecked():
        self.setCurrentIndex(0)
    self.addToConsole('******************************************************************************')
    self.addToConsole('************************ Beginning Transform Processing... ***********************')
    self.addToConsole('******************************************************************************')            
    self.addToConsole('Calibration File: ' + calib_source)
    if os.path.isfile(dataFiles[0]):
        self.addToConsole('Folder to process: ' + os.path.dirname(dataFiles[0]))
    else:
        self.addToConsole("Folder to process: " + dataFiles[0])
    self.addToConsole('')        
    # TransformThread: __init__(self, windowreference, processedPath, calibPath, dataPath, detectorData, files_to_process):
    self.transformThread = TransformThread(self, processed_filedir, calib_source, detectorData, dataFiles, increment)
    self.transformThread.setAbortFlag(False)
    self.abort.clicked.connect(self.transformThread.abortClicked)
    self.int_abort.clicked.connect(self.transformThread.abortClicked) # Making sure that the connections are valid for the current instance of TransformThread.
    self.connect(self.transformThread, SIGNAL("addToConsole(PyQt_PyObject)"), self.addToConsole)
    self.connect(self.transformThread, SIGNAL("setRawImage(PyQt_PyObject)"), self.setRawImage)
    self.connect(self.transformThread, SIGNAL("enableWidgets()"), self.enableWidgets)
    self.connect(self.transformThread, SIGNAL("bar(int, PyQt_PyObject)"), self.setRadialBar)
    self.connect(self.transformThread, SIGNAL("enable()"), self.enableWidgets)
    self.connect(self.transformThread, SIGNAL("finished(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"), self.done)
    self.processDone = False
    self.transformThread.start()        
    
# list str float -> None
# Takes a list of data files (either a list with a string folder name inside or a list of pathnames), and a processed file directory, and starts the stitch thread. The float is the increment to push the queue radial bar
def startStitchThread(self, dataFiles, processed_filedir, increment):
    if self.changeTabCheck.isChecked():

        self.setCurrentIndex(1)
    self.disableWidgets()
    QApplication.processEvents()
    #self.console.clear()
    self.addToConsole('****************************************************')
    self.addToConsole('********** Beginning Stitch Processing... ***********')
    self.addToConsole('****************************************************')
    QApplication.processEvents()
    

    self.stitchThread = StitchThread(self, dataFiles, processed_filedir, increment)
    #self.stitchThread.setAbortFlag(False)
    # make sure that if the abort button is clicked, it is aborting the current running stitch thread, so this needs to be run for every new stitch thread
    self.stitchThread.setAbortFlag(False)
    self.stitch_abort.clicked.connect(self.stitchThread.abortClicked)
    
    # these connections are the only way the thread can communicate with the MONster
    self.connect(self.stitchThread, SIGNAL("addToConsole(PyQt_PyObject)"), self.addToConsole)
    self.connect(self.stitchThread, SIGNAL("bar(int, PyQt_PyObject)"), self.setRadialBar)
    self.connect(self.stitchThread, SIGNAL("finished(PyQt_PyObject, PyQt_PyObject)"), ms.stitchDone)
    self.connect(self.stitchThread, SIGNAL("setImage(PyQt_PyObject, PyQt_PyObject)"), ms.setStitchImage)
    self.connect(self.stitchThread, SIGNAL("resetStitch(PyQt_PyObject)"), ms.resetStitch)
    self.stitchThread.start()        
    self.processDone = False

# list str tuple tuple float-> None
# Takes a list of datafiles (either a list with a string folder name inside or a list of pathnames), a processed file directory, a Q Range, and a Chi Range, and starts the integrate thread. The float is the increment to push the queue radial bar
def startIntegrateThread(self, dataFiles, processed_filedir, QRange, ChiRange, increment):
    if self.changeTabCheck.isChecked():

        self.setCurrentIndex(2)
    self.addToConsole('******************************************************************************')
    self.addToConsole('********************* Beginning Integration Processing... *********************')
    self.addToConsole('******************************************************************************')            
    QApplication.processEvents()
    self.integrateThread = IntegrateThread(self, processed_filedir, dataFiles, (QRange, ChiRange), increment)
    self.integrateThread.setAbortFlag(False)
    self.int_abort.clicked.connect(self.integrateThread.abortClicked)
    
    self.connect(self.integrateThread, SIGNAL("addToConsole(PyQt_PyObject)"), self.addToConsole)
    self.connect(self.integrateThread, SIGNAL("enableWidgets()"), self.enableWidgets)
    self.connect(self.integrateThread, SIGNAL("set1DImage(PyQt_PyObject, PyQt_PyObject)"), mi.set1DImage)
    self.connect(self.integrateThread, SIGNAL("finished(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"), self.done)
    self.connect(self.integrateThread, SIGNAL("bar(int, PyQt_PyObject)"), self.setRadialBar)
    self.connect(self.integrateThread, SIGNAL("enable()"), self.enableWidgets)
    self.connect(self.integrateThread, SIGNAL("plot1dGraph(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"), mi.plot1dGraph)
    self.connect(self.integrateThread, SIGNAL("save1dGraph(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject, PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"), mi.save1dGraph)
    self.integrateThread.start()            
    self.processDone = False
    

    
def addMacroToQueue(self):
    global curIndex

    try:
        if self.editor.curMacro.isWorkflow():
            if self.editor.fieldsChanged == True:
                displayError(self, "Please save your macro!")
                return
            try:
                QRange = (float(str(self.editor.q_min.text())), float(str(self.editor.q_max.text())))
                #            ChiRange = (config['ChiMin'],config['ChiMax'])
                ChiRange = (float(str(self.editor.chi_min.text())), float(str(self.editor.chi_max.text())))    
                if abs(QRange[1]-QRange[0]) < .01:
                    displayError(self, "Please select a more reasonable Q range.")
                    return  
                if abs(ChiRange[1] - ChiRange[0]) < 0.1:  
                    displayError(self, "Please select a more reasonable Chi range.")
                    return        
            except:
                displayError(self, "Please make sure you enter appropriate Q and Chi range values!")
                return
            macro = QListWidgetItem("Process %s: Added macro \"%s\"" % (curIndex, os.path.basename(str(self.editor.curMacro.getFilename()))))
        
            self.macroQueue.append( self.editor.curMacro )     
        else:
            if not self.editor.integrateCheck.isChecked() and not self.editor.transformCheck.isChecked() and not self.editor.stitchCheck.isChecked():
                displayError(self, "Select at least one of the following: Transform, Stitch, or Integrate.")
                return
            if self.editor.fieldsChanged == True:
                displayError(self, "Please save your macro!")
                return
            if self.editor.integrateCheck.isChecked():
                try:
                    QRange = (float(str(self.editor.q_min.text())), float(str(self.editor.q_max.text())))
                    #            ChiRange = (config['ChiMin'],config['ChiMax'])
                    ChiRange = (float(str(self.editor.chi_min.text())), float(str(self.editor.chi_max.text())))    
                    if abs(QRange[1]-QRange[0]) < .01:
                        displayError(self, "Please select a more reasonable Q range.")
                        return  
                    if abs(ChiRange[1] - ChiRange[0]) < 0.1:  
                        displayError(self, "Please select a more reasonable Chi range.")
                        return        
                except:
                    displayError(self, "Please make sure you enter appropriate Q and Chi range values!")
                    return
            macro = QListWidgetItem("Process %s: Added macro \"%s\"" % (curIndex, os.path.basename(str(self.editor.curMacro.getFilename()))))
            
            self.macroQueue.append( self.editor.curMacro )        
    except: # Almost always raised when the user tries to save a macro before saving, so self.editor.curMacro is None
        traceback.print_exc()
        displayError(self, "Please make sure you save your macro!")
        #self.editor.raise_()
        return
        
    curIndex+= 1
    self.queue.addItem(macro)
    self.editor.close()
    QApplication.processEvents()

def addMacro(self):
    self.editor.show()
    self.editor.raise_()

def removeMacro(self):
    global curIndex
    if len(self.queue.selectedItems()) > 0:
        index = self.queue.currentRow()
        self.queue.takeItem(index)
        #print("Removing item: %s" % self.macroQueue[index])
        del self.macroQueue[index]        
        #print("Current macro queue: ")
        #for i in range(len(self.macroQueue)):
            #print(("%s, " % self.macroQueue[i].getFilename()))        
        itemsTextList = [str(self.queue.item(i).text()) for i in range(self.queue.count())]
        for i in range(len(itemsTextList) ):
            process_number = itemsTextList[i].split(':')
            self.queue.item(i).setText(("Process %s: " % (i + 1) ) + process_number[1])
        curIndex = len(itemsTextList) + 1


# Saves the entire queue
def saveQueue(self):
    if len(self.macroQueue) <= 0:
        self.addToConsole("No queue to save!")
        return
    dict_list = []
    for i in range(0, len(self.macroQueue)):
        newdict = {"Process": i + 1, "filename" : self.macroQueue[i].getFilename(), "dict": self.macroQueue[i].getMacroDict()}        
        dict_list.append(newdict)
        
    fname = str(QFileDialog.getSaveFileName(self, "Select the location you wish to save your queue", self.home))
    self.raise_()
    if fname == "":
        self.addToConsole("Queue list not saved!")
        return
    if not fname.endswith('.json'):
        fname += '.json'
    with open(fname, 'w') as fout:
        json.dump(dict_list, fout)


def loadQueue(self):
    fname = str(QFileDialog.getOpenFileName(self, "Select a queue JSON file", self.home))
    self.raise_()
    if fname == "":
        self.addToConsole("No queue list selected!")
        return
    if len(self.macroQueue) > 0:
        self.macroQueue = []
        while self.queue.count() > 0:
            self.queue.takeItem(0)
    try:
        with open(fname) as infile:
            jsondata = json.load(infile)
        for d in jsondata:
            filename = ''
            dicti = None
            process = ""
            for key, value in d.items():
                if key == 'filename':
                    filename = value
                elif key == "Process":
                    process = value
                elif key == "dict":
                    dicti = value
            macro = QListWidgetItem("Process %s: Added macro \"%s\"" % (process, os.path.basename(filename)))
            self.queue.addItem(macro)
            self.macroQueue.append(Macro(filename, dicti))
        global curIndex
        curIndex = 0
    except:
        traceback.print_exc()
        self.addToConsole("Something went wrong. Could not load queue!")
        return
        




def calculateMacroQueueIncrement(self):
    if len(self.macroQueue) <= 0:
        return
    increment = 0
    count = 0
    for macro in self.macroQueue:
        thismacrocount = 0
        
        if macro.isWorkflow():
            datafiles = macro.getTDataFiles()
            if os.path.isdir(datafiles[0]):
                fileList = sorted(glob.glob(os.path.join(datafiles[0], '*.tif')))
                if len(fileList) == 0:
                    fileList = sorted(glob.glob(os.path.join(datafiles[0], '*.raw')))
                    if len(fileList) == 0:
                        return
                files = fileList[0:10000000000000000]
            else:
                fileList = datafiles
            if len(fileList) > 0:
                thismacrocount = len(fileList)
            else:
                return
            thismacrocount *= 3 # for transform, stitch, and integrate
            thismacrocount += 1 # for sttich saving process, adding one because it takes some time to save
            count += thismacrocount
        else:
            if macro.shouldTransform():
                datafiles = macro.getTDataFiles()
                if os.path.isdir(datafiles[0]):
                    fileList = sorted(glob.glob(os.path.join(datafiles[0], '*.tif')))
                    if len(fileList) == 0:
                        fileList = sorted(glob.glob(os.path.join(datafiles[0], '*.raw')))
                        if len(fileList) == 0:
                            return
                    files = fileList[0:10000000000000000]
                else:
                    fileList = datafiles
                if len(fileList) > 0:
                    thismacrocount += len(fileList)
                else:
                    return
            if not macro.isTransformIntegrate():
                if macro.shouldStitch():
                    dataFiles = macro.getSDataFiles()
                    fileList = sorted(glob.glob(os.path.join(dataFiles, '*.mat')))
                    if len(fileList) == 0:
                        thismacrocount += 0
                    else:
                        thismacrocount += len(fileList)
                        thismacrocount += 1

            if macro.shouldIntegrate():
                dataFiles = macro.getIDataFiles()
                if os.path.isdir(dataFiles[0]):
                    fileList = sorted(glob.glob(os.path.join(dataFiles[0], '*.mat')))
                    if len(fileList) == 0:
                        thismacrocount += 0
                    files = fileList[0:10000000000000000]
                else:
                    fileList = dataFiles
                if len(fileList) > 0:
                    thismacrocount += len(fileList)
                else:
                    thismacrocount += 0
            count += thismacrocount
    try:    
        increment = (float(1)/count)*100
    except:
        increment = 0
    return increment
                
