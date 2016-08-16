import wiringpi as wiringpi
from time import sleep

pin_base = 65 # this can be any number greater than 64
i2c_addr = 0x20 # this is the i2c address of your MCP23017, check by running the command: sudo i2cdetect -y 1 (or 0 if you have an old Rev 1 Pi)

wiringpi.wiringPiSetup() # initialise wiringPi
wiringpi.mcp23017Setup(pin_base,i2c_addr) # initialise the mcp23017 extension using the previously defined variables

counter = 0 # create a global variable

# create a dictonary called buttons - this is an associative array containing a button name and its respective pin number
buttons = {
    'increase':72,
    'decrease':80
}

# create a dictionary called seven_seg - this holds the pin numbers for each segment on each digit
seven_seg = {
    #digit: segment a,b,c,d,e,f,g
    0:(65,66,67,68,69,70,71),
    1:(73,74,75,76,77,78,79)
}

# create a dictionary called num - this contains the on/off state of a segment for each of the characters e.g the character "3" requires segment a on, b on, c on, d on, e off, f off, g on
num = {
    ' ':(0,0,0,0,0,0,0),
    '0':(1,1,1,1,1,1,0),
    '1':(0,1,1,0,0,0,0),
    '2':(1,1,0,1,1,0,1),
    '3':(1,1,1,1,0,0,1),
    '4':(0,1,1,0,0,1,1),
    '5':(1,0,1,1,0,1,1),
    '6':(1,0,1,1,1,1,1),
    '7':(1,1,1,0,0,0,0),
    '8':(1,1,1,1,1,1,1),
    '9':(1,1,1,0,0,1,1),
    '-':(0,0,0,0,0,0,1)
}

# create a function that will set stuff up
def setup():
    wiringpi.pinMode(buttons['increase'],0) # set our buttons up as inputs
    wiringpi.pinMode(buttons['decrease'],0)
    wiringpi.pullUpDnControl(buttons['increase'],2) # enable the internal pull up resistor - this means this pin is connected to 3v3 making it high - the mcp23017 doesnt have a pull down resistor, which would have been nicer to use
    wiringpi.pullUpDnControl(buttons['decrease'],2)
    for x in range(0,len(seven_seg)): # loop through each digit
                for seg in seven_seg[x]: # loop through each segment of the digit
                    wiringpi.pinMode(seg,1) # set the segment pin as an output
                    wiringpi.digitalWrite(seg,0) # set the output low/off
    display(0,seven_seg) # with everything setup we are good to go and display the number 0

# define our cleanup function to be used when we exit the script
def cleanUp():
        for x in range(0,len(seven_seg)): # loop through each digit
                for seg in seven_seg[x]: # loop through each segment of the digit
                        wiringpi.digitalWrite(seg,0) # set the segment pin to low/off

# create a function to increase our counter variable by 1
def increase():
    global counter # tell this function that the variable counter is global - this is so we can change its value
    counter += 1 # increase the value by 1
    max = str(1).ljust(len(seven_seg),'0')
    max = int(max)*10 - 1
    if counter > max:
        counter = max
        while not wiringpi.digitalRead(buttons['increase']): # wait until the button is no longer pressed before continuing
                sleep(0.01)

# create a function to decrease our counter variable by 1
def decrease():
    global counter # tell this function that the variable counter is global
    counter -= 1 # decrease the value by 1
    min = str(1).ljust(len(seven_seg),'0')
    min = "-" + min
    min = int(min) + 1
    if counter < min:
        counter = min
    while not wiringpi.digitalRead(buttons['decrease']): # wait until the button is no longer pressed before continuing
        sleep(0.01)

# create a function to send a character to our 7 segment displays
def display(number,display):
    number = str(number).zfill(len(display))
    for i,c in enumerate(number):
        for x in range(0,7):
            wiringpi.digitalWrite(display[i][x],num[c][x])

setup() # run our setup function

try:
    while True: # create an infinite loop
        if not wiringpi.digitalRead(buttons['increase']): # if the increase button is pressed
            increase() # run the increase() function
            display(counter,seven_seg) # display the value of counter on our seven segment displays
        elif not wiringpi.digitalRead(buttons['decrease']): # if the decrease button is pressed
            decrease() # run the decrease() function
            display(counter,seven_seg) # display the value of counter 
        else:
            sleep(0.1)
finally: # everything here gets run when we quit the script
    cleanUp() # when we exit our script we run out cleanUp function
