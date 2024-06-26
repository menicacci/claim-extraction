import json
import os
from scripts import utils
from scripts.constants import Constants


def load_tables_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data


def reset_processed_tables(json_file_path: str):
    data = load_tables_from_json(json_file_path)
    num_tables = 0

    for table_id, table_list in data.items():
        for table_data in table_list:
            table_data[Constants.PROCESSED_ATTR] = False
            num_tables += 1

    utils.write_json(data, json_file_path)

    return num_tables


def check_processed_tables(json_file_path: str, tables_directory_path: str):
    utils.check_path(tables_directory_path)

    tables_to_process = reset_processed_tables(json_file_path)
    data = load_tables_from_json(json_file_path)

    for file_name in os.listdir(tables_directory_path):
        if file_name.endswith('.txt'):
            parts = file_name.split('_')
            if len(parts) == 2:
                article_id = parts[0]
                table_index = int(parts[1].split('.')[0])
            else:
                continue

            if article_id in data:
                article = data[article_id]
                if 0 <= table_index < len(article):
                    article[table_index][Constants.PROCESSED_ATTR] = True
                    tables_to_process -= 1
                    
    utils.write_json(data, json_file_path)
    return tables_to_process
