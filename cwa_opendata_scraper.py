import requests
import json
import os
from pprint import pprint
weather_element_name = {
    'Wx':'天氣現象',
    'PoP':'降雨機率',
    'CI':'舒適度',
    'MinT':"時段最低溫度",
    'MaxT':'時段最高溫度'
}

def get_cities_weather(cwa_api_key: str, locations_name:list):
    header = {
        'Accept':'application/json'    
    }
    #parsmeters放參數
    parsmeters = { 
        'Authorization':cwa_api_key,   
        'locationName':locations_name   
    }
    url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001'
    response = requests.get(url, headers=header, params=parsmeters)
    #print(response)
    if response.status_code == 200:
        weather_data = response.json()
    else:
        print("Requests Fail")
#pprint(weather_data['records']['location'])

    cities_weather = dict() #={}
    #每一個location
    for location in weather_data['records']['location']:
        print(location['locationName'])#城市名稱
        city_name = location['locationName']
        city_weather = get_city_weather(location)#每個城市的資料
        cities_weather[city_name] = city_weather
    return cities_weather    


def get_city_weather(location):
    #給location ,給你數值的dictionary
    city_weather  = dict()  
    for element in location['weatherElement']:
       # print(element['elementName'],end=':')#數值的名稱
      #  print(element['time'][0]['parameter']['parameterName'])#取時間最靠近的數值，所以取index 0
         
        element_name = element['elementName']#英文名稱
        element_value = element['time'][0]['parameter']['parameterName']
        
        if element_name in ['MinT','MaxT']:
            element_unit = 'C'
        elif element_value in['PoP']:
            element_unit = '%'
        else:
            element_unit = ''     
        #city_weather[element_name] = element_value + element_unit
        element_name = weather_element_name[element_name]#轉成對應的中文名稱    
        city_weather[element_name] = element_value + element_unit
    return city_weather
    
    
if __name__ == '__main__':
    cwa_api_key = os.getenv("CWA_API_KEY", None)
    locations = ['桃園市', '花蓮縣','臺中市']
    
    if cwa_api_key:
        pprint(get_cities_weather(cwa_api_key, locations))
    else:
        print("Miss API Key")    