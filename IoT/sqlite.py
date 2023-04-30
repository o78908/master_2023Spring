import time
import random
import datetime
import sqlite3
import RPi.GPIO as GPIO
import Adafruit_DHT
import pymysql


####AIoT Part##############################################
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 7
GPIO_ECHO = 12
GPIO_TEMP = 14
sensor = Adafruit_DHT.DHT11

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)

def send_trigger_pulse():
    GPIO.output(GPIO_TRIGGER,True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER,False)

def distance(speed):
    send_trigger_pulse()
    
    while GPIO.input(GPIO_ECHO)==0:
        StartTime = time.time()
    while GPIO.input(GPIO_ECHO)==1:
        StopTime = time.time()
        
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed*speed)/2
    
    return distance

def get_speed():
   #  humidity, temperature = Adafruit_DHT.read_retry(sensor,GPIO_TEMP)
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
#######################################

###sqlite3 part########################
conn = sqlite3.connect('/home/o895001/Desktop/IoTDB/test.db')
print ("成功連接sqlite")
c = conn.cursor()
#######################################

###pymysql#############################
db = pymysql.connect(host="172.20.10.3",port=3306,user= "sid001",password= "1234", db="speedcameradb",charset="utf8")
print ("成功連接mysql")
cursor = db.cursor()
#######################################
if __name__ =='__main__':
    try:
        while True:
            for index in range (61):
                if index<60:## index = 2 sec = 10,index 4 sec=20, 5min index= 60
                    Setup(2, "IN")
                    #print("The status of the GPIO{0} is (1)".format(2, GetGPIOStatus(2)))
                    Setup(2, "OUT")
                    Setup(3, "IN")
                    Setup(3, "OUT")
                    Setup(4, "IN")
                    Setup(4, "OUT")
                    TurnOffLED(4)
                    TurnOffLED(3)
                    TurnOffLED(2)              
#                     speed = get_speed()
#                     dist1 = distance(speed)
#                     time.sleep(1)
#                     dist2 = distance(speed)
#                     speedPerSecond = abs(dist2-dist1)
                    for i in range(5):
                        speed = get_speed()
                        dist1 = distance(speed)
                        time.sleep(1)
                        dist2 = distance(speed)
                        speedPerSecond = abs(dist2-dist1)
                        
                        if (speedPerSecond>30):
                           TurnOnLED(2)#turn on red light
                           time.sleep(0.1)                
                        elif (20<speedPerSecond and speedPerSecond<30):
                           TurnOnLED(3)#turn on yellow light
                           time.sleep(0.1)
                        elif(10<speedPerSecond and speedPerSecond <20):
                           TurnOnLED(4)#turn on green light
                           time.sleep(0.1)                
                        else:
                           TurnOffLED(2)#red
                           TurnOffLED(3)#yello
                           TurnOffLED(4)#green
                        print("speedPerSecond= %.lf cm"%speedPerSecond) 
                        if (i==4) :
                            gettime = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
                            sql  = "INSERT INTO speedCamera (ID,time,speed)  VALUES (1, '%s', '%d')" %(gettime,speedPerSecond)
                            print(sql)
                            c.execute(sql)
                            conn.commit()
                        time.sleep(0.25)

                else:
                    datas = c.execute("SELECT * FROM speedcamera")
                    for data in datas:
                        try:
                            sql  = f"INSERT INTO speedcamera (ID,time,speed)  VALUES {data}"
#                             print(sql) #check sql
#                             print("test1")#break point
                            cursor.execute(sql)
#                             print("test2") #break point
                            db.commit()
#                             print("test3")#break point
                        except:
                            db.rollback()
#                             print("error")
                    continue
                
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        conn.close()
        GPIO.cleanup()


##########################################################

####SQL Part##############################################

# conn = sqlite3.connect('/home/o895001/Desktop/IoTDB/test.db')
# print ("成功連接")
# c = conn.cursor()

###建立資料表############################
# c.execute('''CREATE TABLE speedCamera
#        (ID            INT      NOT NULL,
#        time           TEXT    NOT NULL,
#        speed      INT     NOT NULL);''')
# print ("成功建立資料表")
# conn.commit()
# conn.close()
#########################################

###插入資料表############################
# gettime = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
# sql  = "INSERT INTO speedCamera (ID,time,speed)  VALUES (1, '%s', 32)" %(gettime)
# # print(sql)
# c.execute(sql)
# conn.commit()
# conn.close()
#########################################

###truncate 資料表############################
# conn = sqlite3.connect('/home/o895001/Desktop/IoTDB/test.db')
# print ("成功連接")
# c = conn.cursor()
# sql = "DELETE FROM speedCamera WHERE ID = '1';"
# c.execute(sql)
# conn.commit()
# conn.close()
#########################################

###select 資料表############################
# conn = sqlite3.connect('/home/o895001/Desktop/IoTDB/test.db')
# print ("成功連接")
# c = conn.cursor()
# for row in c.execute("SELECT* FROM speedCamera"):
#     sql  = f"INSERT INTO speedCamera (ID,time,speed)  VALUES {row}"
#     print(sql)
# c.execute(sql)
# conn.commit()
# conn.close()
#########################################
