# downloader imports
from pydub import AudioSegment
import os
import multiprocessing
import time


# extractor imports
import requests
from bs4 import BeautifulSoup
import os


def download():
    # the url you want to download from
    url = "https://stephenkingaudiobooks.com/the-drawing-of-the-three/"
    
    # send a request to the url and get the response object
    response = requests.get(url)
    
    # extract the page HTML content
    html_content = response.content
    
    # create a BeautifulSoup object for parsing the HTML content
    soup = BeautifulSoup(html_content, "html.parser")
    
    # find all the <a> tags with an href attribute that ends in ".mp3"
    mp3_links = soup.find_all("a", href=lambda href: href.endswith(".mp3"))
    
    # create a directory to store the downloaded mp3 files
    if not os.path.exists("mp3_files"):
        os.makedirs("mp3_files")
    
    # loop through each mp3 link and download the file
    for link in mp3_links:
        mp3_url = link["href"]
        # use the last part of the URL as the file name
        file_name = mp3_url.split("/")[-1]
        # create the file path
        file_path = os.path.join("mp3_files", file_name)
        # download the file
        with open(file_path, "wb") as f:
            f.write(requests.get(mp3_url).content)


def temp():
    # Define the path to the directory containing the mp3 files
    path = "path/to/mp3/files"

    # Define the output file name
    output_file = "output.m4b"

    # Get a list of all the mp3 files in the directory
    mp3_files = [f for f in os.listdir(path) if f.endswith(".mp3")]


def pydub():
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
    download()
    
    # Compare performance
    # print(f"Pydub time: {pydub_time:.2f} seconds")
    # print(f"Multiprocessing time: {multiprocessing_time:.2f} seconds")
    
    

