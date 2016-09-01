'''
This program demonstrates how you can perform web scraping from a website of your choice and extract only the desired information
by pruning the various design and tag elements.
 1.The getSoup function takes care of the errors that might occur while requesting a web page, so that it becomes easier to debug.
 2.The get_news_links function is called by passing the BASE_URL. The BeautifulSoup package is to used to locate and extract the 
portion of text corresponding to a specific sequence of tags. It then returns the links by storing in a Python dictionary.
NOTE : These codes are strictly for educational purposes. Use them sensibly.
'''

from urllib2 import urlopen
from bs4 import BeautifulSoup
from urllib2 import HTTPError

BASE_URL = "http://makautexam.net/"

def getSoup(url):
    try:
        html = urlopen(url).read()
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html, "lxml")
    except AttributeError as e:
        return None
    return bsObj

def get_news_links(url):
    soup = getSoup(url)
    news_sec = soup.find("div", {"class": "block-hdnews"})
    # We'll put the details we want to hang on to in this dictionary
    news_show = []
    for li in news_sec.findAll("li"):
        url_var = BASE_URL + li.a["href"]
        sub_var = li.p.get_text()
        news_show.append({'url': url_var, 'subject': sub_var})
    return news_show

if __name__ == '__main__':
    news_many = get_news_links(BASE_URL)
    # We now have details (in our dictionary) for each inmate. Let's print those out.
    for news in news_many:
        print '{0}, {1}'.format(news['subject'], news['url'])
