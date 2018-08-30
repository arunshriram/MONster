# 
#
# This file creates the MONster Help Menu dialog. 
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
#
#

from PyQt4.QtCore import * # for the GUI
from PyQt4.QtGui import * # for the GUI
import getpass # to get the username
from datetime import datetime # to get the current year to see whether it's a "brand-new" MONster or just a "new" MONster
import sys # always need this when running the app loop

# Represents a help dialog for users to interact with and learn about MONster
class HelpDialog(QWidget):
    def __init__(self, win):
        QWidget.__init__(self)
        self.win = win
        self.Stack = QStackedWidget (self)
        self.stack0 = QWidget()
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        self.stack4 = QWidget()
        self.stack5 = QTabWidget()
        self.stack6 = QWidget()
        
        self.Stack.addWidget (self.stack0)
        self.Stack.addWidget (self.stack1)
        self.Stack.addWidget (self.stack2)
        self.Stack.addWidget (self.stack3)
        self.Stack.addWidget (self.stack4)
        self.Stack.addWidget (self.stack5)
        self.Stack.addWidget (self.stack6)
        self.updateUi()
        
    # None -> None
    # Does most of the setup for the help dialog
    def updateUi(self):
        self.leftlist = QListWidget ()
        self.leftlist.insertItem (0, 'WELCOME')
        self.leftlist.insertItem (1, "MACROS")
        self.leftlist.insertItem (2, 'TRANSFORM' )
        self.leftlist.insertItem (3, 'STITCH' )
        self.leftlist.insertItem (4, 'INTEGRATE' )
        self.leftlist.insertItem (5, 'QUEUE LOADER')
        self.leftlist.insertItem (6, 'OTHER')
        self.leftlist.setFont(QFont("Georgia", 20))
        self.leftlist.setMinimumWidth(250)
        self.leftlist.setSpacing(20)
        self.leftlist.currentRowChanged.connect(self.display)
        
        hbox = QHBoxLayout(self)
        hbox.addWidget(self.leftlist)
        hbox.addWidget(self.Stack)

        self.setLayout(hbox)
        self.leftlist.currentRowChanged.connect(self.display)
        self.stack0UI()
        self.stack1UI()
        self.stack2UI()
        self.stack3UI()
        self.stack4UI()
        self.stack5UI()
        self.stack6UI()
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        self.setWindowTitle('MONster Help Window')
        self.setMinimumHeight(800)
        
        # self.stack4.currentChanged.connect(self.onChange)
        #self.show()
        #self.raise_()
    
    # int -> None
    # Takes the index to display for the menu options
    def display(self,i):
        self.Stack.setCurrentIndex(i)  
        #if i == 1:
            #self.selectiongif.stop()
            #self.selectiongif.start()
            #self.dialgif.stop()
            #self.dialgif.start()
        if i != 4:
            self.onedgraphgif.stop()
        if i == 4:
            self.onedgraphgif.stop()
            self.onedgraphgif.start()
            
        ##print 'hello'
        ##print i
    
    # None -> None
    # Defines the layout for the welcome screen of the help dialog
    def stack0UI(self):
        layout = QVBoxLayout()
        usr = getpass.getuser()
        hello = QLabel("Hello, " + str(usr) + "!")
        hello.setFont(QFont("Futura", 25))
        hello.setStyleSheet("color: rgb(153, 51, 0);")
        layout.addWidget(hello)
        if str(datetime.today())[:4] == "2018":
            welcome = QLabel("Welcome to the brand-new MONster (2018) GUI! ")
        else:
            welcome = QLabel("Welcome to the MONster GUI!")
        welcome.setStyleSheet("background-color: rgb(255, 201, 150);")
        welcome.setStyleSheet("color: rgb(133, 184, 133);")
        
        welcome.setFont(QFont("Avenir", 25))
        layout.addWidget(welcome)
        description = QLabel("MONster is a GUI program used to transform, stitch, and \nintegrate small angle x-ray scattering images captured by area detectors. \nThe original batch analyzing scripts were written by \nRobert Tang-Kong, Fang Ren, and Melissa Wette. \nMONster comes with several handy features, as you'll \nsee in this help dialog. It allows for data processing \nover large batches of files with minimal work from the user, \nso now you can transform, integrate, and stitch your images \ntogether without having to run separate scripts several \ntimes! With the queue loading feature, you can create, \nsave, and load entire queues of instruction macros, making \nhours of work consolidated into just a few minutes. If you \nwould like to see this help menu again, just click the menu \noption!")
        description.setFont(QFont("Avenir", 18))
        description.setStyleSheet("color: rgb(0, 51, 102);")
        layout.addWidget(description)
        author = QLabel("MONster v1.0 - Arun Shriram, 2018 SSRL\n\nFor any questions, please email arun.shriram@gmail.com.")
        github = QLabel("github link: github.com/slaclab/MONster")
        author.setFont(QFont("Avenir", 14))
        github.setFont(QFont("Avenir", 12))

        layout.addWidget(author)
        layout.addWidget(github)
        self.stack0.setLayout(layout)

    # None -> None
    # Defines the layout for the macros screen of the help dialog
    def stack1UI(self):
        layout = QVBoxLayout()
        macroimg = QLabel()
        pix = QPixmap('images/macro.png')
        macroimg.setPixmap(pix.scaled(540, 330, Qt.KeepAspectRatio))
        layout.addWidget(macroimg)
        macros_label = QLabel("What are Macros?")
        macros_label.setFont(QFont("Futura", 25))
        macros_label.setStyleSheet("color: rgb(100, 159, 0);")
        layout.addWidget(macros_label)
        macros = QTextBrowser()
        macros.setFont(QFont("Calibri", 18))
        macros.append("   - Macros are a convenient way to store information about a certain process or set of instructions you wish the program to follow.")
        macros.append("   - MONster uses macros (in the form of CSV files) to store all the information you input, like data sources, calibration info, Q and Chi ranges, and more, to later add to the Queue.")
        macros.moveCursor(QTextCursor.Start)
        layout.addWidget(macros)

        howto_label = QLabel("How to Use Macros in MONster")
        howto_label.setFont(QFont("Futura", 25))
        howto_label.setStyleSheet("color: rgb(100, 159, 0);")
        layout.addWidget(howto_label)

        howto = QTextBrowser()
        howto.setFont(QFont("Calibri", 18))
        howto.append("   - On the Transform, Stitch, and Integrate pages, you can save all the information on each page as an individual macro by clicking the \"Save as a macro\" buttons.")
        howto.append("   - This will take data sources, processed locations, detectors - basically all the information you input, and save it as an instruction for MONster to process in the Queue.")
        howto.append("   - You can also save and add macros to the queue by clicking \"Add this configuration to the queue\". This will save the macro AND add it to the Queue.")
        howto.moveCursor(QTextCursor.Start)
        layout.addWidget(howto)
        self.stack1.setLayout(layout)
 
    # None -> None
    # Defines the layout for the transform screen of the help dialog 
    def stack2UI(self):
        layout = QVBoxLayout()
        transformlabel = QLabel("What is Transform?")
        transformlabel.setFont(QFont("Futura", 25))
        transformlabel.setStyleSheet("color: rgb(100, 159, 0);")
        layout.addWidget(transformlabel)
        transform = QLabel("Transforming is mapping detector images to q-chi space!")
        transform.setFont(QFont("Calibri", 18))
        layout.addWidget(transform)
        data_source_label = QLabel("Data Source Selection")
        data_source_label.setFont(QFont("Futura", 25))
        data_source_label.setStyleSheet("color: rgb(100, 159, 0);")
        layout.addWidget(data_source_label)

        data_source = QTextBrowser()
        data_source.setFont(QFont("Calibri", 18))
        data_source.append("   - MONster accepts either .raw or .tif images for transforming.")
        data_source.append("   - If you wish to select an entire folder, click the \"Select a folder\" button.")
        data_source.append("   - To select one or more files, click the \"Select one or more files\" button and select your files. To select multiple, click one file, hold shift, and click another file. To select specific files, hold control and left click on the files you wish to select.")
        data_source.append("   - When selecting .raw files, be sure to select your detector from the dropdown menu.")
        data_source.append("   - If your detector is not in the dropdown menu, go to Edit->Add or remove detectors and add your detector!")
        data_source.moveCursor(QTextCursor.Start)
        
        layout.addWidget(data_source)
        calib_label = QLabel("Calibration")
        calib_label.setFont(QFont("Futura", 25))
        calib_label.setStyleSheet("color: rgb(100, 159, 0);")
        layout.addWidget(calib_label)
        calib = QTextBrowser()
        calib.setFont(QFont("Calibri", 18))
        calib.append("   - There are two ways of setting your calibration: manually enter each value, or selecting a previously existing calib file.")
        calib.append("   - To select a calib file, click the folder icon and choose your file. The values will automatically fill in, and if you want, you can tweak these values. ")
        calib.append("   - You can choose to save your tweaked values as a new calibration file by clicking the \"Save this calibration!\" button.")
        calib.moveCursor(QTextCursor.Start)
        layout.addWidget(calib)
        
        processed_label = QLabel("Processed Files")
        processed_label.setFont(QFont("Futura", 25))
        processed_label.setStyleSheet("color: rgb(100, 159, 0);")
        layout.addWidget(processed_label)

        processed = QTextBrowser()
        processed.setFont(QFont("Calibri", 18))
        processed.append("   - By default, processed files will be stored in a folder called \"Processed_Transform\" inside the selected data directory.")
        processed.append("   - If you do not change the processed file directory from run to run, each run will overwrite the previous run's processed data!")
        processed.moveCursor(QTextCursor.Start)
        layout.addWidget(processed)
        self.stack2.setLayout(layout)
    
    # None -> None
    # Defines the layout for the scan screen of the help dialog
    
    def stack3UI(self):
        layout = QVBoxLayout()
        stitch_label = QLabel("What is Stitching?")
        stitch_label.setFont(QFont("Futura", 25))
        stitch_label.setStyleSheet("color: rgb(100, 159, 0);")
        layout.addWidget(stitch_label)
        stitch = QLabel()
        stitch.setFont(QFont("Calibri", 18))

        stitch.setText("Stitching is an easy tool to combine images together! Select multiple files from a detector scan and let the program work its magic!")
        layout.addWidget(stitch)

        howto_label = QLabel("How to Stitch Your Files")
        howto_label.setFont(QFont("Futura", 25))
        howto_label.setStyleSheet("color: rgb(100, 159, 0);")
        layout.addWidget(howto_label)

        howto = QTextBrowser()
        howto.setFont(QFont("Calibri", 18))
        howto.append("   - Using Stitch is very simple. Select the folder with the .mat data you wish to process by clicking the folder button.")
        howto.append("   - By default, processed files will be stored in a folder called \"Processed_Stitch\" inside the selected data directory.")
        howto.append("   - If you do not change the processed file directory from run to run, each run will overwrite the previous run's processed data!")
        howto.moveCursor(QTextCursor.Start)
        howto.resize(howto.sizeHint().width(), howto.sizeHint().height())
        layout.addWidget(howto)

        
        self.stack3.setLayout(layout)

    # None -> None
    # Defines the layout for the graphing screen of the help dialog
   
    def stack4UI(self):
        layout = QVBoxLayout()
        whatis_label = QLabel("What is Integrate?")
        whatis_label.setFont(QFont("Futura", 25))
        whatis_label.setStyleSheet("color: rgb(100, 159, 0);")
        layout.addWidget(whatis_label)

        whatis = QLabel()
        whatis.setFont(QFont("Calibri", 18))
        whatis.setText("Integration takes processed transform data and perform column-wise averaging to create a one-dimensional graph of the image.")
        layout.addWidget(whatis)

        howtolabel = QLabel("How to Integrate")
        howtolabel.setFont(QFont("Futura", 25))
        howtolabel.setStyleSheet("color: rgb(100, 159, 0);")
        layout.addWidget(howtolabel)
        howto = QTextBrowser()
        howto.setFont(QFont("Calibri", 18))
        howto.append("   - If you wish to select an entire folder for your data, click the \"Select a folder\" button, and click the folder icon.")
        howto.append("   - To select one or more files, click the \"Select one or more files\" button and select your files. To select multiple, click one file, hold shift, and click another file.  To select specific files, hold control and left click on the files you wish to select.")
        howto.append("   - MONster only accepts .mat files for Integration.")
        howto.append("   - By default, processed files will be stored in a folder called \"Processed_Integrate\" inside the selected data directory.")
        howto.append("   - If you do not change the processed file directory from run to run, each run will overwrite the previous run's processed data!")
        howto.append("   - Be sure to input the Q and Chi range values between which MONster should perform the integration.")
        howto.moveCursor(QTextCursor.Start)
        layout.addWidget(howto)

        howtographlabel = QLabel("How to Navigate the Graph")
        howtographlabel.setFont(QFont("Futura", 25))
        howtographlabel.setStyleSheet("color: rgb(100, 159, 0);")
        layout.addWidget(howtographlabel)

        self.onedgraphgif = QMovie("images/1dgraph.gif")
        giflabel1 = QLabel()
        giflabel1.setMovie(self.onedgraphgif)
        layout.addWidget(giflabel1)
        howtograph = QTextBrowser()
        howtograph.setFont(QFont("Calibri", 18))
        howtograph.append("   - To zoom into a rectangular region of the graph, move your cursor over the graph, left click, and drag.")
        howtograph.append("   - To zoom in or out, move your cursor over the graph and use the scroll wheel.")
        howtograph.append("   - To reset the graph to its original range, right click on the graph.")
        howtograph.moveCursor(QTextCursor.Start)
        layout.addWidget(howtograph)
      
        
        self.stack4.setLayout(layout)

    # None -> None
    # Defines the layout for the Queue Loader screen of the help dialog
    def stack5UI(self):
        layout1 = QVBoxLayout()
        queueimg = QLabel()
        pix = QPixmap('images/queue.png')
        queueimg.setPixmap(pix.scaled(600, 330, Qt.KeepAspectRatio))
        layout1.addWidget(queueimg)        
        lbl = QLabel("What is the Queue Loader?")
        lbl.setFont(QFont("Futura", 25))
        lbl.setStyleSheet("color: rgb(100, 159, 0);")
        layout1.addWidget(lbl)
        ql = QTextBrowser()
        ql.setFont(QFont("Calibri", 18))
        ql.append("   - The Queue Loader is a tool to help you make processes more automated and run with less continual management.")
        ql.append("   - Using the Queue Loader, you can leave MONster running overnight or for hours, transforming, stitching, or integrating your files in the background.")
        ql.append("   - The Queue Loader uses macros to save, store, and load the information you use to calibrate each process you wish to execute.")
        ql.moveCursor(QTextCursor.Start)
        layout1.addWidget(ql)
        page1 = QWidget()
        page1.setLayout(layout1)
        page2 = QWidget()
        layout2 = QVBoxLayout()
        melabel = QLabel("The Macro Editor")
        melabel.setFont(QFont("Futura", 25))
        melabel.setStyleSheet("color: rgb(100, 159, 0);")
        layout2.addWidget(melabel)
      

        me = QTextBrowser()
        me.setFont(QFont("Calibri", 18))
        me.append("   - To open the Macro Editor, click the \"+\" button or double click an existing process.")
        me.append("   - There are two kinds of macros you can create: worfklow macros or independent macros.")
        me.append("Workflow Macros:")
        me.append("   - Workflow macros follow a certain path of data processing: transform images, stitch the transformed images together, and integrate those transformed images.")
        me.append("   - To use workflow macros, do the following: input your data source, calibration information, processed file location, and detector if necessary in the Transform page of the Macro Editor. Then add your Q and Chi ranges in the Integrate page of the Macro Editor, save your macro, and add it to the queue!")
        me.append("Independent Macros:")
        me.append("   - Independent macros hold at least one process: Transform, Stitch, and Integrate. However, you can choose to omit any processes you want. Each process is independent of the other; you should select different data sources for transforming, stitching, and integration.")
        me.append("")
        me.append("   - When saving your macro, each file has its own unique time-stamped tag, so you don't have to worry about renaming the file root every time; the file names will all be unique. However, you can still choose to rename the macros for convenience sake.")
        me.append("   - If you've already created a macro, you can load it into the queue by clicking \"Load a macro\".")
        me.moveCursor(QTextCursor.Start)
        layout2.addWidget(me)
        
       
        self.stack5.addTab(page1, "Page 1")
        
        queuelbl = QLabel("The Queue")
        queuelbl.setFont(QFont("Futura", 25))
        queuelbl.setStyleSheet("color: rgb(100, 159, 0);")
        layout2.addWidget(queuelbl)

        queue = QTextBrowser()
        queue.setFont(QFont("Calibri", 18))
        queue.append("   - The Queue is where you can see and manage all the loaded macros. To add a macro the queue, click \"+\", and to remove a macro from the queue, select your macro and click \"-\".")
        queue.append("   - Before the queue starts, be sure to check whether the checkbox \"Take me to each tab during each process\" is checked. If it is, that means that MONster will automatically switch tabs every time a new process begins. Otherwise, you will remain on the Queue Loader page unless you manually switch tabs.")
        queue.append("   - While the queue is running, you can pause or terminate the queue. Pausing the queue will temporarily stop the queue after whatever process (transform, stitch, integrate) is currently running finishes. Once the queue pauses, you can either restart the queue, resume the queue, or terminate the queue. If you choose to terminate the queue in the middle of a process, it will finish that process before terminating.")
        queue.append("   - If you want to skip a process, such as skipping the transform, just go to the transform page and hit abort!")
        queue.append("")
        queue.append("   - If you have added several macros the queue, quit MONster, and restart it later, you can save yourself the trouble of selecting those macros all over again by saving the queue before you exit MONster. MONster saves the queue as a JSON file, with all the macros and their information stored in the queue. When you want to load the queue back into MONster, click \"Load a queue\" to clear all elements currently in the queue and replace them with the saved queue.")
        queue.moveCursor(QTextCursor.Start)
        layout2.addWidget(queue)
        page2.setLayout(layout2)
        self.stack5.addTab(page2, "Page 2")

        
    # index -> None
    # Plays all GIFS when the tab has been changed
    def onChange(self, i):
        if i == 4:
            self.onedgraphgif.start()
        else:
            self.onedgraphgif.stop()   
    
    # event -> None
    # Stops all gifs (just in case) when the help window closes
    def closeEvent(self, event):
        self.onedgraphgif.stop()
       
        self.win.show()
        self.win.raise_()
        
    # None -> None
    # Defines the layout for the "Other" screen of the help dialog
    
    def stack6UI(self):
        layout = QVBoxLayout()
        
        menulbl = QLabel("Menu Options")
        menulbl.setFont(QFont("Futura", 25))
        menulbl.setStyleSheet("color: rgb(100, 159, 0);")
        layout.addWidget(menulbl)
        menu = QTextBrowser()
        menu.setFont(QFont("Calibri", 18))
        menu.append("File:")
        menu.append("   - To set the location where you want console logs to be saved, go to File->Change log file save location.")
        menu.append("Edit:")
        menu.append("   - MONster saves all its previous run information in a file called Properties.csv. To clear all previous run information, click Edit->Clear previous run information.")
        menu.append("   - If your detector is not in the detector dropdown menu on the Transform page, click Edit->Add or remove a detector to configure your detectors. Clearing the previous run information will reset any added detectors aside from the defaults.")
        layout.addWidget(menu)
        menu.moveCursor(QTextCursor.Start)
        
        bugslabel = QLabel("Currently Known Bugs")
        bugslabel.setFont(QFont("Futura", 25))
        bugslabel.setStyleSheet("color: rgb(159, 100, 0);")
        layout.addWidget(bugslabel)
        bugs = QTextBrowser()
        bugs.setFont(QFont("Calibri", 18))
        bugs.append("")
        layout.addWidget(bugs)
        bugs.moveCursor(QTextCursor.Start)
        self.stack6.setLayout(layout)
        
# Not necessary but it helps to debug; runs the specmain.main function  
def main():
    specmain.main()

if __name__ == '__main__':
    main()
