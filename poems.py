import pprint
import json
import bs4
import time
import random
import sys
import collections
import requests
import requests_cache
requests.exceptions.ConnectTimeout

def make_throttle_hook(wait_factor=1, n_average=3):
    waits = collections.deque(maxlen=n_average)
    def hook(response, *args, **kwargs):
        if not wait_factor:
            return response
        if not getattr(response, 'from_cache', False):
            waits.append(response.elapsed.total_seconds())
            average_wait = wait_factor * sum(waits) / len(waits)
            this_wait = random.expovariate(1 / average_wait)
            msg = (
                f'{average_wait:.02f} elapsed, '
                f'waiting for {this_wait:.02f} seconds'
            )
            print(msg, file=sys.stderr)
            time.sleep(this_wait)
        else:
            msg = f'got {response.url} from cache'
            print(msg, file=sys.stderr)
        return response
    return hook


class CachedSession(requests_cache.CachedSession):

    def delete_url(self, url, params=None):
        request = requests.Request('GET', url, params=params)
        return self.cache.delete_url(self.prepare_request(request).url)

session = CachedSession(cache_name='poetryfoundation')
session.hooks = {
    'response': make_throttle_hook(1),
}


url = "https://www.poetryfoundation.org/ajax/poems"
params = {
    'page': 1,
    'sort_by': 'recently_added',
}
headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "authority": "www.poetryfoundation.org",
    "referer": "https://www.poetryfoundation.org/poems/browse",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/79.0.3945.130 Safari/537.36"
    )
}

def parse_poem(response, entry):

    soup = bs4.BeautifulSoup(response.text, 'lxml')

    schema_data = json.loads(
        soup.find('script', {'type': 'application/ld+json'}).contents[0]
    )
    poem_schema = {}
    for node in schema_data.get('@graph', []):
        if node.get('@type') == 'CreativeWork':
            poem_schema = node

    author = poem_schema.get('author', {}).get('name')
    title = poem_schema.get('name')
    text = poem_schema.get('text')

    poem_div = soup.find('div', {'class': 'o-poem'})
    html = poem_div.decode(formatter='html')

    tag_id_set = set()
    tags = []
    sidecar = soup.find('div', {'class': 'c-sidecar-panel'})
    if sidecar:
        for ul in sidecar.find_all('ul', {'class': 'o-hList'}):
            for li in ul.find_all('li'):
                if li.a:
                    _, tag_string = li.a['href'].rsplit('#', 1)
                    tag_type, tag_number = tag_string.split('=')
                    tag_id = int(tag_number)
                    tag_title = li.get_text().strip()
                    tags.append({
                        'id': tag_id,
                        'type': tag_type,
                        'title': tag_title,
                    })
                    tag_id_set.add(tag_id)

    for category in entry.get('categories', []):
        tag_id = category.get('id')
        if tag_id and tag_id not in tag_id_set:
            tags.append({
                'id': tag_id,
                'title': category.get('title'),
            })
                    
    return {
        '_id': entry.get('id'),
        'url': entry.get('link'),
        'author': author,
        'title': title,
        'text': text,
        'html': html,
        'tags': tags,
    }
    
TIMEOUT = 5
while True:
    response = session.get(url, params=params, headers=headers)
    print(response.url)
    data = response.json()
    params['page'] += 1

    for entry in data.get('Entries', []):
        link = entry.get('link')
        if link:
            try:
                entry_response = session.get(link, timeout=TIMEOUT)
            except:
                continue
            else:
                print(entry_response.url)

            # pprint.pprint(parse_poem(entry_response, entry))
            # if 'blossoms-haiku-senryu' in entry_response.url:
            #     raise 'STOP'
    
    if not data.get('Entries'):
        break
