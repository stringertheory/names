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

def parse_author(author_span):
    result = {}
    a_element = author_span.find('a')
    if a_element:
        text = a_element.get_text().strip()
        name = ' '.join(i for i in text.split() if i)
        result['POET'] = name
    return result

def parse_text(poem_div):
    result = []
    for div in poem_div.find_all('div'):
        sentence = div.get_text().rstrip()
        result.append(sentence)

    if not result:
        text = poem_div.get_text().rstrip()
        if text:
            result = [text]

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
        author_span = soup.find('span', {'class': 'author'})
        authordata = parse_author(author_span)
        if not about_div:
            about_div = soup.find('div', {'id': 'about'})
        metadata = parse_about(about_div)
        text = parse_text(poem_div)
        item = {
            '_id': filename,
            'title': title,
            'text': text,
        }
        item.update(authordata)
        item.update(metadata)
        collection.save(item)
