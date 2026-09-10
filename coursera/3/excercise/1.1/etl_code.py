import glob 
import pandas as pd 
import xml.etree.ElementTree as ET 
from datetime import datetime 

log_file = "log_file.txt" 
target_file = "final_data.csv" 

def extract_file_csv(file_name):
    df = pd.read_csv(file_name)
    return df

def extract_file_json(file_name):
    df = pd.read_json(file_name, lines = True)
    return df

def extract_file_xml(file_name):
    tree = ET.parse(file_name) #etree.parse
    root = tree.getroot() #tree.getroot
    columns = ['name','height','weight']
    df = pd.DataFrame(columns = columns)
    for node in root:
        name = node.find('name').text
        height = float(node.find('height').text)
        weight = float(node.find('weight').text)

        df = pd.concat([df,pd.DataFrame([[name,height,weight]],columns = columns)],ignore_index = True)

    return df

def extract():
    extracted_data = pd.DataFrame(columns = ['name','height','weight'])
    for csvfile in glob.glob('*.csv'):
        if csvfile != target_file:
            extracted_data = pd.concat([extracted_data,extract_file_csv(csvfile)],ignore_index = True)
        
    for jsonfile in glob.glob('*.json'):
        extracted_data = pd.concat([extracted_data,extract_file_json(jsonfile)],ignore_index=True)

    for xmlfile in glob.glob('*.xml'):
        extracted_data = pd.concat([extracted_data,extract_file_xml(xmlfile)],ignore_index=True)

    return extracted_data

def transform(data):
    data['height'] = round(data.height * 0.0254, 2)
    data['weight'] = round(data.weight * 0.45359237, 2)

    return data

def load_data(target_file, transformed_data):
    transformed_data.to_csv(target_file, index = False)

def log_progress(message):
    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open(log_file,'a') as f:
        f.write(timestamp + ', ' + message + '\n')
    

if __name__ == '__main__':
    log_progress('ETL Job Started')

    log_progress("Extract phase Started")
    extracted_data = extract()
    log_progress("Extract phase Ended")

    log_progress("Transform phase Started")
    transformed_data = transform(extracted_data)
    log_progress("Transform phase Ended")

    log_progress("Load phase Started")
    load_data(target_file,transformed_data)
    log_progress("Load phase Ended")

    log_progress("ETL Job End\n")

    print("\n============ DONE ===========\n")