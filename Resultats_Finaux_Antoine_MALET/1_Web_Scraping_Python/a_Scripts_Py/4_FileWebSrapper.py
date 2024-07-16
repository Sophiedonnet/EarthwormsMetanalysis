import pandas as pd
import numpy as np
import itertools as itt
from habanero import Crossref
from unidecode import unidecode


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
pubdate_year_list = []
pubdate_month_list = []
doi_list = []
doi_url_list=[]
first_author_list=[]
last_author_list=[]
first_author_country=[]
last_author_country=[]

titles_file = input("Input the name of your tile file here (default:fichier_titres.txt): ") or "fichier_titres.txt"

myQuery=open(titles_file)
lines=0
cr = Crossref()

# Iterate over titles from the file
for query_title in myQuery:
    print(query_title)
    lines+=1
    title_list.append(query_title[:-1]) # The [:-1] is there to remove newline caracter from the end of the title.

    # Handling servor errors. / Building a Pandas DataFrame with the required data. / Convert it to CSV file.
    try:
        metadata = cr.works(query=query_title, limit=1)
    except:
        print("Server error. . .")
        continue
    try:
        pubdate_year_list.append(metadata['message']['items'][0]['issued']['date-parts'][0][0])
    except (KeyError, IndexError):
        pubdate_year_list.append('No data')

    try:
        pubdate_month_list.append(digit_to_month[metadata['message']['items'][0]['issued']['date-parts'][0][1:][1]])
    except (KeyError, IndexError):
        pubdate_month_list.append('No data')

    try:
        doi_list.append(metadata['message']['items'][0]['DOI'])
    except (KeyError, IndexError):
        doi_list.append('No data')

    try:
        doi_url_list.append(metadata['message']['items'][0]['URL'])
    except (KeyError, IndexError):
        doi_url_list.append('No data')

    try:
        journal_list.append(metadata['message']['items'][0]['publisher'])
    except (KeyError, IndexError):
        journal_list.append('No data')

    try:
        language_list.append(metadata['message']['items'][0]['language'])
    except (KeyError, IndexError):
        language_list.append('No data')

    try:
        first_author_given = metadata['message']['items'][0]['author'][0]['given']
        first_author_family = metadata['message']['items'][0]['author'][0]['family']
        first_author_list.append(f"{first_author_given} {first_author_family}")
    except (KeyError, IndexError):
        first_author_list.append('No data')

    try:
        first_author_affiliation = metadata['message']['items'][0]['author'][0]['affiliation'][0]['name']
        first_author_country.append(first_author_affiliation.split(' ')[-1])
    except (KeyError, IndexError):
        first_author_country.append('No data')

    try:
        last_author_given = metadata['message']['items'][0]['author'][-1]['given']
        last_author_family = metadata['message']['items'][0]['author'][-1]['family']
        last_author_list.append(f"{last_author_given} {last_author_family}")
    except (KeyError, IndexError):
        last_author_list.append('No data')

    try:
        last_author_affiliation = metadata['message']['items'][0]['author'][-1]['affiliation'][-1]['name']
        last_author_country.append(last_author_affiliation.split(' ')[-1])
    except (KeyError, IndexError):
        last_author_country.append('No data')

    try:
        abstract_list.append(metadata['message']['items'][0]['abstract'])
    except (KeyError, IndexError):
        abstract_list.append('No data')

zipped_lists = itt.zip_longest(title_list,first_author_list,last_author_list, abstract_list, journal_list, language_list, pubdate_year_list, pubdate_month_list,first_author_country,last_author_country,doi_list,doi_url_list,fillvalue='No data')
df=pd.DataFrame(zipped_lists, columns=['Title', 'First author','Last author','Abstract', 'Journal', 'Language', 'Year', 'Month','First Author Country','Last Author Country','DOI','DOI URL'])

# Title is first, url is last, allowing a clickabe url to appear in the Terminal.
df.index = np.arange(1, len(df)+1)

print(df)
lines=str(lines)

# FileName set to 'articles'by default, so that the newly named CSV file goes to the right directory.
fileName='articles/'
fileName+=input('Enter desired name for output file (default: dataMyWS_on_file_FILE_(nbLines)): ') or 'dataMyWS_on_file_'+titles_file+'_('+lines+'line(s))'
fileName+='.csv'
df.to_csv(fileName)


