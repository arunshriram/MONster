==================================================================
               MONster v1.1  - Linux GUI for MONhitp
==================================================================

# Written by Arun Shriram
# End date for v1.1: August 31, 2018
# For any questions please contact arun.shriram@gmail.com

==================================================================

INTRODUCTION
====================

MONster is a GUI application designed as a user-friendly and intuitive
way to conduct a variety of data processing on detector images. The GUI
was based on batch processing and stitching code written by 
Robert Tang-Kong, Fang Ren, and Melissa Wette. The GUI runs on Mac OS,

SPECtre is a GUI application designed as a user-friendly and intuitive
way to interface the SPEC terminal. SPECtre was originally designed by 
Stefan Mannsfeld in 2011, but it was designed for Windows. This new version
will allow you to work on OS X, Windows, and Linux! This version is only for 
Linux users. 

SPECtre will let you choose from a select
group of motors depending on whether you are a privileged user or a regular user.
These options should be modified by SSRL staff only, and only if necessary.

This Linux SPECtre can do anything the old SPECtre could do - plus more!
 
To run this program, you must have the following system requirements:

 - PyQt4
 - SIP 4.19.3
 - Python 2.7

The homepage of PyQt4 is http://www.riverbankcomputing.com/software/pyqt/.
If you wish to have a fresh download of PyQt4, visit
https://www.riverbankcomputing.com/software/pyqt/download

The homepage of SIP is http://www.riverbankcomputing.com/software/sip/.
If you wish to have a fresh download of SIP 4.19.3, visit
https://riverbankcomputing.com/software/sip/download

INSTALLATION
====================

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
that's what SPECtre was tested on). This will definitely NOT work on Python 3+.

RUNNING SPECTRE
=======================

To run the SPECtre GUI, simply enter the SPECtre folder and type the following.

        python SPECtre.py

This will load two windows: the GUI and a window that prompts you for the IP address.
Enter the IP address followed by the port. If you are using SPECtre on the same computer
as the SPEC terminal that you are trying to connect to, try:

        localhost:2034

However, if you are trying to connect to the SPECtre at a different beamline, try:

        192.168.14.1:2034

The address and port number will change depending on the beamline. Ask SSRL staff for help
if you are unable to connect.

Once you press "Enter" or click "Go", SPECtre will load previously scanned graph data, MAR data, 
and all available motors.



OTHER HELP
==================
For more detailed information, go to the Help menu in SPECtre.

Currently Known Bugs
--------------------
 - Sometimes, after you've completed a 1D scan, the Gaussian, Lorenztian, or Voigt fits will not display correctly or complete the curve. If this happens, try restarting SPECtre (it will take like two seconds). The 1D graph you just had should load back again and this time the fit should look right. If it still doesn't work, that's how the first is, I guess.
 - If you pause or abort a scan, the buttons may still be disabled. Sorry I wasn't able to fix this in time. Just click "Abort" again and the buttons should be enabled again. You can even click "Resume" if you want to resume the scan.
----------------------------------------------------
MOTORS
----------------------------------------------------

Motor Selection and Movement
----------------------------
 - Spectre can make only one motor move at a time. This motor is highlighted in purple to the left of 
the window, and as that motor moves you can see its position udpating on the screen. 
 - A single motor may be moved in real space using the "Move To" button. For example, if a motor is at 3 mm, entering in "15" 
will move that motor to position 15. You can tell when the motor has stopped moving when the "Position"
label has stopped updating.
 - To stop a motor before it has finished moving, or really, to stop anything, click the "Abort" button. This will send
an abort command to Spec that cannot be undone (unless you are doing a scan, in which case, click "Resume")
 - If you would like to move the motor to a relative position, click the "Move By" button. For example, if the selected
motor is currently at 3 mm, typing "-5" and then clicking "Move By" will move the motor to -2 mm, rather than -5 mm.

Dials
-----
 - Dial angles keep track of hardware limits and prevent complete loss of angles from alignment errors or computer failure.
The dial angles are generally made to agree with a physical indicator on each motor, such as a dial. User angles are related 
to the dial angels through the equation:
        user = sign x dial + offset
 - Redefining a user angle changes the internal value of offset. Dial angles are directly proportional to the values contained 
in the hardware controller registers. The sign of motion is set in the configuration file by the SPEC administrator and normally
isn't changed.
 - The "Set" button is used to set the dial position of a motor. If a motor is at 5 mm, you can set the user dial to whichever 
value you want it to be without moving the motor.

----------------------------------------------------
SCANS
----------------------------------------------------

SPECtre allows the user to perform two types of scans: 1D scans and 2D ("mesh") scans. Scans can be paused, resumed, and saved
as .CSV and .PNG files. To save as .CSV and .PNG, click the "Graph Options" menu option.

1D Scans
--------
 - 1D Scans use one motor and one coutner to createa graph of the counts vs. the motor position. To choose the 1D scan option,
choose "1D Scan" from the scan options to the left of the window.
 - To select the motor, select from the dropdown menu with the purple "Motor" label. To select the counter, choose from the dropdown
menu labeld "Chn".
 - You can use either Center/Halfwidth (C/W) parameters or Start/Finish (S/F) parameters:
   - C/W:
      - The Center parameter is the center of the scan radius. The Halfwidth parameter is the radius of the scan, or how far the scan
      will reach from the center. Once the scan completes, it will return the motors to the center position.
      - By default, motors will return to the center position after the scan completes.
   - S/F:
      - The Start parameter is the initial position of the scan, and the Finish parameter is the final position of the scan.
      - If you would like the scan to complete and leave the motors at the their final position, leave teh "move motors back" checkbox
      unchecked. If checked, the motors will be returned to their start position.
 - To choose how many points you would like in your scan, enter a number in the "Pts" section, and enter the time you would like for each
point to be scanned in the "Time" section.

2D Scans
--------
 - Mesh scans use one counter and two motors to create a two-dimensional plot, with the color of each segement based on a "jet" color
scale. Motor 1 is on the X-Axis of the plot, while Motor 2 is on the Y-Axis of the plot.
 - To access the mesh functionalities, click "2D Scan". Select a second motor and the counter that you would like to use.
 - You can use either Center/Halfwidth (C/W) parameters or Start/Finish (S/F) parameters (for each motor):
   - C/W:
      - The Center parameter is the center of the scan radius. The Halfwidth parameter is the radius of the scan, or how far the scan will reach from the center. Once the scan completes, it will return the motors to the center position.
   - S/F:
      - The Start parameter is the initial position of the scan, and the Finish parameter is the final position of the scan.")

----------------------------------------------------
GRAPHING
----------------------------------------------------

1D Graph
--------
 - Updates in real-time as SPECtre contacts SPEC for the data. Points are drawn in blue circles and are connected.
 - The Y-axis of the graph represents the selected counter; the X-axis of the graph represents the selected motor.
 - You can use the scroll wheel to zoom in and out of the graph. Dragging the mouse on the graph will draw a rectangle and zoom the graph to the contents of that rectangle. To autoscale and reset the position of the graph, simply right-click your mouse on the graph.
 - If you left click on the graph, the \"Selected Coordinates\" label will keep the position you selected for reference.
 - A crosshair will follow your mouse and will update its coordinates in the bright blue label.
 - You can select from three fits: Gaussian, Lorentzian, and Pseudo-Voigt; the last being a combination of Gaussian and Lorentzian. Once selected, the table below the graph will update with the appropriate data. When a fit is selected, the button will turn blue. If you want to remove the fit displayed, click the fit button again.
 - You can change the Y-Axis to be in Log Mode by clicking the "Log plot" checkbox. Similarly, you can change the Y-Axis to be in Derivative Mode by checking the "Derivative" box. Unchecking will reset the graph's mode.

2D Graph
--------
 - This graph will only appear when a 2D scan is being activated.
 - Updates in real-time as SPECtre contacts SPEC for the data. Points are drawn in colors according to the legend to the right hand side. The intervals of the legend update in real-time as well.
 - The horizontal axis represents the first motor, and the vertical axis represents the second motor. You can use the mouse to get the coordinates of each color by moving the mouse over the graph.
 - If you would like to move the motors to a certain position, you can left-click on a point on the graph and move the motors to that specific position. If you would like, you can then move the motors back to their original position just after the scan completed.

----------------------------------------------------
MAR
----------------------------------------------------

Controls
--------
 - Under "DATA DIRECTORY", you can choose the directory where MAR will save its .TIF images after collection. You can also edit what the file name will be (default is \"scan1\"). If the directory does not exist, SPECtre will create the directory.
 - Each file has its own unique time-stamped tag (you will see this in the console log when you begin collection), so you don't have to worry about renaming the file root every time; the file names will all be unique.
 - You can select between 1 and 99 series of frames. Each frame will be exposed for whatever number of seconds you would like (integers only). Entering a number in the "min delay" text box will set a delay between exposures.
 - Clicking "Collect" will send a job file to SPEC. If you want to cancel the current job file, click "Cancel". However, the current tasks will finish before MAR will cancel the remaining scheduled processes.
- The last three rows of the image controls section allow you to select the motors you would like to rock, move, and translate between series. You may enter the appropriate values in the text boxes.
 - If you want to manually open or close the MAR CCD shutter, click the "Shutter OPEN/CLOSED" button at the bottom right-hand-side of the screen.

How to Navigate the Graph
-------------------------
 - The following instructions apply when the mouse is directly over the graph, not over another part of the window or over the ROI. To zoom in or out, scroll up and down with the mouse. The plot will zoom into the mouse's position.
 - Right-click the graph and go to "Mouse Mode".
   - If "3 button" is selected:
      - Left-clicking and dragging the mouse will let you move the graph around.
   - If "1 button" is selected:
      - Left-clicking and dragging the mouse will let you draw a rectangle. The graph's viewing area will then zoom into that rectangle.
      - This does not set the graph's ROI. You can only equalize the graph when you move the ROI to the region you are analyzing. See next page for more information.

How to Change Your Viewing Levels
---------------------------------
 - To the right of the graph is the histogram. If the image does not show, or if you wish to change which part of the image correlates to the color bar, you can drag the top and bottom gold bar on the histogram up and down.
 - For example, if the image is completely black, try slowly dragging the top gold line downwards.

How to Return to Full View
--------------------------
 - If you find yourself too zoomed in or out of the histogram, graph, or ROI line, you can right click on the area you wish to rescale and click "View all".
 - This will not necessarily return the area to its original view (as soon as the exposure finished), but rather will scale the area to the selected viewing area. To reset the graph, ROI, ROI line, and histogram to their original views, click the "Restore Graph" button below the graph.

How to Select Your ROI (Region of Interest)
-------------------------------------------
 - To view the ROI, click the "ROI" button below the histogram.
 - The ROI is the Region of Interest. It creates a box in the graph that you can rotate, scale, and move around the image. Wherever you zoom in or out, if you click ROI, the box will appear within your viewing range. With this ROI, you can study several things:
   - Equalization:
      - If you select an ROI, you can equalize the rest of the image to match the intensity levels of the region of interest. For example, selecting an area with a minimum value of 20 and a maximum value of 300 will set the minimum value for the rest of the graph to be 20 and the maximum value to be 300.
   - ROI Plot:
      - Selecting the ROI box will allow you to see a 1-dimensional representation of the region you are viewing. As you drag the box around, a graph will pop up below the image, allowing you to see trend lines and to identify any peaks or patterns.
      - Right-clicking on this graph will give you various options, including inverting the X and Y axes, exporting, mouse mode, and viewing the graph grid (under "Plot Options").
 - If you do not wish to see the 1-dimensional graph but would like to just move the box, click and drag the dividing line between the graph and the image all the way down. Likewise, if you would like to just see the 1-dimensional graph, click and drag the dividing line all the way up.
 - One thing to remember is that clicking "Equalize" will equalize the rest of the image only according to the region you have selected, not the current view of the image; zooming in and clicking "Equalize" is not enough. Once you zoom into where you want to equalize, click ROI and adjust the boundaries first. Then you can equalize.

How to Export The Graph
-----------------------
 - There are two options to export your graphs. The first is to click "Menu" and then "Export". This option is the quickest and easiest way to save the ENTIRE image as any image format. However, if you do not specify your image format, the image will not save.
 - For more complex exporting options (including the ability to export as CSV, SVG, Image File, Matplotlib Window, and to export only your current view, a.k.a. VIEWBOX, instead of the entire graph), right-click on the graph itself and select the "Export" option.
 - To export the 1-dimensional ROI plot or the histogram, right click on the region you wish to export and click "Export".

How to Change The Color Bar
---------------------------
 - By default, images are displayed with the "jet" color map. To change the colors, you have two options: either select from one of the provided colorbars or create your own temporary color scheme.
 - To select a default color bar, right-click the color bar and select the scheme you would like to use. This may create new ticks to the right hand side. These ticks can be used to inverse the color scheme by dragging them to oppostite locations on the color bar.
 - To create your own color scheme, you can modify the ticks to the right side of the color bar.
 - Ticks have four functionalities: Adding, Removing, Setting Position, and Setting Color:
   - Adding Ticks:
      - Click in the black space to the right of the color bar. You can add an arbitrary number of ticks.
   - Removing Ticks:
      - You can only remove ticks until there are at least two left; you will not be allowed to remove any more otherwise. To remove a tick, right-click on it and click "Remove Tick".
   - Setting Ticks:
      - To set the position of a tick, you can drag an existing tick to the desired position or right-click on it and select "Set Position".
   - Setting Color:
      - This is the most useful feature for setting your own color scheme. The color of the tick can be modified by either double-clicking the tick or by right-clicking on it and selecting "Set Color".

----------------------------------------------------
OTHER
----------------------------------------------------

Inputting Commands
------------------
 - The Custom Command bar is a place where you can input specific SPEC commands.
 - Inputting move and scan commands will update the GUI's position labels and graph.

General Notes
-------------
 - The "Refresh" menu option only refreshes SpecPlot; MAR CCD has a heartbeat that runs a timer every 200 ms and updates SPECtre. SpecPlot, however, does not dynamically update to anything other than the user's own commands. Clicking "Refresh" will update all of SpecPlot.

