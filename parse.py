import os
import sys
import bs4
import collections
import pymongo

def mongo_collection():
    collection = pymongo.MongoClient().poetry.poems
    return collection

def condition(element, transform=None):
    string = element.get_text()
    spaces = ' '.join(string.strip().split()).strip(',')
    if transform:
        return getattr(spaces, transform)()
    else:
        return spaces

def parse_about(about_div):
    result = {}
    for section in about_div.find_all('p', {'class': 'section'}):
        slug = section.find('span', {'class': 'slug'})
        section_name = condition(slug, transform='upper')
        result[section_name] = []
        for a_element in section.find_all('a'):
            result[section_name].append(condition(a_element))
    return result

collection = mongo_collection()
directory = sys.argv[1]
filename_list = os.listdir(directory)
for index, filename in enumerate(filename_list):
    path = os.path.join(directory, filename)
    print >> sys.stderr, index, len(filename_list), filename
    with open(path) as infile:
        soup = bs4.BeautifulSoup(infile, 'lxml')
        title = soup.find('div', {'id': 'poem-top'}).find('h1').get_text()
        main_div = soup.find('div', {'id': 'poem'})
        poem_div = main_div.find('div', {'class': 'poem'})
        about_div = main_div.find('div', {'class': 'about'})
        if not about_div:
            about_div = soup.find('div', {'id': 'about'})
        metadata = parse_about(about_div)
        for i in metadata.keys():
            if i not in KEYS:
                print [i]
                raise 'STOP'
        text = poem_div.get_text().strip()
        item = {
            '_id': filename,
            'title': title,
            'text': text,
        }
        item.update(metadata)
        collection.save(item)
