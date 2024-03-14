import requests
from bs4 import BeautifulSoup
import os
import time
import sys

# Initial page with chess openings.
CHESS_OPENINGS = 'https://www.thechesswebsite.com/chess-openings/'

# Converts a web page to the soup container.
# Ignores pages which are not responding.
def soup_converter(page_url): 
    r = requests.get(page_url)
    
    if not r.status_code == 200:
        return -1
    
    my_html = r.text
    soup = BeautifulSoup(my_html, 'html.parser')

    return soup

# From a CHESS_OPENNINGS it takes all hrefs
# to next pages and saves it to the list. 
# After that returns list.
def create_links(initial_page_url):
    soup = soup_converter(initial_page_url)

    # The page contains two cb-containers, we 
    # need only the second one.
    _, link_fragment = soup.find_all(id='cb-container')
    all_links = []

    # All hrefs are in 'a' block.
    for link in link_fragment.find_all('a'):
        if not 'MEMBERS ONLY' in link.text:
            all_links.append(link.get('href'))
    
    return all_links

# For a given page this function will scrape
# some needed information about the chess opening:
# opening name, description, movements, comments.
# After scraping it will return this information as 
# a list.
def page_analyzer(page_url):

    # (1) Page title,
    # (2) Some text,
    # (3) Movements,
    # (4) Some information about opening. 
    page_information = []

    # Technical variable for controlling 
    # the number of "block information" we 
    # want to save.
    counter = 0

    # Standard soup converting.  
    soup = soup_converter(page_url)

    # If there was a respond, find and save 
    # the page information.
    if not soup == -1:

        # Saving title.
        page_information.append(soup.title.string)

        # Description, movements, comments are in 'p'.
        all_paragraphs = soup.find_all('p')

        for paragraph in all_paragraphs:
            if counter == 0:
                counter += 1
            elif counter <= 4:
                counter += 1
                page_information.append(paragraph.get_text())
            else:
                break    
    
        return page_information

# Creates all links from a main page,
# processes each of the links independently,
# for each chess opening creates a file in 
# markdown folder with the .md extension.
# NOTE: the markdown folder has to be empty.
def main(initial_page_url):
    page_information = []
    folder_path = 'markdown'
    progress = 1
    all_links = create_links(initial_page_url)
    
    # Creates markdown folder
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    for link in all_links:

        # Anti bot method. 
        time.sleep(2)
        page_information = page_analyzer(link)

        # Check if there was any respond and that 
        # this repspond is 200.
        if not page_information == [] and page_information is not None:  
            file_name = page_information[0]
            file_name = file_name.replace(" ", "_") + ".md"
            full_path = os.path.join(folder_path, file_name)
            
            with open(full_path, "a") as f:
                for i in range(4):
                    if i == 0:
                        string = "# " + page_information[i] + "\n"
                    else:
                        string = page_information[i] + "<br>"

                    f.write(string)

        # Printing out the progress.
        sys.stdout.write("Number of downloaded pages: %d   \r" % (progress) )
        sys.stdout.flush()         
        progress += 1   

if __name__ == "__main__":
    main(CHESS_OPENINGS)