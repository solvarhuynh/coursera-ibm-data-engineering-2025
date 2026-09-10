import requests
import sqlite3
import pandas as pd 
from bs4 import BeautifulSoup

url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

db_name = 'Movies.db'
table_name = 'Top_50'
csv_path = '/home/project/top_50_files.csv'
df = pd.DataFrame(columns = ["Average Rank","Film","Year"])
count = 0

html_page = requests.get(url, headers=headers, timeout=30).text
data = BeautifulSoup(html_page,'html.parser')

tables = data.find_all('tbody') #la 1 list, moi phan tu la 1 tbody
rows = tables[0].find_all('tr') #ta truy xuat bang dau tien tren trang nen tables[0]

for row in rows:
    if count < 50:
        col = row.find_all('td')
        if len(col) != 0:
            data_dict = {"Average Rank": col[0].contents[0], "Film": col[1].contents[0], "Year": col[2].contents[0]}
            df = pd.concat([df,pd.DataFrame(data_dict,index=[0])], ignore_index = True)
            count += 1
    else: break

df.to_csv(csv_path,index=False)

conn = sqlite3.connect(db_name)
df.to_sql(table_name, conn, if_exists='replace', index=False)
conn.close()
