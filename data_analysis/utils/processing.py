import re
from collections import Counter

import pandas as pd
from bertopic import BERTopic

from data_analysis.utils.load import load_file_content


def train_model(tokenize_path):
    tokenize_str = load_file_content(tokenize_path)
    tokenize = tokenize_str.split('\n')
    model = BERTopic(language="english", verbose=True)
    topics, probabilities = model.fit_transform(tokenize)
    return model, topics, probabilities


def create_bag_of_words(tokenize_path):
    tokenize_str = load_file_content(tokenize_path)
    tokenize = tokenize_str.split('\n')
    dictionary = dict(Counter(tokenize))

    # Remove elements with count less to 10
    dictionary = {key: value for key, value in dictionary.items() if value >= 10}

    dictionary = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))

    return dictionary


def generate_csv_metadata(csv_file_path):
    try:
        df = pd.read_csv(csv_file_path)

        if not {'country', 'university', 'content'}.issubset(df.columns):
            raise ValueError("El CSV no contiene las columnas requeridas: 'country', 'university', 'content'.")

        num_rows = len(df)
        num_unique_universities = df['university'].nunique()
        num_unique_countries = df['country'].nunique()

        records_per_university = df['university'].value_counts().to_dict()
        records_per_country = df['country'].value_counts().to_dict()

        universities_per_country = df.groupby('country')['university'].nunique().to_dict()

        metadata = {
            'num_records': num_rows,
            'num_universities': num_unique_universities,
            'num_countries': num_unique_countries,
        }

        space_regex = re.compile(r'\s')

        for university, count in records_per_university.items():
            metadata[f"num_records_{space_regex.sub('_', university.lower())}"] = count

        for country, count in records_per_country.items():
            metadata[f"num_records_{space_regex.sub('_', country.lower())}"] = count

        for country, count in universities_per_country.items():
            metadata[f"num_universities_{space_regex.sub('_', country.lower())}"] = count

        return metadata

    except Exception as e:
        print(f"Error al generar metadatos del CSV: {e}")
        return None
