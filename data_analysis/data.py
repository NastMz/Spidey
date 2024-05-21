import pandas as pd
import os

def load_data(folder_path):
    files = os.listdir(folder_path)
    df = pd.DataFrame()

    for file in files:
        if file.endswith('.json'):
            file_path = os.path.join(folder_path, file)
            data = pd.read_json(file_path)
            df = pd.concat([df, data], ignore_index=True)

    return df