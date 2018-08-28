# This file is the main file for the GUI that transforms, stitches, and integrates detector data into 
# Q-chi plots, stitched plots, and one dimensional graphs with peak fitting capabilities. 
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
#
import numpy as np
import glob
import numpy
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
#=====================
import sys
import os, traceback, ast
import getpass
import datetime
from ClickableLineEdit import *
from TransformThread import *
from IntegrateThread import *
from StitchThread import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import HelpDialog

# This class defines the Detector window in the menu.
class DetectorEditor(QWidget):
    def __init__(self, windowreference):
        QWidget.__init__(self)
        self.windowreference = windowreference
        self.listwidget = QListWidget()
        self.listwidget.setMaximumWidth(350)
        self.listwidget.setMinimumWidth(250)
        with open ("Bookkeeping/Properties.csv", 'rb') as p:
            reader = csv.reader(p)
            prop = dict(reader)
            
        detectors = ast.literal_eval(prop["detectors"])
        self.detectorlist = []
        self.string_detectorlist = []
        for item in detectors:
            string = item.split(', ')
            name = string[0]
            width = int(string[1][7:].rstrip())
            height = int(string[2][7:].rstrip())
            detector = Detector(name, width, height)
            self.detectorlist.append(detector)
            self.string_detectorlist.append(str(detector))
            self.windowreference.detectorList.append(detector)
            self.listwidget.addItem(str(detector))
            self.windowreference.detector_combo.addItem(str(detector))
            self.windowreference.editor.detector_combo.addItem(str(detector))
            
        

        self.removeButton = QPushButton("Remove")
        self.nameLabel = QLabel("Name")
        self.name = QLineEdit()
        self.widthLabel = QLabel("Width")
        self.width = QLineEdit()
        self.heightLabel = QLabel("Height")
        self.height = QLineEdit()
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

     
    def removeDetector(self):
        curRow = self.listwidget.currentRow()
        if curRow >= 0:
            message = QLabel("Are you sure you want to delete this detector?\n\n%s" % str(self.detectorlist[curRow]))
            self.win = QWidget()
            self.win.setWindowTitle('ARE YOU SURE?')
            self.ok = QPushButton('Yeah, get rid of it')
            self.no = QPushButton("Please don't")
            self.ly = QVBoxLayout()
            self.ly.addWidget(message)
            h = QHBoxLayout()
            h.addWidget(self.ok)
            h.addWidget(self.no)
            self.ly.addLayout(h)
            self.win.setLayout(self.ly)    
            def hi():
                self.win.close()
                self.raise_()
            self.no.clicked.connect(hi)
            def rem():
                self.listwidget.takeItem(curRow)
                self.windowreference.detector_combo.removeItem(curRow)
                self.windowreference.editor.detector_combo.removeItem(curRow)
                del self.detectorlist[curRow]
                del self.string_detectorlist[curRow]
                with open("Bookkeeping/Properties.csv", 'rb') as infile:
                    reader =csv.reader(infile)
                    prop = dict(reader)
                prop['detectors'] = str(self.string_detectorlist)
                with open("Bookkeeping/Properties.csv", 'wb') as outfile:
                    writer = csv.writer(outfile)
                    for key, value in prop.items():
                        writer.writerow([key, value])
                self.win.close()
                self.windowreference.raise_()
            self.ok.clicked.connect(rem)
            self.win.show()
            self.win.raise_()
        else:
            displayError(self, "No detector selected!")
            return
                        
    def updateConnections(self):
        self.closeButton.clicked.connect(lambda: self.close())
        self.addButton.clicked.connect(self.addDetector)
        self.name.returnPressed.connect(self.addDetector)
        self.width.returnPressed.connect(self.addDetector)
        self.height.returnPressed.connect(self.addDetector)
        self.removeButton.clicked.connect(self.removeDetector)

    def addDetector(self):
        if self.name.text().isEmpty() or self.width.text().isEmpty() or self.height.text().isEmpty():
            displayError(self, "Please make sure you fill out all the relevant information!")
            return
        try:
            name = str(self.name.text())
            width = int(str(self.width.text()))
            height = int(str(self.height.text()))
        except:
            displayError(self, "Could not add your values.")
            return
        detector = Detector(name, width, height)
        exists = False
        for det in self.detectorlist:
            if Detector.__eq__(det,detector):
                exists = True
                break
        if exists  :
            displayError(self, "This detector already exists!")
            return
        self.detectorlist.append(detector)
        self.string_detectorlist.append(str(detector))
        properties = []
        with open("Bookkeeping/Properties.csv", 'rb') as inFile:
            reader = csv.reader(inFile)
            prop = dict(reader)
        detectors = ast.literal_eval(prop['detectors'])
        detectors.append(str(detector))
        prop['detectors'] = str(detectors)
        with open("Bookkeeping/Properties.csv", 'wb') as outFile:
            writer = csv.writer(outFile)
            for key,value in prop.items():
                writer.writerow([key, value])
        
        self.listwidget.addItem(str(detector))
        self.windowreference.detector_combo.addItem(str(detector))
        self.windowreference.editor.detector_combo.addItem(str(detector))
        
# This class is the class that governs all things that occur in the GUI window.
class MONster(QTabWidget):
    def __init__(self):
        QTabWidget.__init__(self)
        if not os.path.isdir("Bookkeeping"):
            os.makedirs("Bookkeeping")
        self.current_user = getpass.getuser()
        self.macroQueue = [] # list of macros for the queue tab
        self.fileProcessedCount = 0
        self.lineEditStyleSheet ="QLineEdit { border-radius: 4px;  color:rgb(0, 0, 0); background-color: rgb(255, 255, 255); border-style:outset; border-width:4px;  border-radius: 4px; border-color: rgb(34, 200, 157); color:rgb(0, 0, 0); background-color: rgb(200, 200, 200); } "
        self.textStyleSheet = "QLabel {background-color : rgb(29, 30, 50); color: white; }"
        self.help_dialog = None
        screenShape = QDesktopWidget().screenGeometry()
        self.imageWidth = screenShape.height()/3.5
        self.properties_OK = False
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
       
        count = 0
        if not os.path.exists("Bookkeeping/Properties.csv"):
            resetProperties()
            message = QLabel("Could not locate Properties.csv, so a new file was generated. Please restart MONster.")
            self.win = QWidget()
            self.win.setWindowTitle('Properties file corrupted!')
            self.ok = QPushButton('Ok')
            self.ly = QVBoxLayout()
            self.ly.addWidget(message)
            self.ly.addWidget(self.ok)
            self.win.setLayout(self.ly)    
            self.ok.clicked.connect(lambda: sys.exit())
            #def closeEvent(event):
                #sys.exit()           
            #self.win.connect(self.win, SIGNAL('triggered()'), closeEvent )
            self.win.show()
            self.win.raise_()
            return            
        
        with open("Bookkeeping/Properties.csv", 'rb') as p:
            reader = csv.reader(p)
            prop = dict(reader)
            for k,v in prop.items():
                count += 1      
        if count < 16:
            resetProperties()
            message = QLabel("Properties.py was found corrupted, so a new one was generated. Please restart MONster.")
            self.win = QWidget()
            self.win.setWindowTitle('Properties file corrupted!')
            self.ok = QPushButton('Ok')
            self.ly = QVBoxLayout()
            self.ly.addWidget(message)
            self.ly.addWidget(self.ok)
            self.win.setLayout(self.ly)    
            self.ok.clicked.connect(lambda: sys.exit())
            #def closeEvent(event):
                #sys.exit()           
            #self.win.connect(self.win, SIGNAL('triggered()'), closeEvent )
            self.win.show()
            self.win.raise_()
            return
        self.properties_OK = True
                            
        self.detectorWindow = DetectorEditor(self)
        self.transformThread = TransformThread(self, None, None, None, None, 0)  # initialize the transform thread
        self.integrateThread = IntegrateThread(self, None, None, None, 0) # initialize the integrate thread
        self.stitchThread = StitchThread(self, None, None, 0) # initialize the stitch thread              
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
        
        if os.path.exists("Bookkeeping/thisRun.txt"):
            self.addToConsole("========================================================")
            self.addToConsole("||   Welcome, %s! Setting up MONster for you, just the way you left it...   ||" % self.current_user)
            self.addToConsole("========================================================")            
            
        else:
            self.addToConsole("===============================================================")
            self.addToConsole("||    Welcome to MONster, %s! No need to be afraid, this MONster's on your side.    ||" % self.current_user)
            self.addToConsole("===============================================================")
        now = datetime.datetime.now()
        months = {1: "January"}
        months[2] = "February"
        months[3] = "March"
        months[4] = "April"
        months[5] = "May"
        months[6] = "June"
        months[7] = "July"
        months[8] = "August"
        months[9] = "September"
        months[10] = "October"
        months[11] = "November"
        months[12] = "December"
        self.addToConsole("The date is %s %d, %s. The time is %d:%d." % (months[now.month], now.day, now.year, now.hour, now.minute))
        self.show()
        self.raise_()
 
        
        ############################################
        ##############CONNECTIONS#################
        ############################################
        self.folder_button.clicked.connect(self.getDataSourceDirectoryPath)
        
        self.file_button.clicked.connect(self.getDataSourceFiles)
        
        self.calib_folder_button.clicked.connect(self.getCalibSourcePath)
        
        self.processed_location_folder_button.clicked.connect(self.setProcessedLocation)
        
        self.start_button.clicked.connect(lambda: mt.transformThreadStart(self))
        
        self.q_min.returnPressed.connect(lambda: mt.transformThreadStart(self))
        
        self.q_min.clicked.connect(lambda: self.q_min.selectAll())        
        
        self.q_max.returnPressed.connect(lambda: mt.transformThreadStart(self))
        
        self.q_max.clicked.connect(lambda: self.q_max.selectAll())
        
        self.chi_min.returnPressed.connect(lambda: mt.transformThreadStart(self))
        
        self.chi_min.clicked.connect(lambda: self.chi_min.selectAll())
        
        self.chi_max.returnPressed.connect(lambda: mt.transformThreadStart(self))
        
        self.chi_max.clicked.connect(lambda: self.chi_max.selectAll())
        
        self.data_source.returnPressed.connect(lambda: mt.transformThreadStart(self))
                
        self.calib_source.returnPressed.connect(lambda: mt.transformThreadStart(self))
                
        self.saveCustomCalib.clicked.connect(self.saveCalibAction)
        
        self.abort.clicked.connect(self.transformThread.abortClicked)
        
        self.int_abort.clicked.connect(self.integrateThread.abortClicked)
        
        self.stitch_abort.clicked.connect(self.stitchThread.abortClicked)
        
        self.addMacroButton.clicked.connect(lambda: mq.addMacro(self))
        
        self.currentChanged.connect(self.windowTabChanged)
        
        self.transform_addToQueueButton.clicked.connect(lambda: mt.addTransformCurrentToQueue(self))

        self.stitch_addToQueueButton.clicked.connect(lambda: ms.addStitchCurrentToQueue(self))

        self.stitch_saveMacroButton.clicked.connect(lambda: ms.saveStitchMacro(self))

        self.integrate_addToQueueButton.clicked.connect(lambda: mi.addIntegrateCurrentToQueue(self))

        self.integrate_saveMacroButton.clicked.connect(lambda: mi.saveIntegrateMacro(self))
        
        self.removeButton.clicked.connect(lambda: mq.removeMacro(self))
        
        self.int_start_button.clicked.connect(lambda: mi.integrateThreadStart(self))
        
        self.int_abort.clicked.connect(self.integrateThread.abortClicked)
                
        self.int_folder_button.clicked.connect(lambda: mi.getIntDataSourceDirectoryPath(self))
        
        self.int_file_button.clicked.connect(lambda: mi.getIntDataFiles(self))
        
        self.int_processed_location_folder_button.clicked.connect(lambda: mi.setIntProcessedLocation(self))
                
        self.startQueueButton.clicked.connect(lambda: mq.beginQueue(self))
        
        self.transform_saveMacroButton.clicked.connect(lambda: mt.saveTransformMacro(self))
        
        self.stitch_start_button.clicked.connect(lambda: ms.beginStitch(self))
        
        self.stitch_folder_button.clicked.connect(lambda: ms.stitchImageSelect(self))
        
        self.stitch_saveLocation_button.clicked.connect(lambda: ms.setStitchSaveLocation(self))
                
        self.saveQueueButton.clicked.connect(lambda: mq.saveQueue(self))
      
        self.loadQueueButton.clicked.connect(lambda: mq.loadQueue(self))

        self.stopQueueButton.clicked.connect(lambda: mq.abortQueue(self))
        
        self.pauseQueueButton.clicked.connect(lambda: mq.pauseQueue(self))

        self.resumeQueueButton.clicked.connect(lambda: mq.resumeQueue(self))
        
        def doubleclick():
            row = self.queue.currentRow()
            if len(self.macroQueue) > 0:
                self.editor.loadMacro(self.macroQueue[row].getFilename())
                self.editor.show()
                self.editor.raise_()

        self.queue.itemDoubleClicked.connect(doubleclick)
        self.setStyleSheet("background-color: rgb(29, 30,51);")
        #self.showFullScreen()

        ###########################################
        ###########################
        #Restore default graphs and data from the previous run upon starting MONster
        ###########################
        # Bookkeeping/Properties.csv has the following information from previous run(s) (in no particular order):
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
    
        if propertiesAreClear():
            self.addToConsole("No previous run information found!")
            resetProperties()
            return

        self.console_saver = ConsoleWindow(self)
        self.console_save_location = str(self.console_saver.save_loc.text())

        with open('Bookkeeping/Properties.csv', 'rb') as prop:
                reader = csv.reader(prop)
                Properties = dict(reader)
        try:
            if os.path.exists(Properties["t_data_source"]):
                dataPath = Properties["t_data_source"]
                self.data_source.setText(dataPath)
                self.t_files_to_process = [dataPath]                
            if os.path.exists(Properties["s_data_source"]):
                self.images_select.setText(Properties["s_data_source"])                
            if os.path.exists(Properties["i_data_source"]):
                dataPath = Properties["i_data_source"]
                self.int_data_source.setText(dataPath)
                self.i_files_to_process = [dataPath]
                
            if os.path.exists(Properties["t_calib_source"]):
                self.calib_source.setText(Properties["t_calib_source"])
                self.loadCalibration()
            if os.path.exists(Properties["t_processed_loc"]):
                self.processed_location.setText(Properties["t_processed_loc"])
            else:
                self.processed_location.setText(str(self.data_source.text()) + "/Processed_Transform")
            if os.path.exists(Properties["s_processed_loc"]):
                self.stitch_saveLocation.setText(Properties["s_processed_loc"])
            else:
                self.stitch_saveLocation.setText(str(self.images_select.text())  + "/Processed_Stitch")                
            if os.path.exists(Properties["i_processed_loc"]):
                self.int_processed_location.setText(Properties["i_processed_loc"])
            else:
                self.int_processed_location.setText(str(self.int_data_source.text()) + "/Processed_Integrate")                
                
            self.setRawImage(Properties["two_d_image"])
            ms.setStitchImage(self, Properties["stitch_image"])
            mi.set1DImage(self, Properties["one_d_image"])
            self.q_min.setText(Properties["qmin"])
            self.q_max.setText(Properties["qmax"])
            self.chi_min.setText(Properties["chimin"])
            self.chi_max.setText(Properties["chimax"])

        except:
            traceback.print_exc()
            self.addToConsole("Something's not right with the previous run information.")
            self.setRawImage('images/SLAC_LogoSD.png')
            mi.set1DImage(self, 'images/SLAC_LogoSD.png')       
            if str(self.processed_location.text()) == "":
                self.processed_location.setText(str(self.data_source.text()) + "/Processed_Transform")
            if str(self.int_processed_location.text()) == "":
                self.int_processed_location.setText(str(self.int_data_source.text()) + "/Processed_Integrate")
            if str(self.stitch_saveLocation.text()) == "":
                self.stitch_saveLocation.setText(str(self.images_select.text())  + "/Processed_Stitch")
                
        self.tabBar().setStyleSheet("QTabBar::tab {color: rgb(230, 90, 0);}")

        
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
            self.editor.int_processed_location.setText(self.int_processed_location.text())
            self.editor.int_data_source.setText(self.int_data_source.text())                   
           

            self.editor.stackList.setCurrentRow(0)
        
    # disables all widgets except abort
    def disableWidgets(self):
        for editor in self.findChildren(ClickableLineEdit):
            editor.setDisabled(True)
        for button in self.findChildren(QPushButton):
            if button != self.abort and button != self.int_abort and button != self.stitch_abort and button != self.stopQueueButton and button != self.pauseQueueButton:
                button.setDisabled(True)
        for box in self.findChildren(QCheckBox):
            box.setDisabled(True)
        self.detector_combo.setDisabled(True)
        self.changeTabCheck.setEnabled(True)

    # enables all widgets
    def enableWidgets(self):
        for editor in self.findChildren(ClickableLineEdit):
            editor.setEnabled(True)
        for button in self.findChildren(QPushButton):
                button.setEnabled(True)
        for box in self.findChildren(QCheckBox):
            box.setEnabled(True)
        self.detector_combo.setEnabled(True)

   
        
    
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
        self.console.moveCursor(QTextCursor.End)
        self.miconsole.moveCursor(QTextCursor.End)
        self.qconsole.moveCursor(QTextCursor.End)
        self.stitch_console.moveCursor(QTextCursor.End)
        #QMessageBox.information(self, "Done!", finishedMessage)
        self.addToConsole(finishedMessage)
        QApplication.processEvents()            
        self.enableWidgets()
        self.stitchThread.quit()
        self.stitchThread.stop()
        self.processDone = True
    
    # What should be done after a thread is finished
    def done(self, loopTime, stage1Time, stage2Time):
        try:
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
        except:
            finishedMessage = ''
            finishedMessage += ('====================================================\n')
            finishedMessage += ('====================================================\n')
            finishedMessage += ('Files finished processing\n')
            finishedMessage += ('-----Total Time Elapsed {:4f}s\n'.format(np.sum(loopTime)))
            finishedMessage += ('====================================================\n')
            finishedMessage += ('====================================================\n')            
        #QMessageBox.information(self, "Done!", finishedMessage)
        self.addToConsole(finishedMessage)
        self.console.moveCursor(QTextCursor.End)
        self.miconsole.moveCursor(QTextCursor.End)
        self.qconsole.moveCursor(QTextCursor.End)
        self.stitch_console.moveCursor(QTextCursor.End)        
        QApplication.processEvents()            
        self.enableWidgets()
        self.transformThread.quit()
        self.integrateThread.quit()
        self.stitchThread.quit()
        #self.transformThread.deleteLater()
        #if self.transformThread.isRunning():
        #self.transformThread.quit()
        self.stitchThread.stop()
        self.transformThread.stop() 
        self.integrateThread.stop() 
        self.processDone = True
        
    # Adds the passed in message to all consoles
    def addToConsole(self, message):
        self.console.append(message)
        self.miconsole.append(message)
        self.qconsole.append(message)
        self.stitch_console.append(message)
        self.console.moveCursor(QTextCursor.End)
        self.miconsole.moveCursor(QTextCursor.End)
        self.qconsole.moveCursor(QTextCursor.End)
        self.stitch_console.moveCursor(QTextCursor.End)
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
     
  
    # Loads the appropriate files based on the data source the user selects
    def getDataSourceDirectoryPath(self):
        try:
            folderpath = str(QFileDialog.getExistingDirectory())
            if folderpath != '':
                self.data_source.setText(folderpath)
                self.data_label.setText("Current data source: (folder)")
                self.processed_location.setText(str(self.data_source.text())  + "/Processed_Transform")
                self.t_files_to_process = [folderpath]
            self.raise_()
        except:
            self.addToConsole("Something went wrong when trying to open your directory.")
     
     # Loads the appropriate files based on the data source the user selects
    def getDataSourceFiles(self):
        try:
            filenames = QFileDialog.getOpenFileNames(self, "Select the files you wish to use.")
            filenames = [str(filename) for  filename in filenames]
            if len(filenames) < 2:
                self.data_label.setText("Current data source: %s" % os.path.basename(filenames[0]))
            else:
                self.data_label.setText("Current data source: (multiple files)")
            print(filenames)
            self.data_source.setText(os.path.dirname(filenames[0]))
            self.processed_location.setText(str(self.data_source.text())  + "/Processed_Transform")
            self.t_files_to_process = filenames
            self.raise_()
        except:
            #traceback.print_exc()
            self.addToConsole("Did not select a data source.")   
            
    # Retrieves and loads the calibration information that the user selects
    def getCalibSourcePath(self):
        path = str(QFileDialog.getOpenFileName(self, "Select Calibration File", ('/Users/arunshriram/Documents/SLAC Internship/monhitp-gui/calib/')))
        if path !='':
            self.calib_source.setText(path)
            self.loadCalibration()
        self.raise_()
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
            self.raise_()
        except:
            self.addToConsole("Calibration could not be saved!")
            return

        
    # Argument is the filename of the q-chi plot, this displays the plot on the screen
    def setRawImage(self, filename):
        try:
            pixmap = QPixmap(filename)
            if filename == ""or not os.path.exists(filename):
                pixmap = QPixmap("images/SLAC_LogoSD.png")
                self.addToConsole("Could not load Qchi image.")
                
            self.raw_image.setPixmap(pixmap.scaled(self.imageWidth, self.imageWidth, Qt.KeepAspectRatio))        
        except:
            self.addToConsole("Could not load Qchi image.")
            return
    # Asks the user for the location where the processed files should go          
    def setProcessedLocation(self):
        path = str(QFileDialog.getExistingDirectory(self, "Select a location for processed files", str(self.data_source.text())))
        #path = str(QFileDialog.getOpenFileName(self, "Select Calibration File", ('/Users/arunshriram/Documents/SLAC Internship/monhitp-gui/calib/')))
        if path !='':
            self.processed_location.setText(os.path.join(path, "Processed_Transform"))
        self.raise_()
    # Returns the number of lines in a file
    def file_len(self, fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1        
    
    def incrementBar(self, inc):
        cur_val = self.queue_bar.getValue()
        new_val = cur_val + inc
        self.queue_bar.setValue(new_val)
        self.bar.setValue(new_val)
        self.int_bar.setValue(new_val)
        self.stitchbar.setValue(new_val)
        
  
    # Sets the bar progress to whatever value is passed in
    def setRadialBar(self, bartype, val):
        if bartype == 1:
            self.int_bar.setValue(val)
        elif bartype == 0:
            self.bar.setValue(val)
        elif bartype == 2:
            self.stitchbar.setValue(val)
        elif bartype == 3:
            self.incrementBar(val)
            
        
    # None -> None
    # Updates the current 1D graph region        
    def updateRegion(self, window, viewRange):
        rgn = viewRange[0]
        self.region.setRegion(rgn)    
    
    # None -> None
    # Updates the current 1D graph ranges
    def update(self):
        self.region.setZValue(10)
        minX, maxX = self.region.getRegion()
        self.one_d_graph.setXRange(minX, maxX, padding=0)   
    
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

# This class is a small one that keeps the information of the console log save file location.
class ConsoleWindow(QWidget):
    def __init__(self, win):
        QWidget.__init__(self)
        self.win = win
        self.message = QLabel("Please choose a log file save location.")
        self.setWindowTitle('Console log save location')
        self.save_loc = QLineEdit()
        self.save_loc.setMinimumWidth(550)
        with open('Bookkeeping/Properties.csv', 'rb') as fil:
            reader = csv.reader(fil)
            prop = dict(reader)
        save_loc = prop.get("console_saving")
        if save_loc is None:
            self.save_loc.setText("")
        else:
            self.save_loc.setText(save_loc)

        self.saveButton = QPushButton("Save")
        self.cancelButton = QPushButton("Cancel")

        ly = QVBoxLayout()
        ly.addWidget(self.message)
        ly.addWidget(self.save_loc)
        h = QHBoxLayout()
        h.addWidget(self.cancelButton)
        h.addWidget(self.saveButton)
        ly.addLayout(h)
        self.setLayout(ly)

        def save():
            self.win.console_save_location = str(self.save_loc.text())
            with open("Bookkeeping/Properties.csv", 'rb') as fil:
                reader = csv.reader(fil)
                prop = dict(reader)
            prop['console_saving'] = str(self.save_loc.text())
            with open("Bookkeeping/Properties.csv", 'wb') as fil:
                writer = csv.writer(fil)
                for key, val in prop.items():
                    writer.writerow([key, val])
            self.close()
            self.win.raise_()
        self.saveButton.clicked.connect(save)
        self.cancelButton.clicked.connect(lambda: self.close())


# This class is the governing class, the highest in the hiearchy. Its central widget is the main GUI window. 
class Menu(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.form_widget = MONster()
        self.setCentralWidget(self.form_widget)
        self.setWindowIcon(QIcon('images/appicon.icns'))
        self.setStyleSheet("""
                QMenuBar {
                    background-color: rgb(29,30,51);
                    color: rgb(255,255,255);
                    border: 1px solid #000;
                }
        
                QMenuBar::item {
                    background-color: rgb(29,30,51);
                    color: rgb(255,255,255);
                }
        
                QMenuBar::item::selected {
                    background-color: rgb(29,30,51);
                }
        
                QMenu {
                    background-color: rgb(29,30,51);
                    color: rgb(255,255,255);
                    border: 1px solid #000;           
                }
        
                QMenu::item::selected {
                    background-color: rgb(29,30,51);
                }
    """)        
        self.updateUi()
        
    def updateUi(self):
        self.help_dialog = None
        bar = self.menuBar()
        file = bar.addMenu('File')
        edit = bar.addMenu("Edit")
        help = bar.addMenu("Click me for answers to your problems")
        console_action = QAction('Change log file save location', self)
        
        
        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        #saveplot_action = QAction('Save Plot Data', self)
        #saveplot_action.setShortcut('Ctrl+Alt+S')
        clear_prop = QAction("Clear previous run information", self)
        help_a = QAction("Open the help dialog!", self)
        quit_action = QAction('Quit', self)
        quit_action.setShortcut('Ctrl+Q')
    

        detectors = QAction("Add or remove detectors", self)
        
        
        file.addAction(console_action)
        #file.addAction(save_action)
        edit.addAction(clear_prop)
        edit.addAction(detectors)
        #file.addAction(saveplot_action)
        file.addAction(quit_action)
        help.addAction(help_a)
        
        quit_action.triggered.connect(lambda: qApp.quit())
        clear_prop.triggered.connect(self.clearProperties)
        help_a.triggered.connect(self.openHelpDialog)
        def console():
            self.form_widget.console_saver.show()
            self.form_widget.console_saver.raise_()




        console_action.triggered.connect(console)
        def stupidpoopypants():
            self.form_widget.detectorWindow.show()
            self.form_widget.detectorWindow.raise_()
        detectors.triggered.connect(stupidpoopypants)
        self.setWindowTitle('SSRL: MONster - v1.1')
        
        #self.setStyleSheet("background-color: rgb(29, 30,51);")
        
        self.show()
        self.raise_()
        #self.setFixedSize(self.minimumSizeHint())
        screenShape = QDesktopWidget().screenGeometry()
        self.form_widget.imageWidth = screenShape.height()/3
        #self.setMaximumHeight(screenShape.height())        
        #self.showFullScreen()
        
    def setHelpDialog(self, hd):
        self.help_dialog = hd
        self.form_widget.help_dialog = hd
        if not os.path.exists("Bookkeeping/thisRun.txt") and self.form_widget.properties_OK:
            self.help_dialog.show()
            self.help_dialog.raise_()        
    def openHelpDialog(self):
        self.help_dialog.show()
        self.help_dialog.raise_()

    # event -> None
    # Prompts the user for console saving upon closing MONster
    def closeEvent(self, event):
        
        message = QLabel("Would you like to save this session's console log in the specified save path?")
        event.ignore()
        self.win = QWidget()
        self.win.setWindowTitle('Console log saving')
        self.ok = QPushButton('Yes, please!')
        self.no = QPushButton("Cancel")
        self.quit = QPushButton("Quit without saving console logs")
        self.ly = QVBoxLayout()
        self.ly.addWidget(message)
        self.ly.addWidget(QLabel(self.form_widget.console_save_location))
        h = QHBoxLayout()
        h.addWidget(self.no)
        h.addWidget(self.quit)
        h.addWidget(self.ok)
        self.ly.addLayout(h)
        self.win.setLayout(self.ly)    
        self.win.show()
        self.win.raise_()
        QApplication.processEvents()
        def saveconsole():
            save_path = self.form_widget.console_save_location.rstrip()
            logs = str(self.form_widget.console.toPlainText())
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            pathname = os.path.join(save_path, "console_%s.txt" % datetime.datetime.today().strftime('%Y-%m-%d'))
            with open(pathname, 'a') as console:
                    console.write(logs)
            sys.exit()
        self.ok.clicked.connect(saveconsole)
        def showmon():
            event.ignore()
            self.form_widget.show()
            self.form_widget.raise_()
            self.win.close()
        self.no.clicked.connect(showmon)
        self.quit.clicked.connect(lambda: sys.exit())


        
    def clearProperties(self):
        try:
            with open("Bookkeeping/Properties.csv", 'rb') as p:
                reader = csv.reader(p)
                prop = dict(reader)
            with open("Bookkeeping/Properties.csv", 'wb') as p:
                writer = csv.writer(p)
                prop["t_data_source"] = ""
                prop["s_data_source"] = ""
                prop["i_data_source"] = ""
                prop["t_calib_source"] = ""
                prop["t_processed_loc"] = ""
                prop["s_processed_loc"] = ""
                prop["i_processed_loc"] = ""
                prop["two_d_image"] = ""
                prop["stitch_image"] = ""
                prop["one_d_image"] = ""
                prop["qmin"] = ""
                prop["qmax"] = ""
                prop["chimin"] = ""
                prop["chimax"] = ""
                prop["console_saving"] = "True"
                prop["detectors"] = "['PILATUS3 X 100K-A, Width: 487, Height: 195', 'PILATUS3 X 200K-A, Width: 487, Height: 407', 'PILATUS3 X 300K, Width: 487, Height: 619', 'PILATUS3 X 300K-W, Width: 1475, Height: 195', 'PILATUS3 X 1M, Width: 981, Height: 1043', 'PILATUS3 X 2M, Width: 1485, Height: 1679', 'PILATUS3 X 6M, Width: 2463, Height: 2527', 'MX225-HE, Width: 6144, Height: 6144']"
                for key, value in prop.items():
                    writer.writerow([key, value])
        except:
            self.form_widget.addToConsole("Could not clear properties - something is wrong with the Properties.csv file!")
            return
def resetProperties():
    try:
        with open("Bookkeeping/Properties.csv", 'wb') as p:
            writer = csv.writer(p)
            prop = {"t_data_source" :  ""}
            prop["s_data_source"] = ""
            prop["i_data_source"] = ""
            prop["t_calib_source"] = ""
            prop["t_processed_loc"] = ""
            prop["s_processed_loc"] = ""
            prop["i_processed_loc"] = ""
            prop["two_d_image"] = ""
            prop["stitch_image"] = ""
            prop["one_d_image"] = ""
            prop["qmin"] = ""
            prop["qmax"] = ""
            prop["chimin"] = ""
            prop["chimax"] = ""
            prop["console_saving"] = "True"
            prop["detectors"] = "['PILATUS3 X 100K-A, Width: 487, Height: 195', 'PILATUS3 X 200K-A, Width: 487, Height: 407', 'PILATUS3 X 300K, Width: 487, Height: 619', 'PILATUS3 X 300K-W, Width: 1475, Height: 195', 'PILATUS3 X 1M, Width: 981, Height: 1043', 'PILATUS3 X 2M, Width: 1485, Height: 1679', 'PILATUS3 X 6M, Width: 2463, Height: 2527', 'MX225-HE, Width: 6144, Height: 6144']"
            for key, value in prop.items():
                writer.writerow([key, value])
    except:
        return
def propertiesAreClear():
    clear = True
    with open('Bookkeeping/Properties.csv', 'rb') as prop:
        reader = csv.reader(prop)
        Properties = dict(reader)
        for key, value in Properties.items():
            if key != "detectors":
                if value != "":
                    clear = False
                    break
    return clear
        
def main():
    app = QApplication(sys.argv)
    menu = Menu()
    hd = HelpDialog.HelpDialog(menu.form_widget)
    menu.setHelpDialog(hd)
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()