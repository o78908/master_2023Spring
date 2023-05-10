import RPi.GPIO as GPIO
import time
import random

def setup(GPIOnum):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIOnum, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) ## 設定GPIO 初始輸入狀態是低電位
def TurnOnLED(GPIOnum):
    GPIO.output(GPIOnum, True)
    
def TurnOffLED(GPIOnum):
    GPIO.output(GPIOnum, False)

def Setup(GPIOnum, OUT_IN):
    GPIO.setmode(GPIO.BCM) 
    if OUT_IN == "OUT":
        GPIO.setup(GPIOnum, GPIO.OUT)#setup GPIO I/O port
    else:
        GPIO.setup(GPIOnum, GPIO.IN)#setup GPIO I/O port
        
Setup(2, "IN") #red
Setup(2, "OUT")
Setup(3, "IN") #yellow
Setup(3, "OUT")
Setup(4, "IN") #green
Setup(4, "OUT")



count = 0
ledChoice = [2,3,4]
def motion(GPIOnum):
    global count    ## 設定全域變數
    
    if GPIO.input(GPIOnum):
        count+=1
        print("motion detected {0}".format(count)) ## 印出偵測到的次數
        led = random.choice(ledChoice)    ## 隨機選擇一個LED
        print(f"turn on led {led}")     ## 印出選擇的LED
        TurnOnLED(led)      ## 點亮LED
        time.sleep(3)
        TurnOffLED(led)     ## 熄滅LED

    else:
        print("no motion")

try:
    setup(14)
    GPIO.add_event_detect(14, GPIO.BOTH, callback=motion, bouncetime=200 )
    while True:  
        time.sleep(1)
except:
    GPIO.cleanup()

