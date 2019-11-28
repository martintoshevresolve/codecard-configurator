
# initialise modules..
import warnings
import time
import binascii
import serial
import serial.tools.list_ports
from art import *

# menu..
print ("\r\n")
strTitle=text2art("CodeCard")
print(strTitle, "Oracle Code Card Configurator..")
print("=========================================================")
print ("\r\n")

print("PURPOSE:")
print ("  Code Card Configurator will update your Code Card configuration settings and perform")
print ("  button 'A' shortpress test..")
print ("\r\n")

print("DIRECTIONS:")
print ("  1. Plug-in your Code Card")
print ("  2. Turn on the Code Card (i.e. via hardware power switch)")
print ("  3. Press 'Enter' to start the process")
print ("  4. On your Code Card, perform simultaneous button 'A+B' shortpress\r\n","    to boot the Code Card into Configuration Mode")

print ("\r\n")
print ("  Your card will be automatically configured - progress will be logged to stdout")
print ("\r\n")

print("WHEN READY:")
print ("  Ensure steps 1&2 are complete, then..")
input("  Press Enter to continue...")

print ("\r\n")
print ("-------------------")
print ("\r\n")

# list all serial ports..
print ("ENUMERATING PORTS:")
for p in serial.tools.list_ports.comports():
    print ("  Port Details:")
    print ("    Device:  " , p.device)
    print ("    Description:  " , p.description)

# identify our code card by the `CP210x` string in the port description..
#   win: "Silicon Labs CP210x USB to UART Bridge"
#   mac: "CP2104 USB to UART Bridge Controller"
codecard_port = [
    p.device
    for p in serial.tools.list_ports.comports()
    if 'Silicon Labs CP210x USB to UART Bridge' in p.description or 'CP2104 USB to UART Bridge Controller' in p.description
]

# exceptions..
if not codecard_port:
    raise IOError("No Code Card found !!")
if len(codecard_port) > 1:
    warnings.warn('Multiple Code Cards found !! - Using the first one..')

# code card port details..
print ("\r\n")
print ("CODE CARD FOUND !!")
time.sleep(1.5)
print ("CODE CARD PORT DETAIL:")
print ("  " , codecard_port)
ser = serial.Serial(codecard_port[0])
print ("  " , ser)
ser.close()

# configure the serial connection to our code card..
ser = serial.Serial(
	port=codecard_port[0],
	baudrate=115200,
    timeout=5,
)

s = ser.read(1488)

exit = 0
while exit < 2:
    more = ser.read(200)
    s += more
    if len(more) == 0:
        exit += 1
    else:
        exit = 0

# convert our buffer content to string..
s = str(s)[2:-1]

# parse buffer content for confirmation that we're in config mode..
if (s.find('developer.oracle.com/codecard') != -1):
    print ("\r\n")
    print ("CODE CARD READY !!")
    time.sleep(3)
    print ("DEBUG - CONFIG MODE BUFFER:")
    print(s)

    print ("\r\n")
    print ("CONFIGURING WIRELESS:")
    command = (b"ssid=pmac851\r\n")
    ser.write(command)
    time.sleep(1)
    s = ser.read(2048)
    print(s)
    command = (b"password=thinkcodetrigger\r\n")
    ser.write(command)
    time.sleep(1)
    s = ser.read(2048)
    print(s)

    print ("\r\n")
    print ("CONFIGURING FINGERPRINTS:")
    command = (b"fingerprinta1=2e66849da52f1cfc40859e739fb3ad4e9c1cf8ed\r\n")
    ser.write(command)
    time.sleep(.5)
    s = ser.read(85)
    print(s)
    command = (b"fingerprinta2=2e66849da52f1cfc40859e739fb3ad4e9c1cf8ed\r\n")
    ser.write(command)
    time.sleep(.5)
    s = ser.read(85)
    print(s)
    command = (b"fingerprintb1=2e66849da52f1cfc40859e739fb3ad4e9c1cf8ed\r\n")
    ser.write(command)
    time.sleep(.5)
    s = ser.read(85)
    print(s)
    command = (b"fingerprintb2=2e66849da52f1cfc40859e739fb3ad4e9c1cf8ed\r\n")
    ser.write(command)
    time.sleep(.5)
    s = ser.read(85)
    print(s)

    #command = (b"restart\r\n")
    #ser.write(command)
    #time.sleep(5)
    #s = ser.read(240)
    #print(s)
    #command = (b"ls\r\n")
    #ser.write(command)
    #time.sleep(1)
    #s = ser.read(661)
    #print(s)

    print ("\r\n")
    print ("SHORTPRESS BUTTON A..")
    print ("DEBUG - BUTTON PRESS BUFFER:")
    command = (b"shortpressa\r\n")
    ser.write(command)
    s = ser.read(500)

    exit = 0
    while exit < 2:
        more = ser.read(100)
        s += more
        if len(more) == 0:
            exit += 1
        else:
            exit = 0
    print(s)

else:
    print ("\r\n")
    print ("CODE CARD NOT READY IN CONFIG MODE")
    print ("QUITTING..")
