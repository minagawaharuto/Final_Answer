
import lxml
from numpy import append
import pandas as pd
from bs4 import BeautifulSoup
import re
import requests
start_url = "https://r.gnavi.co.jp/area/jp/izakaya/rs/"
start_url2 = "https://r.gnavi.co.jp/area/jp/izakaya/rs/?p=2"
ssl_list=[]
name_list=[]
phone_list = []
urls_list = []
address_list = []
building_list = []
def get_url(soup):
    links = []
    for a_tag in soup.find_all('a',class_ = "style_titleLink__oiHVJ",href=True):
        links.append(a_tag['href'])
    return links
def ssl_seach(url_list):
    if 'https' in url_list:
        return True
    else:
        return False

response = requests.get(start_url)
response.encoding = response.apparent_encoding
soup = BeautifulSoup(response.text, features="lxml")


for element in soup.find_all(class_="style_restaurantNameWrap__wvXSR"):
    name_list.append(element.text)

response1 = requests.get(start_url2)
response1.encoding = response1.apparent_encoding
soup1 = BeautifulSoup(response1.text, features="lxml")
urls_list = get_url(soup) + get_url(soup1)

for element2 in soup.find_all(class_="style_restaurantNameWrap__wvXSR"):
    name_list.append(element2.text)
  

for url_list in urls_list:
    ssl_list.append(ssl_seach(url_list))
    response2 = requests.get(url_list)
    response2.encoding = response2.apparent_encoding
    soup2 = BeautifulSoup(response2.text,features="lxml")
    phone_elements = soup2.find('span',class_='number')
    for element in phone_elements:
        phone_list.append(element.text)
    address_elements = soup2.find_all('span',class_='region')
    for element in address_elements:
        address_list.append(element.text)
    building_elements = soup2.find_all('span',class_ ='locality')
    for element in building_elements:
        building_list.append(element.text)

   
def split_address(address_list):
   
    pattern = '''(.+?[都道府県])(.+?[市区町村])(.+)'''
    match = re.match(pattern, address_list)
    if match:
        return match.groups()
    return (None, None, None)  # 分割できなかった場合

# 各住所をパースしてリストに変換

parsed_addresses=[]
for x in address_list:
    parsed_addresses.append(split_address(x))
df_address = pd.DataFrame(parsed_addresses,columns=['都道府県','市区町村','番地'])
df_name= pd.DataFrame(name_list,columns=['店舗名'])
df_url= pd.DataFrame(urls_list,columns=['URL'])
df_phone = pd.DataFrame(phone_list,columns=['電話番号'])
df_mail = pd.DataFrame(columns=['メールアドレス'])
df_building = pd.DataFrame(building_list,columns=['建物名'])
df_ssl = pd.DataFrame(ssl_list,columns=['SSL'])
df_data = pd.concat([df_name,df_phone,df_mail,df_address,df_building,df_url,df_ssl],axis=1)
df_data.to_csv('./1-1.csv')
print("OK!CSV")