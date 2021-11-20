import requests
from bs4 import BeautifulSoup
import csv
import os


URL = 'https://citaty.info/book/quotes'
HEADERS = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
           'accept': '*/*'}
FILE_CSV = 'quotations_csv.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='node__content')

    quotations = []
    for item in items:

        topic_tags = item.find('div', class_='node__topics')
        if topic_tags:
            topic_tags = topic_tags.get_text(', ')
        else:
            topic_tags = 'No tags'

        quotations.append({
            'autor': item.find('a', title='Автор цитаты').get_text(),
            'book': item.find('a', title='Цитата из книги').get_text(),
            'text_quotation': item.find('div', class_='field-item even last').get_text().replace('\xa0', ' ').replace('\n', ' '),
            'topic_tags': topic_tags
        })
    print(*quotations, sep='\n')
    save_file_csv(quotations, FILE_CSV)
    os.startfile(FILE_CSV)


def save_file_csv (items, path):
    with open(path, 'w', newline='') as file:
        writer=csv.writer(file, delimiter=';')
        writer.writerow(['Autor', 'Book', 'Quotation', 'Tags'])
        for item in items:
            writer.writerow([item['autor'], item['book'], item['text_quotation'], item['topic_tags']])


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('Error!')


parse()