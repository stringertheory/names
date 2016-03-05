import sys
import os
import csv

import bs4
from dateutil.parser import parse as date_parse

url_file = open('nyp-urls.txt', 'w')

directory = sys.argv[1]
writer = csv.writer(sys.stdout)
writer.writerow(['url', 'headline', 'date'])

for filename in os.listdir(directory):
    path = os.path.join(directory, filename)
    with open(path) as infile:
        soup = bs4.BeautifulSoup(infile, 'lxml')
        for article in soup.find_all('article'):
            url = article.find('a')['href'].encode('utf8')
            headline = article.find('h3').get_text().strip().encode('utf8')
            meta = article.find('div', {'class': 'entry-meta'})
            date_string = meta.get_text().strip().replace('|', '')
            date = date_parse(date_string)
            row = [url, date, headline]
            writer.writerow(row)
            print >> url_file, url.rstrip('/')
            
url_file.close()
