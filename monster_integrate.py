# This file initializes the widgets, layouts, and various functions necessary to run
# the "integrate" tab in MONster.
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
from QRoundProgressBar import QRoundProgressBar # the progress bar on the integrate tab
from PyQt4.QtGui import * # for the GUI
from PyQt4.QtCore import * # for the GUI
from ClickableLineEdit import * # for all the line edit fields
import os, datetime 
import matplotlib  # to graph the integrate data 
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from IntegrateThread import * # to interface with the integrate processing
import pyqtgraph as pg # to graph the integrate data
import csv # to save integrate data
import numpy as np # to graph and save integrate data
import monster_queueloader as mq # to consolidate all the information on the integrate tab as a macro

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
            

# None -> None
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
    self.miconsole.setMaximumHeight(400)
    self.miconsole.moveCursor(QTextCursor.End)

    self.int_folder_button = QPushButton("Select a folder")
    self.int_folder_button.setFixedSize(self.int_folder_button.sizeHint().width(), self.int_folder_button.sizeHint().height())
    self.int_folder_button.setStyleSheet("background-color: rgb(159, 97, 100); color: black;")
    
    self.int_file_button = QPushButton("Select one or more files")
    self.int_file_button.setFixedSize(self.int_file_button.sizeHint().width(), self.int_file_button.sizeHint().height())
    self.int_file_button.setStyleSheet("background-color: rgb(248, 222, 189); color: black;")
    
    self.miconsole.setFont(QFont("Avenir", 14))
    self.miconsole.setStyleSheet("margin:3px; border:1px solid rgb(0, 0, 0); background-color: rgb(240, 255, 240); color: black;")               
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
    self.int_start_button.setStyleSheet("background-color: rgb(80, 230, 133); color: black;")    
    # self.int_start_button.setFixedSize(160, 30)
    self.int_start_button.resize(self.int_start_button.sizeHint().width(), self.int_start_button.sizeHint().height())

    self.int_abort = QPushButton('Abort Integration')
    self.int_abort.setStyleSheet("background-color: rgb(255, 140, 140); color: black;")              
    # self.int_abort.setFixedSize(150, 30)
    self.int_abort.resize(self.int_abort.sizeHint().width(), self.int_abort.sizeHint().height())

    
    self.int_data_label = QLabel("Current data source:")
    self.int_data_label.setStyleSheet(self.textStyleSheet)
    self.int_data_source = ClickableLineEdit()
    self.int_data_source.setStyleSheet(self.lineEditStyleSheet)
    
    self.int_data_source.setFixedWidth(580)
    self.int_data_folder = QLabel()
    self.int_data_folder.setFixedSize(25, 25)    
    self.int_data_folder.setPixmap(QPixmap('images/folder_select.png').scaled(self.int_data_folder.sizeHint().width(), self.int_data_folder.sizeHint().height()))
    self.int_data_folder.setStyleSheet('border: none;')
    self.int_data_label.setText("Current data source: (folder)")
    
    
    self.int_processed_location_label = QLabel("Destination for processed files:")
    self.int_processed_location_label.setStyleSheet(self.textStyleSheet)
    self.int_processed_location = ClickableLineEdit(str(self.int_data_source.text()).lstrip().rstrip()  + "/Processed_Integrate")
    self.int_processed_location.setStyleSheet(self.lineEditStyleSheet)
    
    self.int_processed_location.setFixedWidth(580)
    self.int_processed_location_folder_button = QPushButton()
    self.int_processed_location_folder_button.setIcon(QIcon('images/folder_select.png'))
    self.int_processed_location_folder_button.setIconSize(QSize(25, 25))
    self.int_processed_location_folder_button.setFixedSize(35, 35)
    self.int_processed_location_folder_button.setStyleSheet('background-color: rgba(34, 200, 157, 100)');     
          
    
    
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
    self.integrate_saveMacroButton.setStyleSheet("background-color: rgb(255, 251, 208); color: black;")
    self.integrate_saveMacroButton.resize(self.integrate_saveMacroButton.sizeHint().width(), self.integrate_saveMacroButton.sizeHint().height())

    self.integrate_addToQueueButton = QPushButton("Add this configuration to the queue")
    # self.integrate_addToQueueButton.setMaximumWidth(220)
    # self.integrate_addToQueueButton.setFixedHeight(30)
    self.integrate_addToQueueButton.setStyleSheet("background-color: rgb(255, 207, 117); color: black;")  
    self.integrate_addToQueueButton.resize(self.integrate_addToQueueButton.sizeHint().width(), self.integrate_addToQueueButton.sizeHint().height())

    
# ndarray ndarray tuple tuple -> None
# Takes the specified q array, the integrated cake array and the q range and chi range to plot with pyqtgraph
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

# tuple string ndarray ndarray tuple -> None
# Takes a tuple of the image path name and the base image name, the save path, q array, integrated cake 
# array, and q and chi ranges to save the integrated graph as a numpy image
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

    plt.savefig(imagename, dpi=300)
    
    plt.close()
    path = os.path.join(processedPath, "Integrated_CSVs")
    if not os.path.exists(path):
        os.makedirs(path)
    txtfilename = os.path.join(os.path.join(processedPath, "Integrated_CSVs"), os.path.splitext(pathname)[0]+'_1D.csv') 
     
    with open(txtfilename, 'wb') as csvwriter:
        writer = csv.writer(csvwriter, delimiter=',')
        writer.writerow(['Q', 'Intensity'])
        index = 0
        while index < len(qArray):
            writer.writerow([qArray[index], integ_cakeArray[index]])
            index += 1
        
# string -> None
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
        self.addToConsole("Could not load integrated graph.")
        
# None -> QVBoxLayout
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
    h_box2.addWidget(self.int_data_folder)
    h_box2.addWidget(self.int_folder_button)
    h_box2.addWidget(self.int_file_button)
    h_box2.addStretch()
    layout.addWidget(self.int_data_label)
    x = QLabel("Data source directory:")
    x.setStyleSheet("color: white;")
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setStyleSheet("color: white;")
    layout.addWidget(line)
    layout.addWidget(x)
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

# None -> None
# Begins integration processing, parsing the relevant fields, making sure that the user has entered
# all fields correctly, and then loading and starting the IntegrateThread
def integrateThreadStart(self):

    if self.transformThread.isRunning() or self.stitchThread.isRunning():
        self.addToConsole("Stop! You're giving me too much to do! Cannot run multiple processes at once.")
        return

    #if not self.int_data_source_check.isChecked() and os.path.isdir(self.i_files_to_process[0]):
        #self.addToConsole("Please make sure you select the files you wish to process, or check the \"I'm going to select a folder\" box.")
        #self.enableWidgets()
        #return
    if self.i_files_to_process == []:
        self.i_files_to_process = [str(self.int_data_source.text()).lstrip().rstrip()]
        self.int_data_label.setText("Current data source: (folder)")
    self.miconsole.moveCursor(QTextCursor.End)
    QApplication.processEvents()
    self.console.clear()
    self.addToConsole('********************************************************')
    self.addToConsole('********** Beginning Integrate Processing... ***********')
    self.addToConsole('********************************************************')
    save_path = str(self.int_processed_location.text())
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
    
    QApplication.processEvents()
    # checking q an chi range values to see if they're appropriate
    try:
        q1 = float(str(self.q_min.text()))
        q2 = float(str(self.q_max.text()))
        c1 = float(str(self.chi_min.text()))
        
        c2 = float(str(self.chi_max.text()))
    except:
        self.addToConsole("Please make sure you have entered appropriate values for the QRange and the ChiRange.")
        self.enableWidgets()
        return
    
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

    dataPath = str(self.int_data_source.text()).lstrip().rstrip()
    if  os.path.isdir(dataPath):
        self.i_files_to_process = [dataPath]        
        
    self.addToConsole('Folder to process: ' + dataPath)
    self.addToConsole('')        
  

    # initialize integrate thread
    

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
    
# None -> None
# Compiles the information on the current integrate tab page into a macro and adds it to the queue
def addIntegrateCurrentToQueue(self):
    cur_time = datetime.datetime.now().strftime('%Y-%m-%d--%H-%M-%S')
    name = (os.path.join(self.mPath, '/stitch-macro-%s' %(cur_time)))
    self.addToConsole("Saving this page in directory \"~/macros\" as \"stitch-macro-%s\" and adding to the queue..." % (cur_time))
    saved = saveIntegrateMacro(self, name)
    if saved is None:
        return    
    self.macroQueue.append( self.editor.curMacro )       
   
    macro = QListWidgetItem("Process %s: Added macro \"%s\"" % (mq.curIndex, os.path.basename(str(self.editor.curMacro.getFilename()))))
    mq.curIndex+= 1 
    self.queue.addItem(macro)
    self.editor.close()
    self.raise_()
    QApplication.processEvents()
    self.addToConsole("Macro saved and added to queue!")

# string  -> int
# Adds functionality to the integrate page "save macro" button; takes all the information currently
# on the integrate page and compiles it into a macro to be loaded into the queue. Returns an int if successfully saved.
def saveIntegrateMacro(self, fileName=''):
    # CHECKING VALUES TO MAKE SURE EVERYTHING IS OKAY BEFORE MACRO CAN BE SAVED
    macrodict = {"workflow" : 'False'}
    macrodict["transform"] = 'False'
    macrodict["stitch"] = 'False'
    macrodict["integrate"] = 'True'
    macrodict['transform_integrate'] = 'False'
    try:
        if str(self.int_processed_location.text()) == "":
            self.int_processed_location.setText(os.path.join(str(self.int_data_source.text()).lstrip().rstrip(), "Processed_Integrate"))

        if self.i_files_to_process == []:
            self.i_files_to_process = [str(self.int_data_source.text()).lstrip().rstrip()]
            i_filenames = self.i_files_to_process
        else:
            i_filenames = self.i_files_to_process    

        data_source = str(self.int_data_source.text()).lstrip().rstrip()
        #if self.int_data_source_check.isChecked() and os.path.isfile(self.i_files_to_process[0]):
            #displayError(self, "Please either check the \"I'm going to select a folder\" option or select at least one file.")
            #return
        #elif not self.int_data_source_check.isChecked() and os.path.isdir(self.i_files_to_process[0]):
            #displayError(self, "Please either check the \"I'm going to select a folder\" option or select at least one file.")
            #return
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
            
    self.editor.curMacro = mq.Macro(fileName, macrodict)
    self.addToConsole("Macro saved successfully!")
    return 1
        
# Loads the appropriate files based on the data source the user selects
def getIntDataSourceDirectoryPath(self):
    try:
        folderpath = str(QFileDialog.getExistingDirectory(self, 'Choose your data', self.home))
        if folderpath != '':
            self.int_data_source.setText(folderpath)
            self.int_data_label.setText("Current data source: (folder)")
            self.int_processed_location.setText(str(self.int_data_source.text())  + "/Processed_Integrate")
            self.i_files_to_process = [folderpath]
        self.raise_()
    except:
        self.addToConsole("Something went wrong when trying to open your directory.")
 
 # Loads the appropriate files based on the data source the user selects
def getIntDataFiles(self):
    try:
        filenames = QFileDialog.getOpenFileNames(self, "Select the files you wish to use.", self.home)
        filenames = [str(filename) for  filename in filenames]
        if len(filenames) < 2:
            self.int_data_label.setText("Current data source: %s" % os.path.basename(filenames[0]))
        else:
            self.int_data_label.setText("Current data source: (multiple files)")
        print(filenames)
        self.int_data_source.setText(os.path.dirname(filenames[0]))
        self.int_processed_location.setText(str(self.data_source.text())  + "/Processed_Transform")
        self.i_files_to_process = filenames
        self.raise_()
    except:
        #traceback.print_exc()
        self.addToConsole("Did not select a data source.")
    
    

# None -> None
# Sets the processed location path for integration
def setIntProcessedLocation(self):
    path = str(QFileDialog.getExistingDirectory(self, "Select a location for processed files", str(self.int_data_source.text()).lstrip().rstrip()))
    if path.endswith('/untitled'):
        path = path[:len(path) - 9]    
    if path !='':
        self.int_processed_location.setText(os.path.join(path, "Processed_Integrate"))
    self.raise_()
# None -> None
# Resets the integrate graph
def resetIntegrate(self):
    self.one_d_graph.clear()
    self.int_bar.setValue(0)
    
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