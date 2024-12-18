
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re
import pandas as pd
from time import sleep
name_list = []
urls_list = []
address_list = []
phone_list = []
ssl_list =[]
building_list = []
service = Service(executable_path='./chromedriver.exe')
driver = webdriver.Chrome(service=service)
url = 'https://r.gnavi.co.jp/area/jp/rs/?date=20241118&fw=%E5%B1%85%E9%85%92%E5%B1%8B'

driver.get(url)
time.sleep(3)
for elem_h2 in driver.find_elements(By.XPATH,'//a/h2'):
    elem_a = elem_h2.find_element(By.XPATH,'..')  
    urls_list.append(elem_a.get_attribute('href'))
driver.get(url)
driver.find_element(By.CLASS_NAME,"style_nextIcon__M_Me_").click()
time.sleep(3)
for elem_h2 in driver.find_elements(By.XPATH,'//a/h2'):
    elem_a = elem_h2.find_element(By.XPATH,'..')  
    urls_list.append(elem_a.get_attribute('href'))

def ssl_seach(url_list):
    if 'https' in url_list:
        return True
    else:
        return False
ssl_list = []

for url_list in urls_list[:49]:
    ssl_list.append(ssl_seach(url_list))
    driver.get(url_list)
    time.sleep(3)
    elem_phone = driver.find_element(By.XPATH,"//li/span[@class='number']")
    elem_address = driver.find_element(By.XPATH,"//p/span[@class='region']")
    elem_name = driver.find_element(By.XPATH,"//td/p[@class='fn org summary']")
    phone_list.append(elem_phone.text)
    address_list.append(elem_address.text) 
    name_list.append(elem_name.text)

    

driver.quit() 

def split_address(address_list):
  
    pattern =  '''(.+?[都道府県])(.+?[市区町村])(.+)'''
    match = re.match(pattern, address_list)
    if match:
        return match.groups()
    return (None, None, None) 

parsed_addresses=[]
for x in address_list:
    parsed_addresses.append(split_address(x))
print(parsed_addresses)
df_name= pd.DataFrame(name_list,columns=['店舗名'])
df_url= pd.DataFrame(columns=['URL'])
df_phone = pd.DataFrame(phone_list,columns=['電話番号'])
df_mail = pd.DataFrame(columns=['メールアドレス'])
df_address = pd.DataFrame(parsed_addresses,columns=['都道府県','市区町村','番地'])
df_ssl = pd.DataFrame(ssl_list,columns=['SSL'])
df_data = pd.concat([df_name,df_phone,df_mail,df_address,df_url,df_ssl],axis=1)
df_data.to_csv('./1-2.csv')
user_agent = "{user agent: Mozilla/5.0(Windows NT10.0;Win64;x64) AppleWebkit/537.36(KHTML,likeGecko)chrome/131.0.0.0 safari/537.36}"
print(user_agent)
      


   