#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import urllib2
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

   menu = [u'КОД', u'ИМЕ', u'ТЕГЛО', u'ЕДЕНИЦА', u'КОПУВА (BGL)', u'ПРОДАВА (BGL)']
   print tabulate(data, menu)
