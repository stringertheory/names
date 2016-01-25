import os
import sys
import urlparse
import time
import random

import requests
import bs4

FILENAME = 'Dropbox/poems-urls.txt'
BASE_URL = 'http://www.poetryfoundation.org/searchresults'
HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/37.0.2062.124 Safari/537.36'
    ),
    'Referer': 'http://www.poetryfoundation.org/browse/',
    'X-Requested-With': 'XMLHttpRequest',
}

def read_url_set(filename):
    result = set()
    if os.path.isfile(filename):
        with open(filename) as infile:
            for line in infile:
                result.add(line.strip())
    return result

def add_new_urls(url, url_set):
    params = {
        'page': 1,
    }
    finished = False
    while not finished:
        new_url_set = set()
        print >> sys.stderr, url, params
        response = requests.get(url, headers=HEADERS, params=params)
        soup = bs4.BeautifulSoup(response.text, "lxml")
        a_list = soup.find_all('a', {'class': 'title'})
        if a_list:
            for a_element in a_list:
                poem_url = urlparse.urljoin(BASE_URL, a_element['href']).strip()
                new_url_set.add(poem_url)
        else:
            finished = True

        for poem_url in new_url_set:
            if poem_url in url_set:
                finished = True
            url_set.add(poem_url)

        params['page'] += 1
        time.sleep(0.1 + 0.1 * random.random())
    
def write_url_set(url_set, filename):
    with open(filename, 'w') as outfile:
        for url in sorted(url_set):
            outfile.write(url + '\n')
        
url_set = read_url_set(FILENAME)

add_new_urls(BASE_URL, url_set)

print url_set

write_url_set(url_set, FILENAME)
