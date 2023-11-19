# Step 1 - Get the list of URLs
# Step 2 - Loop through the list of URLs
# Step 3 - Get the HTML for each URL
# Step 4 - Parse the HTML to get the links to the PDFs
# Step 5 - Download the PDFs
# Step 6 - Save the PDFs to disk
# Step 7 - Repeat for each URL

# TODO: Implement async version of the script
# import aiohttp
# import asyncio
import json
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from unidecode import unidecode

SFCR_SITES_PATH = "sfcr_sites.json"

# Load the data from the JSON file
with open(SFCR_SITES_PATH, "r") as f:
    sfcr_sites = json.load(f)

# Extract the 'url_final_page' from each object in the JSON array
merged_data = [site["url_final_page"] for site in sfcr_sites]

opinions_keywords = [
    "biegł",
    "rewident",
    "opini",
    "badani",
    "raport",
    "niezalezn",
    "audytor"
]

sfcr_keywords = [
    "sprawozdanie o"
    "wypłacalności",
    "kondycji finansowej",
    "Solvency and financial condition report",
    "SFCR"
]

# 2 years as a testing period, can be changed to any value
years_keywords = ["2021", "2022"]

opinions_keywords_uni = [unidecode(x.lower()) for x in opinions_keywords]
sfcr_keywords_uni = [unidecode(x.lower()) for x in sfcr_keywords]

searched = [opinions_keywords, opinions_keywords_uni, sfcr_keywords, sfcr_keywords_uni]


def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")


def get_pdf_links(soup, base_url, searched, years_keywords):
    links = []
    for a in soup.find_all('a', href=True):
        if a['href'].endswith('.pdf'):
            for keywords in searched:
                for keyword in keywords:
                    if keyword in a.text.lower():
                        for year in years_keywords:
                            if year in a.text.lower():
                                link = urljoin(base_url, a['href'])
                                links.append((link, a.text))
    return links


def download_pdfs(links, directory):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    for link, name in links:
        response = requests.get(link, headers=headers, stream=True)
        filename = get_pdf_filename(name, link, directory)
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

def get_year(name):
    # Extract year from name based on year keywords
    for year_keyword in years_keywords:
        if year_keyword in name:
            return year_keyword
    return "YEAR"

def get_tu_code(link):
    # Retrieve TU code from sfcr_sites.json based on the link
    for site in sfcr_sites:
        if site["url_main_page"] in link:
            tu_code = site["tu_code"]
            return tu_code
    return "TU_CODE"
   

def get_name(link):
    # Retrieve name from sfcr_sites.json based on the link
    for site in sfcr_sites:
        if site["url_main_page"] in link:
            name = site["name"]
            return name
    return "NAME"


def get_pdf_filename(name, link, directory):
    filename = link.split("/")[-1]
    if any(word in name.lower() for word in opinions_keywords + opinions_keywords_uni):
        tu_code = get_tu_code(link)
        year = get_year(name)
        tu_name = get_name(link)
        filename = f"[{year}]OPINIA[{tu_code}]_[{tu_name}].pdf"
    elif any(word in name.lower() for word in sfcr_keywords + sfcr_keywords_uni):
        tu_code = get_tu_code(link)
        year = get_year(name)
        tu_name = get_name(link)
        filename = f"[{year}]SFCR[{tu_code}]_[{tu_name}].pdf"
    else:
        filename = f"[{year}]UNDEFINED[{tu_code}]_[{tu_name}].pdf"
    return os.path.join(directory, filename)


# Make sure the directory for the PDFs exists
os.makedirs("pdfs", exist_ok=True)

# Loop through the list of URLs
for url in merged_data:
    try:
        soup = get_soup(url)
        links = get_pdf_links(soup, url, searched, years_keywords)
        download_pdfs(links, "pdfs")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred with URL {url}: {e}")
