import serial

with serial.Serial('/dev/ttyACM0', 9600, timeout=10) as ser:
    while True:
        led_on = input("Do you want to send the data ?")[0]
        if led_on in 'yF':
            ser.write(bytes('F\n', 'utf-8'))
        if led_on in 'nB':
            ser.write(bytes('B\n', 'utf-8'))
        if led_on in 'nL':
            ser.write(bytes('L\n', 'utf-8'))
        if led_on in 'nR':
            ser.write(bytes('R\n', 'utf-8'))