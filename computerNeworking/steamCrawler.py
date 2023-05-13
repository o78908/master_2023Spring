from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select

import time
# import requests
import bs4
import json
import pandas as pd
import datetime
import bs4
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


steamdatas = chrome.find_elements(By.CLASS_NAME,'weeklytopsellers_TableRow_2-RN6') 
res = []
a =0

for i in steamdatas:
    print(a)
    a+=1
    genre = []
    time.sleep(2)
    try: 
        price = i.find_element(By.CLASS_NAME,'salepreviewwidgets_StoreSalePriceBox_Wh0L8').text
    except:
        price = "None"

    ###判斷沒資料的例外條件###############
    # nodata = bs4.BeautifulSoup(chrome.page_source,"html.parser")
    # if (nodata.find("h2", class_="pageheader").get_text()) == "喔，抱歉！":
    #     steam_dic = {"game":game,"gamePrice":price,"players": players,"peakplayers": peakplayers,"url":url,"genre":genre,
    #         "pubilsher":"None","publishDate":"None","deck":"None"}
    #     res.append(steam_dic)
    #     with open('steam.json', 'w', encoding='utf-8') as f:
    #         json.dump(res, f, indent=2,
    #                 sort_keys=False, ensure_ascii=False)
    #     chrome.back()
    #     continue
    #################################

    game = i.find_element(By.CLASS_NAME,"weeklytopsellers_GameName_1n_4-").text
    players= i.find_element(By.CLASS_NAME,"weeklytopsellers_ConcurrentCell_3L0CD").text
    peakplayers = i.find_element(By.CLASS_NAME,"weeklytopsellers_PeakInGameCell_yJB7D").text
    urls = i.find_element(By.CLASS_NAME,"weeklytopsellers_TopChartItem_2C5PJ")
    url = urls.get_attribute('href')
    chrome.get(url)



    try:##無年齡限制
        time.sleep(1)
        genres = chrome.find_elements(By.XPATH,'//*[@id="genresAndManufacturer"]/span/a')
        try:
            pubilsher = chrome.find_element(By.CSS_SELECTOR,"#game_highlights > div.rightcol > div > div.glance_ctn_responsive_left > div:nth-child(4) > div.summary.column > a").text
            deck = chrome.find_element(By.CLASS_NAME,"deckverified_CompatibilityDetailRatingDescription__2HWJ").text    
            date = chrome.find_element(By.CLASS_NAME,"date").text
        except:
            pubilsher = "None"
            deck = "None"
            date = "None"   
        ###日期處理正規化###############
        try:
            date = date.replace("年","-").replace("月","-").replace("日","").replace(" ","")
            date = time.strptime(date, "%Y-%m-%d")
            date =time.strftime("%Y", date)
        except:
            date = date
        ###############################  
        # print(pubilshers)
        for g in genres:
            genre.append(g.text)
        steam_dic = {"game":game,"gamePrice":price,"players": players,"peakplayers": peakplayers,"url":url,"genre":genre,
                    "pubilsher":pubilsher,"publishDate":date,"deck":deck}
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
    except: ##年齡限制
        time.sleep(1)
        select = Select(chrome.find_element(By.ID,"ageYear"))
        select.select_by_value("1990")
        button = chrome.find_element(By.ID,"view_product_page_btn")
        button.click()
        time.sleep(1)
        genres = chrome.find_elements(By.XPATH,'//*[@id="genresAndManufacturer"]/span/a')
        pubilsher = chrome.find_element(By.CSS_SELECTOR,"#game_highlights > div.rightcol > div > div.glance_ctn_responsive_left > div:nth-child(4) > div.summary.column > a").text
        deck = chrome.find_element(By.CLASS_NAME,"deckverified_CompatibilityDetailRatingDescription__2HWJ").text    
        date = chrome.find_element(By.CLASS_NAME,"date").text
        ###日期處理正規化###############
        try:
            date = date.replace("年","-").replace("月","-").replace("日","").replace(" ","")
            date = time.strptime(date, "%Y-%m-%d")
            date =time.strftime("%Y", date)
        except:
            date = date
        ###############################  
        # print(pubilshers)
        for g in genres:
            genre.append(g.text)
        steam_dic = {"game":game,"gamePrice":price,"players": players,"peakplayers": peakplayers,"url":url,"genre":genre,
                    "pubilsher":pubilsher,"publishDate":date,"deck":deck}
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
        time.sleep(2)
        chrome.back()

# with open('steam.json', 'w', encoding='utf-8') as f:
#         json.dump(res, f, indent=2,
#                   sort_keys=False, ensure_ascii=False)