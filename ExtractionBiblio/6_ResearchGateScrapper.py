from parsel import Selector
from playwright.sync_api import sync_playwright
import json
import re

def extract_url(text):
    """
    Extracts the first result between 'href="publication/' and '>'.

    Args:
        text (str): The input text containing the HTML.

    Returns:
        str: The extracted result if found, otherwise None.
    """
    match = re.search(r'href="publication/([^"]+)"', text)
    if match:
        return match.group(1)
    return None

def scrape_researchgate_publications(query: str):
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True, slow_mo=50)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36")
        page_num = 1

        while True:
            page.goto(f"https://www.researchgate.net/search/publication?q={query}&page={page_num}")
            selector = Selector(text=page.content())
            
            for publication in selector.css(".nova-legacy-c-card__body--spacing-inherit"):
                title = publication.css(".nova-legacy-v-publication-item__title .nova-legacy-e-link--theme-bare::text").get().title()
                title_link = f'https://www.researchgate.net{publication.css(".nova-legacy-v-publication-item__title .nova-legacy-e-link--theme-bare::attr(href)").get()}'
                publication_type = publication.css(".nova-legacy-v-publication-item__badge::text").get()
                publication_date = publication.css(".nova-legacy-v-publication-item__meta-data-item:nth-child(1) span::text").get()
                publication_doi = publication.css(".nova-legacy-v-publication-item__meta-data-item:nth-child(2) span").xpath("normalize-space()").get()
                publication_isbn = publication.css(".nova-legacy-v-publication-item__meta-data-item:nth-child(3) span").xpath("normalize-space()").get()
                source_link = f'https://www.researchgate.net{publication.css(".nova-legacy-v-publication-item__preview-source .nova-legacy-e-link--theme-bare::attr(href)").get()}'

                publications.append({
                    "title": title,
                    "link": title_link,
                    "source_link": source_link,
                    "publication_type": publication_type,
                    "publication_date": publication_date,
                    "publication_doi": publication_doi,
                    "publication_isbn": publication_isbn,
                })
            print(f"page number: {page_num}")

            # checks if next page arrow key is greyed out `attr(rel)` (inactive) and breaks out of the loop
            if selector.css(".nova-legacy-c-button-group__item:nth-child(9) a::attr(rel)").get():
                break
            else:
                page_num += 1
                break


        target_url='https://www.researchgate.net/publication/'+extract_url(str(page.content()))

        browser.close()
        return(target_url)
    
publications = []
target_url=scrape_researchgate_publications(query="Soil chemistry turned upside down: a meta-analysis of invasive earthworm effects on soil chemical properties")
print(json.dumps(publications, indent=2, ensure_ascii=False))
print()
print(target_url)