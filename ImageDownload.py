import json
from haralyzer import HarParser
import os
from urllib.parse import urlparse
import requests


def getFileName(url):
    fileName = urlparse(url)
    return os.path.basename(fileName.path)

def file_download(url,fileName):

    response = requests.get(url)

    if response.status_code == 200:

        if os.path.isdir('Images') == False:
            os.mkdir('Images')
        
        with open(f'Images/{fileName}','wb') as savefile:
            savefile.write(response.content)
            print(f'Downloaded File {fileName}')
    else:
        print('Url is not Correct')


def extract_url(har_file):

    try:
        with open(har_file,'r') as har_file:  # Open The Har file
            har_data = json.load(har_file)    # Convert the Har File into json format
    except:
        print('Error Occur in Reading in this file ')
    har_parser = HarParser(har_data)

    try:

        for pages in har_parser.pages:
            
            entries = pages.entries
            for file in entries:

                try:
                    if 'response' in file and 'content' in file['response']:   # Check the content all aviable in particular page 
                        content = file['response']['content']
                        if 'mimeType' in content and content['mimeType'].startswith('image'):  # Check the page have image data or not
                            url = file['request']['url']
                            filename = getFileName(url)
                            file_download(url,filename)
                except:
                    print('No Image Data Found in the File')
    
    except:
        print('Their is no data in the file')



def file_Checking(file):
    if os.path.isfile(file):
        split = os.path.splitext(file)
        extention = split[1]
        if extention == '.har':
            extract_url(file)
        else:
            print('This file is not har file...')
    else:
        print('File Not Found')
    



har_file_path = input('Enter the file path har file : ')


file_Checking(har_file_path)



