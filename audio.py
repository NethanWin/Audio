import requests
from bs4 import BeautifulSoup
import re
import os
import multiprocessing
import time
from moviepy.editor import concatenate_audioclips, AudioFileClip
#from pydub import AudioSegment


def download(url):
    files_list = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')    
    print('download starts')
    for a in soup.find_all('a', href=re.compile(r'http.*\.mp3')):
        filename = a['href'][a['href'].rfind("/") + 1:]
        doc = requests.get(a['href'])
        with open(filename, 'wb') as f:
            f.write(doc.content)
        files_list.append(filename)


"""everyting below this statment is not tested!!!"""


def pydub():
    # Define the path to the directory containing the mp3 files
    path = "path/to/mp3/files"

    # Define the output file name
    output_file = "output.m4b"

    # Get a list of all the mp3 files in the directory
    mp3_files = [f for f in os.listdir(path) if f.endswith(".mp3")]


    # Pydub approach
    start_time = time.time()
    combined_audio = AudioSegment.empty()
    for file in mp3_files:
        audio = AudioSegment.from_file(os.path.join(path, file), format="mp3")
        combined_audio += audio
    combined_audio.export(output_file, format="m4b")
    end_time = time.time()
    pydub_time = end_time - start_time


def multiprocessing():
    # Multiprocessing approach
    start_time = time.time()
    # Split the list of files into multiple sub-lists
    num_processes = multiprocessing.cpu_count()
    file_chunks = [mp3_files[i::num_processes] for i in range(num_processes)]
    
    # Define a function to combine a sub-list of MP3 files
    def combine_files(files):
        combined_audio = AudioSegment.empty()
        for file in files:
            audio = AudioSegment.from_file(os.path.join(path, file), format="mp3")
            combined_audio += audio
        return combined_audio
    
    # Start a separate process for each sub-list of files
    processes = []
    for files in file_chunks:
        p = multiprocessing.Process(target=combine_files, args=(files,))
        p.start()
        processes.append(p)
    
    # Wait for all processes to finish
    for p in processes:
        p.join()
    
    # Combine the output from each process into a single audio segment
    combined_audio = AudioSegment.empty()
    for p in processes:
        combined_audio += p.return_value
    
    # Export the combined audio as an m4b file
    combined_audio.export(output_file, format="m4b")
    end_time = time.time()
    multiprocessing_time = end_time - start_time


def main():
    url = "https://stephenkingaudiobooks.com/dark-tower-1/"
    download(url)
    # Compare performance
    # print(f"Pydub time: {pydub_time:.2f} seconds")
    # print(f"Multiprocessing time: {multiprocessing_time:.2f} seconds")
    
    

if __name__ == '__main__':
    main()