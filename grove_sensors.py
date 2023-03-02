import grovepi
import time,sys
  

if sys.platform == 'uwp':
    import winrt_smbus as smbus
    bus = smbus.SMBus(1)
else:
    import smbus
    import RPi.GPIO as GPIO
    rev = GPIO.RPI_REVISION
    if rev == 2 or rev == 3:
        bus = smbus.SMBus(1)
    else:
        bus = smbus.SMBus(0)

DISPLAY_RGB_ADDR = 0x62
DISPLAY_TEXT_ADDR = 0x3e


def setRGB(r,g,b):
    bus.write_byte_data(DISPLAY_RGB_ADDR,0,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,1,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,0x08,0xaa)
    bus.write_byte_data(DISPLAY_RGB_ADDR,4,r)
    bus.write_byte_data(DISPLAY_RGB_ADDR,3,g)
    bus.write_byte_data(DISPLAY_RGB_ADDR,2,b)

def textCommand(cmd):
    bus.write_byte_data(DISPLAY_TEXT_ADDR,0x80,cmd)

def setText_norefresh(text):
    textCommand(0x02) # return home
    time.sleep(.05)
    textCommand(0x08 | 0x04) # display on, no cursor
    textCommand(0x28) # 2 lines
    time.sleep(.05)
    count = 0
    row = 0
    while len(text) < 32: #clears the rest of the screen
        text += ' '
    for c in text:
        if c == '\n' or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))



if __name__=="__main__":
    grovepi.set_bus("RPI_1")

    potentiometer = 0
    ultrasonic_ranger = 4

    grovepi.pinMode(potentiometer,"INPUT")
    time.sleep(1)
    
    adc_ref = 5

    grove_vcc = 5

    full_angle = 300

    while True:

        try:
            # Collect the values from the potentiometer and the ultrasonic ranger
            sensor_value = grovepi.analogRead(potentiometer)
            val = grovepi.ultrasonicRead(ultrasonic_ranger)

            sentence = ""
            
            # Compare the value from the ultrasonic ranger and the potentiometer and output on the LCD appropriately
            if (val<sensor_value):
                sentence = " " + str(sensor_value) + "cm OBJ PRES" + "\n" + " " + str(val) + "cm"
            else:
                sentence = " " + str(sensor_value) + "cm         " + "\n" + " " + str(val) + "cm"
            
            setText_norefresh(sentence)
            
            # Compare the values and set the color appropriately
            if (val<sensor_value):
                setRGB(255,0,0) # Turns the LCD red 
            else:
                setRGB(0,255,0) # Turns the LCD green
    
    
        except KeyboardInterrupt:
            print("Keyboard Interrupt")
    
        except IOError:
            print("IOError")
    
        except Exception as e:
            print ("Error:{}".format(e))


        time.sleep(0.1)
