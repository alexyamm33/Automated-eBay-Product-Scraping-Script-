from ebaysdk.finding import Connection as finding
from ebaysdk.shopping import Connection as shopping
from bs4 import BeautifulSoup
import pandas as pd
import sys
import math
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
#driver = webdriver.Chrome('/Users/alex/PycharmProjects/untitled/chromedriver 3')
def Get_pgs(name):
    api = finding(appid='AlexYeh-Product-PRD-5b3210513-f775e8d7', config_file=None)
    response = api.execute('findItemsAdvanced', {
        'itemFilter': [
            {'name': 'Seller', 'value': name},
        ],
        'outputSelector': 'SellerInfo',
        'paginationInput': {
            'entriesPerPage': '100',
        },
        'paginationOutput': {'totalPages'}
    })
    soup = BeautifulSoup(response.content, 'lxml')
    total_pages = int(soup.find('totalpages').text)
    print(name, total_pages)
    return(total_pages)
def Seller_Scrape(name, pg):
    api = finding(appid='AlexYeh-Product-PRD-5b3210513-f775e8d7', config_file= None)
    response = api.execute('findItemsAdvanced', {
        'itemFilter': [
            {'name': 'Seller', 'value': name},
        ],
        'outputSelector':'SellerInfo',
        'paginationInput': {
            'entriesPerPage': '100',
            'pageNumber': str(pg)
        },
        'paginationOutput' : {'totalPages'}
    })
    soup = BeautifulSoup(response.content, 'lxml')
    print(name,pg)
    ID = soup.findAll('itemid')
    title = soup.findAll('title')
    price = soup.findAll('currentprice')
    img_url = soup.findAll('galleryurl')
    for i in range(len(title)):
        output_seller.append(name)
        item_ID.append(ID[i].text)
        item_title.append(title[i].text)
        item_price.append(price[i].text)
    print(len(item_ID))
    pg = pg +1
    return(pg)
def get_iteminfo(id):
    api = shopping(appid='AlexYeh-Product-PRD-5b3210513-f775e8d7', config_file=None)
    api_request = {
        'ItemID': id,
        'IncludeSelector': 'Details'
        }
    response = api.execute('GetMultipleItems', api_request)
    soup = BeautifulSoup(response.content, 'lxml')
    quantity = soup.find_all('quantitysold')
    for i in range(len(quantity)):
        print(quantity[i].text, id[i])
        item_quantity.append(int(quantity[i].text))
def get_description(id):
    api = shopping(appid='AlexYeh-Product-PRD-5b3210513-f775e8d7', config_file=None)
    api_request = {
        'ItemID': id,
        'IncludeSelector': 'TextDescription'
    }
    response = api.execute('GetMultipleItems', api_request)
    soup = BeautifulSoup(response.content, 'lxml')
    print(soup)
    description = soup.find_all('description')
    for i in range(len(description)):
        print(description[i].text)
        item_des.append(description[i].text)
def get_sellthrou(quantity):
    sold =sum(quantity)
    print("The number of successful listing is: ", len(quantity), sold)
    print("The sell through rate of this seller is: ", sold/len(quantity)*100, "%")
def img_search(img, d):
    driver.get("http://images.google.com/searchbyimage?image_url=" + img)

#for i in range(len(input)):
if __name__ == "__main__":
    feedback = []
    item_des = []
    item_price = []
    item_link = []
    item_quantity = []
    #import_data = pd.read_excel(r'C:\Users\Alex Y\OneDrive\Desktop\Seller List - Copy.xlsx', usecol = 'Seller')
    seller_name = ['marketparty']
    for i in range (len(seller_name)):
        output_seller = []
        item_img = []
        item_ID = []
        item_title = []
        for k in range(1,int(Get_pgs(seller_name[i]))):
            Seller_Scrape(seller_name[i], k+1)
            new_data = pd.DataFrame(
                {'ebay_title': item_title,
                'ID':item_ID,
                'seller': output_seller}
            )
            file_name = "Item Infos"+ seller_name[i] +".xlsx"
            writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
            new_data.to_excel(writer)
            writer.save()
#reps = math.ceil(len(item_ID)/20)
#for i in range (reps):
#    print(i)
#    if i == reps:
#        get_iteminfo(item_ID[i*20:])
#        get_description(item_ID[i*20:])
#    else:
#        get_iteminfo(item_ID[i*20:(i+1)*20])
#        get_description(item_ID[i*20:(i+1)*20])
#get_sellthrou(item_quantity)

