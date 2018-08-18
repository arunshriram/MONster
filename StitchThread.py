# This file defines the main scientific functions behind transforming raw and .tif data
# into Q-Chi plots. Its main element is the class TransformThread, a thread that
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
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import numpy as np
import os, scipy, math, time, glob, shutil, csv
import scipy.io
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from skimage.transform import resize
###############################################################
okclicked = False
cancelclicked = False
# This class defines the TransformThread, the main processing thread to create and save q-chi plots
# based on the tif and raw files the user supplies.
class StitchThread(QThread):

    def __init__(self, windowreference, dataPath, savePath, increment):
        QThread.__init__(self)
        self.windowreference = windowreference
        self.dataPath = dataPath
        self.savePath = savePath
        self.increment = increment

    
    def setAbortFlag(self, boo):
        self.abort_flag = boo
        
    def getDataPath(self):
        return self.dataPath
    
    def setDataPath(self, dataPath):
        self.dataPath = dataPath
        
    def getSavePath(self):
        return self.savePath
    
    def setSavePath(self, savePath):
        self.savePath = savePath
    
    def stop(self):
        self.terminate()
        
    def __del__(self):
        self.wait()
        
    def abortClicked(self):
        self.emit(SIGNAL("enableWidgets()"))

        try:
            if self.isRunning():
                self.abort_flag = True
                QApplication.processEvents()
            else:
                self.emit(SIGNAL("addToConsole(PyQt_PyObject)"), "No process to abort!")
        except:
            self.emit(SIGNAL("addToConsole(PyQt_PyObject)"), "No process to abort!")
            
   
     
    # Begins stitching, assuming that all the relevant initial information
    # has been correctly passed into StitchThread's __init__
    def beginStitch(self):
        loopTime = []
        fileList = sorted(glob.glob(os.path.join(self.dataPath, '*.mat')))
        numFiles = len(fileList)
        mode = 2
        if self.increment != 0:
            increment = self.increment
            mode = 3
        else:

            increment = (1/(float(numFiles) + 1))*100
        progress = 0
        firstphi = 0
        numphi = 1
        dphi = 1
        rq = 250
        rchi = 5
        phis = [ [ None for c in range(numphi) ] for r in range(1) ]    
        for i in range(numphi):
            phival = firstphi + i * dphi
            if phival < 10:
                phis[i] = ['000', str(phival)]
            elif phival < 100:
                phis[i] = ['00', str(phival)]
            else:
                phis[i] = ['0', str(phival)]
    
        firstfile = fileList[0]
        try:
            data = scipy.io.loadmat(firstfile)
        except:
            self.emit(SIGNAL("addToConsole(PyQt_PyObject)"), "Error: Could not load the first scan file! Try checking your scan indices.")

            return
        Q1 = data['Q']
        chi1 = data['chi']
        minq = np.ndarray.min(Q1)
        minchi = np.ndarray.min(chi1)
        maxchi = np.ndarray.max(chi1)
        lastfile = fileList[numFiles - 1]
        data2 = scipy.io.loadmat(lastfile)
        Q2 = data2['Q']
        maxq = np.ndarray.max(Q2)
        lq0int = int(math.ceil(rq * (maxq - minq)))
        lchi0int = int(math.ceil(rchi * (maxchi - minchi)))
        dQ0 = float(1) / rq
        Q0min = round(rq * minq) / rq
        Q0max = Q0min + (lq0int - 1) * dQ0
        Q0 = np.arange(Q0min, Q0max + dQ0, dQ0)
        dchi0 = float(1) / rchi
        chi0min = round(rchi * minchi) / rchi
        chi0max = chi0min + (lchi0int - 1) * dchi0
        chi0 = np.arange(chi0min, chi0max + dchi0, dchi0)
        Qchi0_allphi = np.zeros((lchi0int, lq0int))
        Qchi0log_allphi = np.zeros((lchi0int, lq0int))
        if self.increment == 0:
            self.emit(SIGNAL("resetStitch(PyQt_PyObject)"), self.windowreference)
        save_path = self.savePath
        if os.path.exists(save_path):
            shutil.rmtree(save_path)    
        
        os.makedirs(save_path)
          
        for p in range(numphi):
            Qchi0raw = np.zeros((lchi0int, lq0int))
            Qchi0 = np.zeros((lchi0int, lq0int))
            count = np.zeros((lchi0int, lq0int))
            broken = False
            for x in range(numFiles):
                if self.abort_flag:
                    writeStitchProperties()
                    self.emit(SIGNAL("enableWidgets()"))                
                    self.emit(SIGNAL("addToConsole(PyQt_PyObject)"), "All stitching has been aborted. Ditching the stitch...")
                    broken = True
                    writeStitchProperties()
                    self.emit(SIGNAL("finished(PyQt_PyObject, PyQt_PyObject)"), self.windowreference,  loopTime)                    
                    break                       
                fullname = fileList[x]
                start = time.time()
                self.emit(SIGNAL("addToConsole(PyQt_PyObject)"), '{0}'.format(fullname))
                self.emit(SIGNAL("addToConsole(PyQt_PyObject)"), os.path.basename(fullname) + ' detected, processing.')
                data = scipy.io.loadmat(fullname)
                Q = data['Q']
                chi = data['chi']
                cake = data['cake']
                lq = rq * (np.max(Q) - np.min(Q))
                lqint = int(math.ceil(lq))
                Q1 = resize(Q, (1, lqint), order=1, preserve_range = True)
                #Q1 = scipy.misc.imresize(Q, (1, lqint), mode='F')
                lchi = rchi * (np.max(chi) - np.min(chi))
                lchiint = int(math.ceil(lchi))
                chi1 = resize(chi, (1, lchiint), order=1, preserve_range = True)
                #chi1 = scipy.misc.imresize(chi, (1, lchiint), mode='F')
                Qchi1 = resize(cake, (lchiint, lqint), preserve_range = True)
                #Qchi1 = scipy.misc.imresize(cake, (lchiint, lqint), mode='F')
                Q0i = round(rq * np.min(Q1)) / rq
                delQ = Q0i - np.min(Q1)
                Q2raw = Q1 + delQ
                Q2 = np.around(rq * Q2raw) / rq
                chi0i = np.around(float(rchi * np.min(chi1))) / float(rchi)
                delchi = chi0i - np.min(chi1)
                chi2raw = chi1 + delchi
                chi2 = np.around(rchi * chi2raw) / rchi
                Qchi2 = np.zeros((lchiint, lqint))
                for n in range(0, lchiint):
                    for m in range(0, lqint):

                        if Qchi1[n][m] <= 0:
                            Qchi2[n][m] = 0
                        elif m + 1 >= lqint:
                            Qchi2[n][m] = 0
                        elif Qchi1[n][m + 1] <= 0:
                            Qchi2[n][m] = 0
                        else:
                            mi = (Qchi1[n][m] - Qchi1[n][m + 1]) / (Q1[0][m] - Q1[0][m + 1])
                            Qchi2[n][m] = Qchi1[n][m] + mi * (Q2[0][m] - Q1[0][m])
    
                for n in range(0, lchiint):
                    for m in range(0, lqint):
                        if Qchi1[n][m] <= 0:
                            Qchi2[n][m] = 0
                        elif n + 1 >= lchiint:
                            Qchi2[n][m] = 0
                        elif Qchi1[n + 1][m] <= 0:
                            Qchi2[n][m] = 0
                        else:
                            mi = (Qchi1[n][m] - Qchi1[n + 1][m]) / (chi1[0][n] - chi1[0][n + 1])
                            Qchi2[n][m] = Qchi1[n][m] + mi * (chi2[0][n] - chi1[0][n])
                            
                #self.emit(SIGNAL("addToConsole(PyQt_PyObject)"), "Shape of Qchi2: %s" % str(np.shape(Qchi2)))
                #self.emit(SIGNAL("addToConsole(PyQt_PyObject)"), "Qchi2 min: %d ; max: %d" % (np.min(Qchi2), np.max(Qchi2)))
                
                indq = np.where(Q0 > np.min(Q2) - 1 / (4 * rq))[0][0]
                indchi = np.where(chi0 > (np.min(chi2) - (1 / (4 * rchi))))[0][0]
                for n in range(lchiint):
                    for m in range(lqint):
                        if Qchi2[n][m] > 0 and (m + indq - 1) < lq0int:
                            Qchi0raw[n + indchi - 1][m + indq - 1] = Qchi0raw[n + indchi - 1][m + indq - 1] + Qchi2[n][m]
                            count[n + indchi - 1][m + indq - 1] += 1
                #self.emit(SIGNAL("addToConsole(PyQt_PyObject)"), "***************************")
                #self.emit(SIGNAL( "addToConsole(PyQt_PyObject)"), "Image %s: shape of Qchi0raw: %s, max is %s, min is %s" % (x, str(np.shape(Qchi0raw)), np.max(Qchi0raw), np.min(Qchi0raw)))
                #self.emit(SIGNAL("addToConsole(PyQt_PyObject)"), "***************************")
                with open("thisRun.txt", 'w') as runFile:
                    runFile.write("s_data_source, " + str(self.dataPath) + "\n")
                    runFile.write("s_processed_loc, " + str(self.savePath) + "\n")
                    imageFilename = os.path.basename(fullname)
                    i = imageFilename.find("scan")
                    imageFilename = imageFilename[:i-1]                    
                    name = os.path.join(save_path, os.path.splitext(imageFilename)[0]+'_gamma')
                    runFile.write("stitch_image, " + name + ".png\n")

                    
                progress += increment
                if self.increment != 0:
                    self.emit(SIGNAL("bar(int, PyQt_PyObject)"), mode, increment)
                else:
                    self.emit(SIGNAL("bar(int, PyQt_PyObject)"), mode, progress)
                end = time.time()
                loopTime += [(end-start)]
            if broken:
                return            
            #self.emit(SIGNAL("addToConsole(PyQt_PyObject)"), "Max / min of count: (%s, %s)" % (np.max(count), np.min(count)))
            #self.emit(SIGNAL("addToConsole(PyQt_PyObject)"), "Max / min of Qchi0raw: (%s, %s)" % (np.max(Qchi0raw), np.min(Qchi0raw)))
            for n in range(lchi0int):
                for m in range(lq0int):
                    if count[n][m] > 0:
                        Qchi0[n][m] = Qchi0raw[n][m] / count[n][m]
                        
            #self.emit(SIGNAL("addToConsole(PyQt_PyObject)"), "***************************")
            #self.emit(SIGNAL( "addToConsole(PyQt_PyObject)"), "shape of Qchi0: %s, max is %s, min is %s" % (str(np.shape(Qchi0)), np.max(Qchi0), np.min(Qchi0)))
            #self.emit(SIGNAL("addToConsole(PyQt_PyObject)"), "***************************")                    
    
            Qchi0log = np.zeros((lchi0int, lq0int))
            for n in range(lchi0int):
                for m in range(lq0int):
                    if Qchi0[n][m] > 0:
                        Qchi0log[n][m] = np.log10(Qchi0[n][m])


        Qchi0_allphi = np.add(Qchi0_allphi, Qchi0)
        Qchi0_allphi = np.divide(Qchi0_allphi, float(numphi)) # normalize the combined-phi image
        
        for n in range(lchi0int): # make a log plot
            for m in range(lq0int):
                if Qchi0_allphi[n][m] > 0:
                        Qchi0log_allphi[n][m] = np.log10(Qchi0_allphi[n][m])
                        
    
        Qchi0_allphi = np.flipud(Qchi0_allphi)
        qname = self.save_Qchi(Q0, chi0, Qchi0_allphi, os.path.basename(fullname), save_path)
        progress += increment
        if self.increment != 0:
            self.emit(SIGNAL("bar(int, PyQt_PyObject)"), mode, increment)
        else:
            self.emit(SIGNAL("bar(int, PyQt_PyObject)"), mode, progress)
        writeStitchProperties()
        self.emit(SIGNAL("finished(PyQt_PyObject, PyQt_PyObject)"), self.windowreference,  loopTime)
        
        
    def run(self):
        self.beginStitch()
    

        
    def save_Qchi(self, Q, chi, cake, imageFilename, save_path):
        scipy.io.savemat(os.path.join(save_path, os.path.splitext(imageFilename)[0]+'_Qchi.mat'), {'Q':Q, 'chi':chi, 'cake':cake})
        Q, chi = np.meshgrid(Q, chi)
    
        fig = plt.figure(1)
        ax = fig.add_subplot(1, 1, 1)
        # plt.title('Q-chi polarization corrected_log scale')
        plt.pcolormesh(Q, chi, np.log(cake), cmap = 'viridis')
        ax.set_facecolor("#000084")
        plt.xlabel('Q')
        plt.ylabel('chi')
        #plt.xlim((0.7, 6.8))
        #plt.ylim((-56, 56))
        #plt.clim(0, 9)    plt.clim((0, np.log(np.nanmax(cake))))
        # the next two lines contributed by S. Suram (JCAP)
        inds = np.nonzero(cake)
        plt.clim(scipy.stats.scoreatpercentile(np.log(cake[inds]), 5), scipy.stats.scoreatpercentile(np.log(cake[inds]), 95))
        plt.colorbar()
        i = imageFilename.find("scan")
        imageFilename = imageFilename[:i-1]
        name = os.path.join(save_path, os.path.splitext(imageFilename)[0]+'_gamma')
        plt.savefig(name, dpi=300)
        plt.close()
        self.emit(SIGNAL("setImage(PyQt_PyObject, PyQt_PyObject)"), self.windowreference, name)


def extents(f):
    delta = f[1] - f[0]
    return [f[0] - delta / 2, f[-1] + delta / 2]

# Writes the latest stitch run info into the Properties.csv file
def writeStitchProperties():
    try:
        properties = []

        with open('Properties.csv', 'rb') as prop:
                reader = csv.reader(prop)
                Properties = dict(reader)
        detectors = Properties["detectors"]
     
        with open("thisRun.txt", 'r') as thisrun:
            properties.append(thisrun.readline().split(", ")[1].rstrip())
            properties.append(thisrun.readline().split(", ")[1].rstrip())
            properties.append(thisrun.readline().split(", ")[1].rstrip())

     
        property_dict = {"s_data_source": properties[0], "s_processed_loc" : properties[1], "stitch_image" : properties[2]}
        if Properties.get("i_data_source") is None:
            property_dict["i_data_source"] = ""
        else:
            property_dict["i_data_source"] = Properties["i_data_source"]
        if Properties.get("i_processed_loc") is None:
            property_dict["i_processed_loc"] = ""   
        else:
            property_dict["i_processed_loc"] = Properties["i_processed_loc"]
        if Properties.get("one_d_image") is None:
            property_dict["one_d_image"] = ""
        else:
            property_dict["one_d_image"] = Properties["one_d_image"]
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
        if Properties.get("qmin") is None:
            property_dict["qmin"] = "0"
        else:
            property_dict["qmin"] = Properties["qmin"]
        if Properties.get("qmax") is None:
            property_dict["qmax"] = "0"
        else:
            property_dict["qmax"] = Properties["qmax"]
        if Properties.get("chimin") is None:
            property_dict["chimin"] = "0"
        else:
            property_dict["chimin"] = Properties["chimin"]
        if Properties.get("chimax") is None:
            property_dict["chimax"] = "0"
        else:
            property_dict["chimax"] = Properties["chimax"]
        property_dict["detectors"] = detectors
    

        with open("Properties.csv", 'wb') as prop:
            writer = csv.writer(prop)
            for key, value in property_dict.items():
                writer.writerow([key, value])    
    except:
        return
    