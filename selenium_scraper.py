from selenium import webdriver    #匯入(import)操控瀏覽器相關的程式
from selenium.webdriver.common.keys import Keys  #操作瀏覽器互動的程式
from selenium.webdriver.common.by import By   #DOM TREE搜尋節點的類別集
import time

driver = webdriver.Firefox()  #生成一個由程式操控的FireFox
driver.get("http://www.python.org") #訪問python的官網
assert "Python" in driver.title  #檢查分頁名稱是否包含python
time.sleep(5)

elem = driver.find_element(By.NAME, "q")  #等同於BeautifulSoup的find  去找python
#elem = driver.find_element(By.CLASS_NAME, "search-field")
#elem = driver.find_element(By.ID, "id-search-field")
time.sleep(5)

elem.clear() #清除搜尋欄
elem.send_keys("pycon")  #輸入pycon 到搜尋欄
time.sleep(5)

elem.send_keys(Keys.RETURN) #按下鍵盤的Enter
assert "No results found." not in driver.page_source #"None resullts found"未出現在頁面上
driver.close() #關掉當前分頁
driver.quit()  #關掉整個模擬瀏覽器
print('Don')   