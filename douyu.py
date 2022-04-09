import time
import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

df = pd.DataFrame(columns=['time', '在线主播(个)', '在线观众(万)'])

while True:
    print("let's begin working!")

    N_ZB = 0  
    N_GZ = 0

    print('getting web page...')
    driver = webdriver.PhantomJS()
    url = "https://www.douyu.com/directory/all"
    driver.get(url)
    html = driver.page_source
    print('Parsing html')
    soup = BeautifulSoup(html, 'html5lib')

    n_pages = int(soup.find_all('span', class_='shark-pager-dot')[0].find_next().get_text())

    print('Parsing first page...')
    L = soup.find_all('div', id="live-list-content")
    N_ZB = N_ZB + len(L[0].find_all('li'))
    audience = L[0].find_all('span', class_="dy-num fr")
    for i in audience:
        n = i.get_text()
        if n[-1] == '万':
            N_GZ = N_GZ + float(n[:-1])
        else:
            N_GZ = N_GZ + 0.0001 * float(n)

    for page in range(2, n_pages+1):
        print('Parsing page  {0}...'.format(page))
        driver.find_element_by_link_text("下一页").click()
        html = driver.page_source
        print('Parsing html')
        soup = BeautifulSoup(html, 'html5lib')
        L = soup.find_all('div', id="live-list-content")
        N_ZB = N_ZB + len(L[0].find_all('li'))

        audience = L[0].find_all('span', class_="dy-num fr")
        for i in audience:
            n = i.get_text()
            if n[-1] == '万':
                N_GZ = N_GZ + float(n[:-1])
            else:
                N_GZ = N_GZ + 0.0001 * float(n)


    df.loc[len(df)] = [str(datetime.datetime.now()), N_ZB, N_GZ]

    print('sleep for 30 minutes.............')
    time.sleep(1800)