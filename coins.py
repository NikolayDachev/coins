#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib2

dict = {
u'Злато с чистота':'Gold with purity',
u'Австралийски Лунар 2008':'Australian Lunar 2008',
u'Австралийски Лунар 2009':'Australian Lunar 2009',
u'Австралийски Лунар 2010':'Australian Lunar 2010',
u'Австралийски Лунар 2011':'Australian Lunar 2011',
u'Австралийски Лунар 2012':'Australian Lunar 2012',
u'Австралийски Лунар 2013':'Australian Lunar 2013',
u'Австралийски Лунар 2014':'Australian Lunar 2014',
u'Австралийски Лунар 2015':'Australian Lunar 2015',
u'Австралийски Лунар 1996-2007':'Australian Lunar 1996-2007',
u'Австралийски Лунар':'Australian Lunar',
u'Австралийско Кенгуру':'Australian Kangaroo',
u'Австрийски 4 дуката':'Australian 4 Ducat',
u'Австрийски дукат':'Australian Ducat',
u'Белгия Леополд II':'Belgian Leopold II',
u'Китайска Панда':'Chinese Panda',
u'Австрия 100 корона':'Austrian 100 Corona',
u'Турция 100 куруши':'Turkey 100 kurush',
u'Дания Кристиян X':'Denmark Christian X',
u'Американски Бизон':'American Bison',
u'Американски Орел':'American Eagle',
u'Британски суверен Елизабет':'British sovereign Elizabeth',
u'Британски монети':'British coins',
u'Франция Серес':'France Ceres',
u'Френски франк Genius':'FGE',
u'Френски франк Мариана':'FMR',
u'Канадски кленов лист':'Canadian maple leaf',
u'Германия Вилхелм II':'GMW',
u'Ванкувър':'GVA',
u'Сребро с чистота':'Silver with purity',
u'Унгария Франц Йозеф I':'HFO',
u'Италия Умберто I':'ILI',
u'Италия Виктор Емануел II':'ILI',
u'Кругерранд':'Krugerrand',
u'Мексико 50 песо':'MXP',
u'Франция Наполеон III':'N10',
u'Франция Наполеон III':'N20',
u'Северна Корея':'NKA',
u'Холандски Гулдер':'NLG',
u'Vienna Philharmonic':'PHA',
u'Златно кюлче':'Gold Bullion',
u'Френски франк Мариана':'Q10',
u'Русия Николай II':'R05',
u'Русия Николай II':'R10',
u'Швейцария Вренели':'SVR',
u'Тунис':'TUN',
u'Инвестиционно сребро':'Other Investment Silver',
u'Друго инвестиционно злато':'Other Investment Gold'
}

sys.path.append('./lib/')
from tabulate import tabulate
from bs4 import BeautifulSoup

url = "http://www.tavex.bg/index.php?main=8"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page)
page.close()

text = soup.get_text()
text = text.split('\n')

data = []
table = soup.find('table', attrs={'class':"prodListTbl"})
table_body = table.find('tbody')
if table_body is None:
    table_body = table
rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    if cols:
      data.append([ele for ele in cols if ele])

def name_pars(i):
    spl = i[1].split(' ')
    weight = spl[-1]
    weight = weight.strip('(').strip(')').strip('.')


# uncia
    if u'унц' in weight:
        weight = 'oz'
# grama
    if u'г' in weight[0]:
        weight = u'гр'

    if len(spl) > 2:
       size = spl[-2]
    size = size.strip('(').strip(')').strip('.')

# specific fixs
    if i[0] == u'CUR':
       i.insert(-2, '')
       i.insert(-2, '')
       i[1] = ' '.join(spl)
    else:
       i.insert(-2, size)
       i.insert(-2, weight)
       i[1] = ' '.join(spl[0:-2])

    try:
        i[-2] = float(i[-2])
    except ValueError:
        i[-2] = 0

    try:
        i[-1] = float(i[-1])
    except ValueError:
        i[-1] = 0

    return i

# format data for table
data = [name_pars(row) for row in data if row]
# sort data by КОД
data = sorted(data, key=lambda x: x[0])

for i in data:
    if i[1] in dict.keys():
        i[1] = dict[i[1]]

### MAIN ###
if __name__ == "__main__":

   if len(sys.argv) > 1:
      if sys.argv[1] in [x[0] for x in data]:
         for i in data:
            if i[0] == sys.argv[1]:
               print i[-2]
               print i[-1]
               sys.exit(0)

      searchtb = []
      for i in data:
          if sys.argv[1] in i:
             searchtb.append(i)
      data = searchtb

   menu = ['CODE', 'NAME', 'WEIGHT', 'UNIT', 'BUY (BGL)', 'SELL (BGL)']
   print tabulate(data, menu)


