from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
import time
# import requests
import bs4
import json
import pandas as pd

# games = []
# players = []
# peakplayer = []
# href = []

# options = Options()
# options.add_argument("--disable-notifications")
# chrome = webdriver.Chrome(executable_path='C:/Users/Modern 14/Desktop', chrome_options=options)
chrome = webdriver.Chrome(executable_path='./chromedriver')
chrome.get("https://store.steampowered.com/charts/mostplayed/")
# time.sleep(4)
urls = (By.XPATH,"//table[@class = 'weeklytopsellers_ChartTable_3arZn']//td/a")
search_input = WebDriverWait(chrome, 3).until(
    EC.presence_of_element_located(urls),
    "errorrr"
)
# steamdatas = chrome.find_elements(By.CLASS_NAME,'responsive_page_template_content') 
# steam_games = chrome.find_elements(By.CLASS_NAME,"weeklytopsellers_TopChartItem_2C5PJ")
# steam_players= chrome.find_elements(By.CLASS_NAME,"weeklytopsellers_ConcurrentCell_3L0CD")
# steam_peakplayers = chrome.find_elements(By.CLASS_NAME,"weeklytopsellers_PeakInGameCell_yJB7D")
# steam_urls = chrome.find_elements(By.XPATH,"//table[@class = 'weeklytopsellers_ChartTable_3arZn']//td/a")
# games = [i.text for i in steam_games]
# player = [i.text for i in steam_players]
# peakplayer = [i.text for i in steam_peakplayers]
# urls = [i.get_attribute('href') for i in steam_urls]

# data = zip(games, player, peakplayer, urls)
# df = pd.DataFrame(data, columns=['games', 'player', 'peakplayer', 'urls'])

# for a in urls:
#     chrome.get(a)
#     time.sleep(4)
#     genres = chrome.find_elements(By.XPATH,'//*[@id="genresAndManufacturer"]/span/a')
#     for i in genres:
        # print(i.text)

steamdatas = chrome.find_elements(By.CLASS_NAME,'weeklytopsellers_TableRow_2-RN6') 
res = []
a =0
for i in steamdatas:
    print(a)
    a+=1
    genre = []
    time.sleep(2)
    game = i.find_element(By.CLASS_NAME,"weeklytopsellers_GameName_1n_4-").text
    players= i.find_element(By.CLASS_NAME,"weeklytopsellers_ConcurrentCell_3L0CD").text
    peakplayers = i.find_element(By.CLASS_NAME,"weeklytopsellers_PeakInGameCell_yJB7D").text
    urls = i.find_element(By.CLASS_NAME,"weeklytopsellers_TopChartItem_2C5PJ")
    url = urls.get_attribute('href')
    chrome.get(url)
    time.sleep(1)
    genres = chrome.find_elements(By.XPATH,'//*[@id="genresAndManufacturer"]/span/a')
    print(genres)
    for g in genres:
        genre.append(g.text)
    steam_dic = {"game":game,"players": players,"peakplayers": peakplayers,"url":url,"genre":genre}
    print(steam_dic)
    try:
        res.append(steam_dic)
        with open('steam.json', 'w', encoding='utf-8') as f:
            json.dump(res, f, indent=2,
                    sort_keys=False, ensure_ascii=False)
    except:
        print('mdfk')
        break

    chrome.back()

# with open('steam.json', 'w', encoding='utf-8') as f:
#         json.dump(res, f, indent=2,
#                   sort_keys=False, ensure_ascii=False)