from MotorModule import Motor
import PS4Joystick as js
from time import sleep

motor = Motor()
#motor.move(0.3,0,2)
#motor.move(0.3,-0.2,2) ## Speed, Turn
#motor.forward(30,2)
#motor.stop(0,2) 
movement = 'Joystick'

## Hints
# Forward (0.3,0,2) 
# Backward (-0.3,0,2) 
# Right Forward (0.3,0.2,2) 
# Left Forward (0.3,-0.2,2) 

def main():
    if movement == 'Joystick':
        jsVal = js.getJS()
        #motor.move(-(jsVal['axis2']), -(jsVal['axis1']),0.1)
        #print(-(jsVal['axis2']), -(jsVal['axis1']))
        motor.move(-(jsVal['axis2']), (jsVal['axis1']),0.1)
        #sleep(0.1)

if __name__ == '__main__':
    while True:
        main()
