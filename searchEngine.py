import os 
from bs4 import BeautifulSoup
import json

# Used to load the content from a specified directory
def load_content(directory):
    documents = [] #Empty list to store the documents' data 
    
    for fileName in os.listdir(directory):  #loops through the directory
        
        if fileName.endswith('.json'):  

            filePath = os.path.join(directory, fileName) #Combines directory and fileName to make a full path
            with open (filePath, 'r', encoding='utf-8') as file: # Encodes the file in utf-8 and reads the file
                try: 
                    data = json.load(file) 
                    
                    #Extracts all the data in the json data
                    url = data.get("url")
                    content = data.get("content")
                    encoding = data.get("encoding")

                    #Adds it to the documents list 
                    documents.append({"filename": fileName, "url": url, "content": content, "encoding": encoding})

                except json.JSONDecodeError:
                    print(f"Error decoding JSON in file {fileName}")
    return documents


#This is just a trial run that I tried to see if it's parsing through the information correctly. 
data_directory = os.path.join(os.path.dirname(__file__), 'ANALYST', 'www_cs_uci_edu')
documents_test = load_content(data_directory)
print(f"loaded {len(documents_test)} documents")