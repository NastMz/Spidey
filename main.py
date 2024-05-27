import pandas as pd

from data_analysis.data import load_json_data, load_pdf_data

university_pdf_dict = {
    'nacional': {'name': 'Universidad Nacional de Colombia', 'country': 'Colombia'},
    # Add more universities as needed
}

json_data = load_json_data('universities_crawler/crawled_files')
pdf_data = load_pdf_data('universities_crawler/crawled_files/pdf', university_pdf_dict)

df = pd.concat([json_data, pdf_data], ignore_index=True)

print(f"Número de registros: {df.shape[0]}")
print(f"Universidades: \n{df['university'].unique()}")
