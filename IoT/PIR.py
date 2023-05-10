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