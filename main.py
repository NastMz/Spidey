from data_analysis.data import load_data

data = load_data('universities_crawler/crawled_files')

print(f"Número de registros: {data.shape[0]}")
