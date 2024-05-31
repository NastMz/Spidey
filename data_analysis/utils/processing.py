import re
from collections import Counter

import numpy as np
import pandas as pd
from umap import UMAP
from bertopic import BERTopic
from sklearn.preprocessing import MinMaxScaler


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


def create_topic_visualization(model_path):
    # Cargar el modelo BERTopic entrenado
    topic_model = BERTopic.load("trained_model.bertopic")

    # Obtener información de los tópicos
    topic_info = topic_model.get_topic_info()
    topic_list = sorted(topic_info.Topic.to_list())
    frequencies = [topic_model.topic_sizes_[topic] for topic in topic_list if topic != -1]
    words = [" | ".join([word[0] for word in topic_model.get_topic(topic)[:5]]) for topic in topic_list if topic != -1]

    # Obtener embeddings de los tópicos y reducir la dimensionalidad con UMAP
    embeddings = topic_model.topic_embeddings_
    umap_model = UMAP(n_neighbors=15, n_components=2, metric='cosine')
    umap_embeddings = umap_model.fit_transform(embeddings)

    # Filtrar tópicos y embeddings para excluir el tópico -1
    filtered_topic_list = [topic for topic in topic_list if topic != -1]
    filtered_umap_embeddings = umap_embeddings[1:]  # Excluir el primer elemento (tópico -1)

    # Crear un DataFrame para exportar los datos
    df = pd.DataFrame({
        "x": filtered_umap_embeddings[:, 0],
        "y": filtered_umap_embeddings[:, 1],
        "Topic": filtered_topic_list,
        "Words": words,
        "Size": frequencies
    })

    # Guardar los datos en un archivo CSV
    return df
