import pandas as pd
import numpy as np
import itertools as itt
from habanero import Crossref
from unidecode import unidecode
from ResearchGateScrapper2 import extract_url,scrape_researchgate_publications

def get_key(liste, val):
    found = False
    for key, value in MA_dict.items():
        if str(val) == str(value):
            liste.append(key)
            found = True
    if not found:
        liste.append('-')


digit_to_month = {
    1: 'Jan',
    2: 'Feb',
    3: 'Mar',
    4: 'Apr',
    5: 'May',
    6: 'Jun',
    7: 'Jul',
    8: 'Aug',
    9: 'Sep',
    10: 'Oct',
    11: 'Nov',
    12: 'Dec'
}

# Initializing the lists we want to fill with API data.
title_list= []
abstract_list=[]
journal_list = []
language_list =[]
pubdate = []
doi_list = []
doi_url_list=[]
first_author_list=[]
last_author_list=[]
first_author_country=[]
last_author_country=[]
MA_list=[]

titles_file = input("Input the name of your tile file here (default:fichier_titres.txt): ") or "fichier_titres.txt"

MA_limit = int(input("How many metaanalyses is there ?: "))
MA_dict = {}
for var in range(MA_limit):
    key = 'MA' + str(var+1)
    MA_dict[key] = input(f"What is the first article of {key} (line number)?: ")

print(MA_dict.items())
print(MA_dict.values())
myQuery=open(titles_file)
lines=1

cr = Crossref()
filler='N/A'

# Iterate over titles from the file
for query_title in myQuery:
    print(query_title)
    get_key(MA_list,lines)
    lines+=1
    title_list.append(query_title[:-1]) # The [:-1] is there to remove newline caracter from the end of the title.
    publications,target_url=scrape_researchgate_publications(query=query_title)
    doi_list.append(publications[0] or filler)
    pubdate.append(publications[1] or filler)
    doi_url_list.append(target_url)

    # Handling servor errors.
    try:
        metadata = cr.works(query=query_title, limit=1)
    except:
        print("Server error. . .")
        continue

    try:
        first_author_given = metadata['message']['items'][0]['author'][0]['given']
        first_author_family = metadata['message']['items'][0]['author'][0]['family']
        first_author_list.append(f"{first_author_given} {first_author_family}")
    except (KeyError, IndexError):
        first_author_list.append(filler)

    try:
        first_author_affiliation = metadata['message']['items'][0]['author'][0]['affiliation'][0]['name']
        first_author_country.append(first_author_affiliation.split(' ')[-1])
    except (KeyError, IndexError):
        first_author_country.append(filler)

    try:
        last_author_given = metadata['message']['items'][0]['author'][-1]['given']
        last_author_family = metadata['message']['items'][0]['author'][-1]['family']
        last_author_list.append(f"{last_author_given} {last_author_family}")
    except (KeyError, IndexError):
        last_author_list.append(filler)

zipped_lists = itt.zip_longest(MA_list,title_list,first_author_list,last_author_list, abstract_list,pubdate,doi_list,doi_url_list,fillvalue=filler)
df=pd.DataFrame(zipped_lists, columns=['MA','Title', 'First author','Last author','Abstract',"OnResearchgate","DOI","rg_URL"])

# Title is first, url is last, allowing a clickabe url to appear in the Terminal.
df.index = np.arange(1, len(df)+1)

print(df)
lines=str(lines)

# FileName set to 'articles'by default, so that the newly named CSV file goes to the right directory.
fileName='articles/'
fileName+='may06_MA_dataMyWS_on_file_'+titles_file+'_('+lines+'line(s))'
fileName+='.csv'
df.to_csv(fileName)

# 1 41 62 75 = first title of each MA annexes.
# The code looks good...
