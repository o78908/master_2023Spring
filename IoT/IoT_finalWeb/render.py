from flask import Flask, render_template
import pymysql
import time
import random
import datetime
import pandas as pd
from itertools import chain
import matplotlib.pyplot as plt

db = pymysql.connect(host="localhost",port=3306,user= "sid001",password= "1234", db="waterplant",charset="utf8")
sql = "SELECT time,soilMoisture,motorOnOff,lightOnOff from waterplant WHERE 1;"

cursor = db.cursor()
with db.cursor() as cursor:
    cursor.execute(sql)   
data = cursor.fetchone()
dataAll = cursor.fetchall()
dataAll = list(chain.from_iterable(dataAll))
timeList = []
moistList =[]
motorList = []
lightList = []


for i in range(0,len(dataAll)):
    if i%4 == 0:
        timeList.append(dataAll[i])
    if i%4 == 1:
        moistList.append(dataAll[i])
    if i%4 == 2 :
        motorList.append(dataAll[i])
    if i%4 == 3 :
        lightList.append(dataAll[i])


app = Flask(__name__)
@app.route('/')
def hello():
    return render_template('page.html',timeList=timeList,moistList=moistList,motorList=motorList,lightList=lightList )


@app.route('/page')
def pageData():
    return render_template('page.html',timeList=timeList,moistList=moistList,motorList=motorList,lightList=lightList )





if __name__ == '__main__':
    
    app.run(debug=False)

