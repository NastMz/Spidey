import pandas as pd
import os
import pdfplumber


def load_json_data(folder_path):
    files = os.listdir(folder_path)
    df = pd.DataFrame()

    for file in files:
        if file.endswith('.json'):
            file_path = os.path.join(folder_path, file)
            print(f"Loading data from file {file_path}")
            data = pd.read_json(file_path)
            df = pd.concat([df, data], ignore_index=True)

    return df


def load_pdf_data(folder_path, university_dict):
    data_list = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.pdf'):
                file_path = os.path.join(root, file)
                try:
                    print(f"Loading data from file {file_path}")
                    with pdfplumber.open(file_path) as pdf:
                        content = ""
                        for page in pdf.pages:
                            content += page.extract_text() or ""
                    # Extract the university short name from the folder path
                    university_short_name = os.path.basename(root)
                    # Get the full university name and country from the dictionary
                    university_info = university_dict.get(university_short_name,
                                                          {'name': university_short_name, 'country': ''})
                    # Collect the data
                    data_list.append({
                        'university': university_info['name'],
                        'title': '',  # Title extraction is not handled in this snippet
                        'content': content,
                        'country': university_info['country']
                    })
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

    # Convert the list of dictionaries to a DataFrame
    data = pd.DataFrame(data_list, columns=['university', 'title', 'content', 'country'])

    return data


def load_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
        return content
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None