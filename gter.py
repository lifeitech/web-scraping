import requests
from bs4 import BeautifulSoup
import pandas as pd


def one_line(x):
    for string in x.stripped_strings:
        return string

L = []
for page_n in range(1, 90):
    print('Parsing Page  {0}...'.format(page_n))
    page = requests.get("http://bbs.gter.net/forum.php?mod=forumdisplay&fid=535&typeid=351&typeid=351&filter=typeid&page={0}".format(page_n))
    soup = BeautifulSoup(page.content, 'html5lib')
    hlinks = soup.find_all('a', class_='xst')
    try:
        for i in range(len(hlinks)):
            print('Parsing link {0}...'.format(i))
            lz = one_line(hlinks[i].find_next('cite'))
            post = requests.get(hlinks[i]['href'])
            soup_post = BeautifulSoup(post.content, 'html5lib') 
            content = soup_post.find('div', class_ = 't_fsz').get_text()
            table = soup_post.find_all('div', class_='typeoption')

            if len(table) > 0:
                tables = table[0].find_all('table')

            bg = {}
            r=set()
            for j in range(len(tables)):
                if tables[j].caption.string == '个人情况':
                    r.add(j)           
                    for tr in tables[j].find_all('tr'):
                        bg[one_line(tr.th)] = one_line(tr.td)
                elif tables[j].caption.string == '给学弟学妹的留言':
                    r.add(j)
                    note = one_line(tables[j].tr)

            for k in set(range(len(tables))).difference(r):           
                    offer = {}
                    for tr in tables[k].find_all('tr'):
                        offer[one_line(tr.th)] = one_line(tr.td)                       
                    offer['给学弟学妹的留言:'] = note
                    offer['帖子内容:'] = content
                    offer['id:'] = lz
                    offer.update(bg)
                    offer = { key[:-1] : value for key, value in offer.items() }               
                    L.append(offer)
    except AttributeError:
        pass

df = pd.DataFrame(L)
order = pd.read_excel('/Users/francis/Desktop/columns.xlsx')
df = df.reindex_axis(order.columns, axis=1)   
df.to_excel('/Users/francis/Desktop/gter_data.xlsx', index=False)
    
print('Done.')