import RPi.GPIO as GPIO
import Adafruit_DHT
import time

GPIO.setmode(GPIO.BCM)

###########################################
GPIO_TRIGGER = 7
GPIO_ECHO = 12
GPIO_TEMP = 14

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)
sensor = Adafruit_DHT.DHT11

def send_trigger_pulse():
    GPIO.output(GPIO_TRIGGER,True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER,False)
    
def get_speed():
    humidity, temperature = Adafruit_DHT.read_retry(sensor,GPIO_TEMP)
    speed = 33100+temperature*60
    return speed
def distance(speed):
    send_trigger_pulse()
    
    while GPIO.input(GPIO_ECHO)==0:
        StartTime = time.time()
    while GPIO.input(GPIO_ECHO)==1:
        StopTime = time.time()
        
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed*speed)/2
    
    return distance
#####################################
def Setup(GPIOnum, OUT_IN):
    GPIO.setmode(GPIO.BCM) 
    if OUT_IN == "OUT":
        GPIO.setup(GPIOnum, GPIO.OUT)#setup GPIO I/O port
    else:
        GPIO.setup(GPIOnum, GPIO.IN)#setup GPIO I/O port
    
def TurnOnLED(GPIOnum):
    GPIO.output(GPIOnum, True)
    
def TurnOffLED(GPIOnum):
    GPIO.output(GPIOnum, False) 

def GetGPIOStatus(GPIOnum):
    GPIO_State = GPIO.input(GPIOnum)# get GPIO port status
    return GPIO_State


if __name__ =='__main__':
    try:
        while True:
            Setup(2, "IN")
            #print("The status of the GPIO{0} is (1)".format(2, GetGPIOStatus(2)))
            Setup(2, "OUT")
            Setup(3, "IN")
            Setup(3, "OUT")
            Setup(4, "IN")
            Setup(4, "OUT")
            TurnOffLED(4)
            TurnOffLED(3)           
            speed = get_speed()
            dist = distance(speed)
            if (dist<10):
                TurnOnLED(4)#turn on red light
                time.sleep(1)
            elif(10<dist and dist<20):
                TurnOnLED(3)#turn on yellow light
                time.sleep(1)
            else:
                TurnOffLED(4)
                TurnOffLED(3)
            print("Measured Distance = %.lf cm"%dist)
            
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
