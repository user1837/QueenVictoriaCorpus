from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import os

def get_headers(url, filename):
    page = urlopen(url)  # Creates a connection to the web page
    page = page.read()  # Reads in the html document of that web page
    soup = BeautifulSoup(page, 'lxml')  # Creates a BeautifulSoup object
    taglist = soup.find_all('h5')  # This statement finds all <h5> tags
    tags = []
    for tag in taglist:
        if re.search(r"h5\sstyle=\"margin-top: 3("r"\.0)?em;\"", str(tag)):
            tags.append(tag)
    with open(filename, 'w') as fout:
        for tag in tags:
            fout.write(str(tag))
            fout.write("ENDOFTAG\n")

url1 = "https://www.gutenberg.org/files/20023/20023-h/20023-h.htm"
print("Working on volume 1")
get_headers(url1, "headers1.txt")
url2 = "https://www.gutenberg.org/files/24780/24780-h/24780-h.htm"
print("Working on volume 2")
get_headers(url2, "headers2.txt")
url3 = "https://www.gutenberg.org/files/28649/28649-h/28649-h.htm"
print("Working on volume 3")
get_headers(url3, "headers3.txt")