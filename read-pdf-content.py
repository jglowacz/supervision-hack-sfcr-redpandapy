import numpy as np
import pathlib, fitz
import pandas as pd
import re

fname = "allianztuir.pdf"  # get document filename - czyli ścieżka gdzie jest plik

# Open the PDF file
doc = fitz.open(fname)

# Initialize variables for extracting the content of each section for "dane jakościowe" table

sections_content_data = {} # initialize dictionary to store the content of each section
current_section_name = None # initialize variable to store the name of the current section
save = False # initialize variable to store whether to save the current line

# Define the section names by assigning only prefixes of the section names
section_name_prefix = ['A.', 'B.', 'C.', 'D.', 'E.', 'Podsumowanie', 'Załączniki']

# Iterate over the pages of the PDF file
for page_num in range(doc.page_count): 
    page = doc[page_num] # get the page
    
    text = page.get_text() # get the text of the page

    for line in text.split('\n'):  # Split the text into lines
        line = line.strip() # Remove leading/trailing white spaces

        # Check if the line start with the section name prefix
        if any(line.startswith(prefix) for prefix in section_name_prefix):
            # If the line is a section name, start a new section
            current_section_name = line # Set the current section name
            sections_content_data[current_section_name] = '' # Initialize the content of the current section
            save = True 
        elif save and line:
            # If the line is not a section name and a section has started, add it to the current section
            sections_content_data[current_section_name] += line + '\n' # Add the line to the current section
        else:
            save = False

# Convert the section_dane_jakosc dictionary to a first DataFrame
df_from_sfcr = pd.DataFrame(list(sections_content_data.items()), columns=['section_name', 'contents'])

# Create second DataFrame with id_tab, sfcr_version, id_parent_section & section name
data_df_ids_and_section = [
    {'id_tab': 1, 'sfcr version': 1, 'id_parent_section' : None, 'section_name' : 'Podsumowanie'},
    {'id_tab': 2, 'sfcr version': 1, 'id_parent_section' : None, 'section_name' : 'A. Działalność i wyniki operacyjne'},
    {'id_tab': 3, 'sfcr version': 1, 'id_parent_section' : 2, 'section_name' : 'A.1 Działalność'},
    {'id_tab': 4, 'sfcr version': 1, 'id_parent_section' : 2, 'section_name' : 'A.2 Wynik z działalności ubezpieczeniowej'},
    {'id_tab': 5, 'sfcr version': 1, 'id_parent_section' : 2, 'section_name' : 'A.3 Wynik z działalności lokacyjnej (inwestycyjnej)'},
    {'id_tab': 6, 'sfcr version': 1, 'id_parent_section' : 2, 'section_name' : 'A.4 Wyniki z pozostałych rodzajów działalności'},
    {'id_tab': 7, 'sfcr version': 1, 'id_parent_section' : 2, 'section_name' : 'A.5 Wszelkie inne informacje'},
    {'id_tab': 8, 'sfcr version': 1, 'id_parent_section' : None, 'section_name' : 'B. System zarządzania'},
    {'id_tab': 9, 'sfcr version': 1, 'id_parent_section' : 8, 'section_name' : 'B.1 Informacje ogólne o systemie zarządzania'},
    {'id_tab': 10, 'sfcr version': 1, 'id_parent_section' : 8, 'section_name' : 'B.2 Wymogi dotyczące kompetencji i reputacji'},
    {'id_tab': 11, 'sfcr version': 1, 'id_parent_section' : 8, 'section_name' : 'B.3 System zarządzania ryzykiem, w tym własna ocena ryzyka i wypłacalności'},
    {'id_tab': 12, 'sfcr version': 1, 'id_parent_section' : 8, 'section_name' : 'B.4 System kontroli wewnętrznej'},
    {'id_tab': 13, 'sfcr version': 1, 'id_parent_section' : 8, 'section_name' : 'B.5 Funkcja audytu wewnętrznego'},
    {'id_tab': 14, 'sfcr version': 1, 'id_parent_section' : 8, 'section_name' : 'B.6 Funkcja aktuarialna'},
    {'id_tab': 15, 'sfcr version': 1, 'id_parent_section' : 8, 'section_name' : 'B.7 Outsourcing'},
    {'id_tab': 16, 'sfcr version': 1, 'id_parent_section' : 8, 'section_name' : 'B.8 Wszelkie inne informacje'},
    {'id_tab': 17, 'sfcr version': 1, 'id_parent_section' : None, 'section_name' : 'C. Profil ryzyka'},
    {'id_tab': 18, 'sfcr version': 1, 'id_parent_section' : 17, 'section_name' : 'C.1 Ryzyko aktuarialne'},
    {'id_tab': 19, 'sfcr version': 1, 'id_parent_section' : 17, 'section_name' : 'C.2 Ryzyko rynkowe'},
    {'id_tab': 20, 'sfcr version': 1, 'id_parent_section' : 17, 'section_name' : 'C.3 Ryzyko kredytowe'},
    {'id_tab': 21, 'sfcr version': 1, 'id_parent_section' : 17, 'section_name' : 'C.4 Ryzyko płynności'},
    {'id_tab': 22, 'sfcr version': 1, 'id_parent_section' : 17, 'section_name' : 'C.5 Ryzyko operacyjne'},
    {'id_tab': 23, 'sfcr version': 1, 'id_parent_section' : 17, 'section_name' : 'C.6 Pozostałe istotne ryzyka'},
    {'id_tab': 24, 'sfcr version': 1, 'id_parent_section' : 17, 'section_name' : 'C.7 Wszelkie inne informacje'},
    {'id_tab': 25, 'sfcr version': 1, 'id_parent_section' : None, 'section_name' : 'D. Wycena do celów wypłacalności'},
    {'id_tab': 26, 'sfcr version': 1, 'id_parent_section' : 25, 'section_name' : 'D.1 Aktywa'},
    {'id_tab': 27, 'sfcr version': 1, 'id_parent_section' : 25, 'section_name' : 'D.2 Rezerwy techniczno-ubezpieczeniowe'},
    {'id_tab': 28, 'sfcr version': 1, 'id_parent_section' : 25, 'section_name' : 'D.3 Inne zobowiązania'},
    {'id_tab': 29, 'sfcr version': 1, 'id_parent_section' : 25, 'section_name' : 'D.4 Alternatywne metody wyceny'},
    {'id_tab': 30, 'sfcr version': 1, 'id_parent_section' : 25, 'section_name' : 'D.5 Wszelkie inne informacje'},
    {'id_tab': 31, 'sfcr version': 1, 'id_parent_section' : None, 'section_name' : 'E. Zarządzanie kapitałem'},
    {'id_tab': 32, 'sfcr version': 1, 'id_parent_section' : 31, 'section_name' : 'E.1 Środki własne'},
    {'id_tab': 33, 'sfcr version': 1, 'id_parent_section' : 31, 'section_name' : 'E.2 Kapitałowy wymóg wypłacalności i minimalny wymóg kapitałowy'},
    {'id_tab': 34, 'sfcr version': 1, 'id_parent_section' : 31, 'section_name' : 'E.3 Zastosowanie podmodułu ryzyka cen akcji opartego na duracji do obliczenia kapitałowego wymogu wypłacalności'},
    {'id_tab': 35, 'sfcr version': 1, 'id_parent_section' : 31, 'section_name' : 'E.4 Różnice między formułą standardową a stosowanym modelem wewnętrznym'},
    {'id_tab': 36, 'sfcr version': 1, 'id_parent_section' : 31, 'section_name' : 'E.5 Niezgodność z minimalnym wymogiem kapitałowym i niezgodność z kapitałowym wymogiem wypłacalności'},
    {'id_tab': 37, 'sfcr version': 1, 'id_parent_section' : 31, 'section_name' : 'E.6 Wszelkie inne informacje'},
]

# Create second DataFrame from list of dictionaries
df_ids_and_section = pd.DataFrame(data_df_ids_and_section)

# Perform an outer join to keep all rows from both DataFrames
merged_two_dfs = pd.merge(df_ids_and_section, df_from_sfcr, on='section_name', how='outer')

# Fill in missing values in 'sfcr version' and 'id_parent_section'
merged_two_dfs['sfcr version'].fillna(1, inplace=True)
merged_two_dfs['id_parent_section'].fillna(np.nan, inplace=True)

# Generate new, unique 'id_tab' values for the rows where 'section_name' was not found in both DataFrames
max_id_tab = int(merged_two_dfs['id_tab'].max())
num_nan = int(merged_two_dfs['id_tab'].isna().sum())
merged_two_dfs.loc[merged_two_dfs['id_tab'].isna(), 'id_tab'] = range(max_id_tab + 1, max_id_tab + 1 + num_nan)

# Convert 'id_tab' to int
merged_two_dfs['id_tab'] = merged_two_dfs['id_tab'].astype(int)

# Save the merged DataFrame to a CSV file
merged_two_dfs.to_csv('merge.csv', index=False)

# # Write the DataFrame to a CSV file
# df_from_sfcr.to_csv('allianztuir_output.csv', index=False)
