import urllib.request
import requests
from bs4 import BeautifulSoup
import scrapy

net_default = 'https://'

def fetch_ir(ir_url):
    response = requests.get(ir_url)

    if response.status_code == 200:
        ir_html = response.text
        ir_soup = BeautifulSoup(ir_html, 'html.parser')
        return ir_soup
    else:
        print(response.status_code)

def alt_fetch_ir(ir_url):
    user_agent = 'Mozilla/5.0'
    headers = {'User-Agent' : user_agent}    
    request = urllib.request.Request(url=ir_url, headers=headers)
    req = urllib.request.urlopen(request)
    soup = BeautifulSoup(req, 'html.parser')
    return soup

def aspx_ir(ir_url):
   pass 


ir_url = 'https://investors.ionq.com/news/default.aspx'


#Select newest article
# newest = soup.select_one('.module_item')
# link = soup.select_one('.module_item > .module_headline-link > a').get('href')

# #Make a list containing date, title and link
# elements = [element.text.strip() for element in newest if element.text != '\n']
# elements.append(link)
