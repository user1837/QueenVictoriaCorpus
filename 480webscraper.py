from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import os
import json

def extract_date(date_info):
    for item in date_info:
        if re.search(r"^18(2|3|4|5|6)\d$", item):
            return item

def clean_up_text(text):
    text = re.sub(r"(\r\n)", " ", text)
    text = re.sub(r"\d+\b", "", text)
    #text = re.sub(r"\[page.+\]", "", text)
    return text

def isNotLetter(header_text):
    header_text = header_text.lower()
    if 'memorandum' in header_text:
        return True
    if 'extract' in header_text:
        return True
    if 'cabinet' in header_text:
        return True
    if 'enclosed' in header_text:
        return True
    if 'minute' in header_text:
        return True
    if 'enclosure' in header_text:
        return True
    if 'decipher' in header_text:
        return True
    if 'ministry' in header_text:
        return True
    if 'abercromby' in header_text:
        return True
    if 'telegram' in header_text:
        return True
    return False

def get_correspondents(header):
    header = re.sub(r"\.", "", header)
    header = re.sub(r"\d+\b", "", header)
    correspondents = [i for i in re.split(r"\sto(\s|{)", header) if i != " "]
    if correspondents[0] == "Queen Victoria to":
        correspondents[0] = re.sub(r"\sto", "", correspondents[0])
        correspondents.append("Viscount Palmerston and Lord John Russell")
    return correspondents

def write_to_json(tags, i, volume_number):
    dictionaries = []
    while i < len(tags):
        if (volume_number == 1) and (i == 0):
            dictionary = dict()
            dictionary['language'] = 'en'
            dictionary['writer'] = 'Queen Adelaide'
            dictionary['addressee'] = 'the Princess Victoria'
            dictionary['year'] = '1821'
            text = tags[i].get_text()
            i = i + 1
            while True:
                if tags[i].name == 'h5':
                    break
                text = text + " " + tags[i].get_text()
                i = i + 1
            text = clean_up_text(text)
            dictionary['text'] = text
            dictionaries.append(dictionary)
        elif (volume_number == 1) and (i == 7):
            dictionary = dict()
            dictionary['language'] = 'en'
            dictionary['writer'] = 'Prince Leopold'
            dictionary['addressee'] = 'the Princess Victoria'
            date_info = [j for j in re.split(r"[^a-zA-Z0-9']", tags[i].get_text()) if len(j) > 0]
            dictionary['year'] = extract_date(date_info)
            i = i + 1
            text = ""
            while True:
                if tags[i].name == 'h5':
                    break
                text = text + tags[i].get_text() + " "
                i = i + 1
            text = clean_up_text(text)
            dictionary['text'] = text
            dictionaries.append(dictionary)
        else:
            header = tags[i].get_text()
            if isNotLetter(header):
                i = i + 1
                while True:
                    if (i >= len(tags)):
                        break
                    if tags[i].name == 'h5':
                        break
                    i = i + 1
            else:
                dictionary = dict()
                dictionary['language'] = 'en'
                correspondents = get_correspondents(header)
                #print(correspondents)
                dictionary['writer'] = correspondents[0]
                dictionary['addressee'] = correspondents[1]
                # dictionary['writer'] = ''
                # dictionary['addressee'] = ''
                i = i + 1
                date_info = [k for k in re.split(r"[^a-zA-Z0-9']", tags[i].get_text()) if len(k) > 0]
                dictionary['year'] = extract_date(date_info)
                i = i + 1
                text = ""
                while True:
                    if (i >= len(tags)):
                        break
                    if tags[i].name == 'h5':
                        break
                    text = text + tags[i].get_text() + " "
                    i = i + 1
                text = clean_up_text(text)
                dictionary['text'] = text
                dictionaries.append(dictionary)
    return dictionaries


def scrape_page(url, volume_number):
    """
    Takes as input a url and a filename, scrapes specified elements from the url's web page, and writes the text of
    those elements to a text file
    """
    page = urlopen(url)  # Creates a connection to the web page
    page = page.read()  # Reads in the html document of that web page
    soup = BeautifulSoup(page, 'lxml')  # Creates a BeautifulSoup object
    taglist = soup.find_all(['p', 'h5'])  # This statement finds all <p> and <h5> tags
    tags = []
    # This loop searches the taglist, finds <p> tags in the class "ind" or "ind1" and <h5> tags with the style
    # "margin-top: 3em;" or "margin-top: 3.0em;" and appends them to the paragraphs list
    for tag in taglist:
        if re.search(r"p\sclass=\"ind(1|(right))?\"", str(tag)) or re.search(r"h5\sstyle=\"margin-top: 3("
                                                                                 r"\.0)?em;\"", str(tag)):
            tags.append(tag)

    return write_to_json(tags, 0, volume_number)

    # This block of code writes the text of the tags in the paragraphs list to a text file
    # with open(filename, 'w') as fout:
    #     for tag in tags:
    #         fout.write(paragraph.get_text() + "\n")
    #         fout.write(str(tag))
    #         fout.write("ENDOFTAG\n")

letters = []
url1 = "https://www.gutenberg.org/files/20023/20023-h/20023-h.htm"
print("Working on volume 1")
letters.extend(scrape_page(url1, 1))
url2 = "https://www.gutenberg.org/files/24780/24780-h/24780-h.htm"
print("Working on volume 2")
letters.extend(scrape_page(url2, 2))
url3 = "https://www.gutenberg.org/files/28649/28649-h/28649-h.htm"
print("Working on volume 3")
letters.extend(scrape_page(url3, 3))
#print(letters)
print("Writing to file")
with open('letters.json', 'w', encoding='utf8') as fout:
    str = json.dumps(letters, indent=4, separators=(',', ': '), ensure_ascii=False)
    fout.write(str)

# Create an array of dictionaries and initialize the iterator outside the while loop, create a new dictionary each
# iteration of the while loop
# First letter: no date or header, three paragraphs, start i at 0 and increment to 2, set date to 1821,
# writer is Queen Adelaide, addressee is the Princess Victoria
# Third letter: date but no header, date is tag 7, letter is tag 8, postscript is tag 9, writer is the Princess
# Victoria, addressee is Prince Leopold
# Skip memorandum, extract from the Queen's journal, the cabinet of, draft enclosed, Cabinet Minute, Extract from
# the Will, Minute by the governor-general of India, Minute of interview by the Prince Albert, enclosure in previous
# letter, Enclosure-copy, Extract of a letter, Decipher from Lord Cowley (probably skip), the Ministry as formed by,
# Enclosure:
# skip 2 tags (
# increment i twice), if it's memorandum continue until the next h5 tag (use tag.name to get name of the tag)
# From Sir Ralph Abercromby: think it's to the Queen, probably just skip it
# Normal entry:
# while i < len(tags)
#   create a new dictionary
#   insert a key value pair for language (set value to 'en')
#   get next h5 tag (should be tag at index of current value of i)
#   split the h5 tag on " to " and save into array (should have name of writer at index 0 and name of addressee at
#   index 1), insert key-value pair for writer and key-value pair for addressee
#   increment i
#   get the next tag (should be a p tag), split text into words, and extract year using regular expression
#   increment i, create string to hold main text
#   get the next tag (should be a p tag), should have main text of the letter, concatenate it to string
#   increment i
#   check to see if next tag is a p tag, if it is concatenate it to string, increment i, and repeat. If not,
#   don't increment i and continue to next iteration of while loop
#   at the end of iteration add the dictionary to the array
