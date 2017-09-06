''' Produced by Sourcode '''
''' v. 1.2 '''

import serial
from serial import SerialException


def exceptionCheckPort(comPort):
    global ser
    try:
        ser = serial.Serial(comPort, 9600)
        return True
    except SerialException:
        return False


def serialCommSetup(comPort):
    global ser
    #ser = serial.Serial(comPort, 9600)
    print 'COM Port: ' + comPort + ' || BAUD: ' + str(9600)

    
def importData(receiveString, count):
    global ser
    # Turning the onboard LED on just to make sure serial com is built successfully
    ser.write('1')
    for count in range(21):
        #receiveString.append(count+1)
        receiveString.append(str(ser.read()))
        print receiveString[count] 
    return count


def closeSerial():
    global ser
    # Check the existence of a global variable (ser)
    # if global variable (ser) exists then close the serial com
    if 'ser' in globals():
        ser.close()
        print '-> Serial closed'
    else:
        print '-> Serial not opened'  
