==========================================================================================
               MONster v1.1  - Linux, Windows, and Mac OS X GUI for MONhitp
==========================================================================================

# Written by Arun Shriram
# End date for v1.1: August 31, 2018
# For any questions please contact arun.shriram@gmail.com

==================================================================

INTRODUCTION
====================

MONster is a GUI application designed as a user-friendly and intuitive
way to conduct a variety of data processing on detector images. The GUI
was based on batch processing and stitching code written by 
Robert Tang-Kong, Fang Ren, and Melissa Wette. The GUI runs on Mac OS X,
Windows, and Linux. 
 
To run this program, you must have the following system requirements:

 - PyQt4
 - SIP 4.19.3 (optional, but if it requires it, download and install it)
 - Python 2.7
 - pyFAI
 - numpy
 - scikit-image
 - scipy
 - fabio
 - pandas
 - PIL

It may seem like a pain, but it's worth it :)

INSTALLATION
====================

The homepage of PyQt4 is http://www.riverbankcomputing.com/software/pyqt/.
If you wish to have a fresh download of PyQt4, visit
https://www.riverbankcomputing.com/software/pyqt/download

The homepage of SIP is http://www.riverbankcomputing.com/software/sip/.
If you wish to have a fresh download of SIP 4.19.3, visit
https://riverbankcomputing.com/software/sip/download

Most, if not all, of these dependencies can be installed using pip, in
the format:
	
	pip install --user -U pyFAI

If you also have python3 installed on your computer, use
	
	pip2.7 install --user -U pyFAI

to install your packages.

The first step is to configure PyQt4. To do this, either download PyQt4 fresh 
from the website or go to the 'dependencies' folder and unzip the PyQt4 file. 
There, configure PyQT4 by running the following command.

	python configure-ng.py

This assumes that the correct Python interpreter is on your path.

If you have multiple versions of Python installed then make sure you use the
interpreter for which you wish to generate bindings for.

The configure-ng.py script takes many options.  Use the "--help" command line
option to display a full list of the available options.

The next step is to build PyQt4 using your platform's make command.

	make

The final step is to install PyQt4 by running the following command.
(Depending on your system you may require root or administrator privileges.)

	make install

The second and last step is to configure SIP 4.19.3. The steps are nearly the same
as above. Once you extract from the .tar.gz file:

        cd /path/to/src/sip-4.19.3
        
        python configure.py
        
        make

        make install

Lastly, make sure that you are running Python 2.7 (preferably Python v2.7.5, because
that's what MONster was tested on). This program will definitely NOT work on Python 3+.

RUNNING MONster
=======================

To run the MONster GUI, simply enter "mon" into your terminal window. If this
alias hasn't been set up yet, simply enter the MONster folder and type the following.

	python MONster.py
	
If you have not run any processes yet, or have deleted the "thisRun.txt" file in the
Bookkeeping folder in your home directory, this will load two windows: the GUI
and the help menu.

If your Properties.csv file is uncorrupted/located, MONster will load all previous
run data, making it easier to see what you were last doing.

Upon closing MONster, you will be prompted to save console log data (unless you hard
quit with Control+Q). You can specify your console log save location under 
	
	File -> Change log file save location


OTHER HELP
==================
For more detailed information, go to the Help menu in MONster.

Currently Known Bugs
--------------------
 - 
----------------------------------------------------
MACROS
----------------------------------------------------

What are Macros?
----------------------------
 - Macros are a convenient way to store information about a certain process or set of 
instructions you wish the program to follow.
 - MONster uses macros (in the form of CSV files) to store all the information you input, 
like data sources, calibration info, Q and Chi ranges, and more, to later add to the Queue.

How to Use Macros in MONster
----------------------------
 - On the Transform, Stitch, and Integrate pages, you can save all the information on each 
page as an individual macro by clicking the "Save as a macro" buttons.
 - This will take data sources, processed locations, detectors - basically all the information 
you input, and save it as an instruction for MONster to process in the Queue.
 - You can also save and add macros to the queue by clicking "Add this configuration to the 
queue". This will save the macro AND add it to the Queue.

----------------------------------------------------
TRANSFORM
----------------------------------------------------

What is Transform?
------------------
 - Transforming is mapping detector images to q-chi space!

Data Source Selection
---------------------
 - MONster accepts either .raw or .tif images for transforming.
 - If you wish to select an entire folder, click the "Select a folder" button.
 - To select one or more files, click the "Select one or more files" button and select your files. 
To select multiple, click one file, hold shift, and click another file. To select specific files, hold 
control and left click on the files you wish to select.
 - When selecting .raw files, be sure to select your detector from the dropdown menu.
 - If your detector is not in the dropdown menu, go to Edit->Add or remove detectors and add your 
detector!

Calibration
-----------
 - There are two ways of setting your calibration: manually enter each value, or selecting a 
previously existing calib file.
 - To select a calib file, click the folder icon and choose your file. The values will automatically 
fill in, and if you want, you can tweak these values. 
 - You can choose to save your tweaked values as a new calibration file by clicking the "Save this 
calibration!" button.

Processed Files
----------------
  - By default, processed files will be stored in a folder called "Processed_Transform" inside the 
selected data directory.
  - If you do not change the processed file directory from run to run, each run will overwrite the 
previous run's processed data!

----------------------------------------------------
STITCH
----------------------------------------------------

What is Stitching?
------------------
 - Stitching is an easy tool to combine images together! Select multiple files from a detector scan 
and let the program work its magic!
 - Note: Unfortunately, if you would like to stitch images taken with different detector positions, 
you will have to supply the correct calibration file for each image and transform them individually.

How to Stitch Your Files
------------------------
 - Using Stitch is very simple. Select the folder with the .mat data you wish to process by clicking 
the folder button.
 - By default, processed files will be stored in a folder called "Processed_Stitch" inside the 
selected data directory.
 - If you do not change the processed file directory from run to run, each run will overwrite the 
previous run's processed data!

----------------------------------------------------
INTEGRATE
----------------------------------------------------

What is Integrate?
------------------
 - Integration takes processed transform data and perform column-wise averaging to create a one-dimensional 
graph of the image.

How to Integrate
----------------
 - If you wish to select an entire folder for your data, click the "Select a folder" button, and click 
the folder icon.
 - To select one or more files, click the "Select one or more files" button and select your files. To 
select multiple, click one file, hold shift, and click another file.  To select specific files, hold control and 
left click on the files you wish to select.")
 - MONster only accepts .mat files for Integration.
 - By default, processed files will be stored in a folder called "Processed_Integrate" inside the selected 
data directory.
 - If you do not change the processed file directory from run to run, each run will overwrite the previous 
run's processed data!
 - Be sure to input the Q and Chi range values between which MONster should perform the integration.

How to Navigate the Graph
-------------------------
 - To zoom into a rectangular region of the graph, move your cursor over the graph, left click, and drag.
 - To zoom in or out, move your cursor over the graph and use the scroll wheel.
 - To reset the graph to its original range, right click on the graph.

----------------------------------------------------
QUEUE LOADER
----------------------------------------------------

What is the Queue Loader?
-------------------------
 - The Queue Loader is a tool to help you make processes more automated and run with less continual 
management.
 - Using the Queue Loader, you can leave MONster running overnight or for hours, transforming, stitching, 
or integrating your files in the background.
 - The Queue Loader uses macros to save, store, and load the information you use to calibrate each 
process you wish to execute.

The Macro Editor
----------------
- To open the Macro Editor, click the "+" button or double click an existing process.
- There are two kinds of macros you can create: worfklow macros or independent macros.
- Workflow Macros
  - Workflow macros follow a certain path of data processing: transform images, stitch the transformed images 
together, and integrate those transformed images.
  - To use workflow macros, do the following: input your data source, calibration information, processed file 
location, and detector if necessary in the Transform page of the Macro Editor. Then add your Q and Chi ranges in 
the Integrate page of the Macro Editor, save your macro, and add it to the queue!
- Independent Macros:
  - Independent macros hold at least one process: Transform, Stitch, and Integrate. However, you can choose to 
omit any processes you want. Each process is independent of the other; you should select different data sources 
for transforming, stitching, and integration.
- When saving your macro, each file has its own unique time-stamped tag, so you don't have to worry about 
renaming the file root every time; the file names will all be unique. However, you can still choose to rename the 
macros for convenience sake.
- If you've already created a macro, you can load it into the queue by clicking "Load a macro".

The Queue
---------
- The Queue is where you can see and manage all the loaded macros. To add a macro the queue, click "+", and to 
remove a macro from the queue, select your macro and click "-".
- Before the queue starts, be sure to check whether the checkbox "Take me to each tab during each process" is 
checked. If it is, that means that MONster will automatically switch tabs every time a new process begins. Otherwise, 
you will remain on the Queue Loader page unless you manually switch tabs.
- While the queue is running, you can pause or terminate the queue. Pausing the queue will temporarily stop the 
queue after whatever process (transform, stitch, integrate) is currently running finishes. Once the queue pauses, 
you can either restart the queue, resume the queue, or terminate the queue. If you choose to terminate the queue in 
the middle of a process, it will finish that process before terminating.
- If you want to skip a process, such as skipping the transform, just go to the transform page and hit abort!
- If you have added several macros the queue, quit MONster, and restart it later, you can save yourself the trouble of 
selecting those macros all over again by saving the queue before you exit MONster. MONster saves the queue as a JSON 
file, with all the macros and their information stored in the queue. When you want to load the queue back into MONster, 
click "Load a queue" to clear all elements currently in the queue and replace them with the saved queue.

----------------------------------------------------
OTHER
----------------------------------------------------

Menu Options
------------
- File:
  - To set the location where you want console logs to be saved, go to File->Change log file save location.
- Edit:
  - MONster saves all its previous run information in a file called Properties.csv. To clear all previous run information, 
click Edit->Clear previous run information.
  - If your detector is not in the detector dropdown menu on the Transform page, click Edit->Add or remove a detector to 
configure your detectors. Clearing the previous run information will reset any added detectors aside from the defaults.

