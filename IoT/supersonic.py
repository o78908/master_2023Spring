import RPi.GPIO as GPIO
import Adafruit_DHT
import time

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 7
GPIO_ECHO = 12
# GPIO_TEMP = 14

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)
# sensor = Adafruit_DHT.DHT11

def send_trigger_pulse():
    GPIO.output(GPIO_TRIGGER,True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER,False)
    
def get_speed():
#     humidity, temperature = Adafruit_DHT.read_retry(sensor,GPIO_TEMP)
#     speed = 33100+temperature*60
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

if __name__ =='__main__':
    try:
        while True:
            speed = get_speed()
            dist = distance(speed)
            print("Measured Distance = %.lf cm"%dist)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()