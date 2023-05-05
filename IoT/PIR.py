import RPi.GPIO as GPIO
import time

def setup(GPIOnum):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIOnum, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) ## 設定GPIO 初始輸入狀態是低電位

count = 0 
def motion(GPIOnum):
    global count
    if GPIO.input(GPIOnum):
        count+=1
        print("motion detected {0}".format(count))
    else:
        print("no motion")
    
try:
    setup(14)
    GPIO.add_event_detect(14, GPIO.BOTH, callback=motion, bouncetime=200 )
    while True:
        time.sleep(1)
except:
    GPIO.cleanup()