#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Администратор
#
# Created:     07.02.2022
# Copyright:   (c) Администратор 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()
import requests
from bs4 import BeautifulSoup
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



URL = 'https://itdashboard.gov/#home-dive-in'
HEADERS = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko)Chrome/97.0.4692.99 Safari/537.36',
    'Accept':
        '*/*'}
HOST = 'https://itdashboard.gov'
FILE = 'departments.csv'

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x935')
browser= webdriver.Chrome(executable_path='chromedriver.exe',chrome_options=options)
browser.get(URL)
xpath='/html/body/main/div[1]/div/div/div[3]/div/div/div/div/div/div/div/div/div/a'
button= browser.find_element_by_xpath(xpath).is_selected



def get_html(url, params=None):
    r= requests.get(url, headers= HEADERS, params= params)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html,'html.parser')
    pagination= soup.find_all('div', class_='btn')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1



def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='js')

    departments=[]
    for item in items:
        departments.append({
        'title': item.find('div', class_='h4').get_text(strip=True),
        'summary': item.find('div', class_='h1').get_text(strip=True),
        'highlights': item.find('div', class_="row top-gutter lined").get_text(strip=True),
        'link': HOST + item.find('div', class_='js').get('href'),
        })

    return departments

def save_file(items,path):
    with open(path,'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Title', 'Summary', 'Investment Highlights','Link'])
        for item in items:
            writer.writerow([
                item['title'],
                item['summary'],
                item['highlights'],
                item['link']
                ])

def parse():
    URL= input("Enter the URL: ")
    URL= URL.strip()

    html = get_html(URL)
    if html.status_code == 200:

        information=[]

        pages_count=get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f"Page parsing: {page} of {pages_count}")
            html= get_html(URL, params={'page':page})
            information.extend(get_content(html.text))
        save_file(information, FILE)
        print(f'We get {len(information)} following information about {URL}')
        os.startfile(FILE)
    else:
        return ConnectionError

parse()