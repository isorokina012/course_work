#блок імпорту бібліотек та модулів
import requests #бібліотека для роботи з HTTP запитами
from bs4 import BeautifulSoup #бібліотека для парсингу контенту отримано з HTTP запита
import csv #вбудований модуль Python для роботи з файлами csv
import os #вбудований модуль Python для роботи з операцыйною системою

#блок задання констант
URL = 'https://citaty.info/book/quotes' #посилання на сайт, який будемо парсити
HEADERS = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
           'accept': '*/*'} #словник із заголовками, щоб сервер сайту не вважав програму за бота та дозволив доступ
FILE_CSV = 'quotations_csv.csv' #назва файлу для запису результатів парсингу

#функція для виконання get запитів (отримання інформації з веб-сторінки)
def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

"""функція для отримання контенту з HTML коду і запису потрібної нам текстової
інформації в список, виведення її на консоль і запис у файл csv та відкриття після запису"""
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='node__content')

    quotations =[]
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
    return quotations
    save_file_csv(quotations, FILE_CSV)
    os.startfile(FILE_CSV)


#функція для збереження отриманої інформації у файл csv
def save_file_csv (items, path):
    with open(path, 'w', newline='') as file:
        writer=csv.writer(file, delimiter=';')
        writer.writerow(['Autor', 'Book', 'Quotation', 'Tags'])
        for item in items:
            writer.writerow([item['autor'], item['book'], item['text_quotation'], item['topic_tags']])

#основна функція для звернення до всіх інших функцій та ввімкнення програми
def parse():
    html = get_html(URL)
    if html.status_code == 200 :
        get_content(html.text)
    else:
        print('Error!')

parse()