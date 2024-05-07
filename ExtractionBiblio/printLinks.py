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
    print(str(lines)+'. '+target_url)
    print()