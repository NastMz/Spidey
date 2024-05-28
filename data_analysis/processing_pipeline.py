import os
import logging
import json
import pandas as pd
import joblib

from data_analysis.utils.load import load_json_data, load_pdf_data
from data_analysis.utils.clean import create_corpus_from_csv, clean_corpus
from data_analysis.utils.pre_processing import remove_stopwords_from_corpus, corpus_word_tokenize
from data_analysis.utils.processing import train_model, create_bag_of_words, generate_csv_metadata

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

logging.getLogger().addHandler(console_handler)


def load_data():
    logging.info('Loading data...')
    university_pdf_dict = {
        'nacional': {'name': 'Universidad Nacional de Colombia', 'country': 'Colombia'},
        'andes': {'name': 'Universidad de los Andes', 'country': 'Colombia'},
        'campinas': {'name': 'Universidad de Campinas', 'country': 'Brasil'},
        'cundinamarca': {'name': 'Universidad de Cundinamarca', 'country': 'Colombia'},
        'cambridge': {'name': 'University of Cambridge', 'country': 'United Kingdom'},
        # Add more universities as needed
    }

    json_data = load_json_data('universities_crawler/crawled_files/json')
    pdf_data = load_pdf_data('universities_crawler/crawled_files/pdf', university_pdf_dict)
    df = pd.concat([json_data, pdf_data], ignore_index=True)
    df.to_csv('universities_data.csv', index=False)
    logging.info('Data loaded successfully.')
    return df


def create_corpus():
    logging.info('Creating corpus...')
    if not os.path.exists('universities_data.csv'):
        raise FileNotFoundError("universities_data.csv does not exist. Run load_data first.")

    corpus = create_corpus_from_csv('universities_data.csv')
    if corpus:
        with open('corpus.txt', 'w', encoding='utf-8') as f:
            f.write(corpus)
            f.close()
    else:
        raise ValueError("Failed to create corpus")

    logging.info('Corpus created successfully.')


def clean_corpus_step():
    logging.info('Cleaning corpus...')
    if not os.path.exists('corpus.txt'):
        raise FileNotFoundError("corpus.txt does not exist. Run create_corpus first.")

    cleaned_corpus = clean_corpus('corpus.txt')
    if cleaned_corpus:
        with open('cleaned_corpus.txt', 'w', encoding='utf-8') as f:
            f.write(cleaned_corpus)
            f.close()
    else:
        raise ValueError("Failed to clean corpus")

    logging.info('Corpus cleaned successfully.')


def remove_stopwords_step():
    logging.info('Removing stopwords...')
    if not os.path.exists('cleaned_corpus.txt'):
        raise FileNotFoundError("cleaned_corpus.txt does not exist. Run clean_corpus first.")

    final_corpus = remove_stopwords_from_corpus('cleaned_corpus.txt')
    if final_corpus:
        with open('final_corpus.txt', 'w', encoding='utf-8') as f:
            f.write(final_corpus)
            f.close()
    else:
        raise ValueError("Failed to remove stopwords")

    logging.info('Stopwords removed successfully.')


def tokenize_step():
    logging.info('Tokenizing...')
    if not os.path.exists('final_corpus.txt'):
        raise FileNotFoundError("final_corpus.txt does not exist. Run remove_stopwords first.")

    tokenized = corpus_word_tokenize('final_corpus.txt')
    if tokenized:
        tokenized_str = '\n'.join(tokenized)
        with open('tokenized.txt', 'w', encoding='utf-8') as f:
            f.write(tokenized_str)
            f.close()
    else:
        raise ValueError("Failed to tokenize corpus")

    logging.info('Corpus tokenized successfully.')


def create_bag_of_words_step():
    logging.info('Creating bag of words...')
    if not os.path.exists('tokenized.txt'):
        raise FileNotFoundError("tokenized.txt does not exist. Run tokenize first.")

    dictionary = create_bag_of_words('tokenized.txt')
    if dictionary:
        with open('bag_of_words.json', 'w', encoding='utf-8') as f:
            json.dump(dictionary, f)
            f.close()
    else:
        raise ValueError("Failed to create bag of words")

    logging.info('Bag of words created successfully.')


def train_model_step():
    logging.info('Training model...')
    if not os.path.exists('tokenized.txt'):
        raise FileNotFoundError("tokenized.txt does not exist. Run tokenize first.")

    model, topics, probabilities = train_model('tokenized.txt')
    model_filename = 'trained_model.joblib'
    joblib.dump(model, model_filename)

    logging.info('Model trained successfully.')

    return model_filename


def load_model(model_path):
    logging.info(f'Loading model from {model_path}...')
    try:
        model = joblib.load(model_path)
        logging.info('Model loaded successfully.')
        return model
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        return None


def get_metadata():
    logging.info('Getting metadata...')
    if not os.path.exists('universities_data.csv'):
        raise FileNotFoundError("universities_data.csv does not exist. Run load_data first.")

    metadata = generate_csv_metadata('universities_data.csv')
    if metadata:
        with open('metadata.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f)
            f.close()
    else:
        raise ValueError("Failed to create metadata")

    logging.info('Metadata created successfully.')
