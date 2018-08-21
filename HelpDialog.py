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
        self.stack4 = QTabWidget()
        self.stack5 = QWidget()
        
        self.Stack.addWidget (self.stack0)
        self.Stack.addWidget (self.stack1)
        self.Stack.addWidget (self.stack2)
        self.Stack.addWidget (self.stack3)
        self.Stack.addWidget (self.stack4)
        self.Stack.addWidget (self.stack5)
        self.updateUi()
        
    # None -> None
    # Does most of the setup for the help dialog
    def updateUi(self):
        self.leftlist = QListWidget ()
        self.leftlist.insertItem (0, 'WELCOME')
        self.leftlist.insertItem (1, 'TRANSFORM' )
        self.leftlist.insertItem (2, 'STITCH' )
        self.leftlist.insertItem (3, 'INTEGRATE' )
        self.leftlist.insertItem (4, 'QUEUE LOADER')
        self.leftlist.insertItem (5, 'OTHER')
        self.leftlist.setFont(QFont("Georgia", 20))
        self.leftlist.setFixedWidth(230)
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
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        self.setWindowTitle('MONster Help Window')
        self.setMinimumHeight(800)
        
        self.stack4.currentChanged.connect(self.onChange)
        #self.show()
        #self.raise_()
    
    # int -> None
    # Takes the index to display for the menu options
    def display(self,i):
        self.Stack.setCurrentIndex(i)  
        if i == 1:
            self.selectiongif.stop()
            self.selectiongif.start()
            self.dialgif.stop()
            self.dialgif.start()
        if i == 4:
            self.navigategif.stop()
            self.levelsgif.stop()
            self.navigategif.start()
            self.levelsgif.start()
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
    # Defines the layout for the motor selection and movement screen of the help dialog 
    def stack1UI(self):
        layout = QVBoxLayout()
        motorlabel = QLabel("Motor Selection and Movement")
        motorlabel.setFont(QFont("Futura", 25))
        motorlabel.setStyleSheet("color: rgb(100, 159, 0);")
        self.selectiongif = QMovie("images/motor_selection_movement.gif")
        giflabel1 = QLabel()
        giflabel1.setMovie(self.selectiongif)
        layout.addWidget(motorlabel)
        layout.addWidget(giflabel1)
        motorselection = QTextBrowser()
        motorselection.setFont(QFont("Calibri", 18))
        motorselection.append("   - SPECtre can make only one motor move at a time. This motor is highlighted in purple to the left of the window, and as that motor moves you can see its position updating on the screen. ")
        motorselection.append("   - A single motor may be moved in real space using the \"Move To\" button. For example, if a motor is at 3 mm, entering in \"15\" will move that motor to position 15. You can tell when the motor has stopped moving when the \"Position\" label has stopped updating. ")
        motorselection.append("   - To stop a motor before it has finished moving, click the \"Abort\" button. This will send an abort command to Spec that cannot be undone. ")
        motorselection.append("   - If you would like to move the motor to a relative position, click the \"Move By\" button. For example, if the selected motor is currently at 3 mm, typing \"-5\" and then clicking \"Move By\" will move the motor to -2 mm, rather than -5 mm.")
        motorselection.moveCursor(QTextCursor.Start)
        
        diallabel = QLabel("Dials")
        diallabel.setFont(QFont("Futura", 25))
        diallabel.setStyleSheet("color: rgb(100, 159, 0);")
        layout.addWidget(motorselection)
        layout.addWidget(diallabel)
    
        self.dialgif = QMovie("images/dials.gif")
        giflabel2 = QLabel()
        giflabel2.setMovie(self.dialgif)
        layout.addWidget(giflabel2)
        dials = QTextBrowser()
        dials.setFont(QFont("Calibri", 18))
        dials.append("   - Dial angles keep track of hardware limits and prevent complete loss of angles from alignment errors or computer failure. The dial angles are generally made to agree with a physical indicator on each motor, such as a dial. User angles are related to the dial angles through the equation: user = sign x dial + offset")
        dials.append("   - Redefining a user angle changes the internal value of offset. Dial angles are directly proportional to the values contained in the hardware controller registers. The sign of motion is set in the configuration file by the Spec administrator and normally isn't changed. ")
        dials.append("   - The \"Set\" button is used to set the dial position of a motor. If a motor is at 5 mm, you can set the user dial to whichever value you want it to be without moving the motor.")
        dials.moveCursor(QTextCursor.Start)
        layout.addWidget(dials)
        #layout.addQ
        self.stack1.setLayout(layout)
    
    # None -> None
    # Defines the layout for the scan screen of the help dialog
    
    def stack2UI(self):
        layout = QVBoxLayout()
        descriptionlabel = QLabel("SPECtre allows the user to perform two types of scans: 1D scans and 2D (\"mesh\") scans. Scans can be\npaused, resumed, and saved as .CSV and .PNG files.\nTo take save as .CSV and .PNG, click the \"Graph Options\" menu option. ")
        descriptionlabel.setStyleSheet("color: rgb(100, 0, 0);")
        descriptionlabel.setFont(QFont("Georgia", 20))
        layout.addWidget(descriptionlabel)
        scanlabel1d = QLabel("1D Scans")
        scanlabel1d.setFont(QFont("Futura", 25))
        scanlabel1d.setStyleSheet("color: rgb(100, 159, 0);")
        layout.addWidget(scanlabel1d)
        self.onedscangif = QMovie("images/1dscan.gif")
        giflabel1 = QLabel()
        giflabel1.setMovie(self.onedscangif)
        layout.addWidget(giflabel1)
        textbrowser1d = QTextBrowser()
        textbrowser1d.setFont(QFont("Calibri", 18))
        textbrowser1d.append("   - 1D scans use one motor and one counter to create a graph of the counts vs. the motor position. To choose the 1D scan option, choose \"1D Scan\" from the scan options to the left of the window.")
        textbrowser1d.append("   - To select the motor, select from the dropdown menu with the purple \"Motor\" label. To select the counter, choose from the dropdown menu labeled \"Chn\".")
        textbrowser1d.append("   - You can use either Center/Halfwidth (C/W) parameters or Start/Finish (S/F) parameters:")
        textbrowser1d.append("      - C/W:")
        textbrowser1d.append("         - The Center parameter is the center of the scan radius. The Halfwidth parameter is the radius of the scan, or how far the scan will reach from the center. Once the scan completes, it will return the motors to the center position.")
        textbrowser1d.append("      - S/F:")
        textbrowser1d.append("         - The Start parameter is the initial position of the scan, and the Finish parameter is the final position of the scan.")
        textbrowser1d.append("         - If you would like the scan to complete and leave the motors at their final position, leave the \" move motors back\" checkbox unchecked. If checked, the motors will be returned to the start position.")
        textbrowser1d.append("   - To choose how many points you would like in your scan, enter a number in the \"Pts\" section, and enter the time you would like for each point to be scanned in the \"Time\" section.")
        textbrowser1d.moveCursor(QTextCursor.Start)
        layout.addWidget(textbrowser1d)
        scanlabel2d = QLabel("2D Scans")
        scanlabel2d.setFont(QFont("Futura", 25))
        scanlabel2d.setStyleSheet("color: rgb(100, 159, 0);")
        layout.addWidget(scanlabel2d)
        self.twodscangif = QMovie("images/2dscan.gif")
        giflabel2 = QLabel()
        giflabel2.setMovie(self.twodscangif)
        layout.addWidget(giflabel2)
        textbrowser2d = QTextBrowser()
        textbrowser2d.setFont(QFont("Calibri", 18))        
        textbrowser2d.append("   - Mesh scans use one counter and two motors to create a two-dimensional plot, with the color of each segment based on a \"jet\" color scale. Motor 1 is on the X-Axis, while Motor 2 is on the Y-Axis.")
        textbrowser2d.append("   - To access the mesh functionalities, click \"2D Scan\". Select a second motor and the counter you would like to use.")
        textbrowser2d.append("   - You can use either Center/Halfwidth (C/W) parameters or Start/Finish (S/F) parameters (for each motor):")
        textbrowser2d.append("      - C/W:")
        textbrowser2d.append("         - The Center parameter is the center of the scan radius. The Halfwidth parameter is the radius of the scan, or how far the scan will reach from the center. Once the scan completes, it will return the motors to the center position.")
        textbrowser2d.append("      - S/F:")
        textbrowser2d.append("         - The Start parameter is the initial position of the scan, and the Finish parameter is the final position of the scan.")
        textbrowser2d.append("         - If you would like the scan to complete and leave the motors at their final position, leave the \" move motors back\" checkbox unchecked. If checked, the motors will be returned to the start position.")
        
        textbrowser2d.append("   - To choose how many points you would like in your scan, enter a number in the \"Pts\" section, and enter the time you would like for each point to be scanned in the \"Time\" section - for BOTH motors.")
        layout.addWidget(textbrowser2d)
        textbrowser2d.moveCursor(QTextCursor.Start)
        
        
        self.stack2.setLayout(layout)

    # None -> None
    # Defines the layout for the graphing screen of the help dialog
   
    def stack3UI(self):
        layout = QVBoxLayout()
        graph1d = QLabel("1D Graph")
        graph1d.setFont(QFont("Futura", 25))
        graph1d.setStyleSheet("color: rgb(100, 159, 0);")
        layout.addWidget(graph1d)
        self.onedgraphgif = QMovie("images/1dgraph.gif")
        giflabel1 = QLabel()
        giflabel1.setMovie(self.onedgraphgif)
        layout.addWidget(giflabel1)
        ascan = QTextBrowser()
        ascan.setFont(QFont("Calibri", 18))
        ascan.append("   - Updates in real-time as SPECtre contacts SPEC for the data. Points are drawn in blue circles and are connected. ")
        ascan.append("   - The Y-axis of the graph represents the selected counter; the X-axis of the graph represents the selected motor.  ")
        ascan.append("   - You can use the scroll wheel to zoom in and out of the graph. Dragging the mouse on the graph will draw a rectangle and zoom the graph to the contents of that rectangle. To autoscale and reset the position of the graph, simply right-click your mouse on the graph.")
        ascan.append("   - If you left click on the graph, the \"Selected Coordinates\" label will keep the position you selected for reference.")
        ascan.append("   - A crosshair will follow your mouse and will update its coordinates in the bright blue label. ")
        ascan.append("   - You can select from three fits: Gaussian, Lorentzian, and Pseudo-Voigt; the last being a combination of Gaussian and Lorentzian. Once selected, the table below the graph will update with the appropriate data. When a fit is selected, the button will turn blue. If you want to remove the fit displayed, click the fit button again.")
        ascan.append("   - You can change the Y-Axis to be in Log Mode by clicking the \"Log plot\" checkbox. Similarly, you can change the Y-Axis to be in Derivative Mode by checking the \"Derivative\" box. Unchecking will reset the graph's mode.")
        layout.addWidget(ascan)
        ascan.moveCursor(QTextCursor.Start)
        graph2d = QLabel("2D Graph")
        graph2d.setFont(QFont("Futura", 25))
        graph2d.setStyleSheet("color: rgb(100, 159, 0);")
        layout.addWidget(graph2d)
        self.twodgraphgif = QMovie("images/2dgraph.gif")
        giflabel2 = QLabel()
        giflabel2.setMovie(self.twodgraphgif)
        layout.addWidget(giflabel2)
        meshscan = QTextBrowser()
        meshscan.setFont(QFont("Calibri", 18))
        meshscan.append("   - This graph will only appear when a 2D scan is being activated.")
        meshscan.append("   - Updates in real-time as SPECtre contacts SPEC for the data. Points are drawn in colors according to the legend to the right hand side. The intervals of the legend update in real-time as well.")
        meshscan.append("   - The horizontal axis represents the first motor, and the vertical axis represents the second motor. You can use the mouse to get the coordinates of each color by moving the mouse over the graph.")
        meshscan.append("   - If you would like to move the motors to a certain position, you can left-click on a point on the graph and move the motors to that specific position. If you would like, you can then move the motors back to their original position just after the scan completed.")
        layout.addWidget(meshscan)
        meshscan.moveCursor(QTextCursor.Start)
        self.stack3.setLayout(layout)

    # None -> None
    # Defines the layout for the "MAR" screen of the help dialog
    
    def stack4UI(self):
        
        layout1 = QVBoxLayout()
        lbl = QLabel("Controls")
        lbl.setFont(QFont("Futura", 25))
        lbl.setStyleSheet("color: rgb(100, 159, 0);")
        layout1.addWidget(lbl)
        controls = QTextBrowser()
        controls.setFont(QFont("Calibri", 18))
        controls.append("   - Under \"DATA DIRECTORY\", you can choose the directory where MAR will save its .TIF images after collection. You can also edit what the file name will be (default is \"scan1\"). If the directory does not exist, SPECtre will create the directory. ")
        controls.append("   - Each file has its own unique time-stamped tag (you will see this in the console log when you begin collection), so you don't have to worry about renaming the file root every time; the file names will all be unique.")
        controls.append("   - You can select between 1 and 99 series of frames. Each frame will be exposed for whatever number of seconds you would like (integers only). Entering a number in the \"min delay\" text box will set a delay between exposures.")
        controls.append("   - Clicking \"Collect\" will send a job file to SPEC. If you want to cancel the current job file, click \"Cancel\". However, the current tasks will finish before MAR will cancel the remaining scheduled processes.")
        controls.append("   - The last three rows of the image controls section allow you to select the motors you would like to rock, move, and translate between series. You may enter the appropriate values in the text boxes.")
        controls.append("   - If you want to manually open or close the MAR CCD shutter, click the \"Shutter OPEN/CLOSED\" button at the bottom right-hand-side of the screen.")
        layout1.addWidget(controls)        
        controls.moveCursor(QTextCursor.Start)
        layout1.addStretch()
        page1 = QWidget()
        page1.setLayout(layout1)
        page2 = QWidget()
        layout3 = QVBoxLayout()
        page3 = QWidget()
        page3.setLayout(layout3)
        self.stack4.addTab(page1, "Page 1")
        self.stack4.addTab(page2, "Page 2")
        self.stack4.addTab(page3, "Page 3")
       # self.stack4.setLayout(layout)
        #dividerline = QFrame()
        #dividerline.setObjectName(QString.fromUtf8("line"))
        #dividerline.setGeometry(QRect(0, 190, 270, 20))
        #dividerline.setFrameShape(QFrame.HLine)
        #dividerline.setFrameShadow(QFrame.Sunken)
        #layout.addStretch()
        #layout.addWidget(dividerline)
        #layout.addStretch()
        layout2 = QVBoxLayout()
        self.navigategif = QMovie("images/navigate.gif")
        gif1label = QLabel()
        gif1label.setMovie(self.navigategif)
        navigatelbl = QLabel("How to Navigate The Graph")
        navigatelbl.setFont(QFont("Futura", 25))
        navigatelbl.setStyleSheet("color: rgb(100, 159, 0);")
        layout1.addWidget(navigatelbl)
        layout1.addWidget(gif1label)
        #self.navigategif.start()
        
        navigate = QTextBrowser()
        navigate.setFont(QFont("Calibri", 18))
        navigate.append("   - The following instructions apply when the mouse is directly over the graph, not over another part of the window or over the ROI. To zoom in or out, scroll up and down with the mouse. The plot will zoom into the mouse's position.")
        navigate.append("   - Right-click the graph and go to \"Mouse Mode\". ")
        navigate.append("      - If \"3 button\" is selected: ")
        navigate.append("         - Left-clicking and dragging the mouse will let you move the graph around.")
        navigate.append("      - If \"1 button\" is selected: ")
        navigate.append("         - Left-clicking and dragging the mouse will let you draw a rectangle. The graph's viewing area will then zoom into that rectangle. ")
        navigate.append("         - This does not set the graph's ROI. You can only equalize the graph when you move the ROI to the region you are analyzing. See next page for more information.")
        layout1.addWidget(navigate)
        navigate.moveCursor(QTextCursor.Start)
        layout1.addStretch()
        
        
        levelslbl = QLabel("How to Change Your Viewing Levels")
        
        self.levelsgif = QMovie("images/levels.gif")
        gif2label = QLabel()
        gif2label.setMovie(self.levelsgif)

        levelslbl.setFont(QFont("Futura", 25))
        levelslbl.setStyleSheet("color: rgb(100, 159, 0);")
        layout1.addWidget(levelslbl)
        layout1.addWidget(gif2label)
        #self.levelsgif.start()        
        levels = QTextBrowser()
        levels.setFont(QFont("Calibri", 18))
        levels.append("   - To the right of the graph is the histogram. If the image does not show, or if you wish to change which part of the image correlates to the color bar, you can drag the top and bottom gold bar on the histogram up and down. ")
        levels.append("   - For example, if the image is completely black, try slowly dragging the top gold line downwards.")
        layout1.addWidget(levels)
        levels.moveCursor(QTextCursor.Start)
        layout1.addStretch()
        
        autoscalelbl = QLabel("How to Return to Full View")
        autoscalelbl.setFont(QFont("Futura", 25))
        autoscalelbl.setStyleSheet("color: rgb(100, 159, 0);")
        layout2.addWidget(autoscalelbl)
        autoscale = QTextBrowser()
        autoscale.setFont(QFont("Calibri", 18))
        autoscale.append("   - If you find yourself too zoomed in or out of the histogram, graph, or ROI line, you can right click on the area you wish to rescale and click \"View all\".")
        autoscale.append("   - This will not necessarily return the area to its original view (as soon as the exposure finished), but rather will scale the area to the selected viewing area. To reset the graph, ROI, ROI line, and histogram to their original views, click the \"Restore Graph\" button below the graph. ")
        layout2.addWidget(autoscale)
        autoscale.moveCursor(QTextCursor.Start)
        #layout2.addStretch()
        
        roilbl = QLabel("How to Select Your ROI (Region of Interest)")
        roilbl.setFont(QFont("Futura", 25))
        roilbl.setStyleSheet("color: rgb(100, 159, 0);")
        layout2.addWidget(roilbl)
        self.roigif = QMovie("images/roi.gif")
        gif3label = QLabel()
        gif3label.setMovie(self.roigif)
        layout2.addWidget(gif3label)
        #self.roigif.start()
        roi = QTextBrowser()
        roi.setFont(QFont("Calibri", 18))
        roi.append("   - To view the ROI, click the \"ROI\" button below the histogram.")
        roi.append("   - The ROI is the Region of Interest. It creates a box in the graph that you can rotate, scale, and move around the image. With this ROI, you can study several things:")
        roi.append("      - Equalization:")
        roi.append("         - If you select an ROI, you can equalize the rest of the image to match the intensity levels of the region of interest. For example, selecting an area with a minimum value of 20 and a maximum value of 300 will set the minimum value for the rest of the graph to be 20 and the maximum value to be 300.")
        roi.append("      - ROI Plot:")
        roi.append("         - Selecting the ROI box will allow you to see a 1-dimensional representation of the region you are viewing. As you drag the box around, a graph will pop up below the image, allowing you to see trend lines and to identify any peaks or patterns.")
        roi.append("         - Right-clicking on this graph will give you various options, including inverting the X and Y axes, exporting, mouse mode, and viewing the graph grid (under \"Plot Options\").")
        roi.append("   - If you do not wish to see the 1-dimensional graph but would like to just move the box, click and drag the dividing line between the graph and the image all the way down. Likewise, if you would like to just see the 1-dimensional graph, click and drag the dividing line all the way up.")
        roi.append("   - One thing to remember is that clicking \"Equalize\" will equalize the rest of the image only according to the region you have selected, not the current view of the image; zooming in and clicking \"Equalize\" is not enough.")
        roi.append("   - Before you click \"Equalize\" make sure you click the \"ROI\" button and select your region of interest.")
        layout2.addWidget(roi)
        roi.moveCursor(QTextCursor.Start)
        
        exportlbl = QLabel("How to Export The Graph")
        exportlbl.setFont(QFont("Futura", 25))
        exportlbl.setStyleSheet("color: rgb(100, 159, 0);")
        layout3.addWidget(exportlbl)
        self.exportgif = QMovie("images/export.gif")
        gif4label = QLabel()
        gif4label.setMovie(self.exportgif)
        layout3.addWidget(gif4label)
        #self.exportgif.start()
        export = QTextBrowser()
        export.setFont(QFont("Calibri", 18))
        export.append("   - There are two options to export your graphs. The first is to click \"Menu\" and then \"Export\". This option is the quickest and easiest way to save the ENTIRE image as any image format. However, if you do not specify your image format, the image will not save.")
        export.append("   - For more complex exporting options (including the ability to export as CSV, SVG, Image File, Matplotlib Window, and to export only your current view, a.k.a. VIEWBOX, instead of the entire graph), right-click on the graph itself and select the \"Export\" option.")
        export.append("   - To export the 1-dimensional ROI plot or the histogram, right click on the region you wish to export and click \"Export\".")
        layout3.addWidget(export)
        export.moveCursor(QTextCursor.Start)
        layout3.addStretch()
        
        colorbarlbl = QLabel("How to Change The Color Bar")
        colorbarlbl.setFont(QFont("Futura", 25))
        colorbarlbl.setStyleSheet("color: rgb(100, 159, 0);")
        layout3.addWidget(colorbarlbl)
        self.colorbargif = QMovie("images/colorbar.gif")
        gif5label = QLabel()
        gif5label.setMovie(self.colorbargif)
        layout3.addWidget(gif5label)
        #self.colorbargif.start()
        colorbar = QTextBrowser()
        colorbar.setFont(QFont("Calibri", 18))
        colorbar.append("   - By default, images are displayed with the \"jet\" color map. To change the colors, you have two options: either select from one of the provided colorbars or create your own temporary color scheme.")
        colorbar.append("   - To select a default color bar, right-click the color bar and select the scheme you would like to use. This may create new ticks to the right hand side. These ticks can be used to inverse the color scheme by dragging them to opposite locations on the color bar (refer to example above).")
        colorbar.append("   - To create your own color scheme, you can modify the ticks to the right side of the color bar.")
        colorbar.append("   - Ticks have four functionalities: Adding, Removing, Setting Position, and Setting Color:")
        colorbar.append("      - Adding Ticks:")
        colorbar.append("         - Click in the black space to the right of the color bar. You can add an arbitrary number of ticks.")
        colorbar.append("      - Removing Ticks")
        colorbar.append("         - You can only remove ticks until there are at least two left; you will not be allowed to remove any more otherwise. To remove a tick, right-click on it and click \"Remove Tick\".")
        colorbar.append("      - Setting Ticks")
        colorbar.append("         - To set the position of a tick, you can drag an existing tick to the desired position or right-click on it and select \"Set Position\".")
        colorbar.append("      - Setting Color")
        colorbar.append("         - This is the most useful feature for setting your own color scheme. The color of the tick can be modified by either double-clicking the tick or by right-clicking on it and selecting \"Set Color\".")
        layout3.addWidget(colorbar)
        layout3.addStretch()
        
        colorbar.moveCursor(QTextCursor.Start)
        
        page2.setLayout(layout2)    
        
        
    # index -> None
    # Plays all GIFS when the tab has been changed
    def onChange(self, i):
        if i == 0:
            self.navigategif.stop()
            self.levelsgif.stop()            
            self.navigategif.start()
            self.levelsgif.start()
        elif i == 1:
            self.roigif.stop()
            self.roigif.start()
            
        elif i == 2:
            self.colorbargif.stop()
            self.exportgif.stop()
            self.colorbargif.start()
            self.exportgif.start()            
    
    # event -> None
    # Stops all gifs (just in case) when the help window closes
    def closeEvent(self, event):
        self.navigategif.stop()
        self.levelsgif.stop()
        self.roigif.stop()
        self.colorbargif.stop()
        self.exportgif.stop()
        self.onedscangif.stop()
        self.onedgraphgif.stop()
        self.twodscangif.stop()
        self.twodgraphgif.stop()
        self.selectiongif.stop()
        self.dialgif.stop()
        
        self.win.show()
        self.win.raise_()
        
    # None -> None
    # Defines the layout for the "Other" screen of the help dialog
    
    def stack5UI(self):
        layout = QVBoxLayout()
        lbl = QLabel("Inputting Commands")
        lbl.setFont(QFont("Futura", 25))
        lbl.setStyleSheet("color: rgb(100, 159, 0);")
        layout.addWidget(lbl)
        commands = QTextBrowser()
        commands.setFont(QFont("Calibri", 18))
        commands.append("   - The Custom Command bar is a place where you can input specific SPEC commands.")
        commands.append("   - Inputting move and scan commands will update the GUI's position labels and graph.")
        layout.addWidget(commands)        
        commands.moveCursor(QTextCursor.Start)
        
        noteslabel = QLabel("General Notes")
        noteslabel.setFont(QFont("Futura", 25))
        noteslabel.setStyleSheet("color: rgb(100, 159, 0);")
        layout.addWidget(noteslabel)
        notes = QTextBrowser()
        notes.setFont(QFont("Calibri", 18))
        notes.append("   - The \"Refresh\" menu option only refreshes SpecPlot; MAR CCD has a heartbeat that runs a timer every 200 ms and updates SPECtre. SpecPlot, however, does not dynamically update to anything other than the user's own commands. Clicking \"Refresh\" will update all of SpecPlot.")
        layout.addWidget(notes)
        notes.moveCursor(QTextCursor.Start)
        
        bugslabel = QLabel("Currently Known Bugs")
        bugslabel.setFont(QFont("Futura", 25))
        bugslabel.setStyleSheet("color: rgb(159, 100, 0);")
        layout.addWidget(bugslabel)
        bugs = QTextBrowser()
        bugs.setFont(QFont("Calibri", 18))
        bugs.append("   - Sometimes, after you've completed a 1D scan, the Gaussian, Lorenztian, or Voigt fits will not display correctly or complete the curve. If this happens, try restarting SPECtre (it will take like two seconds). The 1D graph you just had should load back again and this time the fit should look right. If it still doesn't work, that's how the first is, I guess.")
        bugs.append("   - If you pause a scan or abort a scan, the buttons may still be disabled. Sorry I wasn't able to fix this in time. Just click \"Abort\" again and the buttons will be enabled again. You can even click \"Resume\" if you want to resume the scanning.")
        layout.addWidget(bugs)
        bugs.moveCursor(QTextCursor.Start)
        self.stack5.setLayout(layout)
        
# Not necessary but it helps to debug; runs the specmain.main function  
def main():
    specmain.main()

if __name__ == '__main__':
    main()
