---------------------------------------------------------------------
Files Required
---------------------------------------------------------------------
ExifData.py
imageTamper.py
imageTamperUI.py

---------------------------------------------------------------------
Dependencies
---------------------------------------------------------------------
wx: 4.0.4 msw (phoenix) wxWidgets 3.0.5
piexif: 1.1.2

---------------------------------------------------------------------
Description
---------------------------------------------------------------------
This program provides a GUI for the imageTamper class. imageTamperUI.py should be
used to run the program. imageTamper.py serves as a helper class providing
some random value calculations and writing the file out. The ExifData class handles
the transition between the pie exif native data format and a flat format that
is easier to handle in the UI.

Through the UI you can randomize latitude, longitude, direction, date, and time
values for the specified picture. You can also modify these values by hand using 
the controls. Then you can save out a new file with those values.

---------------------------------------------------------------------
Usage Instructions
---------------------------------------------------------------------
This program has no command line parsing available. To run the GUI, you need to call
the imageTamperUI.py script. Depends on the installation of additional libraries
wxPython and piexif. Versions listed above. wx library must provide wx.adv to support
some controls.

---------------------------------------------------------------------
Examples:
---------------------------------------------------------------------

python "C:\Users\User\imageTamperUI.py"

---------------------------------------------------------------------
Known Issues:
---------------------------------------------------------------------
No bugs. Error checking on parameters is minimal.