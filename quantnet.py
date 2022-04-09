"""
Scrape admisison data from QuantNet (https://www.quantnet.com/tracker/).
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd

def main(totalPage):
    data=[]
    for i in range(1, totalPage+1):
        print('Parsing page {0}...'.format(i))
        page = requests.get("https://www.quantnet.com/tracker/?page={0}".format(i))
        soup = BeautifulSoup(page.content, 'html5lib')        
        items = soup.find_all('li', 'applicationListItem')        
        for item in items:
            d={}
            d['program'] = item.find_all('span','programTitle')[0].get_text()
            d['poster'] = item['data-author']
            d['DateTime'] = item.find_all('div','listBlock program')[0].find_next(class_='DateTime').get_text()
            d['UGPA'] = item.find_all('div','listBlock ugpa')[0].find_next().get_text()
            d['GRE_Q'] = item.find_all('div','listBlock GRE_Q')[0].find_next().get_text()
            d['GRE_V'] = item.find_all('div','listBlock GRE_V')[0].find_next().get_text()
            d['GRE_AWA'] = item.find_all('div','listBlock GRE_AWA')[0].find_next().get_text()
            d['submitted'] = [string for string in item.find_all('div','listBlock submitted')[0].find_next().stripped_strings][0]
            d['result'] = item.find_all('div','listBlock result')[0].find_next('div', 'status').find_next().get_text()
            if d['result'] == 'Admit' or 'Reject':
                d['result_time'] = item.find_all('div','listBlock result')[0].find_next('div', 'status').find_next().find_next().get_text()[1:-1] 
            d['result_days'] = [string for string in item.find_all('div','listBlock result')[0].find_all('div', 'secondRow')[0].stripped_strings][0]
            d['last_updated'] = item.find_all('div','listBlock updated')[0].find_next(class_='DateTime').get_text()
            if len(item.find_all('div','listBlock updated')[0].find_all('div', class_='applicationNote'))>0:
                d['note'] = item.find_all('div','listBlock updated')[0].find_all('div', class_='applicationNote')[0].get_text()
            data.append(d)
    return data

 
 if __name__ == '__main__':
    data = main(300)
    df = pd.DataFrame(data)  
    order = pd.read_excel('/Users/francis/Desktop/quantnet.xlsx')
    df = df.reindex_axis(order.columns, axis=1)   
    df.to_excel('/Users/francis/Desktop/data.xlsx', index=False)
