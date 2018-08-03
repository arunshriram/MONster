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
import pyFAI
from PIL import Image
import numpy as np
from scipy import signal
from image_loader import load_image
import time, glob, os, re, random
from saveDimRedPack import save_1Dplot, save_1Dcsv, save_texture_plot_csv
from extDimRedPack import ext_max_ave_intens, ext_peak_num, ext_text_extent, ext_SNR
import traceback
from reportFn import addFeatsToMaster
from add_feature_to_master import add_feature_to_master

# The class that defines a thread that runs the integration processing 
class IntegrateThread(QThread):
    def __init__(self, windowreference, dataPath, calibPath, processedpath, detectordata, files_to_process, ranges):
        QThread.__init__(self)
        self.files_to_process = files_to_process
        self.dataPath = dataPath
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
    
    def setAbortFlag(self, boo):
        self.abort_flag = boo
    
    # Begins the integration, assuming that all the relevant calibration and data information
    # has been correctly passed into IntegrateThread's __init__
    def beginIntegration(self):
        QApplication.processEvents()
        ##########################################Extension chooser?...
        if self.files_to_process == "folder":
            fileList = sorted(glob.glob(os.path.join(self.dataPath.rstrip(), '*.tif')))
            if len(fileList) == 0:
                self.emit(SIGNAL("addToConsole(PyQt_PyObject)"), "No files found in specified source directory!")
                return
           
            files = fileList[0:10000000000000000]
        else:
            files = self.files_to_process
        loopTime = []
        stage1Time = []
        stage2Time = []
        increment = (1/float(len(files)))*100
        progress = 0
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
        
    
            save_path = os.path.join(os.path.dirname(filePath), 'Processed')
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
        # PP: beam polarization, according to beamline setup. 
        # Contact beamline scientist for this number
        pixelSize = 79  # detector pixel size, measured in microns

        # pathname was imageFullName
        folder_path = os.path.dirname(pathname)
        filename = os.path.basename(pathname)
        # fileRoot was imageFilename
        fileRoot, ext = os.path.splitext(filename)
        index = re.match('.*?([0-9]+).[a-zA-Z]+$',filename).group(1)
        base_filename = re.match('(.*?)[0-9]+.[a-zA-Z]+$',filename).group(1) # name w/o ind

        # Master CSV path
        masterPath = os.path.join(folder_path,base_filename + 'master.csv')

        # generate a folder to put processed files
        save_path = os.path.join(self.processedPath, 'Processed')
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        # make master index (vestigial)
        master_index = str(int(random.random()*100000000))

        attDict = dict.fromkeys(['scanNo', 'SNR', 'textureSum', 'Imax',
                                     'Iave', 'I_ratio', 'numPeaks'])
       
        ###### BEGIN READING CALIB FILE #################################################
        # initializing params, transform the calibration parameters from WxDiff to Fit2D
        d_in_pixel = float(str(self.detectorData[0]))
        Rotation_angle = float(str(self.detectorData[1]))
        tilt_angle = float(str(self.detectorData[2]))
        lamda = float(str(self.detectorData[3]))
        x0 = float(str(self.detectorData[4]))
        y0 = float(str(self.detectorData[5]))
        #d_in_pixel, Rotation_angle, tilt_angle, lamda, x0, y0 = parse_calib(calibPath)
        Rot = (np.pi * 2 - Rotation_angle) / (2 * np.pi) * 360  # detector rotation
        tilt = tilt_angle / (2 * np.pi) * 360  # detector tilt  # wavelength
        d = d_in_pixel * pixelSize * 0.001  # measured in milimeters        

        ###### BEGIN PROCESSING IMAGE####################################################
        # import image and convert it into an array
        self.imArray = load_image(pathname)

        # data_reduction to generate 1D spectra, Q
        Qlist, IntAve = self.data_reduction(d, Rot, tilt, lamda, x0, y0, pixelSize)


        ###### SAVE PLOTS ###############################################################
        # save 1D spectra as a *.csv
        save_1Dcsv(Qlist, IntAve, fileRoot, save_path)

        ###### EXTRACT ATTRIBUTES #######################################################
        # extract composition information if the information is available
        # extract the number of peaks in 1D spectra as attribute3 by default
        newRow3, peaks = ext_peak_num(Qlist, IntAve, index)
        attDict['numPeaks'] = len(peaks)
        #attribute3.append(newRow3)
        #attributes = np.array(attribute3)

        # save 1D plot with detected peaks shown in the plot
        if self.QRange:
            titleAddStr = ', Q:' + str(self.QRange) + ', Chi:' + str(self.ChiRange)
        else: 
            titleAddStr = '.' 
        save_1Dplot(Qlist, IntAve, peaks, fileRoot, save_path, 
                        titleAdd=titleAddStr)

        if True: 
            # extract maximum/average intensity from 1D spectra as attribute1
            newRow1 = ext_max_ave_intens(IntAve, index)
            attDict['scanNo'], attDict['Imax'], attDict['Iave'], attDict['I_ratio'] = newRow1
            #attribute1.append(newRow1)
            #attributes = np.concatenate((attribute1, attributes), axis=1)

        #if True:
            ## save 1D texture spectra as a plot (*.png) and *.csv
            #Qlist_texture, texture = save_texture_plot_csv(Q, chi, cake, fileRoot, save_path)
            ## extract texture square sum from the 1D texture spectra as attribute2
            #newRow2 = ext_text_extent(Qlist_texture, texture, index)
            #attDict['textureSum'] = newRow2[1]
            ##attribute2.append(newRow2)
            ##attributes = np.concatenate((attribute2, attributes), axis=1)

        if False:
            # extract neighbor distances as attribute4
            newRow4 = nearst_neighbor_distance(index, Qlist, IntAve, 
                                                   folder_path, save_path, base_filename,num_of_smpls_per_row)
            #attribute4.append(newRow4)
            #attributes = np.concatenate((attribute4, attributes), axis=1)

        if True:
            # extract signal-to-noise ratio
            try:
                newRow5 = ext_SNR(index, IntAve)
            except:
                traceback.print_exc()
                self.emit(SIGNAL("addToConsole(PyQt_PyObject)"), "----------------ERROR: Optimal parameters not found.----------------")
                self.abort_flag = True
                return
            attDict['SNR'] = newRow5[1]
            #attribute5.append(newRow5)
            #attributes = np.concatenate((attribute5, attributes), axis=1)

        # add features (floats) to master metadata
        attDict['scanNo'] = int(index)
        addFeatsToMaster(attDict, masterPath)            
        
        # -*- coding: utf-8 -*-
        """
        Created on Mon Jun 13
        
        @author: fangren
        
        """
        
    # Uses pyFAI to integrate the tif file as a one dimensional plot
    def data_reduction(self, d, Rot, tilt, lamda, x0, y0, pixelsize):
        """
        The input is the raw file's name and calibration parameters
        return Q-chi (2D array) and a spectrum (1D array)
        """    
        s1 = int(self.imArray.shape[0])
        s2 = int(self.imArray.shape[1])
        self.imArray = signal.medfilt(self.imArray, kernel_size = 5)
    
        detector_mask = np.ones((s1,s2))*(self.imArray <= 0)
        p = pyFAI.AzimuthalIntegrator(wavelength=lamda)
    
        # refer to http://pythonhosted.org/pyFAI/api/pyFAI.html for pyFAI parameters
        p.setFit2D(d,x0,y0,tilt,Rot,pixelsize,pixelsize) 
    
        # the output unit for Q is angstrom-1.  Always integrate all in 2D
        cake,Q,chi = p.integrate2d(self.imArray,1000, 1000,
                                   #azimuth_range=azRange, radial_range=radRange,
                                mask = detector_mask, polarization_factor = self.PP)
    

    
        # create azimuthal range from chi values found in 2D integrate
        # modify ranges to fit with detector geometry
        centerChi = (np.max(chi) + np.min(chi)) / 2
        if (self.QRange is not None) and (self.ChiRange is not None): 
            azRange = (centerChi+self.ChiRange[0] ,centerChi + self.ChiRange[1] ) 
            radRange = tuple([y/10E8 for y in self.QRange])
            #azRange = tuple([x-Rot for x in self.ChiRange])
            #radRange = tuple([y/10E8 for y in self.QRange])
            print(azRange, radRange)
        else: 
            azRange, radRange = None, None
    
        Qlist, IntAve = p.integrate1d(self.imArray, 1000, 
                                      azimuth_range=azRange, radial_range=radRange,
                                mask = detector_mask, polarization_factor = self.PP)
    
        # the output unit for Q is angstrom-1
        Qlist = Qlist * 10e8
        
        return Qlist, IntAve

    
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
