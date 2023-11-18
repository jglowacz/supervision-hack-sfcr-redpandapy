import requests
from bs4 import BeautifulSoup
import os
import json 

#  Load the data from the JSON file
with open('scfr_sites.json', 'r') as f:
    merged_data = json.load(f)

# Loop through the list of URLs
for data in merged_data:
    url = data["url"]
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links to PDF files
        pdf_links = [a['href'] for a in soup.find_all('a', href=True)]

        # Write the links to a file
        with open("scraperesult.txt", "a") as f:
            for link in pdf_links:
                f.write(url + link + '\n')
    except requests.exceptions.RequestException as e:
        print(f"An error occurred with URL {url}: {e}")


    # Download and save each PDF
    # for pdf_url in pdf_links:
    #     if 'http' not in pdf_url:
    #         pdf_url = url + pdf_url
    #     pdf_response = requests.get(pdf_url)
    #     with open(os.path.join("pdfs", pdf_url.split("/")[-1]), 'wb') as f:
    #         f.write(pdf_response.content)