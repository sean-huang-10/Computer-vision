from selenium import webdriver    #匯入(import)操控瀏覽器相關的程式
from selenium.webdriver.common.keys import Keys  #操作瀏覽器互動的程式
from selenium.webdriver.common.by import By   #DOM TREE搜尋節點的類別集
import time
import requests
from bs4 import BeautifulSoup

driver = webdriver.Firefox()  #生成一個由程式操控的FireFox
url = "https://cybersec.ithome.com.tw/2024/exhibitionDirectory"
response = requests.get(url)
driver.get(url) 
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
#電話
telephone_element = driver.find_element(By.CLASS_NAME, "info-tel")
if telephone_element:  #確定有東西
    print("Telephone:", telephone_element.text)
else:
     print("Telephone not found")

#Email     
email_element = driver.find_element(By.CLASS_NAME, "info-mail")
if email_element: #確定有東西
    print("Email:",email_element.text)
else:
     print("email not found")

#Website
website_elements = driver.find_elements(By.CLASS_NAME, "border-icon")
if website_elements:  #確定有找到東西
 for website_element in website_elements:
    if website_element:  #確定有東西
      # 利用 element.get_attribute("屬性名稱") 取得資訊
      href = website_element.get_attribute('href')
      if href:
          if'facebook' in href:  # facebook這幾個字有無出現在連結
             print("Facebook: ",href) 
      elif'twitter' in href:
             print("Twitter: ",href)   
      elif'linkedin' in href:
             print("Linkedin: ",href)
      else:
             print("Website: ", href)                 
    print("Website: ", website_element.get_attribute('href'))

else:
     print("Website not found")     
driver.close()