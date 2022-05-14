import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class Motor():
    def __init__(self, *args, **kwargs):
        super(Motor, self).__init__(*args, **kwargs)
        self.left_motor_pwm = 33
        self.right_motor_pwm = 32
        self.left_motor = [35,36]
        self.right_motor = [38,37]

        GPIO.setup(self.left_motor_pwm, GPIO.OUT)
        GPIO.setup(self.right_motor_pwm, GPIO.OUT)
        GPIO.setup(self.left_motor[0], GPIO.OUT)
        GPIO.setup(self.left_motor[1], GPIO.OUT)
        GPIO.setup(self.right_motor[0], GPIO.OUT)
        GPIO.setup(self.right_motor[1], GPIO.OUT)
        self.pwm = [GPIO.PWM(self.left_motor_pwm,50), GPIO.PWM(self.right_motor_pwm,50)]
        self.pwm[0].start(0)
        self.pwm[1].start(0)

    def forward(self,speed=1.0, t=0):
        print("Forward")
        GPIO.output(self.left_motor[0], GPIO.HIGH)
        GPIO.output(self.right_motor[0], GPIO.HIGH)
        GPIO.output(self.left_motor[1], GPIO.LOW)
        GPIO.output(self.right_motor[1], GPIO.LOW)
        self.pwm[0].ChangeDutyCycle(speed)
        self.pwm[1].ChangeDutyCycle(speed)
        sleep(t)
    
    def backward(self,speed=1.0, t=0):
        print("Backward")
        GPIO.output(self.left_motor[0],GPIO.LOW)
        GPIO.output(self.right_motor[0],GPIO.LOW) 
        GPIO.output(self.left_motor[1],GPIO.HIGH)
        GPIO.output(self.right_motor[1],GPIO.HIGH) 
        self.pwm[0].ChangeDutyCycle(speed)
        self.pwm[1].ChangeDutyCycle(speed)
        sleep(t)
    
    def stop(self,speed=1.0, t=0):
        print("Stop")
        GPIO.output(self.left_motor[0], GPIO.LOW)
        GPIO.output(self.right_motor[0], GPIO.LOW)
        GPIO.output(self.left_motor[1], GPIO.LOW)
        GPIO.output(self.right_motor[1], GPIO.LOW)
        self.pwm[0].ChangeDutyCycle(speed)
        self.pwm[1].ChangeDutyCycle(speed)
        sleep(t)

    def move(self, speed=0.5, turn=0, t=0):
        speed *=100
        turn *=100
        leftSpeed = speed - turn
        rightSpeed = speed + turn
        print(leftSpeed, rightSpeed)

        if leftSpeed > 100 : leftSpeed = 100
        elif leftSpeed <-100: leftSpeed = -100
        if rightSpeed > 100 : rightSpeed = 100
        elif rightSpeed <-100: rightSpeed = -100

        self.pwm[0].ChangeDutyCycle(abs(leftSpeed))
        self.pwm[1].ChangeDutyCycle(abs(rightSpeed))

        if leftSpeed > 0 :
            GPIO.output(self.left_motor[0], GPIO.HIGH)
            #GPIO.output(self.right_motor[0], GPIO.LOW)
            GPIO.output(self.left_motor[1], GPIO.LOW)
            #GPIO.output(self.right_motor[1], GPIO.LOW)
            #sleep(t)

        else:
            GPIO.output(self.left_motor[0], GPIO.LOW)
            #GPIO.output(self.right_motor[0], GPIO.LOW)
            GPIO.output(self.left_motor[1], GPIO.HIGH)
           # GPIO.output(self.right_motor[1], GPIO.LOW)
            #sleep(t)


        if rightSpeed >0 :
            #GPIO.output(self.left_motor[0], GPIO.HIGH)
            GPIO.output(self.right_motor[0], GPIO.HIGH)
            #GPIO.output(self.left_motor[1], GPIO.LOW)
            GPIO.output(self.right_motor[1], GPIO.LOW)
            #sleep(t)

        else:
            #GPIO.output(self.left_motor[0], GPIO.HIGH)
            GPIO.output(self.right_motor[0], GPIO.LOW)
            #GPIO.output(self.left_motor[1], GPIO.LOW)
            GPIO.output(self.right_motor[1], GPIO.HIGH)
        sleep(t)
def main():
    motor1.forward(30,2)
    motor1.stop(0,2)
    motor1.backward(30,2)
    motor1.stop(0,2)
    GPIO.cleanup()

if __name__ == '__main__':
    motor1 = Motor()
    main()


