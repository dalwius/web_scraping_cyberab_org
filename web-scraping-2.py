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
cities = []
states = []
zips = []
countries = []
emails = []
sites = []
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
        csz_contents = city_state_zip.split(', ')
        if len(csz_contents) == 1:
            cities.append(city_state_zip)
            states.append(city_state_zip)
            zips.append(city_state_zip)
        elif len(csz_contents) >= 2:
            cities.append(csz_contents[0])
            sz_contents = csz_contents[-1].split(' ')
            states.append(sz_contents[0])
            zips.append(sz_contents[-1])
        address_names.append(address_n)
        # city_state_zips.append(city_state_zip)
        countries.append(country)
    

    for card in driver.find_elements(By.CSS_SELECTOR, '.card.catalog-result-card'):
        driver.execute_script("arguments[0].click();", card)
        # card.click()
        updated_html = driver.page_source
        soup = BeautifulSoup(updated_html, "lxml")
        carddata = soup.find('div', class_="col-12 col-md-7 order-1 order-md-2")

        name = carddata.find("h3", class_="mt-5 ng-binding").text.strip()
        address = carddata.find("span", class_="ng-binding").text.strip()
        remaining = []
        for a in carddata.find_all("small", class_="small ng-binding"):
            remaining.append(a.get_text())
        email = 'N/A'
        website = 'N/A'
        if len(remaining) == 1:
            email = remaining[0]
        elif len(remaining) == 2:
            email = remaining[0]
            website = remaining[1]
        else:
            email = 'N/A'
        names.append(name)
        emails.append(email)
        sites.append(website)
        # print(name)
        
        '''
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
        '''

scrape_page()
button = driver.find_elements(By.TAG_NAME, 'button')[-2] #next page button

for i in range(1, 6): #rp: 264, rpo: 35, c3pao: 6
    button.click()
    time.sleep(3)
    scrape_page()

print(len(names), len(address_names), len(cities), len(states), len(zips), len(countries), len(emails), len(sites), )
dict = {'company name': names, 'address': address_names, 'city': cities, 'state': states, 'zip':zips, 'country':countries, 'email': emails, 'website': sites}
df = pd.DataFrame(dict)
df = df.set_index('company name')
df.to_csv('out_ver2_test.csv') #set output name
print('done')

'''
print(address_names)
print(cities)
print(states)
print(zips)
print(countries)
print(emails)
print(sites)
'''


driver.quit()