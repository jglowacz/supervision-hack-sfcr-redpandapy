from dotenv import load_dotenv
load_dotenv() # Loading .env file 

import os
from supabase import create_client # Importing supabase client

# Getting environment variables
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client(url, key) # Creating supabase client

# Names of tables in supabase
table_name_dane_jakosc = "Dane jakosciowe template" 
table_name_tabele_obligat = "Tabele obligatoryjne template" 
table_name_weyfik_komplet = "Weryfikacja kompletnosci SFCR template"

# get_data_dane_jakosc = supabase.table(table_name_dane_jakosc).select("*").execute() # Getting data from table "Dane jakosciowe template"
# print(get_data_dane_jakosc) # Printing data from table "Dane jakosciowe template"

# get_data_tabele_obligat = supabase.table(table_name_tabele_obligat).select("*").execute() # Getting data from table "Tabele obligatoryjne template"
# print(get_data_tabele_obligat) # Printing data from table "Tabele obligatoryjne template"

# get_data_weyfik_komplet = supabase.table(table_name_weyfik_komplet).select("*").execute() # Getting data from table "Weryfikacja kompletnosci SFCR template"
# print(get_data_weyfik_komplet) # Printing data from table "Weryfikacja kompletnosci SFCR template"

# insert_data_dane_jakosc = supabase.table(table_name_dane_jakosc).insert({"ID_TAB":"2"}).execute()

