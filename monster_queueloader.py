# This file initializes the various widgets used in the queue loader tab and its layout. It also
# includes a class that defines what a Macro is and a class for the macro editor itself, interfacing that
# with MONster.
#
# This is one of the six main files (IntegrateThread, MONster, monster_queueloader, monster_transform, monster_stitch, TransformThread) that controls the MONster GUI. 
#
# Runs with PyQt4, SIP 4.19.3, Python version 2.7.5
# 
# Author: Arun Shriram
# Written for my SLAC Internship at SSRL
# File Start Date: June 25, 2018
# File End Date: 
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
import monster_integrate as mi
from QRoundProgressBar import QRoundProgressBar


curIndex = 1

class Macro():
    def __init__(self, filename, qrange, chirange, calib_source, processed_filedir, data_files, transform, stitch, integrate):
        self.filename = filename
        self.QRange = qrange
        self.ChiRange = chirange
        self.calib_source = calib_source
        self.processed_filedir = processed_filedir
        self.data_files = data_files
        # Boolean values
        self.transform = transform
        self.stitch = stitch
        self.integrate = integrate
        
    def __eq__(self, other):
        return type(other) == Macro and self.transform == other.transform and self.stitch == other.stitch and self.integrate == other.integrate and self.filename == other.filename and self.QRange == other.QRange and self.ChiRange == other.ChiRange and self.calib_source == other.calib_source and self.processed_filedir == other.processed_filedir and self.data_files == other.data_files
    
    def __repr__(self):
        return ("Filename: %s, QRange: %s, ChiRange: %s, Calibration source: %s, Processed File Directory: %s, Data Files: %s, Transform: %s, Stitch: %s, Integrate: %s") % (self.filename, self.QRange, self.ChiRange, self.calib_source, self.processed_filedir, self.data_files, self.transform, self.stitch, self.integrate)
    def getFilename(self):
        return self.filename
    def setCalibInfo(self, calib_source):
        self.calib_source = calib_source
    
    def setDataInfo(self, data_source, filenames):
        self.data_files = (data_source,)
        for f in filenames:
            self.data_files += (f,)
    def shouldTransform(self):
        return self.transform
    def shouldStitch(self):
        return self.stitch
    def shouldIntegrate(self):
        return self.integrate
    def getQRange(self):
        return self.QRange
    def getProcessedFileDir(self):
        return self.processed_filedir
    # Returns a tuple with two elements: First element is either "" or it has the folder path for whatever directory is being used. If the first is "", then the next element is a list of files. If the first is a directory name, the next element is "folder".
    def getDataFiles(self): 
        return self.data_files
    def getCalibInfo(self):
        return self.calib_source
    def getChiRange(self):
        return self.ChiRange
    
    def getDetectorData(self):
        try:
            d_in_pixel, Rotation_angle, tilt_angle, lamda, x0, y0 = parse_calib(str(self.calib_source))
        except:
            return
        return (d_in_pixel, Rotation_angle, tilt_angle, lamda, x0, y0)
            
class MacroEditor(QWidget):
    def __init__(self, queueTabReference):
        QWidget.__init__(self)
        self.queueTabReference = queueTabReference
        self.curMacro = None
        self.tipLabel = QLabel("Note: Always save any changes you make before adding to the queue! Unsaved changes will not update the macro.")
        self.saveButton = QPushButton("Save this macro")
        self.saveButton.setMaximumWidth(150)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setMaximumWidth(150)
        self.addToQueueButton = QPushButton("Add this macro the queue!")
        self.addToQueueButton.setMaximumWidth(180)
        self.q_min_label = QLabel('Q Min:')
        self.q_min = ClickableLineEdit('0.0')
        self.q_min.setFixedWidth(65)
    
        self.q_max_label = QLabel('Q Max:')
        self.q_max = ClickableLineEdit('0.0')
        self.q_max.setFixedWidth(65)
    
        self.chi_min_label = QLabel("Chi min:")
        self.chi_min = ClickableLineEdit('0.0')
        self.chi_min.setFixedWidth(65)
    
        self.chi_max_label = QLabel("Chi max:")
        self.chi_max = ClickableLineEdit('0.0')
        self.chi_max.setFixedWidth(65)
    
        self.data_label = QLabel("Current data source:")
        #self.data_source = QLineEdit("/Users/arunshriram/Documents/SLAC Internship/test")
        self.data_source = ClickableLineEdit()
        self.data_source.setFixedWidth(580)
        self.data_folder_button = QPushButton()
        self.data_folder_button.setIcon(QIcon('images/folder_select_gray.png'))
        self.data_folder_button.setIconSize(QSize(25, 25))
        self.data_folder_button.setFixedSize(25, 25)
        self.data_folder_button.setStyleSheet('border: none;')
    
        self.data_source_check = QCheckBox("I'm going to select a folder")
        self.data_source_check.setChecked(True)
    
        self.files_to_process = "folder"
        self.calib_label = QLabel("Current calibration file source:")
        #self.calib_source = QLineEdit("/Users/arunshriram/Documents/SLAC Internship/calib/cal_28mar18.calib")
        self.calib_source = ClickableLineEdit()
        self.calib_source.setFixedWidth(580)
        self.calib_folder_button = QPushButton()
        self.calib_folder_button.setIcon(QIcon('images/folder_select_gray.png'))
        self.calib_folder_button.setIconSize(QSize(25, 25))
        self.calib_folder_button.setFixedSize(25, 25)
        self.calib_folder_button.setStyleSheet('border: none;')
        
        self.macroSelected = QLabel("Current macro selected: ")
        font = QFont()
        font.setBold(True)
        self.macroSelected.setFont(font)
        
        self.processed_location_label = QLabel("Current location for processed files:")
        self.processed_location = ClickableLineEdit(self.data_source.text())
        self.processed_location.setFixedWidth(580)
        self.processed_location_folder_button = QPushButton()
        self.processed_location_folder_button.setIcon(QIcon('images/folder_select_gray.png'))
        self.processed_location_folder_button.setIconSize(QSize(25, 25))
        self.processed_location_folder_button.setFixedSize(25, 25)
        self.processed_location_folder_button.setStyleSheet('border: none;')
        
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
        
        self.loadMacroButton = QPushButton("Load a macro")
        
        self.checkLabel = QLabel("Please select at least one of the following:")
        self.transformCheck = QCheckBox("Transform")
        self.stitchCheck = QCheckBox("Stitch")
        self.integrateCheck = QCheckBox("Integrate")        
        
        h_box = QHBoxLayout()
        v_box1 = QVBoxLayout()
        v_box1.addWidget(self.tipLabel)
        v_box1.addWidget(self.macroSelected)
        v_box2 = QVBoxLayout()
        h_box1 = QHBoxLayout()
        h_box1.addWidget(self.data_label)
        h_box1.addStretch()
        h_box1.addWidget(self.data_source_check)
        v_box1.addLayout(h_box1)
        h_box2 = QHBoxLayout()
        h_box2.addWidget(self.data_source)
        h_box2.addWidget(self.data_folder_button)
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
        v_box1.addWidget(self.processed_location_label)
        h_box6 = QHBoxLayout()
        h_box6.addWidget(self.processed_location)
        h_box6.addWidget(self.processed_location_folder_button)
        h_box6.addStretch()
        v_box1.addLayout(h_box6)
        
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.q_min_label)
        hbox1.addWidget(self.q_min)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.q_max_label)
        hbox2.addWidget(self.q_max)        
        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.chi_min_label)
        hbox3.addWidget(self.chi_min)        
        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.chi_max_label)
        hbox4.addWidget(self.chi_max)        
        v_box2.addLayout(hbox1)
        v_box2.addLayout(hbox2)
        v_box2.addLayout(hbox3)
        v_box2.addLayout(hbox4)
        v_box2.addWidget(self.checkLabel)
        v_box2.addWidget(self.transformCheck)
        v_box2.addWidget(self.stitchCheck)
        v_box2.addWidget(self.integrateCheck)        
        hbox5 = QHBoxLayout()
        hbox5.addWidget(self.saveButton)
        hbox5.addWidget(self.loadMacroButton)        
        v_box2.addLayout(hbox5)
        hbox6 = QHBoxLayout()
        hbox6.addWidget(self.cancelButton)        
        hbox6.addWidget(self.addToQueueButton)

        v_box2.addLayout(hbox6)
        h_box.addLayout(v_box1)
        h_box.addStretch()
        h_box.addLayout(v_box2)
        self.setLayout(h_box)
        
        self.setWindowTitle("Add or edit a macro!")
        
        self.updateConnections()

    def updateConnections(self):
        self.cancelButton.clicked.connect(lambda: self.close())
        self.loadMacroButton.clicked.connect(self.loadMacro)
        self.addToQueueButton.clicked.connect(lambda: addMacroToQueue(self.queueTabReference))
        self.saveCustomCalib.clicked.connect(self.saveCalibAction)
        self.data_folder_button.clicked.connect(self.getDataSourceDirectoryPath)
        self.calib_folder_button.clicked.connect(self.getCalibSourcePath)
        self.processed_location_folder_button.clicked.connect(self.setProcessedLocation)        
        self.saveButton.clicked.connect(self.saveMacro)
        
    def getDataSourceDirectoryPath(self):
        if self.data_source_check.isChecked():
            try:
                folderpath = str(QFileDialog.getExistingDirectory())
                if folderpath != '':
                    self.data_source.setText(folderpath)
                    self.data_label.setText("Current data source:")
                    self.processed_location.setText(self.data_source.text())
                    self.files_to_process = "folder"
            except: 
                self.addToConsole("Something went wrong when trying to open your directory.")
        else:
            try:
                filenames = QFileDialog.getOpenFileNames(self, "Select the files you wish to use.")
                filenames = [str(filename) for  filename in filenames]
                if len(filenames) < 2:
                    self.data_label.setText("Current data source: %s" % os.path.basename(filenames[0]))
                else:    
                    self.data_label.setText("Current data source: (multiple files)")
                    self.data_source.setText(os.path.dirname(filenames[0]))
                self.processed_location.setText(self.data_source.text())
                self.files_to_process = filenames   
            except:
                #traceback.print_exc()
                self.addToConsole("Something went wrong when trying to select your files.")
    
    def getCalibSourcePath(self):
        path = str(QFileDialog.getOpenFileName(self, "Select Calibration File", ('/Users/arunshriram/Documents/SLAC Internship/monhitp-gui/calib/')))
        if path !='':
            self.calib_source.setText(path)
            self.loadCalibration()
            
    def setProcessedLocation(self):
        path = str(QFileDialog.getExistingDirectory(self, "Select a location for processed files", str(self.data_source.text())))
        #path = str(QFileDialog.getOpenFileName(self, "Select Calibration File", ('/Users/arunshriram/Documents/SLAC Internship/monhitp-gui/calib/')))
        if path !='':
            self.processed_location.setText(path)
        
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
        except:
            self.addToConsole("Calibration not saved!")
            return        
        
    def addToConsole(self, message):
        self.queueTabReference.addToConsole(message)
        
    def saveMacro(self):
        if (str(self.calib_source.text()) == '' and str(self.dcenterx.text()) == '') or str(self.data_source.text()) == '' or str(self.q_min.text()) == '' or str(self.q_max.text()) == '' or str(self.chi_min.text()) == '' or str(self.chi_max.text()) == '':
            displayError(self, "Unable to save macro! Please make sure all values are correctly filled in.")    
            return
        if self.integrateCheck.isChecked():
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
        transform = self.transformCheck.isChecked()
        stitch = self.stitchCheck.isChecked()
        integrate = self.integrateCheck.isChecked()
        if not transform and not stitch and not integrate:
            displayError(self, "Please select either Transform, Stitch, or Integrate!")        
            return
        if str(self.calib_source.text()) == '':
            displayError(self, "Please make sure you select a calibration source or save your custom calibration!")
            return        
        current = os.getcwd()
        final_dir = os.path.join(current, r'macros')
        if not os.path.exists(final_dir):
            os.makedirs(final_dir)
                
        cur_time = datetime.datetime.now().strftime('%Y-%m-%d--%H-%M-%S')
        name = (final_dir + '/macro-%s') %(cur_time)        
        fileName = QFileDialog.getSaveFileName(self, 'Save your new macro!', name)
        fileName = str(fileName)
        if fileName == '':
            self.raise_()
            return

        self.curMacro = Macro(fileName, (str(self.q_min.text()), str(self.q_max.text())), (str(self.chi_min.text()), str(self.chi_max.text())), None, str(self.processed_location.text()), None, transform, stitch, integrate)

        
        with open(fileName, 'w') as macro:
            macro.write("qmin, qmax, chimin, chimax, calib_source, filename, processed_file_source, folder?, data_source_file(s)/directory\n")
            data_source = ""
            filenames = tuple([])
            calib_filename = ''
            
         
            calib_filename = str(self.calib_source.text())
            if self.files_to_process != "folder":
                filenames += tuple(self.files_to_process)
            else:
                filenames += (str(self.data_source.text()),)
                data_source = str(self.data_source.text())
            
            self.curMacro.setCalibInfo(calib_filename)
            self.curMacro.setDataInfo(data_source, filenames)
            macro.write(("%s, %s, %s, %s, %s, ") % (self.curMacro.getQRange()[0], self.curMacro.getQRange()[1], self.curMacro.getChiRange()[0], self.curMacro.getChiRange()[1], str(self.curMacro.getCalibInfo())) + "%s, " % str(self.curMacro.getProcessedFileDir()) + ", ".join([str(s) for s in list(self.curMacro.getDataFiles())]))
            macro.write('\n%s\n' % transform)
            macro.write('%s\n' % stitch)
            macro.write('%s' % integrate)
        self.macroSelected.setText("Current macro selected: %s" % (os.path.dirname(fileName).split("/")[-1] + "/" + os.path.basename(fileName)))
            
    
    def loadMacro(self):
        '''
        Macro file format:
        <specifiers on top>
        <values on bottom>
        <transform boolean>
        <stitch boolean>
        <integrate boolean>
        example:
        qmin, qmax, chimin, chimax, calib_source, processed_file_source, folder?, data_source_file(s)/directory\n
        <values>
        true
        false
        true
        '''
        current = os.getcwd()
        final_dir = os.path.join(current, r'macros')
        if os.path.exists(final_dir):
            filename = QFileDialog.getOpenFileName(self, "Select your macro", directory=final_dir)
        else:   
            filename = QFileDialog.getOpenFileName(self, "Select your macro", directory=current)
        
        filename = str(filename)
        data = ''
        transform = stitch = integrate = False
        try:
            with open(filename, 'r') as macro:
                macro.readline()
                data = macro.readline().split(', ')
                if "True" in macro.readline():
                    transform = True
                if "True" in macro.readline():
                    stitch = True
                if "True" in macro.readline():
                    integrate = True
            QRange = (float(data[0]), float(data[1]))
            ChiRange = (float(data[2]), float(data[3]))
            self.q_min.setText(str(QRange[0]).rstrip())
            self.q_max.setText(str(QRange[1]).rstrip())
            self.chi_min.setText(str(ChiRange[0]).rstrip())
            self.chi_max.setText(str(ChiRange[1]).rstrip())
            calib_source = data[4].rstrip()
            self.calib_source.setText(calib_source)
            self.loadCalibration()
            processedLocation = data[5].rstrip()
            self.processed_location.setText(processedLocation)
            folder = ""
            directory_or_files = data[6] # "1" if it's a folder, "0" if it's one or more files to process
            if directory_or_files == "1":
                folder = data[7].rstrip()
                self.data_source.setText(folder)
                self.files_to_process = "folder"
                self.data_source_check.setChecked(True)
            else:
                self.data_source.setText(os.path.dirname(data[7]).rstrip())
                self.data_source_check.setChecked(False)
                self.files_to_process = []
                for i in range(7, len(data)):
                    self.files_to_process.append(data[i].rstrip())
            
            self.curMacro = Macro(filename, QRange, ChiRange, calib_source, processedLocation, (folder, self.files_to_process), transform, stitch, integrate)
            self.transformCheck.setChecked(transform)
            self.stitchCheck.setChecked(stitch)
            self.integrateCheck.setChecked(integrate)
            self.macroSelected.setText("Current macro selected: %s" % (os.path.dirname(str(filename)).split("/")[-1] + "/" + os.path.basename(str(filename))))
            if self.data_source_check.isChecked():
                self.data_label.setText("Current data source:")
            if len(data) < 9:
                self.data_label.setText("Current data source: %s" % os.path.basename(data[7]))
            else:
                self.data_label.setText("Current data source: (multiple files)")
                                 
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
    self.qconsole = QTextBrowser()
    self.qconsole.setMinimumHeight(100)
    self.qconsole.setFont(QFont("Avenir", 14))
    self.qconsole.setStyleSheet("margin:3px; border:1px solid rgb(0, 0, 0); background-color: rgb(240, 255, 240);")           
    self.startQueueButton = QPushButton("Start queue")
    self.startQueueButton.setFixedWidth(170)
    self.startQueueButton.setFixedHeight(30)
    self.startQueueButton.setStyleSheet("background-color: rgb(100, 215, 76);")
    
    self.queue_bar_files = QRoundProgressBar()
    self.queue_bar_files.setFixedSize(150, 150)
    self.queue_bar_files.setDataPenWidth(.01)
    self.queue_bar_files.setOutlinePenWidth(.01)
    self.queue_bar_files.setDonutThicknessRatio(0.85)
    self.queue_bar_files.setDecimals(1)
    self.queue_bar_files.setFormat('%p %')
    self.queue_bar_files.setNullPosition(90)
    self.queue_bar_files.setBarStyle(QRoundProgressBar.StyleDonut)
    self.queue_bar_files.setDataColors([(0, QColor(qRgb(34, 200, 157))), (1, QColor(qRgb(34, 200, 157)))])
    self.queue_bar_files.setRange(0, 100)
    self.queue_bar_files.setValue(0)    
    
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

    
def generateQueueLayout(self):
    v_box = QVBoxLayout()
    add_remove_box = QHBoxLayout()
    v_box.addWidget(self.queue)
    add_remove_box.addWidget(self.addMacroButton)
    add_remove_box.addWidget(self.removeButton)
    add_remove_box.addStretch()
    v_box.addLayout(add_remove_box)
    v_box.addWidget(self.startQueueButton)
    v_box.addStretch()
    h = QHBoxLayout()
    h.addStretch()
    h.addWidget(self.queue_bar_files)
    h.addWidget(self.queue_bar)
    h.addStretch()
    v_box.addLayout(h)
    v_box.addWidget(self.qconsole)
    return v_box


def beginQueue(self):
    if len(self.macroQueue) < 1:
        self.addToConsole("No elements in the queue!")
        return
    self.addToConsole("*************************************************")
    self.addToConsole("**************Beginning Queue...****************")
    self.addToConsole("*************************************************")
    increment = (1/float(len(self.macroQueue)))*100
    progress = 0
    self.queue_bar.setValue(progress)
    for macro in self.macroQueue:
        self.addToConsole("Processing macro %s..." % os.path.basename(str(macro.getFilename())))
        calib_source = macro.getCalibInfo()
        processed_filedir = macro.getProcessedFileDir()
        QRange = macro.getQRange()
        ChiRange = macro.getChiRange()
        detectorData = macro.getDetectorData()
        files_to_process = ""
        dataFiles = ""
        if macro.getDataFiles()[1] == "folder":
            dataFiles = "folder"
            data_source = macro.getDataFiles()[0]
        else:
            dataFiles = macro.getDataFiles()[1]
            data_source = os.path.dirname(macro.getDataFiles()[1][0])
            
        # Adding percentage increments to see how much of current macro is finished (setting the radial bar and all),
        # but need to itereate over all contents 
        increment = 0
        progress = 0
        filesToProcess = 0
        if macro.shouldTransform():
            filesToProcess += calculateBarIncrement(dataFiles, data_source)
        if macro.shouldStitch():
            filesToProcess += calculateBarIncrement(dataFiles, data_source)
        if macro.shouldIntegrate():
            filesToProcess += calculateBarIncrement(dataFiles, data_source)
            
        increment = (1/float(filesToProcess))*100
        curFileCount = 0
            
        if macro.shouldTransform():
            self.addToConsole('******************************************************************************')
            self.addToConsole('************************ Beginning Transform Processing... ***********************')
            self.addToConsole('******************************************************************************')            
            self.addToConsole('Calibration File: ' + calib_source)
            self.addToConsole('Folder to process: ' + data_source)
            self.addToConsole('')        
            # TransformThread: __init__(self, windowreference, processedPath, calibPath, dataPath, detectorData, files_to_process):
            self.transformThread = TransformThread(self, processed_filedir, calib_source, data_source, detectorData, dataFiles)
            self.transformThread.setAbortFlag(False)
            self.abort.clicked.connect(self.transformThread.abortClicked)
            self.int_abort.clicked.connect(self.transformThread.abortClicked) # Making sure that the connections are valid for the current instance of TransformThread.
            self.connect(self.transformThread, SIGNAL("addToConsole(PyQt_PyObject)"), self.addToConsole)
            self.connect(self.transformThread, SIGNAL("setRawImage(PyQt_PyObject)"), self.setRawImage)
            self.connect(self.transformThread, SIGNAL("enableWidgets()"), self.enableWidgets)
            self.connect(self.transformThread, SIGNAL("bar(int, PyQt_PyObject)"), self.setRadialBar)
            def addToProcessedFile():
                self.fileProcessedCount += 1
            self.connect(self.transformThread, SIGNAL("fileProcessed()"), addToProcessedFile)
            self.connect(self.transformThread, SIGNAL("finished(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"), self.done)
            self.processDone = False
            self.transformThread.start()        
            while self.processDone == False:
                time.sleep(.2)
                QApplication.processEvents()
                if self.fileProcessedCount > curFileCount:
                    difference = self.fileProcessedCount - curFileCount
                    progress += increment * difference
                    self.queue_bar_files.setValue(progress)
                    
            
        #if macro.shouldStitch():
        
        if macro.shouldIntegrate():
            self.addToConsole('******************************************************************************')
            self.addToConsole('********************* Beginning Integration Processing... *********************')
            self.addToConsole('******************************************************************************')            
            QApplication.processEvents()
            self.integrateThread = IntegrateThread(self, data_source, calib_source, processed_filedir, detectorData, dataFiles, (QRange, ChiRange))
            self.integrateThread.setAbortFlag(False)
            self.int_abort.clicked.connect(self.integrateThread.abortClicked)
            
            self.connect(self.integrateThread, SIGNAL("addToConsole(PyQt_PyObject)"), self.addToConsole)
            self.connect(self.integrateThread, SIGNAL("enableWidgets()"), self.enableWidgets)
            self.connect(self.integrateThread, SIGNAL("set1DImage(PyQt_PyObject, PyQt_PyObject)"), mi.set1DImage)
            self.connect(self.integrateThread, SIGNAL("finished(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"), self.done)
        
            self.integrateThread.start()            
        progress += increment
        self.queue_bar.setValue(progress)
        
# returns the number of files specified either by the dataFiles or the data source passed in
def calculateBarIncrement(dataFiles, dataSource):
    num_files = 0
    if dataFiles == "folder":
        fileList = sorted(glob.glob(os.path.join(dataSource, '*.tif')))
        files = fileList[0:10000000000000000]         
        try: # need a try block in case len(files) comes out to zero
            num_files = (1/float(len(files)))*100
        except:
            num_files = 0
            # No need to tell user that the data source has no files, since TransformThread will take care of that later. Just
            # need to make sure that the radial progress bar doesn't increase, as there are no files to process
    else:
        num_files = (1/float(len(dataFiles)))*100    
    return num_files
    
def addMacroToQueue(self):
    global curIndex

    try:
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