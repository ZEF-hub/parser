import requests as rq
import pandas as pd
from bs4 import BeautifulSoup as BS

r = rq.get('http://stih.su/')
html = BS(r.content, 'html.parser')


file = open('ex.xlsx', 'w')
df = pd.DataFrame({'Сюда, наверное, что-то нужно написать, но мне лень, поэтому здесь этот текст.': ['']})
df.to_excel('ex.xlsx', sheet_name='Начальная страница', index=False)
file.close()


file = open('authors.txt', 'w')
for link in html.find_all('a', href=True):
    s = link.get('href')
    if len(s) > 1 and s.startswith('/'):
        file.write('http://stih.su' + s + '\n')
file.close()


count = 0
for i in open('authors.txt').readlines():
    data = {}
    bio = ''
    r = rq.get(i[:-1])
    html = BS(r.content, 'html.parser')

    for el in html.select('.taxonomy-description > .page-title'):
        bio = el.text

    if bio == '':
        for elmt in html.select('.taxonomy-description > .title-subcategory'):
            bio = elmt.text

    verses = []

    for el in html.select('.number-navi > li'):
        verses.append(el.text)

    data[bio] = verses
    if bio != '':
        df = pd.DataFrame(data)

        with pd.ExcelWriter('ex.xlsx', mode='a') as writer:
            df.to_excel(writer, sheet_name=f'{bio}', index=False)

        count += 1
        print(f'№{count} {bio}')
