import bs4
import pymongo

collection = pymongo.MongoClient().poetry.poems

for i, document in enumerate(collection.find({'html': {'$exists': True}}).batch_size(5), 1):

    html = document.get('html')
    soup = bs4.BeautifulSoup(html, 'lxml')

    lines = []
    for div in soup.find_all('div'):
        if not div.find('div'):
            for line in div.get_text().split('\n'):
                lines.append(line.strip())
    
    document['lines'] = lines

    collection.update_one(
        {'_id': document.get('_id')},
        {'$set': {'lines': lines}},
    )
    print(i, document['_id'])
