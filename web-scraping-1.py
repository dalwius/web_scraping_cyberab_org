import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

driver = webdriver.Chrome()  # Change to webdriver.Firefox() for Firefox
url = 'https://cyberab.org/Catalog#!/c/s/Results/Format/list/Page/1/Size/9/Sort/NameAscending?typeId=7'
# rp: https://cyberab.org/Catalog#!/c/s/Results/Format/list/Page/1/Size/9/Sort/NameAscending?typeId=4
# rpo: https://cyberab.org/Catalog#!/c/s/Results/Format/list/Page/1/Size/9/Sort/NameAscending?typeId=3
# c3pao: https://cyberab.org/Catalog#!/c/s/Results/Format/list/Page/1/Size/9/Sort/NameAscending?typeId=7
driver.get(url)
# cards = []
names = []
address_names = []
city_state_zips = []
countries = []
wait = WebDriverWait(driver, 15)
dynamic_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'store-title')))

def scrape_page():
    updated_html = driver.page_source
    soup = BeautifulSoup(updated_html, "lxml") # html.parser
    for card in soup.find_all('div', class_="col-12 mb-3 pointer ng-scope"):
        name = card.find("span", class_="ng-binding").text.strip()
        address = []
        for obj in card.find_all("span", class_="ng-binding ng-scope"):
            address.append(obj.get_text())
        address_len = len(address)
        city_state_zip = "N/A"
        if address_len > 1:
            city_state_zip = address[-2]
        country = address[-1]
        address_n = "N/A"
        if address_len == 3:
            address_n = address[0]
        elif address_len > 3:
            address_n = address[0] + ", " + address[1]
        names.append(name)
        address_names.append(address_n)
        city_state_zips.append(city_state_zip)
        countries.append(country)

scrape_page()
button = driver.find_elements(By.TAG_NAME, 'button')[-2] #next page button

for i in range(1, 6): #rp: 264, rpo: 35, c3pao: 6
    button.click()
    time.sleep(2.5)
    scrape_page()

dict = {'name': names, 'address name': address_names, 'city/state/zip code': city_state_zips, 'country': countries}
df = pd.DataFrame(dict)
df = df.set_index('name')
df.to_csv('out_c3pao.csv') #set output name
print('done')

driver.quit()