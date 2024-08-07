import requests
from bs4 import BeautifulSoup
import pandas as pd
url = "https://cybersec.ithome.com.tw/2024/exhibitionDirectory"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
exd_cards = soup.find_all("div", class_="exd-card")
url_prefix = "https://cybersec.ithome.com.tw"
exd_cards_info = list()

for exd_card in exd_cards:
    #找連結
    href = url_prefix + exd_card.a["href"]
    #展攤名稱'
    exd_name = exd_card.h5.text

    #展攤位置編號
    if exd_card.h6: #判斷是否為None
      exd_id = exd_card.h6.text.split("：")[-1] #用split將展攤編號分割掉
    else:
      exd_id = ""

    # print(href, exd_name, exd_id)
    exd_cards_info.append({
        'exd_link': href,
        'exd_name': exd_name,
        'exd_id': exd_id
    })
exd_cards_info[:5]
#data = pd.DataFrame(exd_cards_info) # 轉換成DataFrame
#data.to_csv('cybersec_exd.csv')