import requests
import sys, os
import csv
import time
import urllib.request
from bs4 import BeautifulSoup
from random import choice, uniform

mainUrl = 'https://www.houzz.es/professionals/arquitectos/'
flow = 0 #delete after finishing

# def get_html(url): 
#     response = urllib.request.urlopen(url)
#     return response.read()

def get_html(url, useragent=None, proxy=None): 
    response = requests.get(url, headers=useragent, proxies=proxy)
    return response.text

def get_profies_count(html):
    soup = BeautifulSoup(html)
    num = soup.find('h1').text
    num = num.replace('.','')
    num = num.rsplit(' ', 4)
    count = int(num[0])
    
    return count

def check_el(element):
    if element:
        return element.span.text
    else:
        return 'none'

def parse(html):
    soup = BeautifulSoup(html)
    proList = soup.find('div', class_='browseListBody')
    
    
    profies = []

    for proCard in proList.find_all('div', class_='pro-card'):
        
        profies.append({
            'name': proCard.find('div', class_='name-info').a.text,
            'link': proCard.find('div', class_='name-info').a.get('href'),
            'phone': check_el(proCard.find('li', class_='pro-phone')),
            'location': check_el(proCard.find('li', class_='pro-location'))
            })
        global flow
        flow = flow + 1
        # print(flow)

    return profies

def createFile(profies, path):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Name', 'Link', 'Phone', 'Location'))

        writer.writerows(
            (profi['name'], profi['link'], profi['phone'], profi['location']) for profi in profies
        )


def main():
    print('Введи полный url нужно категории:\n(Пример https://www.houzz.es/professionals/s/fabricas_de_madera/)')
    print('C какой страницы начинать парсинг?')
    #setPage = input()
    #setPage = int(setPage)
    # setPage = (setPage - 1) * 15
    # print('До какой страницы включительно необходимо парсить?')
    # profies_count = input()
    # profies_count = int(profies_count)
    # profies_count = profies_count * 15

    print('Процесс парсинга сейчас начнется')
    time.sleep(2)


    #profies_count = get_profies_count(get_html(mainUrl))
    #print('Всего записей', profies_count)

    profies = []
    setPage = 0
    profies_count = 100

    pathname = os.path.dirname(sys.argv[0])       
    uaPath = pathname + '/useragents.txt'
    proxiesPath = pathname + '/proxies.txt'
    resultPath = pathname + '/result.csv'

    print('Загрузка список UA')
    useragents = open(uaPath).read().split('\n')
    print('Загрузка списка Proxy')
    proxies = open(proxiesPath).read().split('\n')

    while setPage < profies_count:
        proxy = {'http': 'http://' + choice(proxies)}
        #print('Выбран proxy для итерации')
        useragent = {'User-Agent': choice(useragents)}
        # print('Выбран proxy для итерации')
        try:
            #profies.extend(parse(get_html(mainUrl + 'p/%d' %setPage)))
            profies.extend(parse(get_html(mainUrl + 'p/%d' %setPage, useragent, proxy)))
        except:
            continue
        print('Подключение к странице: ' + mainUrl + 'p/%d' %setPage)
        print('Парсинг %d%% (%d/%d)' % (setPage / profies_count * 100, setPage, profies_count))
        profies.extend(parse(get_html(mainUrl + 'p/%d' % setPage)))
        createFile(profies, resultPath)
        #print('Пересоздание файла')
        setPage = setPage + 15
        # print(profies)
        pause = uniform(15,30)
        time.sleep(pause)

    

if __name__ == '__main__':
    main()
