import RPi.GPIO as GPIO
import time
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
        Setup(2, "IN") #red
        #print("The status of the GPIO{0} is (1)".format(2, GetGPIOStatus(2)))
        Setup(2, "OUT")
        Setup(3, "IN") #yellow
        Setup(3, "OUT")
        Setup(4, "IN") #green
        Setup(4, "OUT")
        while True:
            TurnOnLED(2)#turn on red light
            time.sleep(1)
            TurnOffLED(2)
            time.sleep(1)
#             for i in range(5): #turn on yellow light
#                 TurnOnLED(3)
#                 time.sleep(0.2)
#                 TurnOffLED(3)
#                 time.sleep(0.2)
#             TurnOnLED(4) #turn on green light
#             time.sleep(2)
#             TurnOffLED(4)
#             time.sleep(1)
            #print("The status of the GPIO{0} is (1)".format(2, GetGPIOStatus(2)))
    except KeyboardInterrupt:
        GPIO.cleanup() 
