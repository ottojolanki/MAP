# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests
from bs4 import BeautifulSoup


def get_links(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    links = [link.get('href') for link in soup.find_all('a')]
    return links

def get_ORIS_from_link(link):
    data = requests.get(link)
    data_soup = BeautifulSoup(data.text, 'lxml')
    data_pretags = data_soup.find_all('pre')
    result  = []
    for tag in data_pretags:
        for tag_token in tag:   
            content = tag_token.string.split('\n')
            content_tidy = [line.strip() for line in content if not (line.startswith('CITY') or line =='')]
            result.extend(content_tidy)
    return result
        
        
    
base_URL = 'https://www.icpsr.umich.edu/NACJD/ORIs/'
ORI_root = baseURL + 'STATESoris.html'
links_from_root = get_links(ORI_root)
links_from_root = [base_URL + link for link in links_from_root]
ORI_dictionary = dict()


examplelink = links_from_root[0]
exdata = requests.get(examplelink)
exsoup = BeautifulSoup(exdata.text, 'xml')
exsoup_pretags = exsoup.find_all('pre')
example_content = exsoup_pretags[0].contents
ex_text = example_content[0].split('\n')
ex_text = [line.strip() for line in ex_text if not (line.startswith('CITY') or line =='')]
