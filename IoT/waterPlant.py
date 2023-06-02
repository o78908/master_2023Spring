import RPi.GPIO as GPIO,LED
import time
import pymysql
# Importing modules
import spidev # To communicate with SPI devices
from numpy import interp  # To scale values

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT) ## motor GPIO
GPIO.setup(21,GPIO.IN)## PRResistor GPIO
light = int(GPIO.input(21))
GPIO.setup(2,GPIO.IN) ##LED
GPIO.setup(2,GPIO.OUT) ##LED



def Setup(GPIOnum, OUT_IN):
    GPIO.setmode(GPIO.BCM) 
    if OUT_IN == "OUT":
        GPIO.setup(GPIOnum, GPIO.OUT)#setup GPIO I/O port
    else:
        GPIO.setup(GPIOnum, GPIO.IN)#setup GPIO I/O port
    
    
def turnOnOffLED(GPIOpin,LDR_DO):
    if LDR_DO == 1:
        GPIO.output(2, True)
    else:
        GPIO.output(2, False)
        
# Start SPI connection
spi = spidev.SpiDev() # Created an object
spi.open(0,0)
# Read MCP3008 data
def analogInput(channel):
  spi.max_speed_hz = 1350000
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

db = pymysql.connect(host="172.20.10.3",port=3306,user= "sid001",password= "1234", db="waterplant",charset="utf8")
cursor = db.cursor()
# sql =  f"insert into waterPlant(time,soilMoisture,motorOnOff,lightOnOff) values ({time},{output},{motorOnOff},{lightOnOff})"
# print(sql)



if __name__ == "__main__":
    try:
        while(1):
            t = time.localtime()
            timeNow = time.strftime("%Y/%m/%d %H:%M:%S", t)##time
                     
            if GPIO.input(21)==1:       ##if light is enough
                turnOnOffLED(2,GPIO.input(21))  ##turn on LED
                lightStatus = 1
                print("Turn on LED")
                print(timeNow)
            if GPIO.input(21)==0:       ##if light is not enough
                turnOnOffLED(2,GPIO.input(21)) ##turn off LED
                lightStatus = 0
                print("Light is enough turn OFF LED")
                print(timeNow)
                
            output = analogInput(0) # Reading from CH0
            output = interp(output, [0, 1023], [100, 0])
            output = int(output)
            print("Moisture:", output)
            if (output<20):             ##if moisture is less than 20
                while 1:                ##馬達持續運轉 每5秒檢查一次 檢查到濕度大於50就停止
                    GPIO.output(27, True)
                    print("Motor On")
                    output = analogInput(0) # Reading from CH0
                    output = interp(output, [0, 1023], [100, 0])
                    output = int(output)
                    t = time.localtime()
                    timeNow = time.strftime("%Y/%m/%d %H:%M:%S", t)
                    motorStatus = 1
                    sql = f"insert into waterPlant(time,soilMoisture,motorOnOff,lightOnOff) values ('{timeNow}','{output}','{motorStatus}','{lightStatus}')"
                    print(timeNow)
                    try:
                        cursor.execute(sql)
                        db.commit()
#                         print("data Successfully Uploaded")
                    except:
                        db.rollback()
                        print("data Uploaded error1")
                    time.sleep(5)
                    t = time.localtime()
                    timeNow = time.strftime("%Y/%m/%d %H:%M:%S", t)
                    
                    if (output>50): #如果濕度大於50 就把馬達停止
                        print("Motor Off")
                        print("Moisture:", output)
                        print(timeNow)
                        GPIO.output(27, False)
                        motorStatus=0               
                        sql = f"insert into waterPlant(time,soilMoisture,motorOnOff,lightOnOff) values ('{timeNow}','{output}','{motorStatus}','{lightStatus}')"
                        try:
                            cursor.execute(sql)
                            db.commit()
#                             print("data Successfully Uploaded")
                        except:
                            db.rollback()
                            print("data Uploaded error2")
                        time.sleep(5)
                        break

            else: ##如果濕度大於20 就把馬達停止(不用澆水)
#                 time.sleep(1)
                t = time.localtime()
                timeNow = time.strftime("%Y/%m/%d %H:%M:%S", t)
                GPIO.output(27, False)
                motorStatus=0
                lightStatus=int(GPIO.input(21))
                sql = f"insert into waterPlant(time,soilMoisture,motorOnOff,lightOnOff) values ('{timeNow}','{output}','{motorStatus}','{lightStatus}')"

                try:
                    cursor.execute(sql)
                    db.commit()
#                     print("data Successfully Uploaded")
                except:
                    db.rollback()
                    print("data Uploaded error3")
                    
#                 print(timeNow)
                time.sleep(5)
                continue
            
    except KeyboardInterrupt:
        print("The end")
#     except:
#         print("Something wrong!")
    finally:
        GPIO.cleanup()

