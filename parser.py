import requests as rq
import pandas as pd
from bs4 import BeautifulSoup as BS


r = rq.get('http://stih.su/')
html = BS(r.content, 'html.parser')


file = open('authors.txt', 'w')
for link in html.find_all('a', href=True):
    s = link['href']
    if len(s) > 1 and s.startswith('/'):
        file.write('http://stih.su' + s + '\n')
file.close()


data = {}
for i in open('authors.txt').readlines():
    bio = ''
    r = rq.get(i[:-1])
    html = BS(r.content, 'html.parser')

    for el in html.select('.taxonomy-description > .page-title'):
        bio = el.text

    verses = []

    for el in html.select('.number-navi > li'):
        verses.append(el.text)

    data[bio] = verses


# Нужна одинаковая длина списков
mx = 0
for x in data.keys():
    mx = max(len(data.get(x)), mx)
for x in data.keys():
    data[x].extend([''] * (mx - len(data[x])))


df = pd.DataFrame(data)
df.to_excel('ex.xlsx', index=False)
