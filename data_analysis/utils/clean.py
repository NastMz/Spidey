import re
import pandas as pd
from deep_translator import GoogleTranslator

from data_analysis.utils.load import load_file_content


def split_text(text, limit=5000):
    """
    Split the text into chunks of size 'limit'
    """
    return [text[i:i + limit] for i in range(0, len(text), limit)]


def create_corpus_from_csv(csv_file_path, target_language='en'):
    try:
        df = pd.read_csv(csv_file_path)

        if 'content' not in df.columns:
            raise ValueError("El CSV no contiene una columna llamada 'content'.")

        translated_contents = []
        texts = df['content'].dropna()
        for i, text in enumerate(texts):
            text_segments = split_text(text, limit=3000)
            print(f'Translating text {i+1}/{len(texts)}...')
            text_len = len(text_segments)
            for j, segment in enumerate(text_segments):
                print(f"Translating segment {j+1}/{text_len}")
                translated_text = GoogleTranslator(source='auto', target=target_language).translate(segment)
                translated_contents.append(translated_text)

        corpus = ' '.join(translated_contents)

        return corpus

    except Exception as e:
        print(f"Error creating corpus: {e}")
        return None


def clean_corpus(corpus_path):
    corpus = load_file_content(corpus_path)

    url_regex = re.compile(r'http://\S+|https://\S+|www\.\S+')
    non_word_regex = re.compile(r'\W')
    multi_space_regex = re.compile(r'\s+')
    digit_regex = re.compile(r'\d+')
    tab_regex = re.compile(r'\t+')
    single_letter_regex = re.compile(r'\b\w\b')
    repeated_letters_regex = re.compile(r'(.)\1+')

    # Remove URLs
    cleaned_corpus = url_regex.sub('', corpus)

    # Normalize text
    cleaned_corpus = cleaned_corpus.strip().lower()

    # Replace non-word characters with space
    cleaned_corpus = non_word_regex.sub(' ', cleaned_corpus)

    # Remove digits
    cleaned_corpus = digit_regex.sub('', cleaned_corpus)

    # Replace tabs with space
    cleaned_corpus = tab_regex.sub(' ', cleaned_corpus)

    # Replace repeated letters
    cleaned_corpus = repeated_letters_regex.sub(r'\1', cleaned_corpus)

    # Remove single letters
    cleaned_corpus = single_letter_regex.sub('', cleaned_corpus)

    # Replace multiple spaces with a single space
    cleaned_corpus = multi_space_regex.sub(' ', cleaned_corpus)

    return cleaned_corpus
