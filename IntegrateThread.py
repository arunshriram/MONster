# This file defines the main scientific functions behind one dimensional integration
# as well as peak fitting. Its main element is the class IntegrateThread, a thread that
# runs parallel to the GUI.
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
import pyFAI, shutil
from pyqtgraph import *
import numpy as np
import scipy.io
import scipy
from image_loader import load_image
import time, glob, os, re, random
from saveDimRedPack import save_1Dplot, save_1Dcsv, save_texture_plot_csv
from extDimRedPack import ext_max_ave_intens, ext_peak_num, ext_text_extent, ext_SNR
import traceback, csv
from reportFn import addFeatsToMaster
from add_feature_to_master import add_feature_to_master
import monster_integrate as mi
import pyqtgraph.exporters
# The class that defines a thread that runs the integration processing 
class IntegrateThread(QThread):
    def __init__(self, windowreference, processedpath, files_to_process, ranges, increment):
        QThread.__init__(self)
        self.home = os.path.expanduser("~")
        self.bkPath = os.path.join(self.home, "MONster_Bookkeeping")
        self.pPath = os.path.join(self.bkPath, "Properties.csv")
        self.tPath = os.path.join(self.bkPath, "thisRun.txt")
        self.mPath = os.path.join(self.home, "macros")
        self.files_to_process = files_to_process
        self.ranges = ranges
        self.abort_flag = False
        self.PP = 0.95           
        self.windowreference = windowreference
        self.processedPath = processedpath
        self.increment = increment

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
            files = [x for x in self.files_to_process if x.endswith('.mat')]


        loopTime = []
        stage1Time = []
        stage2Time = []
        mode = 1
        if self.increment != 0:
            increment = self.increment
            mode = 3
        else:

            increment = (1/float(len(files)))*100
        progress = 0
        self.emit(SIGNAL("resetIntegrate(PyQt_PyObject)"), self.windowreference)
        # generate a folder to put processed files
        save_path = self.processedPath
        if os.path.exists(save_path):
            shutil.rmtree(save_path)    
        
        os.mkdir(save_path)
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
        
    
            save_path = str(self.processedPath)
            imageFilename = os.path.basename(filePath.rsplit('.', 1)[0])
            with open(self.tPath, 'w') as runFile:
                runFile.write("i_data_source, " + str(self.dataPath)+'\n')
                runFile.write("i_processed_loc, " + str(self.processedPath) + '\n')
                name = os.path.join(os.path.join(save_path, "Integrated_CSVs"), os.path.splitext(imageFilename)[0]+'_1D.csv')                
                self.emit(SIGNAL("set1DImage(PyQt_PyObject, PyQt_PyObject)"), self.windowreference, name)
                runFile.write("one_d_image, " + name + '\n')
                QApplication.processEvents()
                runFile.write("qmin, " + str(self.QRange[0])+'\n')
                runFile.write("qmax, " + str(self.QRange[1])+'\n')
                runFile.write("chimin, " + str(self.ChiRange[0])+'\n')
                runFile.write("chimax, " + str(self.ChiRange[1]) + "\n")
            progress += increment
           
            if self.increment != 0:
                self.emit(SIGNAL("bar(int, PyQt_PyObject)"), mode, increment)
            else:
                self.emit(SIGNAL("bar(int, PyQt_PyObject)"), mode, progress)
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
        imArray = scipy.io.loadmat(new_pathname)
        cakeArray = imArray['cake']
        qArray = imArray['Q'][0]
        chiArray = imArray['chi'][0]
        nanCakeArray = cakeArray.copy()
        nanCakeArray[nanCakeArray == 0] = np.nan
        chimin = int(self.ChiRange[0])
        chimax = int(self.ChiRange[1])
        qmin = int(self.QRange[0])
        qmax = int(self.QRange[1])
      
        qmin_ind = min(range(len(qArray)), key=lambda i: abs(qArray[i]-qmin))
        qmax_ind = min(range(len(qArray)), key=lambda i: abs(qArray[i]-qmax))
        chimin_ind = min(range(len(chiArray)), key=lambda i: abs(chiArray[i]-(chiArray.mean()+chimin)))
        chimax_ind = min(range(len(chiArray)), key=lambda i: abs(chiArray[i]-(chiArray.mean()+chimax)))
        integrated_cake = np.nanmean(cakeArray ,  axis=0)

        to_int = nanCakeArray[chimin_ind:chimax_ind, qmin_ind:qmax_ind]
        integrated_cake = np.nanmean(cakeArray,  axis=0)
        nan_integ_cake = np.nanmean(nanCakeArray, axis=0)
        masked_integ_cake = np.nanmean(to_int, axis=0)
        imageFilename = os.path.basename(pathname.rsplit('.', 1)[0])
        if not os.path.exists(os.path.join(self.processedPath, "Integrated_Images")):
            os.makedirs(os.path.join(self.processedPath, "Integrated_Images"))  
        filename = os.path.join(os.path.join(self.processedPath, "Integrated_Images"), os.path.splitext(imageFilename)[0]+'_1D.png') 
        self.emit(SIGNAL("plot1dGraph(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"), self.windowreference, qArray[qmin_ind: qmax_ind], masked_integ_cake, self.QRange, self.ChiRange)
        time.sleep(.3)
        self.emit(SIGNAL("save1dGraph(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject, PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"), self.windowreference, (filename, imageFilename), self.processedPath, qArray[qmin_ind: qmax_ind], masked_integ_cake, (self.QRange, self.ChiRange))


        # data_reduction to generate 1D spectra, Q
        #Qlist, IntAve = self.data_reduction(d, Rot, tilt, lamda, x0, y0, pixelSize)



     

    
    # Defines what should be done when the user aborts the current integration.
    def abortClicked(self):
        self.emit(SIGNAL("enableWidgets()"))

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
        
# Writes the latest transform run info into the Properties.csv file
def writeIntegrateProperties():
    try:
        properties = []
        home = os.path.expanduser("~")
        bkPath = os.path.join(home, "MONster_Bookkeeping")
        pPath = os.path.join(bkPath, "Properties.csv")
        tPath = os.path.join(bkPath, "thisRun.txt")
        mPath = os.path.join(home, "macros")
        with open(pPath, 'rb') as prop:
                reader = csv.reader(prop)
                Properties = dict(reader)
        detectors = Properties["detectors"]

        with open(tPath, 'r') as thisrun:
            properties.append(thisrun.readline().split(", ")[1].rstrip())
            properties.append(thisrun.readline().split(", ")[1].rstrip())
            properties.append(thisrun.readline().split(", ")[1].rstrip())
            properties.append(thisrun.readline().split(", ")[1].rstrip())
            properties.append(thisrun.readline().split(", ")[1].rstrip())
            properties.append(thisrun.readline().split(", ")[1].rstrip())
            properties.append(thisrun.readline().split(", ")[1].rstrip())

     
        property_dict = {"i_data_source": properties[0], "i_processed_loc" : properties[1], "one_d_image" : properties[2], "qmin" : properties[3], "qmax" : properties[4], "chimin" : properties[5], "chimax" : properties[6]}
        if Properties.get("t_data_source") is None:
            property_dict["t_data_source"] = ""
        else:
            property_dict["t_data_source"] = Properties["t_data_source"]
        if Properties.get("t_processed_loc") is None:
            property_dict["t_processed_loc"] = ""
        else:
            property_dict["t_processed_loc"] = Properties["t_processed_loc"]
        if Properties.get("t_calib_source") is None:
            property_dict["t_calib_source"] = ""
        else:
            property_dict["t_calib_source"] = Properties["t_calib_source"]
        if Properties.get("two_d_image") is None:
            property_dict["two_d_image"] = ""
        else:
            property_dict["two_d_image"] = Properties["two_d_image"]
        if Properties.get("s_processed_loc") is None:
            property_dict["s_processed_loc"] = ""
        else:
            property_dict["s_processed_loc"] = Properties["s_processed_loc"]
        if Properties.get("s_data_source") is None:
            property_dict["s_data_source"] = ""
        else:
            property_dict["s_data_source"] = Properties["s_data_source"]
        if Properties.get("stitch_image") is None:
            property_dict["stitch_image"] = ""
        else:
            property_dict["stitch_image"] = Properties["stitch_image"]
        if Properties.get("console_saving") is None:
            property_dict["console_saving"] = "True"
        else:
            property_dict["console_saving"] = Properties["console_saving"]
        property_dict["detectors"] = detectors

        with open(pPath, 'wb') as prop:
            writer = csv.writer(prop)
            for key, value in property_dict.items():
                writer.writerow([key, value])    
    except:
        return
