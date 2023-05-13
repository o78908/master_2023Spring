import json
import pandas as pd
import numpy as np


#read jsonfile
with open('steam.json', newline='') as f:
    data = json.load(f)

for i in data:
    steamdata={
        'game':i['game'],
        'gamePrice':i['gamePrice'],
    }

print(steamdata)