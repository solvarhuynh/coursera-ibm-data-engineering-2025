import sqlite3
import pandas as pd 


tables_name = 'Departments'
conn = sqlite3.connect('STAFF.db')
attribute_name = ['DEPT_ID','DEP_NAME','MANAGER_ID','LOC_ID']

df = pd.read_csv('Departments.csv', names = attribute_name)
df.to_sql(tables_name,conn,if_exists = 'replace',index = False)

df = pd.concat([df,pd.DataFrame([[9,'Quality Assurance',30010,'L0010']], columns=attribute_name)], ignore_index=True)

df.to_sql(tables_name,conn,if_exists='append',index = False)

query_name1 = f'SELECT * FROM {tables_name}'
query_name2 = f'SELECT DEP_NAME FROM {tables_name}'
query_name3 = f'SELECT COUNT(*) FROM {tables_name}'

print(pd.read_sql(query_name1,conn), '\n')
print(pd.read_sql(query_name2,conn), '\n')
print(pd.read_sql(query_name3,conn), '\n')