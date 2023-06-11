from flask import Flask, render_template
import pymysql
import time
import random
import datetime
import pandas as pd
import numpy as np
import json
import os
## You must add it in case file cannot be read by page.py!!!!
os.chdir("C:/Users/Modern 14/Desktop/gitRepo/master_2023Spring/computerNeworking") ## 改成自己的路徑
## You must add it in case file cannot be read by page.py!!!!
app = Flask(__name__)
@app.route('/')
def index():
    with open('steam.json', newline='',encoding="utf-8") as f:
        data = json.load(f)
    return render_template('page.html',data = data)


@app.route('/statics')
def stats():
    with open('steam.json', newline='',encoding="utf-8") as f:
        data = json.load(f)

    # 計算每個開發商出現次數
    publishers = {}
    for i in data:
        publisher = i['pubilsher']
        if publisher in publishers:
            publishers[publisher] += 1
        else:
            publishers[publisher] = 1

    publishdates = {}
    for i in data:
        publishdate = i['publishDate']
        if publishdate in publishdates:
            publishdates[publishdate] += 1
        else:
            publishdates[publishdate] = 1

    # 排序開發商出現次數
    sorted_publisher = sorted(publishers.items(), key=lambda x: x[1], reverse=True)

    # 取出前10名開發商
    top_publishers = [publisher[0] for publisher in sorted_publisher[:10]if publisher[0] != "None"]

    # 計算前10名開發商的出現次數
    publisher_counts = [publisher[1] for publisher in sorted_publisher[:10]if publisher[0] != "None" ]

#############################################################
    # 排序開發日期出現次數
    sorted_publishdate = sorted(publishdates.items(), key=lambda x: x[1], reverse=True)

    # 取出前10名開發日期
    top_publishdates = [publishdate[0] for publishdate in sorted_publishdate[:10]if publishdate[0] != "None"]

    # 計算前10名開發日期的出現次數
    publishdate_counts = [publishdate[1] for publishdate in sorted_publishdate[:10]if publishdate[0] != "None"]
#############################################################
    return render_template('statics.html', labels=top_publishers, values=publisher_counts,dateLabels=top_publishdates, dateValues=publishdate_counts)




if __name__ == '__main__':
    app.debug = True
    app.run()