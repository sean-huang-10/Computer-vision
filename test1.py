from selenium import webdriver    #匯入(import)操控瀏覽器相關的程式
from selenium.webdriver.common.keys import Keys  #操作瀏覽器互動的程式
from selenium.webdriver.common.by import By   #DOM TREE搜尋節點的類別集
import time

#driver = webdriver.Firefox()
#url = "https://cybersec.ithome.com.tw/2024/exhibition-page/2054"
#driver.close()
def get_exd_card_detail(driver,url):

    data = dict() 
    driver.get(url) 

    #電話
    telephone_element = driver.find_element(By.CLASS_NAME, "info-tel")
    if telephone_element:  #確定有東西
        data["telephone"] =  telephone_element.text
   

    #Email     
    email_element = driver.find_element(By.CLASS_NAME, "info-mail")
    if email_element: #確定有東西
        data["email"] = email_element.text

    #Website
    website_elements = driver.find_elements(By.CLASS_NAME, "border-icon")
    if website_elements:  #確定有找到東西
        for website_element in website_elements:
            if website_element:  #確定有東西
            # 利用 element.get_attribute("屬性名稱") 取得資訊
             href = website_element.get_attribute('href')
             if href:
                for social_media_name in ['facebook','twitter,','linkedin']:
                 if social_media_name in href:  # facebook這幾個字有無出現在連結
                    data[social_media_name] = href
                 else:
                    data['website'] = href

            #elif'twitter' in href:
                # date[twitter] = href  
            #elif'linkedin' in href:
                # date[linkedin] = href 
       

    #else:
        #print("Website not found")     
    return data

if __name__ == '__main__' :
   test_driver = webdriver.Firefox()
   exd_url = "https://cybersec.ithome.com.tw/2024/exhibition-page/2054"
   exd_data = get_exd_card_detail( driver=test_driver,url=exd_url )
   print(exd_data)
   test_driver.close()
   