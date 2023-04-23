import RPi.GPIO as GPIO
import time
import random
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

if __name__ == "__main__":
    try:
        Setup(2, "IN")
        #print("The status of the GPIO{0} is (1)".format(2, GetGPIOStatus(2)))
        Setup(2, "OUT")
        Setup(3, "IN")
        Setup(3, "OUT")
        Setup(4, "IN")
        Setup(4, "OUT")
        TurnOnLED(4) #turn on green light
        while True:
            temp = random.randint(25,40)
            humid = random.randint(20,80)
            print("temp value=",temp,"humid value=",humid)
            if (humid>30 and temp>38) or(humid>80 and temp>31):
                TurnOffLED(4)
                print("heatstroke!!! red")
                for i in range(10):
                    TurnOnLED(2)#turn on red light
                    time.sleep(0.2)
                    TurnOffLED(2)
                    time.sleep(0.2)
            elif temp>34:
                print("heatstroke!!! yellow")
                for i in range(10): #turn on yellow light
                    TurnOffLED(4)
                    TurnOnLED(3)
                    time.sleep(0.2)
                    TurnOffLED(3)
                    time.sleep(0.2)
            else:                
                TurnOnLED(4) #turn on green light
                print("normal :)")
                time.sleep(5)
            time.sleep(10)
            #print("The status of the GPIO{0} is (1)".format(2, GetGPIOStatus(2)))
    except KeyboardInterrupt:
        GPIO.cleanup() 

