import Adafruit_DHT
import time
import LED

sensor = Adafruit_DHT.DHT11

temp=14
while True:
    LED.Setup(2,"OUT")
    currentTime=time.strftime("%H:%M:%S")
    humidity, temperature = Adafruit_DHT.read_retry(sensor,temp)
    
    if humidity is not None and temperature is not None:
        print(currentTime,'->Temp={0}%C Humidity={1}%'.format(temperature,humidity))
        
        if (temperature>25 and humidity>60):
            LED.TurnOnLED(2)
            time.sleep(1)
            LED.TurnOffLED(2)
            time.sleep(1)
    else:
        print('Failed to get reading')
    time.sleep(5)