# This file is the main file for the GUI that transforms, stitches, and integrates detector data into 
# Q-chi plots, stitched plots, and one dimensional graphs with peak fitting capabilities. 
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
import numpy as np
import glob
import numpy
import Tkinter, tkFileDialog
from saveDimRedPack import save_Qchi, save_1Dplot, save_1Dcsv, save_texture_plot_csv
###############################################################
from peakBBA import peakFitBBA
from save_wafer_heatMap import FWHMmap, contrastMap
from input_file_parsing import parse_calib
import time
import monster_transform as mt
import monster_stitch as ms
import monster_integrate as mi
import monster_queueloader as mq
import Properties
#=====================
import sys
import os, traceback
import getpass
import datetime
from ClickableLineEdit import *
from TransformThread import *
from IntegrateThread import *
from StitchThread import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *

        
# This class is the class that governs all things that occur in the GUI window.
class MONster(QTabWidget):
    def __init__(self):
        QTabWidget.__init__(self)
        self.macroQueue = [] # list of macros for the queue tab
        self.fileProcessedCount = 0
        self.lineEditStyleSheet =" QLineEdit { border-radius: 4px;  color:rgb(0, 0, 0); background-color: rgb(255, 255, 255); border-style:outset; border-width:4px;  border-radius: 4px; border-color: rgb(34, 200, 157); color:rgb(0, 0, 0); background-color: rgb(200, 200, 200); } "
        self.textStyleSheet = "QLabel {background-color : rgb(29, 30, 50); color: white; }"
        self.current_user = getpass.getuser()
        self.transformThread = TransformThread(self, None, None, None, None, None)  # initialize the transform thread
        self.integrateThread = IntegrateThread(self, None, None, None, None, None, None) # initialize the integrate thread
        self.stitchThread = StitchThread(self, None, None, None, None) # initialize the stitch thread
        screenShape = QDesktopWidget().screenGeometry()
        self.imageWidth = screenShape.height()/2.5
        mt.generateTransformWidgets(self) 
        ms.generateStitchWidgets(self)
        mi.generateIntegrateWidgets(self)
        mq.generateQueueWidgets(self)
        self.transformTab = QWidget()
        self.stitchTab = QWidget()
        self.integrateTab = QWidget()
        self.queueTab = QWidget()
        self.editor = mq.MacroEditor(self) # reference to the queue macro editor
        self.processDone = True # To check if current process in the macro queue is over
        self.updateUi()
        
    # Generates layouts and sets connections between buttons and functions
    def updateUi(self):

        self.transformTab.setLayout(mt.generateTransformLayout(self))
        self.stitchTab.setLayout(ms.generateStitchLayout(self))
        self.integrateTab.setLayout(mi.generateIntegrateLayout(self))
        self.queueTab.setLayout(mq.generateQueueLayout(self))
        self.addTab(self.transformTab, "Transform")
        self.addTab(self.stitchTab, "Stitch")
        self.addTab(self.integrateTab, "Integrate")
        self.addTab(self.queueTab, "Queue Loader")
        self.show()
        self.raise_()
 
        
        ############################################
        ##############CONNECTIONS#################
        ############################################
        self.data_folder_button.clicked.connect(self.getDataSourceDirectoryPath)
        
        self.calib_folder_button.clicked.connect(self.getCalibSourcePath)
        
        self.processed_location_folder_button.clicked.connect(self.setProcessedLocation)
        
        self.start_button.clicked.connect(self.transformThreadStart)
        
        self.q_min.returnPressed.connect(self.transformThreadStart)
        
        self.q_min.clicked.connect(lambda: self.q_min.selectAll())        
        
        self.q_max.returnPressed.connect(self.transformThreadStart)
        
        self.q_max.clicked.connect(lambda: self.q_max.selectAll())
        
        self.chi_min.returnPressed.connect(self.transformThreadStart)
        
        self.chi_min.clicked.connect(lambda: self.chi_min.selectAll())
        
        self.chi_max.returnPressed.connect(self.transformThreadStart)
        
        self.chi_max.clicked.connect(lambda: self.chi_max.selectAll())
        
        self.data_source.returnPressed.connect(self.transformThreadStart)
                
        self.calib_source.returnPressed.connect(self.transformThreadStart)
                
        self.saveCustomCalib.clicked.connect(self.saveCalibAction)
        
        self.abort.clicked.connect(self.transformThread.abortClicked)
        
        self.int_abort.clicked.connect(self.integrateThread.abortClicked)
        
        self.stitch_abort.clicked.connect(self.stitchThread.abortClicked)
        
        self.addMacroButton.clicked.connect(lambda: mq.addMacro(self))
        
        self.currentChanged.connect(self.windowTabChanged)
        
        self.addToQueueButton.clicked.connect(self.addCurrentToQueue)
        
        self.removeButton.clicked.connect(lambda: mq.removeMacro(self))
        
        self.int_start_button.clicked.connect(lambda: mi.integrateThreadStart(self))
        
        self.int_abort.clicked.connect(self.integrateThread.abortClicked)
        
        self.int_calib_folder_button.clicked.connect(lambda: mi.getIntCalibSourcePath(self))
        
        self.int_data_folder_button.clicked.connect(lambda: mi.getIntDataSourceDirectoryPath(self))
        
        self.int_processed_location_folder_button.clicked.connect(lambda: mi.setIntProcessedLocation(self))
        
        self.int_saveCustomCalib.clicked.connect(lambda: mi.saveIntCalibAction(self))
        
        self.startQueueButton.clicked.connect(lambda: mq.beginQueue(self))
        
        self.saveMacroButton.clicked.connect(lambda: mt.saveMacro(self))
        
        self.stitch_start_button.clicked.connect(lambda: ms.beginStitch(self))
        
        self.images_select_files_button.clicked.connect(lambda: ms.stitchImageSelect(self))
        
        self.stitch_saveLocation_button.clicked.connect(lambda: ms.setStitchSaveLocation(self))
        # random name, don't read into it
        def martyr():
            if self.data_source_check.isChecked():
                self.data_label.setText("Current data source:")
                self.files_to_process = "folder"        
        self.data_source_check.stateChanged.connect(martyr)
        ###########################################
        ###########################
        #Restore default graphs and data from the previous run upon starting MONster
        ###########################
        # Properties.py has the following information from previous run(s), in this order:
        #
        #
        # Transform data source
        # Stitch data source
        # Integrate data source
        # Transform calibration source
        # Integrate calibration source
        # Transform processed location
        # Stitch processed location
        # Integrate processed location
        # Qchi image location
        # Stitched image location
        # Integrated image location
        # Q min
        # Q max
        # Chi min
        # Chi max
        # First index for stitch scan
        # Last index for stitch scan
        
        try:
            if os.path.exists(Properties.t_data_source):
                self.data_source.setText(Properties.t_data_source)
            if os.path.exists(Properties.s_data_source):
                self.images_select.setText(Properties.s_data_source)                
            if os.path.exists(Properties.i_data_source):
                self.int_data_source.setText(Properties.i_data_source)
            if os.path.exists(Properties.t_calib_source):
                self.calib_source.setText(Properties.t_calib_source)
            if os.path.exists(Properties.i_calib_source):
                self.int_calib_source.setText(Properties.i_calib_source)
            if os.path.exists(Properties.t_processed_loc):
                self.processed_location.setText(Properties.t_processed_loc)
            if os.path.exists(Properties.s_processed_loc):
                self.stitch_saveLocation.setText(Properties.s_processed_loc)
            if os.path.exists(Properties.i_processed_loc):
                self.int_processed_location.setText(Properties.i_processed_loc)
            self.setRawImage(Properties.two_d_image)
            ms.setStitchImage(self, Properties.stitch_image)
            mi.set1DImage(self, Properties.one_d_image)
            self.q_min.setText(Properties.qmin)
            self.q_max.setText(Properties.qmax)
            self.chi_min.setText(Properties.chimin)
            self.chi_max.setText(Properties.chimax)
            self.first_index.setText(Properties.findex)
            self.last_index.setText(Properties.lindex)
        except:
            self.addToConsole("Something's not right with the previous run information.")
            self.setRawImage('images/SLAC_LogoSD.png')
            mi.set1DImage(self, 'images/SLAC_LogoSD.png')       
        
        self.loadCalibration()
        self.loadIntegrateCalibration()
        
        self.setStyleSheet("background-color: rgb(29, 30,51);")
   
    # Compiles the information on the current transform tab page into a macro and adds it to the queue
    def addCurrentToQueue(self):
        cur_time = datetime.datetime.now().strftime('%Y-%m-%d--%H-%M-%S')
        name = ('/Users/arunshriram/Documents/SLAC Internship/monhitp-gui/macros/transform-macro-%s') %(cur_time)
        self.addToConsole("Saving this page in directory \"macros\" as \"transform-macro-%s\" and adding to the queue..." % (cur_time))
        mt.saveMacro(self, name)
        mq.addMacroToQueue(self)
        self.addToConsole("Macro saved and added to queue!")
        
    # Copies all the information from the transform tab to either the macro editor or the integrate tab.
    def windowTabChanged(self, index):
        if index == 3:
            self.editor.q_min.setText(self.q_min.text())
            self.editor.q_max.setText(self.q_max.text())
            self.editor.chi_min.setText(self.chi_min.text())
            self.editor.chi_max.setText(self.chi_max.text())
            self.editor.detectordistance.setText(self.detectordistance.text())
            self.editor.detect_tilt_alpha.setText(self.detect_tilt_alpha.text())
            self.editor.detect_tilt_delta.setText(self.detect_tilt_delta.text())
            self.editor.dcenterx.setText(self.dcenterx.text())
            self.editor.dcentery.setText(self.dcentery.text())
            self.editor.wavelength.setText(self.wavelength.text())
            self.editor.calib_source.setText(self.calib_source.text())
            self.editor.processed_location.setText(self.processed_location.text())
            self.editor.data_source.setText(self.data_source.text())            
            if self.data_source_check.isChecked():
                self.editor.data_source_check.setChecked(True)
            else:
                self.editor.data_source_check.setChecked(False)
        elif index == 2:
            self.int_detectordistance.setText(self.detectordistance.text())
            self.int_detect_tilt_alpha.setText(self.detect_tilt_alpha.text())
            self.int_detect_tilt_delta.setText(self.detect_tilt_delta.text())
            self.int_dcenterx.setText(self.dcenterx.text())
            self.int_dcentery.setText(self.dcentery.text())
            self.int_wavelength.setText(self.wavelength.text())
            self.int_calib_source.setText(self.calib_source.text())
            self.int_processed_location.setText(self.processed_location.text())
            self.int_data_source.setText(self.data_source.text())            
            if self.data_source_check.isChecked():
                self.int_data_source_check.setChecked(True)
            else:
                self.int_data_source_check.setChecked(False)            
        
    # disables all widgets except abort
    def disableWidgets(self):
        for editor in self.findChildren(ClickableLineEdit):
            editor.setDisabled(True)
        for button in self.findChildren(QPushButton):
            if button != self.abort and button != self.int_abort and button != self.stitch_abort:
                button.setDisabled(True)
        for box in self.findChildren(QCheckBox):
            box.setDisabled(True)

    # enables all widgets
    def enableWidgets(self):
        for editor in self.findChildren(ClickableLineEdit):
            editor.setEnabled(True)
        for button in self.findChildren(QPushButton):
                button.setEnabled(True)
        for box in self.findChildren(QCheckBox):
            box.setEnabled(True)
        
        
    # Begins the transform thread
    def transformThreadStart(self):
        # Check if the user has correctly selected either a folder or a group of files
        if not self.data_source_check.isChecked() and self.files_to_process == "folder":
            self.addToConsole("Please make sure you select the files you wish to process, or check the \"I'm going to select a folder\" box.")
            return
            
        self.disableWidgets()
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
        # Check if entered calibration information is correctly entered
        if (calibPath is '' and str(self.detectordistance.text()) == '' and str(self.dcenterx.text()) == '' and str(self.dcentery.text()) == '' and str(self.detect_tilt_alpha.text()) == '' and str(self.detect_tilt_delta.text()) == '' and str(self.wavelength.text()) == '') or dataPath is '':
                
            self.addToConsole("Please make sure you have entered valid data or calibration source information.")
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
        detectorData = (str(self.detectordistance.text()), str(self.detect_tilt_alpha.text()), str(self.detect_tilt_delta.text()), str(self.wavelength.text()), str(self.dcenterx.text()), str(self.dcentery.text()))
        # Initialize transform thread
        self.transformThread = TransformThread(self, str(self.processed_location.text()), calibPath, dataPath, detectorData, self.files_to_process)
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
        self.transformThread.start()
        
    
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
    
    # What should be done after a thread is finished
    def done(self, loopTime, stage1Time, stage2Time):
        avgTime = np.mean(loopTime)
        maxTime = np.max(loopTime)
        avg1 = np.mean(stage1Time)
        avg2 = np.mean(stage2Time)
        max1 = np.max(stage1Time)
        max2 = np.max(stage2Time)
        finishedMessage = ''
        finishedMessage += ('====================================================\n')
        finishedMessage += ('====================================================\n')
        finishedMessage += ('Files finished processing\n')
        finishedMessage += ('-----Avg {:.4f}s / file, max {:.4f}.s / file\n'.format(avgTime, maxTime))
        finishedMessage += ('-----Stage1: Avg {:.4f}s / file, max {:.4f}.s / file\n'.format(avg1, max1))
        finishedMessage += ('-----Stage2: Avg {:.4f}s / file, max {:.4f}.s / file\n'.format(avg2, max2))
        finishedMessage += ('-----Total Time Elapsed {:4f}s\n'.format(np.sum(loopTime)))
        finishedMessage += ('====================================================\n')
        finishedMessage += ('====================================================')        
        #QMessageBox.information(self, "Done!", finishedMessage)
        self.addToConsole(finishedMessage)
        QApplication.processEvents()            
        self.enableWidgets()
        self.transformThread.quit()
        self.integrateThread.quit()
        self.stitchThread.quit()
        #self.transformThread.deleteLater()
        #if self.transformThread.isRunning():
        #self.transformThread.quit()
        self.stitchThread.stop()
        if self.transformThread.isRunning():
            self.transformThread.stop() 
        if self.integrateThread.isRunning():
            self.integrateThread.stop() 
        self.processDone = True
        
    # Adds the passed in message to all consoles
    def addToConsole(self, message):
        self.console.append(message)
        self.miconsole.append(message)
        self.qconsole.append(message)
        self.stitch_console.append(message)
        QApplication.processEvents()
   
    # Loads transform calibration information based on the filename the user selects
    def loadCalibration(self):
        if str(self.calib_source.text()) != '':
            try:
                d_in_pixel, Rotation_angle, tilt_angle, lamda, x0, y0 = parse_calib(str(self.calib_source.text()))
            except:
                self.addToConsole("Unable to locate calibration source file.")
                return
            self.wavelength.setText(str(lamda))
            self.detectordistance.setText(str(d_in_pixel))
            self.dcenterx.setText(str(x0))
            self.dcentery.setText(str(y0))
            self.detect_tilt_alpha.setText(str(Rotation_angle))
            self.detect_tilt_delta.setText(str(tilt_angle))
     
     # Loads integrate calibration information based on the filename the user selects          
    def loadIntegrateCalibration(self):
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
                                      
    # Loads the appropriate files based on the data source the user selects
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
                print(filenames)
                self.data_source.setText(os.path.dirname(filenames[0]))
                self.processed_location.setText(self.data_source.text())
                self.files_to_process = filenames
            except:
                #traceback.print_exc()
                self.addToConsole("Something went wrong when trying to select your files.")
    # Retrieves and loads the calibration information that the user selects
    def getCalibSourcePath(self):
        path = str(QFileDialog.getOpenFileName(self, "Select Calibration File", ('/Users/arunshriram/Documents/SLAC Internship/monhitp-gui/calib/')))
        if path !='':
            self.calib_source.setText(path)
            self.loadCalibration()
        
    # Saves the custom calibration that the user enters as a new calibration file
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
            self.addToConsole("Calibration could not be saved!")
            return

        
    # Argument is the filename of the q-chi plot, this displays the plot on the screen
    def setRawImage(self, filename):
        try:
            pixmap = QPixmap(filename)
            self.raw_image.setPixmap(pixmap.scaled(self.imageWidth, self.imageWidth, Qt.KeepAspectRatio))        
        except:
            self.addToConsole("Could not load Qchi image.")
            return
    # Asks the user for the location where the processed files should go          
    def setProcessedLocation(self):
        path = str(QFileDialog.getExistingDirectory(self, "Select a location for processed files", str(self.data_source.text())))
        #path = str(QFileDialog.getOpenFileName(self, "Select Calibration File", ('/Users/arunshriram/Documents/SLAC Internship/monhitp-gui/calib/')))
        if path !='':
            self.processed_location.setText(path)
        
    # Returns the number of lines in a file
    def file_len(self, fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1        
    

            
        
    
            

           
    # Sets the bar progress to whatever value is passed in
    def setRadialBar(self, bartype, val):
        if bartype == 1:
            self.int_bar.setValue(val)
        elif bartype == 0:
            self.bar.setValue(val)
        elif bartype == 2:
            self.stitchbar.setValue(val)
            
        self.queue_bar_files.setValue(val)
   
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
    


# Defines which lines are wanted/unwanted when writing previous run information during stitching
def stitch_is_wanted(line):
    if "s_data_source" in line or "findex" in line or "s_processed_loc" in line or "lindex" in line or "stitch_image" in line:
        return True
    return False    

# Defines which lines are wanted/unwanted when writing previous run information during integrating
def integrate_is_wanted(line):
    if "i_data_source" in line or "i_calib_source" in line or "qmin" in line or "qmax" in line or "chimin" in line or "chimax" in line or "i_processed_loc" in line or "one_d_image" in line:
        return True
    return False     

# This class is the governing class, the highest in the hiearchy. Its central widget is the main GUI window. 
class Menu(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.form_widget = MONster()
        self.setCentralWidget(self.form_widget)
        
        
        self.updateUi()
        
    def updateUi(self):
        bar = self.menuBar()
        file = bar.addMenu('File')
        home_action = QAction('Home', self)
        
        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        saveplot_action = QAction('Save Plot Data', self)
        saveplot_action.setShortcut('Ctrl+Alt+S')
        quit_action = QAction('Quit', self)
        quit_action.setShortcut('Ctrl+Q')
        
        file.addAction(home_action)
        file.addAction(save_action)
        file.addAction(saveplot_action)
        file.addAction(quit_action)
        
        
        quit_action.triggered.connect(lambda: qApp.quit())
        self.setWindowTitle('MONster')
        
        self.setStyleSheet("background-color: rgb(29, 30,51);")
        
        self.show()
        self.raise_()
        self.showMaximized()
        
        
  
        
        
def main():
    app = QApplication(sys.argv)
    menu = Menu()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()