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
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from IntegrateThread import *
import pyqtgraph as pg
import csv
import numpy as np
import monster_queueloader as mq
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
    self.one_d_graph.autoRange() 
    self.one_d_graph.sigRangeChanged.connect(self.updateRegion)
    self.region.sigRegionChanged.connect(self.update)
    self.one_d_graph.sigRangeChanged.connect(self.updateRegion)
    self.one_d_graph.setFixedWidth(self.imageWidth)
    self.one_d_graph.setMaximumHeight(self.imageWidth)
    self.i_files_to_process = []
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
    # self.int_start_button.setFixedSize(160, 30)
    self.int_start_button.resize(self.int_start_button.sizeHint().width(), self.int_start_button.sizeHint().height())

    self.int_abort = QPushButton('Abort Integration')
    self.int_abort.setStyleSheet("background-color: rgb(255, 140, 140);")              
    # self.int_abort.setFixedSize(150, 30)
    self.int_abort.resize(self.int_abort.sizeHint().width(), self.int_abort.sizeHint().height())

    
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
    self.integrate_saveMacroButton = QPushButton("Save as a macro")
    # self.integrate_saveMacroButton.setMaximumWidth(160)
    # self.integrate_saveMacroButton.setFixedHeight(30)
    self.integrate_saveMacroButton.setStyleSheet("background-color: rgb(255, 251, 208);")
    self.integrate_saveMacroButton.resize(self.integrate_saveMacroButton.sizeHint().width(), self.integrate_saveMacroButton.sizeHint().height())

    self.integrate_addToQueueButton = QPushButton("Add this configuration to the queue")
    # self.integrate_addToQueueButton.setMaximumWidth(220)
    # self.integrate_addToQueueButton.setFixedHeight(30)
    self.integrate_addToQueueButton.setStyleSheet("background-color: rgb(255, 207, 117);")  
    self.integrate_addToQueueButton.resize(self.integrate_addToQueueButton.sizeHint().width(), self.integrate_addToQueueButton.sizeHint().height())

    
    
def plot1dGraph(self, qArray, integ_cake, QRange, ChiRange):
    self.one_d_graph.clear()
    QApplication.processEvents()
    self.one_d_graph.plot(qArray, integ_cake)
    self.one_d_graph.autoRange()
        # save 1D plot with detected peaks shown in the plot
    if QRange:
        titleAddStr = ', Q:' + str(QRange) + ', Chi:' + str(ChiRange)
    else: 
        titleAddStr = '.' 
    self.one_d_graph.setLabel("bottom", 'Q')
    self.one_d_graph.setLabel("left", "Intensity")
    title = "Column Average" + titleAddStr
    self.one_d_graph.setLabel("top", title)        
    # time.sleep(.2)
    QApplication.processEvents()

def save1dGraph(self, pathnames, processedPath, qArray, integ_cakeArray, ranges):
    #time.sleep(.2)
    imagename = pathnames[0]
    pathname = pathnames[1]
    #exporter = pyqtgraph.exporters.ImageExporter(self.one_d_graph.plotItem)
    #exporter.export(imagename, 'png') 
    if ranges[0]:
        titleAddStr = ', Q:' + str(ranges[0]) + ', Chi:' + str(ranges[1])
    else: 
        titleAddStr = '.' 
    title = "Column Average" + titleAddStr
    plt.figure(1)
    plt.title(title)
    plt.plot(qArray, integ_cakeArray)
    plt.xlabel('Q')
    plt.ylabel('Intensity')
    #plt.xlim((0.7, 6.4))

    plt.savefig(imagename)
    
    plt.close()
    
    txtfilename = os.path.join(processedPath, os.path.splitext(pathname)[0]+'_1D.csv') 
     
    with open(txtfilename, 'wb') as csvwriter:
        writer = csv.writer(csvwriter, delimiter=',')
        writer.writerow(['Q', 'Intensity'])
        index = 0
        while index < len(qArray):
            writer.writerow([qArray[index], integ_cakeArray[index]])
            index += 1
        
    
# Takes a CSV filename and displays the 1D image specified by the filename on the GUI.
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
                
        self.one_d_graph.clear()

        self.one_d_graph.plot(qArray, integrated_cake)
        self.one_d_graph.autoRange()
        self.one_d_graph.setLabel("bottom", "Q")
        try:
            qrange = (float(str(self.q_min.text())), float(str(self.q_max.text())))
            chirange = (float(str(self.chi_min.text())), float(str(self.chi_max.text())))
        except:
            qrange = None
            pass

        if qrange != None:
            title = 'Column Average, Q:' + str(qrange) + ', Chi:' + str(chirange)
        else: 
            title = '.' 
        self.one_d_graph.setLabel("bottom", 'Q')
        self.one_d_graph.setLabel("top", title)
        self.one_d_graph.setLabel("left", "Intensity")
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
    
    h_box7 = QHBoxLayout()
    h_box7.addWidget(self.int_processed_location)
    h_box7.addWidget(self.int_processed_location_folder_button)
    h_box7.addStretch()
    layout.addWidget(self.int_processed_location_label)
    layout.addLayout(h_box7)
    h = QHBoxLayout()
    h.addWidget(self.int_start_button)
    h.addWidget(self.int_abort)
    h.addWidget(self.integrate_saveMacroButton)
    h.addWidget(self.integrate_addToQueueButton)
    h.addStretch()
    layout.addLayout(h)
    layout.addWidget(self.miconsole)
    return layout

# Begins integration processing, parsing the relevant fields, making sure that the user has entered
# all fields correctly, and then loading and starting the IntegrateThread
def integrateThreadStart(self):



    if not self.int_data_source_check.isChecked() and os.path.isdir(self.i_files_to_process[0]):
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
    
    dataPath = str(self.int_data_source.text())
    if  os.path.isdir(dataPath) and self.int_data_source_check.isChecked():
        self.i_files_to_process = [dataPath]        
        
    self.addToConsole('Folder to process: ' + dataPath)
    self.addToConsole('')        
    self.QRange = (float(str(self.q_min.text())), float(str(self.q_max.text())))
    self.ChiRange = (float(str(self.chi_min.text())), float(str(self.chi_max.text())))    
    if abs(self.QRange[1]-self.QRange[0]) < .01:
        self.addToConsole("Please select a Q range.")
        self.enableWidgets()
        return
    if abs(self.ChiRange[1] - self.ChiRange[0]) < 0.1:
        self.addToConsole("Please select a more reasonable Chi range.")
        self.enableWidgets()
        return        
    

    self.integrateThread = IntegrateThread(self, str(self.int_processed_location.text()), self.i_files_to_process, (self.QRange, self.ChiRange), 0)
    self.integrateThread.setAbortFlag(False)
    self.int_abort.clicked.connect(self.integrateThread.abortClicked)
    
    self.connect(self.integrateThread, SIGNAL("addToConsole(PyQt_PyObject)"), self.addToConsole)
    self.connect(self.integrateThread, SIGNAL("enableWidgets()"), self.enableWidgets)
    #self.connect(self.integrateThread, SIGNAL("set1DImage(PyQt_PyObject, PyQt_PyObject)"), set1DImage)
    self.connect(self.integrateThread, SIGNAL("finished(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"), self.done)
    self.connect(self.integrateThread, SIGNAL("bar(int, PyQt_PyObject)"), self.setRadialBar)
    self.connect(self.integrateThread, SIGNAL("resetIntegrate(PyQt_PyObject)"), resetIntegrate)
    self.connect(self.integrateThread, SIGNAL("incrementBar(PyQt_PyObject)"), self.incrementBar)
    self.connect(self.integrateThread, SIGNAL("plot1dGraph(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"), plot1dGraph)
    self.connect(self.integrateThread, SIGNAL("save1dGraph(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject, PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"), save1dGraph)
    self.disableWidgets()
    self.integrateThread.start()
    
# Compiles the information on the current integrate tab page into a macro and adds it to the queue
def addIntegrateCurrentToQueue(self):
    cur_time = datetime.datetime.now().strftime('%Y-%m-%d--%H-%M-%S')
    name = ('/Users/arunshriram/Documents/SLAC Internship/monhitp-gui/macros/stitch-macro-%s') %(cur_time)
    self.addToConsole("Saving this page in directory \"macros\" as \"stitch-macro-%s\" and adding to the queue..." % (cur_time))
    saved = saveIntegrateMacro(self, name)
    if saved is None:
        return    
    self.macroQueue.append( self.editor.curMacro )       
   
    macro = QListWidgetItem("Process %s: Added macro \"%s\"" % (mq.curIndex, os.path.basename(str(self.editor.curMacro.getFilename()))))
    mq.curIndex+= 1 
    self.queue.addItem(macro)
    self.editor.close()
    QApplication.processEvents()
    self.addToConsole("Macro saved and added to queue!")


# Adds functionality to the integrate page "save macro" button; takes all the information currently
# on the integrate page and compiles it into a macro to be loaded into the queue
def saveIntegrateMacro(self, fileName=''):
    # CHECKING VALUES TO MAKE SURE EVERYTHING IS OKAY BEFORE MACRO CAN BE SAVED
    macrodict = {"workflow" : 'False'}
    macrodict["transform"] = 'False'
    macrodict["stitch"] = 'False'
    macrodict["integrate"] = 'True'
    try:
        if str(self.int_processed_location.text()) == "":
            self.int_processed_location.setText(os.path.join(str(self.int_data_source.text()), "Processed_Integrate"))

        if self.i_files_to_process == []:
            self.i_files_to_process = [str(self.int_data_source.text())]
            i_filenames = self.i_files_to_process
        else:
            i_filenames = self.i_files_to_process    

        data_source = str(self.int_data_source.text())
        if self.int_data_source_check.isChecked() and os.path.isfile(self.i_files_to_process[0]):
            displayError(self, "Please either check the \"I'm going to select a folder\" option or select at least one file.")
            return
        elif not self.int_data_source_check.isChecked() and os.path.isdir(self.i_files_to_process[0]):
            displayError(self, "Please either check the \"I'm going to select a folder\" option or select at least one file.")
            return
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
        values = (i_filenames, i_proc_dir)
        macrodict["i_data_source"] = values[0]
        macrodict["i_proc_dir"] = values[1]
    except:
        traceback.print_exc()
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
        i_filenames = []    

    if os.path.isfile(self.i_files_to_process[0]):
        i_filenames += self.i_files_to_process
    elif os.path.isdir(self.i_files_to_process[0]):
        i_filenames = [str(self.int_data_source.text())]
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
            
    self.editor.curMacro = mq.Macro(fileName, macrodict)
    self.addToConsole("Macro saved successfully!")
    return 1
        
def getIntDataSourceDirectoryPath(self):
    if self.int_data_source_check.isChecked():
        try:
            folderpath = str(QFileDialog.getExistingDirectory())
            if folderpath != '':
                self.int_data_source.setText(folderpath)
                self.int_data_label.setText("Current data source:")
                self.int_processed_location.setText(os.path.join(folderpath, "Processed_Integrate"))
                self.i_files_to_process = [folderpath]
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
            self.i_files_to_process = filenames
        except:
            #traceback.print_exc()
            self.addToConsole("Something went wrong when trying to select your files.")
    
    


def setIntProcessedLocation(self):
    path = str(QFileDialog.getExistingDirectory(self, "Select a location for processed files", str(self.int_data_source.text())))
    if path !='':
        self.int_processed_location.setText(os.path.join(path, "Processed_Integrate"))
def resetIntegrate(self):
    set1DImage(self, "images/SLAC_LogoSD.png")
    self.int_bar.setValue(0)
    
    
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