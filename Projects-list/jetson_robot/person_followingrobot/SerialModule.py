import serial
import os
from time import sleep

os.system('sudo chmod 666 /dev/ttyACM0')

def initConnection(portNo, baudrate):
    try:
        ser = serial.Serial(portNo, baudrate)
        print("Device Connected")
        return ser
    except:
        print("Not Connected")

def sendData(se, data, digits):
    myString="$"
    for d in data:
        myString +=str(d).zfill(digits)
    try:
        se.write(myString.encode())
        print(myString)
    except:
        print("Data Transmission Failed")
        
if __name__ == "__main__":
    ser = initConnection("/dev/ttyACM0",9600)
    #while True:
        
    