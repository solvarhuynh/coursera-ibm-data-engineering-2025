import requests
import pandas as  pd 
from bs4 import BeautifulSoup
import sqlite3 

url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
db_name = 'movies.db'
tables_name = 'TOP 25 - Released in the 2000s'
csv_path = '/home/project/top25movies.csv'
df = pd.DataFrame(columns = ['Film','Year',"Rotten Tomatoes' Top 100"])
count = 0

html_page = requests.get(url).text
data = BeautifulSoup(html_page,'html.parser')
tables = data.find_all('tbody')
rows = tables[0].find_all('tr')

for row in rows:
    if count < 25:
        col = row.find_all('td')
        if len(col) != 0: #vi hang dau la th (ten cot)
            if int(col[2].text) >= 2000:
                data_dict = {'Film' : str(col[1].contents[0]),
                'Year' : int(col[2].contents[0]),
                "Rotten Tomatoes' Top 100" : str(col[3].contents[0])}

                df = pd.concat([df, pd.DataFrame(data_dict,index = [0])], ignore_index = True)
                count += 1
    else: break

print(df)

df.to_csv(csv_path)
conn = sqlite3.connect(db_name)
df.to_sql(tables_name,conn,if_exists = 'replace', index = False)
conn.close()
