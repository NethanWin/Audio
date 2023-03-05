import requests
from bs4 import BeautifulSoup
import re
import os
import tempfile


# manage many inner urls from the same main url
def downlad_url_manager(homepage_url):
    # downlad_url the first page
    downlad_url(homepage_url)

    homepage_title = get_url_title(homepage_url)
    page_number = 2
    inner_url = homepage_url + str(page_number)
    # as long as the inner pages exist downlad_url the mp3
    while is_inner_url_exist(homepage_title, inner_url):
        downlad_url(inner_url)
        page_number += 1
        inner_url = homepage_url + str(page_number)
        

def downlad_url(url):
    path = os.path.join(os.path.expanduser("~"), "downlad_urls", "temp_mp3")

    if not os.path.exists(path):
        os.makedirs(path)
    
    files_list = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')    
    for a in soup.find_all('a', href=re.compile(r'http.*\.mp3')):
        filename = os.path.join(path, a['href'][a['href'].rfind("/") + 1:])
        doc = requests.get(a['href'])
        with open(filename,'wb') as f:
            f.write(doc.content)
        files_list.append(filename)


def get_url_title(url):
    url_content = requests.get(url).content
    url_title = BeautifulSoup(url_content, 'html.parser').title.string
    return url_title


def is_inner_url_exist(homepage_title, inner_url):
    return homepage_title != get_url_title(inner_url)


def main():
    homepage_url = "https://staraudiobooks.net/stephen-king-drawing-of-three-dt2-audio-book/"
    downlad_url_manager(homepage_url)
    # combine
    #delete temp_mp3 folder
    

if __name__ == '__main__':
    main()
