import sys
import requests

def iterdates(start_year, end_year):
    for year in range(start_year, end_year + 1):
        for month in range(1, 12 + 1):
            if year == 2011 and month < 7:
                continue
            yield year, month

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/47.0.2526.111 Safari/537.36'
    ),
    'Accept': 'text/html, */*; q=0.01',
    'Referer': 'http://nypost.com/2003/01/',
    'X-Requested-With': 'XMLHttpRequest',
}

# for year, month in iterdates(2005, 2015):
for year, month in iterdates(2011, 2016):
    base_url = 'http://nypost.com/%04i/%02i' % (year, month)
    headers['Referer'] = base_url
    unread_pages = True
    if year == 2011 and month == 7:
        page = 481
    else:
        page = 1
    while unread_pages:
        filename = 'Dropbox/newyorkpost/index/%04i-%02i-%04i.html' % (year, month, page)
        url = '%s/page/%i' % (base_url, page)
        print >> sys.stderr, url
        response = requests.get(url, headers=headers)
        with open(filename, 'w') as outfile:
            outfile.write(response.text.encode('utf8'))
        if response.status_code == 404:
            unread_pages = False
        page += 1
