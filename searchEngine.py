import os
import re
import math
from bs4 import BeautifulSoup
import json
from collections import defaultdict  #for create_inverted_index
from nltk.stem import PorterStemmer
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext


inverted_index = defaultdict(list)  #tdefault dict will handle missing keys if necessary

stemmer = PorterStemmer()  #Initialize Porter Stemmer

#Used to load the content from a specified directory
def load_content(directory):
    documents = []  #Empty list to store the documents' data
    for subdirectory in os.listdir(directory):
        subdirectory_path = os.path.join(directory, subdirectory)
        if os.path.isdir(subdirectory_path):
            for fileName in os.listdir(subdirectory_path):  #Loops through the directory
                if fileName.endswith('.json'):
                    filePath = os.path.join(subdirectory_path, fileName)  #Combines directory and fileName to make a full path
                    with open(filePath, 'r', encoding='utf-8') as file:  #Encodes the file in utf-8 and reads the file
                        try:
                            data = json.load(file) #Extracts all the data in the JSON file
                            url = data.get("url")
                            content = data.get("content")
                            encoding = data.get("encoding") #Adds it to the documents list
                            documents.append({"filename": fileName, "url": url, "content": content, "encoding": encoding})
                        except json.JSONDecodeError:
                            print(f"Error decoding JSON in file {fileName}")
    print(f"Loaded {len(documents)} documents")  #Add this line to verify loaded documents
    return documents

#Clean HTML content using BeautifulSoup
def clean_html(raw_html):
    if raw_html:
        soup = BeautifulSoup(raw_html, "html.parser")
        important_words = set()
        for bold in soup.find_all(['b', 'strong']):
            important_words.update(bold.get_text().split())
        for heading in soup.find_all(['h1', 'h2', 'h3']):
            important_words.update(heading.get_text().split())
        title = soup.find('title')
        if title:
            important_words.update(title.get_text().split())
        # Clean out all HTML tags and get plain text
        text = soup.get_text()
        return text, important_words
    return "", set()

#Tokenize and stem text
def tokenize_text_and_stem(text):
    clean_text, important_words = clean_html(text) #Clean the text to exclude HTML tags
    raw_tokens = re.findall(r'[a-zA-Z]{2,}', clean_text.lower()) #Find sequences of alphabet characters that are at least 2 characters long
    #Stem tokens using Porter Stemmer
    stemmed_tokens = [stemmer.stem(token) for token in raw_tokens]
    print(f"Tokens: {stemmed_tokens}")  #Add this line to verify tokens
    return stemmed_tokens, important_words



#Create the inverted index
def create_inverted_index(documents):
    for document in documents:  #Iterate through documents list
        file_name = document['filename']  #Pull from load_content using type filename and type content
        content = document['content']
        if content:
            print(f"Document: {document['filename']}, Content length: {len(content)}")  #Verify content length
        term_frequency = defaultdict(int)  #Will also handle missing keys

        #Tokenize and stem the content
        tokens, important_words = tokenize_text_and_stem(content)
        for token in tokens:  #Iterate through the tokens
            term_frequency[token] += 1  #Increment term frequency of a found token per loop

        #Generate a posting using the term frequency, (Technically incomplete, since this only uses the "tf" in the tf-idf score)
        tokens, important_words = tokenize_text_and_stem(content)
        for token, frequency in term_frequency.items():
            posting = {
                'document': file_name,
                'url': document['url'], #added for GUI 
                'term_frequency': frequency,
                'important': token in important_words
            }
            inverted_index[token].append(posting)  #Add posting to the inv index
    return inverted_index

#Save the inverted index to a JSON file
def saveInvertedIndex(file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(inverted_index, file, indent=4)

def save_report(file_path, numDocuments, numUniqueTokens, indexSizeKB):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"Number of indexed documents: {numDocuments}\n")
        file.write(f"Number of unique tokens: {numUniqueTokens}\n")
        file.write(f"Total size of the index on disk (KB): {indexSizeKB}\n")

#M2-----------------------------------------

def calculate_tf_idf(posting, token, total_documents, document_frequencies):
    term_frequency = posting['term_frequency'] # gets the term frequency from a posting 
    document_frequency = document_frequencies.get(token, 1) # Checks how many documents the token, uses 1 count to avoid 0 errors
    tf_idf = term_frequency * math.log(total_documents / document_frequency) # Calculates tf_idf
    if posting['important']:
        tf_idf += 2
    return tf_idf

#Uses a query and the invertedIndex to look for the token
def search(query, invertedIndex, total_documents): 

    posting_list = [] #List for postings that contain the search query 
    query_tokens, _ = tokenize_text_and_stem(query) #Stemming and tokenizing query to make search more efficient 
    document_frequencies = {}

    for token in query_tokens: # Iterates through the tokens made from the query
        postings = invertedIndex.get(token, []) # makes a list of postings that contain the token
        document_frequencies[token] = len(postings)
        documents = {posting['document'] for posting in postings} # makes a set containing the document id of the postings 
        posting_list.append(documents) # appends the document names to posting_list


    if posting_list:
        result_docs = set.intersection(*posting_list) # makes a set where only the postings have all the tokens from the search query 
        if result_docs: # Checks if result_docs isn't empty
            ranked_results = [] # Creates a ranked results list 
            for doc in result_docs: # Iterates through result_docs
                score = 0 # Score Variable to store tf_idf
                url = ""
                for token in query_tokens: # Goes through the token in the search query
                    postings = invertedIndex.get(token, []) #gets the postings where the token is mentioned 
                    for posting in postings: # Iterated through the postings
                        if posting['document'] == doc: # if the posting document id matches the documentid from result_docs
                            score += calculate_tf_idf(posting, token, total_documents, document_frequencies) # add the tf_idf from this token to total score
                            url = posting['url'] #grab url from posting
                ranked_results.append((url, score)) #CHECK! Change back url to "doc" if doesnt work #Resolved
                # Once done going through tokens in query then it would add the total score and the document to the list as a tuple
            ranked_results.sort(key=lambda x:x[1], reverse=True) # Sorts the list based on the score, that's why its x[1]
            return [doc for doc, score in ranked_results] #returns a list of just doc ID's from tuples in ranked results. 
    return [] #Returns empty list if posting_list is empty 


#uses search function to display list results of search query
def search_gui(invertedIndex, total_documents): # not sure if we need invertedIndex since it seems to not be used int search function. Feel free to change
    def on_search():
        query = search_bar.get()
        results = search(query, invertedIndex, total_documents)  # Call the provided search function
        results_box.delete('1.0', tk.END)  # Clear previous results
        results_box.insert(tk.END, f"Found {len(results)} search results for '{query}'\n\n")

        results_box.tag_configure("blue_underline", foreground = "blue") #for hyperlink look

        if results:
            for result in results:
                url = result 
                results_box.insert(tk.END, f"{url}\n\n", "blue_underline")
        else:
            results_box.insert(tk.END, "No results found.")

    # Create the GUI
    root = tk.Tk()
    root.title("Simple Search Engine")
    root.configure(bg="#D3D3D3") # color

    # Frame for search label and search bar
    search_frame = tk.Frame(root, padx=10, pady=10)
    search_frame.pack(pady=10)

    # Search label
    search_label = tk.Label(search_frame, text="Search: ")
    search_label.pack(side=tk.LEFT)

    # Search bar
    search_bar = tk.Entry(search_frame, width=50)
    search_bar.pack(side=tk.LEFT)

    # Added Functionality to use "Enter" to search Note: throwing errors, leave for next milestone
    #search_bar.bind("<Return>", on_search) 

    # Text widget for showing results
    results_box = scrolledtext.ScrolledText(root, width=70, height=20, wrap=tk.WORD)
    results_box.pack(pady=10)

    # Search button
    search_button = tk.Button(root, text="Search", command=on_search)
    search_button.pack(pady=5)

    root.mainloop()


#Main function
def main():
    directory = "./ANALYST"
    documents = load_content(directory)
    inverted_index = create_inverted_index(documents)
    saveInvertedIndex("inverted_index.json")

    #Print data for the report
    num_documents = len(documents)
    num_unique_tokens = len(inverted_index)
    index_size_kb = os.path.getsize("inverted_index.json") / 1024

    print(f"Number of documents: {num_documents}")
    print(f"Number of unique tokens: {num_unique_tokens}")
    print(f"Index size (KB): {index_size_kb}")
    #Save the report to a text file
    save_report("report.txt", num_documents, num_unique_tokens, index_size_kb)

    with open("inverted_index.json", 'r', encoding='utf-8') as file:
        inverted_index = json.load(file)

#M2 TESTING ------------------------------------------------------------------------------------------------------------------------------
    #example of using search 
    #search_result = search("Elon Musk", inverted_index, num_documents)
    #print(search_result)

    #example of creating search GUI
    search_gui(inverted_index, num_documents)

if __name__ == "__main__":
    main()