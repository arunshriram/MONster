# This file defines the main scientific functions behind one dimensional integration
# as well as peak fitting. Its main element is the class IntegrateThread, a thread that
# runs parallel to the GUI.
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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pyFAI, shutil
from PIL import Image
from pyqtgraph import *
import numpy as np
import scipy.io
import scipy
from image_loader import load_image
import time, glob, os, re, random
from saveDimRedPack import save_1Dplot, save_1Dcsv, save_texture_plot_csv
from extDimRedPack import ext_max_ave_intens, ext_peak_num, ext_text_extent, ext_SNR
import traceback
from reportFn import addFeatsToMaster
from add_feature_to_master import add_feature_to_master
import monster_integrate as mi
# The class that defines a thread that runs the integration processing 
class IntegrateThread(QThread):
    def __init__(self, windowreference, calibPath, processedpath, detectordata, files_to_process, ranges):
        QThread.__init__(self)
        self.files_to_process = files_to_process
        self.calibPath = calibPath
        self.detectorData = detectordata
        self.ranges = ranges
        self.abort_flag = False
        self.PP = 0.95           
        self.windowreference = windowreference
        self.processedPath = processedpath

        if ranges != None:
            self.QRange = (float(ranges[0][0]), float(ranges[0][1]))
            self.ChiRange = (float(ranges[1][0]), float(ranges[1][1]))
        try:
            if os.path.isdir(files_to_process[0]):
                self.dataPath = files_to_process[0]
            else:   
                self.dataPath = os.path.dirname(files_to_process[0])
        except TypeError: # Nonetype error happens when initializing transform thread with Nones
            pass    
        
    def setAbortFlag(self, boo):
        self.abort_flag = boo
        
    def stop(self):
        self.terminate()        
    
    # Begins the integration, assuming that all the relevant calibration and data information
    # has been correctly passed into IntegrateThread's __init__
    def beginIntegration(self):
        QApplication.processEvents()
        ##########################################Extension chooser?...
        if os.path.isdir(self.files_to_process[0]):
            fileList = sorted(glob.glob(os.path.join(self.dataPath.rstrip(), '*.mat')))
            if len(fileList) == 0:
                self.emit(SIGNAL("addToConsole(PyQt_PyObject)"), "No .mat files found in specified source directory!")
                self.emit(SIGNAL("enableWidgets()"))
                return  
           
            files = fileList[0:10000000000000000]
        else:
            files = self.files_to_process
        loopTime = []
        stage1Time = []
        stage2Time = []
        increment = (1/float(len(files)))*100
        progress = 0
        self.emit(SIGNAL("resetIntegrate(PyQt_PyObject)"), self.windowreference)
        # generate a folder to put processed files
        save_path = self.processedPath
        if os.path.exists(save_path):
            shutil.rmtree(save_path)    
        
        os.makedirs(save_path)
        for filePath in files:
            filePath = filePath.rstrip()
            QApplication.processEvents()
            if (self.abort_flag):
                writeIntegrateProperties()
                self.emit(SIGNAL("enableWidgets()"))                
                break
            filename = os.path.basename(filePath)
        
               
            start = time.time()
            
            self.emit(SIGNAL("addToConsole(PyQt_PyObject)"), '{0}'.format(filePath))
            self.emit(SIGNAL("addToConsole(PyQt_PyObject)"), filename + ' detected, processing')
            QApplication.processEvents()
            ########## Begin data reduction scripts ###########################
            self.beginReduction(filePath) #QRange=QRange, ChiRange=ChiRange)
            stage1int = time.time()
           
        
            
            QApplication.processEvents()
                       #peakFitBBA(filePath, config)
            stage2int = time.time()
            ########## Visualization #########################################
            # Pulling info from master CSV
            #FWHMmap(filePath)
            #contrastMap(filePath, hiLimit)
        
            self.emit(SIGNAL("addToConsole(PyQt_PyObject)"), filename + " completed")
            QApplication.processEvents()
            end = time.time()
            loopTime += [(end-start)]
            stage1Time += [(stage1int - start)]
            stage2Time += [(stage2int - stage1int)]
        
    
            save_path = os.path.join(os.path.dirname(filePath), 'Processed_Integrate')
            imageFilename = os.path.basename(filePath.rsplit('.', 1)[0])
            with open("thisRun.txt", 'w') as runFile:
                runFile.write("i_data_source = \"" + str(self.dataPath)+'\"\n')
                runFile.write("i_calib_source = \"" + str(self.calibPath)+'\"\n')
                runFile.write("i_processed_loc = \"" + str(self.processedPath) + '\"\n')
                name = os.path.join(save_path, os.path.splitext(imageFilename)[0]+'_1D.png')                
                self.emit(SIGNAL("set1DImage(PyQt_PyObject, PyQt_PyObject)"), self.windowreference, name)
                runFile.write("one_d_image = \"" + name + '\"\n')
                QApplication.processEvents()
                runFile.write("qmin = \"" + str(self.QRange[0])+'\"\n')
                runFile.write("qmax = \"" + str(self.QRange[1])+'\"\n')
                runFile.write("chimin = \"" + str(self.ChiRange[0])+'\"\n')
                runFile.write("chimax = \"" + str(self.ChiRange[1]) + "\"\n")
            progress += increment
           
            self.emit(SIGNAL("bar(int, PyQt_PyObject)"), 1, progress)
        writeIntegrateProperties()
        self.emit(SIGNAL("finished(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"), loopTime, stage1Time, stage2Time)
        #self.stop()

        
    # Plots and displays the one dimensional graph by using the calibration data to calculate the graph's shape
    def beginReduction(self, pathname):
        '''
        Processing script, reducing images to 1D plots (Q-Chi, Texture, etc)
        '''
        print('\n')
        print('******************************************** Begin image reduction...')
      
        ###### BEGIN PROCESSING IMAGE####################################################
        # import image and convert it into an array
        new_pathname = os.path.splitext(pathname)[0]
        self.imArray = scipy.io.loadmat(new_pathname)
        cakeArray = self.imArray['cake']
        qArray = self.imArray['Q']
        chiArray = self.imArray['chi']
        cakeArray[cakeArray == 0] = np.nan
        chimin = int(self.ChiRange[0])
        chimax = int(self.ChiRange[1])
        qmin = int(self.QRange[0])
        qmax = int(self.QRange[1])
        #chiindexlist = []
        #i = 0
        #for val in chiArray.flatten().tolist():
            #if val >= chimin and val <= chimax:
                #chiindexlist.append(i)
            #i += 1
        #qindexlist = []
        #i = 0
        #for val in qArray.flatten().tolist():
            #if val >= qmin and val <= qmax:
                #qindexlist.append(i)
            #i += 1
        

        #chiminind = min(chiindexlist)
        #chimaxind = max(chiindexlist)
        #qminind = min(qindexlist)
        #qmaxind = max(qindexlist)
        #to_int = cakeArray[qminind:qmaxind][chiminind:chimaxind]
        #integrated_cake = np.nanmean(to_int ,  axis=0)
        integrated_cake = np.nanmean(cakeArray ,  axis=0)
        self.windowreference.one_d_graph.clear()
        
        self.windowreference.one_d_graph.plot(qArray.flatten(), integrated_cake)
        self.windowreference.one_d_graph.autoRange()
        mi.centerButtonClicked(self.windowreference)
        time.sleep(.2)
        QApplication.processEvents()
        p = QPixmap.grabWindow(self.windowreference.one_d_graph.winId())
        imageFilename = os.path.basename(pathname.rsplit('.', 1)[0])
        filename = os.path.join(self.processedPath, os.path.splitext(imageFilename)[0]+'_1D.png') 
        p.save(filename, 'png')                 
        # data_reduction to generate 1D spectra, Q
        #Qlist, IntAve = self.data_reduction(d, Rot, tilt, lamda, x0, y0, pixelSize)


        ###### SAVE PLOTS ###############################################################
        # save 1D spectra as a *.csv
        #save_1Dcsv(Qlist, IntAve, fileRoot, save_path)


        # save 1D plot with detected peaks shown in the plot
        if self.QRange:
            titleAddStr = ', Q:' + str(self.QRange) + ', Chi:' + str(self.ChiRange)
        else: 
            titleAddStr = '.' 
        #save_1Dplot(Qlist, IntAve, peaks, fileRoot, save_path, 
                        #titleAdd=titleAddStr)

    
    # Defines what should be done when the user aborts the current integration.
    def abortClicked(self):
        try:
            if self.isRunning():
                self.emit(SIGNAL("addToConsole(PyQt_PyObject)"), "Process aborted! Completing any processes that were already started...")                
                self.abort_flag = True
                QApplication.processEvents()
            else:
                self.emit(SIGNAL("addToConsole(PyQt_PyObject)"), "No process to abort!")
        except:
            self.emit(SIGNAL("addToConsole(PyQt_PyObject)"), "No process to abort!")
    
    def run(self):
        self.beginIntegration()
        
# Writes the latest transform run info into the Properties.py file
def writeIntegrateProperties():
    prop = open("Properties.py", 'r')
    properties = []
    for line in prop:
        properties.append(line)
    prop.close()
    with open("thisRun.txt", 'r') as thisrun:
        properties[2] = thisrun.readline()
        properties[4] = thisrun.readline()
        properties[7] = thisrun.readline()
        properties[10] = thisrun.readline()
        properties[11] = thisrun.readline()
        properties[12] = thisrun.readline()
        properties[13] = thisrun.readline()
        properties[14] = thisrun.readline()
    propw = open("Properties.py", 'w')
    for prawperty in properties:
        propw.write(prawperty)
    propw.close()
