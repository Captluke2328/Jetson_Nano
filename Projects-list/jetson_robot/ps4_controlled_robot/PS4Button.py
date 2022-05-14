import serial
import PS4Joystick as js
from time import sleep

with serial.Serial('/dev/ttyACM0',9600,timeout=10) as ser:
    while True:
        jsVal = js.getJS()
        if (jsVal['t']):
            ser.write(bytes('F\n', 'utf-8'))
            
        if (jsVal['x']):
            ser.write(bytes('B\n', 'utf-8'))
            
        if (jsVal['s']):
            ser.write(bytes('L\n', 'utf-8'))
        
        if (jsVal['o']):
            ser.write(bytes('R\n', 'utf-8'))
            
        else:
            ser.write(bytes('S\n', 'utf-8'))
            
        
        