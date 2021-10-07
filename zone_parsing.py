import sys,os
import re
import requests
import time
from bs4 import BeautifulSoup

project_dir = '../tr/tr/'

sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()


def get_html(url):
    r = requests.get(url)
    return r.text

def get_links(url):
    soup = BeautifulSoup(url, 'lxml')
    list = []
    container = soup.find('div', class_='_2JFxx view-container _31mcj _2s3Nk')
    links = container.find_all('a')
    for a in links:
        list.append(a)
    print (list)


def main():
    html = get_html("https://www.nic.ru/info/domains/all/")
    lists = get_links(html)

if __name__ == '__main__':
    main()
