# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests
from bs4 import BeautifulSoup


def getlinks(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    links = [link.get('href') for link in soup.find_all('a')]
    return links
base_URL = 'https://www.icpsr.umich.edu/NACJD/ORIs/'
ORI_root = baseURL + 'STATESoris.html'
links_from_root = getlinks(ORI_root)
links_from_root = [base_URL + link for link in links_from_root]

examplelink = links_from_root[0]
exdata = requests.get(examplelink)
exsoup = BeautifulSoup(exdata.text, 'xml')
exsoup_pretags = exsoup.find_all('pre')
example_content = exsoup_pretags[0].contents
ex_text = example_content[0].split('\n')
ex_text = [line.strip() for line in ex_text if not (line.startswith('CITY') or line =='')]