# Spectrometer-GUI-Project
This project is designed for a custom built and redesigned spectrometer by NUST Karachi. This GUI gets the data from sensors and is aimed to perform some advanced calculations and later plot the graph. Required from R&D to add just a couple of buttons to do the whole job and it must have a very simple but efficient UI.

NOTE: This project isn't complete, I am currently working on it. This repository is shared here just to make it available to all team members of this project.

Update 7 September 2017
main.py and comm.py are completely redesigned with completely automated serial port recognizer and handler. Added a proper try-except exception to only the selected serial port to avoid resetting other ports that may be connected with the software and are busy. This software works perfectly on Win machine but I haven't tested it on Linux or Mac yet. If you see this code, please perform the tests and add the results in this README.md file. I am currently at this time working on efficiency of this GUI.

Update 6 September 2017
File received over serial port is error free with some added delay in the script to allow the serial receiver to get reset.

Update 5 September 2017
Currently the serial communication is built successfully. Filing and saving raw data into the received.txt is completed but will not perfectly work.
