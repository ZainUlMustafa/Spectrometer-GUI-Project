''' Python 27 '''
''' Produced by Sourcode '''
''' v. 1.5.1 '''

import serial.tools.list_ports
import numpy as np
import matplotlib.pyplot as plt
import atexit
import time
import os
import _csv as csv
from Tkinter import*
from comm import *


def exitHandler():
    print 'Attempting to end serial com...'
    closeSerial()


# atexit will register exit handler to end serial com when program is closed
atexit.register(exitHandler)

root = Tk()
root.title('Spectrometer Serial Data Plotter')
root.iconbitmap('D:/Sciencestic Knowledgebase/logos/zams16-17.ico')
root.minsize(450, 200)
receiveString = []
ser = serial.Serial


def setupComm():
    global mainFrame
    mainFrame = Frame(root)
    mainFrame.pack()
    commSelection()

    
def runProgram():
    root.mainloop()

    
def commSelection():
    global mainFrame, commRadioVar, connection
    # Destroy the elements of the current mainFrame (Controls Button /OR otherwise)
    # You do that just in order to place new widgets in the mainFrame
    for child in mainFrame.winfo_children():
        child.destroy()
        
    # list of all available ports
    portList = list(serial.tools.list_ports.comports())
    s_portList = []
    for spl in portList:
        s_portList.append(str(spl))
    
    # Convert the list into numpy list
    # and check if the numpy list is not empty
    # If empty then no ports are found
    np_s_portList = np.array(s_portList)
    if np.size(np_s_portList) == 0:
        connection = False
    else:
        connection = True
    
    # Radio Buttons require Variable classes to work properly
    # commRadioVar will be a variable for rSelect
    # so whatever you will have to do with rSelect, you will use commRadioVar
    # e.g. get the radio button current state (selected or unselected)? use commRadioVar 
    commRadioVar = StringVar()
    
    if connection == True:
        # Listing all available ports on GUI
        lAllPorts = Label(mainFrame, text='Available Port(s)')
        lAllPorts.grid(pady=5)
        for pl in s_portList:
            print pl + ' -> ' +str(type(pl))        #Printing the type of pl to check if everything is ok
            p_pl = pl.partition(' ')[0]             #Extracting the name of the port from pl
            rSelect = Radiobutton(mainFrame, text=pl, variable=commRadioVar, value=p_pl)
            rSelect.config(command=rPress)
            rSelect.grid(pady=20)
    elif connection == False:
        lNoPort = Label(mainFrame, text='No port available!\n\nSuggestions:\n 1. Try reconnecting the USB\n 2. Close the previously opened Spectrometer app')
        lNoPort.grid(pady=40)

    
def mainScreen():
    global mainFrame
    # Destroy the elements of the current mainFrame (Radio button and label made for com port selection)
    # You do that just in order to place new widgets in the mainFrame
    for child in mainFrame.winfo_children():
        child.destroy()
    
    # Creating control buttons
    # for reading from serial port and start filing them
    # Use lambda during function callback as we want the function to be called only when the button is pressed
    
    l_receiveFromSerial = Label(mainFrame, text='Receive from Serial')
    receiveButton = Button(mainFrame, text='Receive', fg='white', bg='blue', height=1, width=10)
    receiveButton.config(command=lambda: receiveFromSerial(receiveButton))
    
    l_saveData = Label(mainFrame, text='Save Data')
    saveDataButton = Button(mainFrame, text='Save', fg='white', bg='blue', height=1, width=10)
    saveDataButton.config(command=lambda: saveDataToFile(saveDataButton))
    
    l_readFileDir = Label(mainFrame, text='Read the file from directory')
    readFileDirButton = Button(mainFrame, text='Read', fg='white', bg='blue', height=1, width=10)
    readFileDirButton.config(command=lambda: readFileFromDir(readFileDirButton))
    
    # Making a grid layout
    # Added a delay of 3 seconds to allow the serial port to get reset
    time.sleep(3)
    l_receiveFromSerial.grid(row=0, column=0, sticky=E, padx=20, pady=20)
    receiveButton.grid(row=0, column=1)
    
    l_saveData.grid(row=1, column=0, sticky=E, padx=20)
    saveDataButton.grid(row=1, column=1)
    
    l_readFileDir.grid(row=2, column=0, sticky=E, padx=20, pady=20)
    readFileDirButton.grid(row=2, column=1)
    

def receiveFromSerial(receiveButton):
    global count
    count = 1
    count = importData(receiveString, count)
        

def saveDataToFile(saveDataButton):
    global count
    print 'saveDataButton works'
    print count
    if count == 20:
        print 'Data saving started...'
        # Save received data into received.txt
        csv_receive_info = open('received.txt', 'w')
        for i in range(count):
            csv_receive_info.write(str(receiveString[i]) + ',' + str(int(receiveString[i]) **2) + '\n')
        print 'Data saving complete'
        csv_receive_info.close()
    else:
        print 'Data not completely received, cannot save!'
    

def readFileFromDir(readFileDirButton):
    x, y = [], []
    print 'readFileDirButton works'
    # Checking if the file is not empty
    if os.stat('received.txt').st_size == 0:
        print 'File is empty'
        return 0
    csv_file_dir = open('received.txt', 'r')
    fileDirReader = csv.reader(csv_file_dir, delimiter=',')
    for row in fileDirReader:
        x.append(row[0])
        y.append(row[1])
    csv_file_dir.close()
    np_x = np.array(x)
    np_y = np.array(y)
    plt.scatter(np_x, np_y)
    print 'Graph plotted successfully!'
    plt.show()


def rPress():
    global commRadioVar
    # Exception check to verify if com port is available
    # Exception returns a boolean result
    # so you can take relevant actions accordingly
    if exceptionCheckPort(commRadioVar.get()) == True:
        serialCommSetup(commRadioVar.get())
        # Now after serial communication is set up
        # go to mainScreen() function where control buttons are present
        mainScreen()
    else:
        print 'Selected COM port is busy, select other one if available'
        commSelection()

setupComm()
runProgram()
    
