from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import chromedriver_autoinstaller
from time import sleep
import os
import bms_download


if __name__ == '__main__':
    SATELLITE_URL = 'https://stellabms.xyz/sl/table.html'

    '''
    chromedriver_autoinstaller.install()

    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    driver.get(SATELLITE_URL)

    sleep(5) # wait for a page to load

    html_doc = driver.page_source
    '''

    f = open("a.html", "r",  encoding="utf-8")
    html_doc = f.read()

    soup = BeautifulSoup(html_doc, 'html.parser')

    rows = soup.find_all('tr', {'class' : 'tr_normal'})

    dl_links = []
    normal_links = []

    for row in rows:
        dl_link = row.find_all('td')[3]
        if dl_link.text == 'DL':
            dl_links.append(dl_link.find('a')['href'])
        else:
            normal_links.append(row.find_all('td')[2].find('a')['href'])

    download_folder = './d'
    os.chdir(download_folder) # change the working directory

    bms_download.download_normal_link('http://www.dream-pro.info/~lavalse/LR2IR/search.cgi?mode=ranking&bmsmd5=68d25d64c16a22b5f4d041466534b772')