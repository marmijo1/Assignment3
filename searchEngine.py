import os 
import re
#from bs4 import BeautifulSoup #uncomment this when needed, it was throwing me errors while i was testing cuz it wasnt being used (-Tsunami)
import json
from collections import defaultdict#for create_inverted_index
from nltk.stem import PorterStemmer

all_tokens = []  #global
<<<<<<< HEAD
inverted_index = defaultdict(list) #tdefault dict  will handle missing keys if necessary

stemmer = PorterStemmer() # Intialize Porter Stemmer
=======

from collections import defaultdict #for create_inverted_index

>>>>>>> edfa1e777f49020342ab53b13c71343f6209565c
# Used to load the content from a specified directory
def load_content(directory):
    documents = [] #Empty list to store the documents' data 
    for subdirectory in os.listdir(directory):
        subdirectory_path = os.path.join(directory, subdirectory)
    if os.path.isdir(subdirectory_path):
        for fileName in os.listdir(subdirectory_path):  #loops through the directory
        
            if fileName.endswith('.json'):

                filePath = os.path.join(subdirectory_path, fileName) #Combines directory and fileName to make a full path
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
    print(f"Loaded {len(documents)} documents")  # Add this line to verify loaded documents
    return documents

#tokenizer (needs work,, add filters?)
<<<<<<< HEAD
def tokenize_text_and_stem(text):
    # tokens = []
    # excluded_terms = {} #include any excluded terms here <<-------

    # Find sequences of alphabet characters that are at least 2 characters long
    raw_tokens = re.findall(r'[a-zA-Z]{2,}', text.lower())
    #
    # # Filter out unwanted tokens
    # for token in raw_tokens:
    #     normalized_token = token.lower()
    #     if normalized_token not in excluded_terms:
    #         tokens.append(normalized_token)
    stemmed_tokens = [stemmer.stem(token) for token in raw_tokens]
    # Update the master token list
    # append_to_token_list(tokens)
    print(f"Tokens: {stemmed_tokens}")  # Add this line to verify tokens
    return stemmed_tokens

# def append_to_token_list(new_tokens): #helper for tokenizer. You can leave this alone
#     global all_tokens
#     all_tokens.extend(new_tokens) #this will hold the tokens permanently. NOte: May need to clear memory after runs, depending on how we implement this
    #I figured we can store the inverted index into a JSON file for better memory usage (when looking
    #at the porter stemmer on various websites like geeksforgeeks.org suggested keeping inverted index in file)
=======
def tokenize_text(text):
    tokens = []
    excluded_terms = {} #include any excluded terms here <<-------

    # Find sequences of alphabet characters that are at least 2 characters long
    raw_tokens = re.findall(r'[a-zA-Z]{2,}', text)

    # Filter out unwanted tokens
    for token in raw_tokens:
        normalized_token = token.lower()
        if normalized_token not in excluded_terms:
            tokens.append(normalized_token)
    
    # Update the master token list
    append_to_token_list(tokens)
    return tokens

def append_to_token_list(new_tokens): #helper for tokenizer. You can leave this alone
    global all_tokens
    all_tokens.extend(new_tokens) #this will hold the tokens permanently. NOte: May need to clear memory after runs, depending on how we implement this

>>>>>>> edfa1e777f49020342ab53b13c71343f6209565c

#inv idx creation 
def create_inverted_index(documents):

<<<<<<< HEAD

=======
    inverted_index = defaultdict(list) #tdefault dict  will handle missing keys if necessary
>>>>>>> edfa1e777f49020342ab53b13c71343f6209565c
    
    #Implementation Required

    for document in documents: #iterate through documents list 
        file_name = document['filename'] #pull from load content use type filename and type content
        content = document['content']
<<<<<<< HEAD
        if content:
            print(
                f"Document: {document['filename']}, Content length: {len(content)}")  # Verify content length

        term_frequency = defaultdict(int)  #will also handle missing keys

        tokens = tokenize_text_and_stem(content)
=======

        term_frequency = defaultdict(int)  #will also handle missing keys

        tokens = tokenize_text(content)
>>>>>>> edfa1e777f49020342ab53b13c71343f6209565c
        for token in tokens: #iterate through the tokens
            term_frequency[token] += 1 #increment term frequency of a found token per loop


        #Generate a posting using the term frequency, (Technically incomplete, since this only uses the "tf" in the tf-idf score)
        for token, frequency in term_frequency.items():
            posting = {
                'document': file_name,
                'term_frequency': frequency
            }
            inverted_index[token].append(posting) # add posting to the inv index
        
    return inverted_index

<<<<<<< HEAD
#Save the inverted index to a JSON file
def saveInvertedIndex(file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(inverted_index, file, indent =4)

def save_report(file_path, numDocuments, numUniqueTokens, indexSizeKB):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"Number of indexed documents: {numDocuments}\n")
        file.write(f"Number of unique tokens: {numUniqueTokens}\n")
        file.write(f"Total size of the index on disk (KB): {indexSizeKB}\n")

=======
>>>>>>> edfa1e777f49020342ab53b13c71343f6209565c
#for output file, reading the terminal with this many lines frickin sux 
def write_to_file(inverted_index, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for token, postings in inverted_index.items():
            file.write(f"Token: {token}\n")
            for posting in postings:
                file.write(f"  Document: {posting['document']}, Term Frequency: {posting['term_frequency']}\n")
            file.write("\n")  # 4 readability purposes


#This is just a trial run that I tried to see if it's parsing through the information correctly. 
<<<<<<< HEAD
# data_directory = os.path.join(os.path.dirname(__file__), 'ANALYST', 'www_cs_uci_edu')
# documents_test = load_content(data_directory)
# print(f"loaded {len(documents_test)} documents")
#
# #Create the inverted index
# inverted_index = create_inverted_index(documents_test) #using documents_test)
#
#
#
# output_file_path = os.path.join(os.path.dirname(__file__), 'invertedIDX_output.txt')
# write_to_file(inverted_index, output_file_path)
#
# print(f"Inverted index written to {output_file_path}")

def main():
    directory = "./ANALYST"
    documents = load_content(directory)
    inverted_index = create_inverted_index(documents)
    saveInvertedIndex("inverted_index.json")

    # Print data for the report
    num_documents = len(documents)
    num_unique_tokens = len(inverted_index)
    index_size_kb = os.path.getsize("inverted_index.json") / 1024

    print(f"Number of documents: {num_documents}")
    print(f"Number of unique tokens: {num_unique_tokens}")
    print(f"Index size (KB): {index_size_kb}")
    # Save the report to a text file
    save_report("report.txt", num_documents, num_unique_tokens, index_size_kb)

if __name__ == "__main__":
    main()
=======
data_directory = os.path.join(os.path.dirname(__file__), 'ANALYST', 'www_cs_uci_edu')
documents_test = load_content(data_directory)
print(f"loaded {len(documents_test)} documents")

#Create the inverted index
inverted_index = create_inverted_index(documents_test) #using documents_test)



output_file_path = os.path.join(os.path.dirname(__file__), 'invertedIDX_output.txt')
write_to_file(inverted_index, output_file_path)

print(f"Inverted index written to {output_file_path}")
>>>>>>> edfa1e777f49020342ab53b13c71343f6209565c
