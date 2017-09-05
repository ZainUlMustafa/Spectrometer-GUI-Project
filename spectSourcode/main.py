'''Python 27'''
'''Produced by Sourcode'''

# Steps:
''' Serial Port Setup and Connection Establishment '''
# 1. Create setup window
# 2. Setup radio button for com port
# 3. Make connection with com port prior to radio button selected
# 4. After comm.py has setup the Serial
# 5. Clear the current radio button, and create control buttons for Spectrometer
# 6. Click readSerial button to begin reading from Serial
''' Filing, Advanced Calculations, and Plotting '''
# 7. Save the read data into a .txt formatted file
# 8. After manual checking, click readFile button to start reading the file
# 9. Perform some data manipulations and save coordinates into dynamic arrays
# 10. Plot the graph

import numpy as np
import matplotlib.pyplot as plt
import atexit
from Tkinter import*
from comm import *
from serial import SerialException


def exitHandler():
    print 'Attempting to end serial com...'
    closeSerial()


# atexit will register exit handler to end serial com when program is closed
atexit.register(exitHandler)

root = Tk()
root.title('Spectrometer')
root.minsize(500, 500)
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
    for child in mainFrame.winfo_children():
        child.destroy()
        
    # Radio Buttons require Variable classes to work properly
    # commRadioVar will be a variable for rSelect
    # so whatever you will have to do with rSelect, you will use commRadioVar
    # e.g. get the radio button current state (selected or unselected)? use commRadioVar 
    commRadioVar = StringVar()
    
    # Exception check to verify if com port is available
    try:
        ser = serial.Serial('COM3', 9600)
        connection = True
    except SerialException:
        connection = False
        
    # Exception returns a connection boolean result
    # so you can take relevant actions
    if connection == True:
        rSelect = Radiobutton(mainFrame, text='COM3', variable=commRadioVar, value='COM3')
        rSelect.config(command=rPress)
        rSelect.pack()
    elif connection == False:
        lNoPort = Label(mainFrame, text='No port available!\nSuggestion: Try reconnecting the USB')
        lNoPort.pack()

    
def mainScreen():
    global mainFrame
    # Destroy the elements of the current mainFrame (Radio button and label made for com port selection)
    # You do that just in order to place new widgets in the mainFrame
    for child in mainFrame.winfo_children():
        child.destroy()
    
    # Creating control buttons
    # for reading from serial port and start filing them
    # Use lambda during function callback as we want the function to be called only when the button is pressed
    receiveButton = Button(mainFrame, text='Receive from Serial')
    receiveButton.config(command=lambda: receiveFromSerial(receiveButton))
    
    saveDataButton = Button(mainFrame, text='Save data')
    saveDataButton.config(command=lambda: saveDataToFile(saveDataButton))
    
    # Making a grid layout
    receiveButton.grid(row=0, column=0)
    saveDataButton.grid(row=1, column=0)
    

def receiveFromSerial(receiveButton):
    global count
    count = 1
    count = importData(receiveString, count)
        

def saveDataToFile(saveDataButton):
    global count
    print 'saveData button works'
    print count
    if count == 20:
        print 'Data saving started...'
        # Save received data into received.txt
        csv_receive_info = open('received.txt', 'w')
        for i in range(count):
            csv_receive_info.write(str(receiveString[i]) + '\n')
        print 'Data saving complete'
    else:
        print 'Data not completely received, cannot save!'
    

def rPress():
    global commRadioVar
    serialCommSetup(commRadioVar.get())
    # Now after serial communication is set up
    # go to mainScreen() function where control buttons are present
    mainScreen()


setupComm()
runProgram()
    