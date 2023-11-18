# import requests
# from bs4 import BeautifulSoup
# import os

#  Load the data from the JSON file
# with open('sfcr_sites.json', 'r') as f:
#     merged_data = json.load(f)

merged_data = [
    # "https://www.allianz.pl/pl_PL/dla-ciebie/o-allianz/tu-allianz-zycie.html#sfcr",
    "https://www.allianz.pl/pl_PL/dla-ciebie/o-allianz/tuir.html#sfcr",
    # "https://cardif.pl/onas/informacje-finansowe-i-podatkowe",
    # "https://ca-ubezpieczenia.pl/ca-towarzystwo-ubezpieczen",
    # "https://www.compensa.pl/o-nas/#raporty",
    # "https://www.ergohestia.pl/o-ergo-hestii/wyniki-finansowe-i-raporty/",
    # "https://www.generali.pl/dla-ciebie/informacje-korporacyjne",
    # "https://interpolska.pl/grupa-inter/sprawozdania/",
    # "https://www.nn.pl/notowania-i-wyniki-finansowe/raporty-finansowe",
    # "https://www.openlife.pl/o-nas/raporty-publiczne/",
    # "https://pkoubezpieczenia.pl/pko-zycie-towarzystwo-ubezpieczen",
    # "https://www.pocztowenazycie.pl/strefa-klienta-dokumenty",
    # "https://polskigaztuw.pl/a_pgtuw_sfcr/",
    # "https://www.pzu.pl/relacje-inwestorskie/raporty",
    # "https://rejentlife.com.pl/ujawnienia-publiczne/",
    # "https://saltus.pl/o-nas/saltus_tu_zycie_sa/",
    # "https://www.santander.allianz.pl/raporty-roczne/",
    # "https://www.signal-iduna.pl/o-nas/sprawozdania-finansowe/",
    # "https://tueuropa.pl/raporty-roczne",
    # "https://www.uniqa.pl/centrum-informacyjne/wyniki-finansowe/"
]

# # Loop through the list of URLs
# for data in merged_data:
#     url = data
#     try:
#         response = requests.get(url)
#         soup = BeautifulSoup(response.text, 'html.parser')

#         # Find all links to PDF files
#         pdf_links = [(a['href'], a.text) for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]

#         # Write the links to a file
#         with open("scrapepdfs.txt", "a") as f:
#             for link, text in pdf_links:
#                 if "https" not in link:
#                     link = url + link
#                 f.write(f"{link}\t{text}\n")
#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred with URL {url}: {e}")

        
    # Download and save each PDF
    # for pdf_url in pdf_links:
    #     if 'http' not in pdf_url:
    #         pdf_url = url + pdf_url
    #     pdf_response = requests.get(pdf_url)
    #     with open(os.path.join("pdfs", pdf_url.split("/")[-1]), 'wb') as f:
    #         f.write(pdf_response.content)
    
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

def get_pdf_links(soup, base_url):
    links = [(a['href'], a.text) for a in soup.find_all('a', href=True) 
             if a['href'].endswith('.pdf') and 
             ('sfcr' in a.text.lower() or 'sprawozdanie' in a.text.lower() or 'wyp' in a.text.lower())]
    absolute_links = [(urljoin(base_url, link), text) for link, text in links]
    return absolute_links

def write_links_to_file(links, filename):
    with open(filename, "a") as f:
        for link, text in links:
            f.write(f"{link}\t{text}\n")

def download_pdfs(links, directory):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    for link, _ in links:
        response = requests.get(link, headers=headers, stream=True)
        filename = os.path.join(directory, link.split("/")[-1])
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

# Make sure the directory for the PDFs exists
os.makedirs("pdfs", exist_ok=True)

# Loop through the list of URLs
for url in merged_data:
    try:
        soup = get_soup(url)
        links = get_pdf_links(soup, url)
        write_links_to_file(links, "scrapepdfs.txt")
        download_pdfs(links, "pdfs")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred with URL {url}: {e}")

