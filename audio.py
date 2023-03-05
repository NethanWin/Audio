import requests
from bs4 import BeautifulSoup
import re
import os
import tempfile
from pydub import AudioSegment


INSTALL_PATH = os.path.join(os.path.expanduser("~"), "Downloads")
TEMP_INSTALL_PATH = os.path.join(INSTALL_PATH, "temp_mp3")


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
    print(url)
    path = TEMP_INSTALL_PATH

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
        print(filename)


def get_url_title(url):
    url_content = requests.get(url).content
    url_title = BeautifulSoup(url_content, 'html.parser').title.string
    return url_title


def is_inner_url_exist(homepage_title, inner_url):
    return homepage_title != get_url_title(inner_url)


def combine_mp3_files(url):
    filename = '{}.m4a'.format(url.split('/')[-2])
    # create output file path in Downloads folder
    output_path = os.path.join(INSTALL_PATH, filename)

    # get list of all mp3 files in directory
    mp3_files = sorted([f for f in os.listdir(TEMP_INSTALL_PATH) if f.endswith(".mp3")])

    # combine mp3 files into a single audio segment
    audio_segment = AudioSegment.empty()
    for mp3_file in mp3_files:
        audio_segment += AudioSegment.from_file(os.path.join(TEMP_INSTALL_PATH, mp3_file))

    # export audio segment as m4a file
    audio_segment.export(output_path, format="mp3")#, tags={'album': 'Combined Audiobooks'})

    print("Combined MP3 files to M4B: ", output_path)


def main():
    homepage_url = "https://staraudiobooks.net/stephen-king-drawing-of-three-dt2-audio-book/"
    
    downlad_url_manager(homepage_url)
    print('download finished')
    combine_mp3_files(homepage_url)
    print('combine finished')

    #delete temp_mp3 folder
    

if __name__ == '__main__':
    main()
