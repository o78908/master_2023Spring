import RPi.GPIO as GPIO
import Adafruit_DHT
import time



GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.OUT)
pwm = GPIO.PWM(21,50)
pwm.start(0)
GPIO.output(21,True)

GPIO_TRIGGER = 7
GPIO_ECHO = 12
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)

def send_trigger_pulse():
    GPIO.output(GPIO_TRIGGER,True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER,False)
    
def get_speed():
    speed = 33100+15*60
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


def SetAngle(angle):
    dutyCycle = 1/20 * angle + 3
    pwm.ChangeDutyCycle(dutyCycle)
    
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
        Setup(2, "IN")
        #print("The status of the GPIO{0} is (1)".format(2, GetGPIOStatus(2)))
        Setup(2, "OUT")
        Setup(3, "IN")
        Setup(3, "OUT")
        Setup(4, "IN")
        Setup(4, "OUT")
        
        
        while True:
            TurnOnLED(4) #turn on green light
            time.sleep(0.1)
            for i in range(0,181,10):
                time.sleep(0.1)
                SetAngle(int(i))
                speed = get_speed()
                dist = distance(speed)
                print("Measured Distance = %.lf cm"%dist)

                if(dist<30): #if distance<30 stop &print message
                    TurnOffLED(4)
                    time.sleep(0.1)
                    local_time = time.ctime()
                    print(f"stop time:{local_time}")
                    print(f"angle degree:{i}")
                    print(f"distance:{dist}")
                    for a in range(0,11):
                        TurnOnLED(2)#turn on red light
                        time.sleep(0.2)
                        TurnOffLED(2)
                        time.sleep(0.2)                        
                    time.sleep(3)# buffer time
                    
                if(i>=180): #if angle >180 reverse gear
                    for i in range(181,0,-10):
                        time.sleep(0.1)
                        SetAngle(int(i))
                        dist = distance(speed)
                        print("Measured Distance = %.lf cm"%dist)
                        if(dist<30):#if distance<30 stop &print message
                            TurnOffLED(4)
                            time.sleep(0.2)
                            local_time = time.ctime()
                            print(f"stop time:{local_time}")
                            print(f"angle degree:{i}")
                            print(f"distance:{dist}")
                            for a in range(0,11):
                                TurnOnLED(2)#turn on red light
                                time.sleep(0.2)
                                TurnOffLED(2)
                                time.sleep(0.2)
                                
                            time.sleep(3)#buffer time
                        
                       
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()




