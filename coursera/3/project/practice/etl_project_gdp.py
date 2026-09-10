# Importing the required libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd 
import sqlite3
import numpy as np 
from datetime import datetime

table_attribs = ['Country','GDP_USD_millions']
db_name = 'World_Economies.db'
table_name = 'Countries_by_GDP'
csv_path = 'Countries_by_GDP.csv'
url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'

def extract(url, table_attribs):
    page = requests.get(url).text
    data = BeautifulSoup(page,'html.parser')
    tables = data.find_all('tbody')
    rows = tables[2].find_all('tr')
    df = pd.DataFrame(columns = table_attribs)

    for row in rows:
        col = row.find_all('td')
        if len(col) != 0:
            if col[0].find('a') is not None and '—' not in col[2]:
                dict_data = {'Country' : col[0].a.contents[0],
                'GDP_USD_millions' : col[2].contents[0]}

                df = pd.concat([df,pd.DataFrame(dict_data,index = [0])],ignore_index = True)
    return df

def transform(df):
    gdp_list = df['GDP_USD_millions'].tolist()
    gdp_list = [float("".join(x.split(','))) for x in gdp_list]
    gdp_list = [np.round(x/1000,2) for x in gdp_list]
    df['GDP_USD_millions'] = gdp_list
    df = df.rename(columns = {"GDP_USD_millions":"GDP_USD_billions"})
    return df

def load_to_csv(df, csv_path):
    df.to_csv(csv_path)

def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name,sql_connection,if_exists = 'replace', index = False)

def run_query(query_statement, sql_connection):
    print(query_statement)
    print(pd.read_sql(query_statement,sql_connection))

def log_progress(message):
    timestamp_format = '%Y-%h-%d-%H-%M-%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open('etl_project_log.txt','a') as f:
        f.write(timestamp + ', '+message+'\n')

if __name__ == '__main__':
    log_progress("Initiating ETL process.")

    log_progress("Initiating Extraction process.")
    extracted_data = extract(url,table_attribs)
    log_progress("Data extraction complete.")
    
    log_progress("Initiating Transformation process")
    transformed_data = transform(extracted_data)
    log_progress("Data transformation complete")

    load_to_csv(transformed_data,csv_path)
    log_progress("Data saved to CSV file.")
    
    log_progress("SQL Connection initiated.")
    conn = sqlite3.connect(db_name)
    load_to_db(transformed_data,conn, table_name)
    log_progress("Data loaded to Database as table.")

    log_progress("Running the query.")
    query_statement = f"SELECT * FROM {table_name} WHERE GDP_USD_billions >= 100"
    run_query(query_statement,conn)

    log_progress("Process Complete.")
    conn.close()


