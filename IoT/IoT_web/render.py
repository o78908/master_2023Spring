from flask import Flask, render_template
import pymysql
import time
import random
import datetime
import pandas as pd
from itertools import chain
import matplotlib.pyplot as plt

db = pymysql.connect(host="localhost",port=3306,user= "sid001",password= "1234", db="weather",charset="utf8")
sql = "SELECT `humi`,`temp`,`gettime` from `th` WHERE 1;"

cursor = db.cursor()
with db.cursor() as cursor:
    cursor.execute(sql)   
data = cursor.fetchone()
dataAll = cursor.fetchall()
dataAll = list(chain.from_iterable(dataAll))
humiList =[]
tempList = []
timeList = []

for i in range(0,len(dataAll)):
    if i%3 == 0:
        humiList.append(dataAll[i])
    if i%3 == 1:
        tempList.append(dataAll[i])
    if i%3 == 2 :
        timeList.append(dataAll[i])

# def drawGraph():
#     cursor = db.cursor()
#     with db.cursor() as cursor:
#         cursor.execute(sql)   
#     data = cursor.fetchone()
#     dataAll = cursor.fetchall()
#     dataAll = list(chain.from_iterable(dataAll))
#     humiList =[]
#     tempList = []
#     timeList = []

#     for i in range(0,len(dataAll)):
#         if i%3 == 0:
#             humiList.append(dataAll[i])
#         if i%3 == 1:
#             tempList.append(dataAll[i])
#         if i%3 == 2 :
#             timeList.append(dataAll[i])

#     info = pd.DataFrame({'humid':humiList,
#                         'temperature': tempList,
#                         'time':timeList})
#     plt.plot(info['time'], info['humid'],label='humid')  # 讀出time及humid的資料，產生紅色線
#     plt.plot(info['time'], info['temperature'],label='temperature') # 讀出time及temperature的資料，產生藍色線
#     plt.xlabel('time')                   # x軸的Label
#     plt.title('溫濕度圖表') # 此圖的title
#     plt.legend()
#     plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']
#     plt.show()





# for i in range (5):
#     siteid= ("001")
#     gettime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     temp = round(random.uniform(30, 40),1)
#     humi = round(random.uniform(40, 80),2)
#     newcol = 0
#     sql = f"insert into th({siteid},{gettime},{temp},{humi},{newcol})"
#     time.sleep(0.3)
    # print(sql)
# cursor = db.cursor()

# try:
#     for i in range (5):
#         siteid= ("001")
#         gettime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         temp = round(random.uniform(30, 40),1)
#         humi = round(random.uniform(40, 80),2)
#         newcol = 0
#         sql = f"insert into th({siteid},{gettime},{temp},{humi},{newcol})"
#         cursor.execute(sql)
#         time.sleep(0.1)
#         db.commit()
# except:
#     db.rollback()   


app = Flask(__name__)
@app.route('/')
def hello():
    return 'Hello World'


@app.route('/text')
def text():
    return '<html><body><h1>Hello World</h1></body></html>'


@app.route('/home')
def home():
    return render_template('page.html')


@app.route('/page/text')
def pageText():
    return render_template('page.html', text="Python Flask !")


@app.route('/page/app')
def pageAppInfo():
    appInfo = {  # dict
        'id': 5,
        'name': 'Python - Flask',
        'version': '1.0.1',
        'author': 'Enoxs',
        'remark': 'Python - Web Framework'
    }
    return render_template('page.html', appInfo=appInfo)


@app.route('/page/data')
def pageData():
    return render_template('page.html',humiList=humiList,tempList=tempList,timeList=timeList)


@app.route('/static')
def staticPage():
    return render_template('static.html')


if __name__ == '__main__':
    app.run()
